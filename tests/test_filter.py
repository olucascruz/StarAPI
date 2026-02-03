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
    file_path = os.path.join(base_path, 'mocks', f'page_{page_number}.json')
    
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