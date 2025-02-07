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
    ads_data = get_facebook_ads_insights()
    
    # print(f"test_facebook_api: {data}")
    # print(f"ads_data: {ads_data}")
    
    # Verifica se ads_data tem dados válidos
    dados_para_analise = ads_data.get("data", [])
    
    if not dados_para_analise:  
        print("⚠️ Nenhum dado de anúncios encontrado. Usando dados do Facebook API para relatório.")
        dados_para_analise = data  # Usa os dados do Facebook em vez de Ads
    
    # Passa os dados para análise da CrewAI
    crew.kickoff(inputs={"dados": dados_para_analise})
    
    # Criar relatório
    report = f"""
    📊 Relatório de Tráfego:
    {dados_para_analise}

    📢 Insights:
    - Impressões: {dados_para_analise[0]['impressions'] if isinstance(dados_para_analise, list) and dados_para_analise else "N/A"}
    - Alcance: {dados_para_analise[0]['reach'] if isinstance(dados_para_analise, list) and dados_para_analise else "N/A"}
    - Cliques: {dados_para_analise[0]['clicks'] if isinstance(dados_para_analise, list) and dados_para_analise else "N/A"}
    - Investimento: {dados_para_analise[0]['spend'] if isinstance(dados_para_analise, list) and dados_para_analise else "N/A"}
    """

    print(report)
