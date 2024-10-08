# Watchmeter

**Watchmeter** é uma aplicação em Python que consome a API do [OpenWeather](https://openweathermap.org/api) para salvar estatísticas de clima a cada 2 minutos e fornece uma API para consultas de temperatura. A aplicação salva dados meteorológicos, como temperatura e descrição do clima, para a cidade especificada, e permite consultas por meio de uma API construída com Flask.

## Funcionalidades

- **Captura de Temperatura**: Consulta a temperatura e a descrição do clima da cidade configurada a cada 2 horas e salva os dados no banco de dados.
- **API para Consulta de Temperatura**: Fornece uma API para consultas de dados meteorológicos, incluindo as rotas:
  - Temperatura da última hora.
  - Temperatura registrada no dia atual para uma cidade específica.
  - Temperatura de uma cidade em um intervalo de tempo personalizado.

## Tecnologias Utilizadas

- **Python**: Linguagem principal da aplicação.
- **Flask**: Framework web para criar a API.
- **SQLAlchemy**: ORM para interação com o banco de dados MySQL.
- **MySQL**: Banco de dados utilizado para armazenar os dados meteorológicos.
- **OpenWeather API**: Fonte de dados meteorológicos.
- **Requests**: Biblioteca para realizar chamadas HTTP para a API OpenWeather.

## Como Configurar e Executar

### Pré-requisitos

- Python 3.x
- MySQL
- Conta na OpenWeather API (para obter sua chave de API)
