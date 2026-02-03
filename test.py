
from pprint import pprint
import asyncio
import httpx


async def get_batched_data(category, filter_key, filter_value):
    # Configurações do MVP
    BATCH_SIZE = 5  # Quantas páginas pedimos por vez
    TARGET_COUNT = 10 # Quantos resultados queremos para nossa página

    all_filtered = []
    current_page = 1
    
    async with httpx.AsyncClient() as client:
        while len(all_filtered) < TARGET_COUNT:
            # 1. Cria um lote de tarefas (ex: páginas 1 a 5, depois 6 a 10...)
            tasks = [
                client.get(f"https://swapi.dev/api/{category}/?page={i}")
                for i in range(current_page, current_page + BATCH_SIZE)
            ]
            
            # 2. Executa o lote em paralelo
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            
            for resp in responses:
                if isinstance(resp, httpx.Response) and resp.status_code == 200:
                    items = resp.json().get('results', [])
                    # 3. Filtra os dados deste lote
                    matches = [i for i in items if filter_value.lower() in i.get(filter_key, '').lower()]
                    all_filtered.extend(matches)
                
                # 4. EARLY EXIT: Se já temos o suficiente, paramos o processamento
                if len(all_filtered) >= TARGET_COUNT:
                    return all_filtered[:TARGET_COUNT]

        
            current_page += BATCH_SIZE
            
            if current_page > 100: 
                break

    return all_filtered

pprint("Buscando naves com 'star' no nome...")
hair_color="blond"
pprint(asyncio.run(get_batched_data('people', 'hair_color', hair_color)))