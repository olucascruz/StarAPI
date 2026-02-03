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

@functions_framework.http
def star_wars_proxy(request):
    """Ponto de entrada da Cloud Function"""
    # Captura parâmetros da Persona (ex: ?category=people&key=hair_color&value=blond)
    category = request.args.get('category', 'people')
    filter_key = request.args.get('key', 'name')
    filter_value = request.args.get('value', '')

    # Executa a lógica assíncrona
    results = asyncio.run(search_star_wars_logic(category, filter_key, filter_value))
    
    return jsonify({
        "status": "success",
        "persona_filter": f"{filter_key}={filter_value}",
        "count": len(results),
        "results": results
    }), 200