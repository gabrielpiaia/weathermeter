import requests

API_KEY = "2aa6d979d34f9c35275a767a6bc2d620"  
city_name = "Santa Vitória do Palmar"

# adicionado units=metric para receber temperatura em Celsius e lang para tradução
link = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric&lang=pt_br"


requisicao = requests.get(link)

if requisicao.status_code == 200:
    requisicao_dic = requisicao.json()
    descricao = requisicao_dic['weather'][0]['description']  # Pega o dicionário
    temperatura = requisicao_dic['main']['temp']  # Corrigido para 'main'
    
    print(descricao, f"{temperatura} graus")
else:
    print(f"Erro: {requisicao.status_code} - {requisicao.text}")