from flask import jsonify
import functions_framework
import asyncio
import httpx

async def fetch_page(client, url):
    """Helper para buscar uma página individual"""
    try:
        resp = await client.get(url, timeout=10.0)
        return resp.json() if resp.status_code == 200 else None
    except Exception:
        return None

async def search_star_wars_logic(category, filter_key, filter_value):
    all_filtered = []
    current_page = 1
    BATCH_SIZE = 5  # Quantas páginas pedimos por vez
    TARGET_COUNT = 10 # Quantos resultados queremos para nossa página

    async with httpx.AsyncClient() as client:
        while len(all_filtered) < TARGET_COUNT:
            # 1. Cria o lote de tarefas (ex: páginas 1 a 5)
            tasks = [
                fetch_page(client, f"https://swapi.dev/api/{category}/?page={i}")
                for i in range(current_page, current_page + BATCH_SIZE)
            ]
            
            # 2. Dispara o lote em paralelo
            pages_data = await asyncio.gather(*tasks)
            
            found_in_batch = False
            for data in pages_data:
                if not data: continue
                
                items = data.get('results', [])
                if not items: continue # Fim dos dados da SWAPI

                # 3. Filtra os itens (ex: cor de cabelo ou clima)
                for item in items:
                    val_to_check = item.get(filter_key, "").lower()
                    if filter_value.lower() in val_to_check:
                        all_filtered.append(item)
                    
                    # 4. EARLY EXIT: Encontrou o suficiente? Para tudo.
                    if len(all_filtered) >= TARGET_COUNT:
                        return all_filtered[:TARGET_COUNT]
                
                found_in_batch = True

            # Se o lote não trouxe nada ou não há mais páginas, encerra
            if not found_in_batch:
                break
                
            current_page += BATCH_SIZE
    
    return all_filtered

async def find_movie_data(identifier, client):
    """
    Tenta achar o filme. Se o identifier for número, vai direto.
    Se for texto, usa o endpoint de search.
    """
    if identifier.isdigit():
        url = f"https://swapi.dev/api/films/{identifier}/"
        res = await client.get(url)
        return res.json() if res.status_code == 200 else None
    else:
        # Busca pelo nome (ex: "A New Hope")
        search_url = f"https://swapi.dev/api/films/?search={identifier}"
        res = await client.get(search_url)
        if res.status_code == 200:
            results = res.json().get("results", [])
            return results[0] if results else None # Pega o primeiro match
    return None

async def get_film_subresource(movie_identifier, category, client):
    """Agora aceita nome ou ID do filme"""
    # 1. Passo extra: Resolve o filme primeiro
    movie_data = await find_movie_data(movie_identifier, client)
    
    if not movie_data:
        return {"error": f"Filme '{movie_identifier}' não encontrado."}

    # 2. O resto da lógica continua igual (Resolvionador de Links)
    urls = movie_data.get(category, [])
    if not urls:
        return {"movie": movie_data.get("title"), "category": category, "results": []}

    tasks = [client.get(url) for url in urls]
    responses = await asyncio.gather(*tasks)
    
    resolved_names = [
        r.json().get('name') or r.json().get('title') 
        for r in responses if r.status_code == 200
    ]

    return {
        "movie_found": movie_data.get("title"),
        "category": category,
        "results": resolved_names
    }

@functions_framework.http
def star_wars_proxy(request):
    """Ponto de entrada da Cloud Function"""

    movie_query = request.args.get('movie')
    sub_category = request.args.get('category')

    if movie_query and sub_category:
        async def run_subresource():
            async with httpx.AsyncClient() as client:
                return await get_film_subresource(movie_query, sub_category, client)
        
        data = asyncio.run(run_subresource())
        return jsonify(data), 200 if "error" not in data else 400

    category = request.args.get('category', 'people')
    filter_key = request.args.get('key', 'name')
    filter_value = request.args.get('value', '')
    sort_by = request.args.get('sort_by')
    order = request.args.get('order', 'asc').lower()

    results = asyncio.run(search_star_wars_logic(category, filter_key, filter_value))
    
    if sort_by and results:
        def sorting_key(item):
            val = item.get(sort_by, "")
            try:
                return float(str(val).replace(',', ''))
            except (ValueError, TypeError):
                return str(val).lower()

        is_reverse = True if order == 'desc' else False
        results.sort(key=sorting_key, reverse=is_reverse)


    return jsonify({
        "status": "success",
        "persona_filter": f"{filter_key}={filter_value}",
        "count": len(results),
        "results": results
    }), 200