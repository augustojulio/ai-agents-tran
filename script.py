import os
import requests
from crewai import Agent, Task, Crew
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

# Função para pegar estatísticas do Instagram
def test_facebook_api():
    url = f"https://graph.facebook.com/v22.0/me"
    params = {
        "access_token": ACCESS_TOKEN
    }
    response = requests.get(url, params=params)
    return response.json()

# Função para pegar dados da API de Marketing do Facebook
def get_facebook_ads_insights():
    AD_ACCOUNT_ID = os.getenv("AD_ACCOUNT_ID")
    url = f"https://graph.facebook.com/v22.0/act_{AD_ACCOUNT_ID}/insights"
    params = {
        "fields": "campaign_name,impressions,reach,clicks,spend",
        "level": "campaign",
        "time_range": '{"since":"2024-01-01","until":"2025-02-01"}',  
        "access_token": ACCESS_TOKEN
    }

    response = requests.get(url, params=params)
    return response.json()

# Definir agentes
coletor = Agent(
    name="Coletor de Dados",
    role="Extrai métricas de tráfego do Facebook e Instagram",
    backstory="Especialista em análise de tráfego digital no Facebook e Instagram.",
    goal="Obter métricas detalhadas das redes sociais para análise."
)

analista = Agent(
    name="Analista de Tráfego",
    role="Analisa padrões de tráfego e comportamento dos usuários",
    backstory="Especialista em marketing digital, detecta tendências e padrões.",
    goal = "Analisar dados de tráfego para identificar oportunidades."
)

gerador_relatorio = Agent(
    name="Gerador de Relatórios",
    role="Cria resumos e insights a partir dos dados analisados",
    backstory="Especialista em comunicação e estratégia digital, gera relatórios prontos para ação.",
    goal = "Sintetizar dados e insights em um relatório executivo."
)

# Definir tarefas
tarefa_coletar = Task(
    description="Obter métricas de tráfego do Facebook e Instagram usando APIs.",
    agent=coletor,
    expected_output = "Dados coletados com sucesso."
)

tarefa_analisar = Task(
    description="Analisar padrões de tráfego com base nos dados coletados.",
    agent=analista,
    expected_output = "Análise de tráfego concluída."
)

tarefa_gerar_relatorio = Task(
    description="Gerar um relatório com insights e recomendações.",
    agent=gerador_relatorio,
    expected_output = "Relatório gerado com sucesso."
)

# Criar equipe de agentes
crew = Crew(
    agents=[coletor, analista, gerador_relatorio],
    tasks=[tarefa_coletar, tarefa_analisar, tarefa_gerar_relatorio]
)

if __name__ == "__main__":
    # Coletar dados
    data = test_facebook_api()
    print(f"test_facebook_api: {data}")
    ads_data = get_facebook_ads_insights()
    print(f"ads_data: {ads_data}")
    
    # Executa CrewAI para análise e relatório
    # result = crew.kickoff()
    
    # Cria um relatório simples com os dados
    # report = f"""
    # 📊 Relatório de Tráfego:
    # - Impressões: {data['data'][0]['category']}
    # - Alcance: {data['data'][0]['category_list'][0]}
    # - Visualizações de Perfil: {data['data'][0]['name']}
    
    # 📢 Insights:
    # {result}
    # """

    # # - Impressões: {data['data'][0]['values'][0]['value']}
    # # - Alcance: {data['data'][1]['values'][0]['value']}
    # # - Visualizações de Perfil: {data['data'][2]['values'][0]['value']}
    # print(f"reportt: {report}")
