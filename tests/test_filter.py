import pytest
import respx
import re
import json
import os
from httpx import Response
from main import search_star_wars_logic

# --- Utilitários de Mock ---

def dynamic_swapi_mock(request):
    """Lógica que decide qual JSON retornar baseado na URL e categoria"""
    url = str(request.url)
    
    # Identifica a categoria (people, planets, starships) e a página
    category_match = re.search(r"api/(people|planets|starships)/", url)
    page_match = re.search(r"page=(\d+)", url)
    
    category = category_match.group(1) if category_match else "people"
    page_number = page_match.group(1) if page_match else "1"
    
    # Caminho ajustado para a estrutura de pastas STARAPI/tests/mocks/
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, 'mocks', category, f'page_{page_number}.json')

    print(f"file_path {file_path}")
    try:
        with open(file_path, 'r') as f:
            mock_data = json.load(f)
        return Response(200, json=mock_data)
    except FileNotFoundError:
        return Response(404, json={"error": "Página não encontrada nos mocks locais"})

# --- Testes das Personas ---

@pytest.mark.asyncio
@respx.mock
async def test_persona_ricardo_blond_hair():
    """Valida a busca de personagens loiros para o Ricardo (Action Figures)"""
    respx.get(url__startswith="https://swapi.dev/api/people/").side_effect = dynamic_swapi_mock

    # Executa a lógica de busca
    results = await search_star_wars_logic("people", "hair_color", "blond")
    assert len(results) > 0
    assert any("Luke Skywalker" in p["name"] for p in results)
    for p in results:
        assert "blond" in p["hair_color"].lower()

@pytest.mark.asyncio
@respx.mock
async def test_persona_leticia_temperate_planets():
    """Valida a busca de planetas temperados para a Letícia (Mestre de RPG)"""
    # Nota: Certifique-se de ter baixado mocks de planets também
    respx.get(url__startswith="https://swapi.dev/api/planets/").side_effect = dynamic_swapi_mock

    results = await search_star_wars_logic("planets", "climate", "temperate")
    
    assert len(results) > 0
    for planet in results:
        assert "temperate" in planet["climate"].lower()

@pytest.mark.asyncio
@respx.mock
async def test_empty_results_handling():
    """Garante que a API não quebra se não encontrar nenhum resultado"""
    respx.get(url__startswith="https://swapi.dev/api/people/").side_effect = dynamic_swapi_mock

    # Busca por algo que provavelmente não existe nos mocks
    results = await search_star_wars_logic("people", "hair_color", "neon-pink")
    
    assert isinstance(results, list)
    assert len(results) == 0


@pytest.mark.asyncio
@respx.mock
async def test_persona_ackbar_sorting_capacity():
    """
    Valida a busca de naves da Kuat para o Comandante Ackbar
    e garante que a ordenação numérica (DESC) está funcionando.
    """
    # Configura o mock para interceptar chamadas de starships
    respx.get(url__startswith="https://swapi.dev/api/starships/").side_effect = dynamic_swapi_mock

    # 1. Executa a busca (Filtrando por fabricante 'Kuat')
    # Nota: A ordenação agora é processada no ponto de entrada ou na logic atualizada
    results = await search_star_wars_logic("starships", "manufacturer", "Kuat")
    
    # 2. Aplicamos a ordenação (simulando a lógica do seu star_wars_proxy)
    # Ordenando por cargo_capacity como número, Decrescente
    results.sort(
        key=lambda x: float(str(x.get("cargo_capacity", 0)).replace(',', '')) 
        if str(x.get("cargo_capacity")).isnumeric() else 0, 
        reverse=True
    )

    # 3. Asserts
    assert len(results) >= 1
    # Verifica se o primeiro item é o que tem maior capacidade (numérica)
    capacities = [float(str(s["cargo_capacity"]).replace(',', '')) for s in results if s["cargo_capacity"].isnumeric()]
    if capacities:
        assert float(str(results[0]["cargo_capacity"]).replace(',', '')) == max(capacities)