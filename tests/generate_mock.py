import requests
import json
import os
import time

def generate_star_wars_mocks():
    categories = ["people", "planets", "starships"]
    base_dir = "tests/mocks"

    for category in categories:
        print(f"\n--- Gerando: {category.upper()} ---")
        target_path = os.path.join(base_dir, category)
        os.makedirs(target_path, exist_ok=True)

        url = f"https://swapi.dev/api/{category}/"
        page = 1

        while url:
            success = False
            for tentativa in range(3): # Tenta 3 vezes por página
                try:
                    print(f"  > [{tentativa+1}/3] Baixando {category} - pág {page}...", end="\r")
                    response = requests.get(url, timeout=30) # Aumentamos o timeout
                    response.raise_for_status()
                    data = response.json()
                    
                    with open(os.path.join(target_path, f"page_{page}.json"), 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=4)
                    
                    url = data.get('next')
                    page += 1
                    success = True
                    break 
                except Exception as e:
                    time.sleep(2) # Espera 2 segundos antes de tentar de novo
            
            if not success:
                print(f"\n  [!] Falha definitiva na página {page} de {category}. Pulando...")
                break

    print("\n✅ Processo finalizado. Verifique se as pastas contêm arquivos JSON.")

if __name__ == "__main__":
    generate_star_wars_mocks()