🌌 StarAPI - Middleware de Orquestração Star Wars
Middleware de orquestração assíncrona desenvolvido em GCP, projetado para o enriquecimento e tratamento granular de dados da saga Star Wars, atendendo a demandas complexas de customização, logística e narrativa.

A StarAPI atua como uma camada de inteligência sobre a SWAPI, resolvendo limitações de busca original, tratando tipos de dados e orquestrando múltiplas requisições paralelas para entregar um JSON pronto para consumo.

🚀 Funcionalidades Principais
👤 Filtros Baseados em Personas
A API foi desenhada para resolver problemas de três perfis de usuários específicos:

Ricardo (Customizador): Filtros combinados de eye_color e skin_color para referências de pintura.

Letícia (Narradora de RPG): Busca parcial de climas (ex: "temperate") em strings compostas de planetas.

Comandante Ackbar (Analista de Frota): Filtro por fabricante e capacidade de carga com conversão numérica dinâmica (ordenação real).

🔗 Resolvionador de Correlações (O diferencial "Feral")
Diferente da API original que retorna URLs, a StarAPI resolve os links e entrega os nomes reais de:

Personagens, Planetas, Naves, Veículos e Espécies.

Suporte a busca de filmes por ID ou Nome (Search).

🛠️ Stack Tecnológica e Arquitetura
Tecnologias
Linguagem: Python 3.11+

Concorrência: AsyncIO e HTTPX (Processamento paralelo de alta performance).

Infraestrutura: Google Cloud Functions (2nd Gen) e Google API Gateway.

Testes: Pytest com Respx para mocks dinâmicos de sistema de arquivos.

Contrato: OpenAPI 2.0 (Swagger).

Arquitetura de Nuvem
A solução utiliza o padrão Facade (Fachada) através do API Gateway, garantindo que o backend (Cloud Function) permaneça isolado e seguro.

Gateway: Valida API Keys e restringe categorias via enum.

Function: Orquestra chamadas assíncronas via asyncio.gather, reduzindo a latência de N requisições para o tempo de apenas uma.

<img width="1024" height="559" alt="image" src="https://github.com/user-attachments/assets/76462cb9-128a-49e5-9722-9170f865c4eb" />


📁 Estrutura do Projeto

STARAPI/
├── main.py              # Lógica de orquestração, filtros e roteamento interno.
├── openapi.yaml         # Contrato de interface e definições de segurança.
├── requirements.txt     # Dependências do projeto.
├── tests/
│   ├── test_sorting.py  # Validação de ordenação numérica/alfabética.
│   ├── test_logic.py    # Testes das personas Ricardo e Letícia.
│   └── mocks/           # JSONs locais para testes determinísticos.
└── README.md            # Documentação técnica.

Este é o README.md definitivo para o seu projeto. Ele foi estruturado com uma linguagem técnica de alto nível para impressionar o time da PowerOfData, destacando sua competência em Sistemas de Informação e sua capacidade de entregar valor real através de arquitetura em nuvem.

🌌 StarAPI - Middleware de Orquestração Star Wars
Middleware de orquestração assíncrona desenvolvido em GCP, projetado para o enriquecimento e tratamento granular de dados da saga Star Wars, atendendo a demandas complexas de customização, logística e narrativa.

A StarAPI atua como uma camada de inteligência sobre a SWAPI, resolvendo limitações de busca original, tratando tipos de dados e orquestrando múltiplas requisições paralelas para entregar um JSON pronto para consumo.

🚀 Funcionalidades Principais
👤 Filtros Baseados em Personas
A API foi desenhada para resolver problemas de três perfis de usuários específicos:

Ricardo (Customizador): Filtros combinados de eye_color e skin_color para referências de pintura.

Letícia (Narradora de RPG): Busca parcial de climas (ex: "temperate") em strings compostas de planetas.

Comandante Ackbar (Analista de Frota): Filtro por fabricante e capacidade de carga com conversão numérica dinâmica (ordenação real).

🔗 Resolvionador de Correlações
Diferente da API original que retorna URLs, a StarAPI resolve os links e entrega os nomes reais de:

Personagens, Planetas, Naves, Veículos e Espécies.

Suporte a busca de filmes por ID ou Nome (Search).

🛠️ Stack Tecnológica e Arquitetura
Tecnologias
Linguagem: Python 3.11+

Concorrência: AsyncIO e HTTPX (Processamento paralelo de alta performance).

Infraestrutura: Google Cloud Functions (2nd Gen) e Google API Gateway.

Testes: Pytest com Respx para mocks dinâmicos de sistema de arquivos.

Contrato: OpenAPI 2.0 (Swagger).

Arquitetura de Nuvem
A solução utiliza o padrão Facade (Fachada) através do API Gateway, garantindo que o backend (Cloud Function) permaneça isolado e seguro.



Gateway: Valida API Keys e restringe categorias via enum.

Function: Orquestra chamadas assíncronas via asyncio.gather, reduzindo a latência de N requisições para o tempo de apenas uma.

Security: Camada dupla de proteção com API Key (Borda) e IAM Service Account (Backend).

📁 Estrutura do Projeto
Plaintext
STARAPI/
├── main.py              # Lógica de orquestração, filtros e roteamento interno.
├── openapi.yaml         # Contrato de interface e definições de segurança.
├── requirements.txt     # Dependências do projeto.
├── tests/
│   ├── test_sorting.py  # Validação de ordenação numérica/alfabética.
│   ├── test_logic.py    # Testes das personas Ricardo e Letícia.
│   └── mocks/           # JSONs locais para testes determinísticos.
└── README.md            # Documentação técnica.
🧪 Como Executar e Testar
1. Ambiente Local
Para rodar a função localmente simulando o GCP:

pip install -r requirements.txt
functions-framework --target star_wars_proxy --debug

2. Executando Testes Unitários
Os testes utilizam mocks dinâmicos, não dependendo da SWAPI estar online:

pytest tests/

3. Exemplos de Chamada (Produção)
Busca com Ordenação Numérica: GET /v1/search?category=starships&key=manufacturer&value=Kuat&sort_by=cargo_capacity&order=desc

Correlação de Filme por Nome: GET /v1/filmes/correlacao?movie=A%20New%20Hope&category=planets

👨‍💻 Autor

Lucas Cruz
