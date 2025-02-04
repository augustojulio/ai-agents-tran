import os
import requests
from crewai import Agent, Task, Crew
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
INSTAGRAM_ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID")

# Função para pegar estatísticas do Instagram
def get_instagram_insights():
    url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_ACCOUNT_ID}/insights"
    params = {
        "metric": "impressions,reach,profile_views",
        "period": "day",
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
    data = get_instagram_insights()
    print(data)
    
    # Executa CrewAI para análise e relatório
    result = crew.kickoff()
    
    # Cria um relatório simples com os dados
    report = f"""
    📊 Relatório de Tráfego:
    - Impressões: {data['data'][0]['category']}
    - Alcance: {data['data'][0]['category_list'][0]}
    - Visualizações de Perfil: {data['data'][0]['name']}
    
    📢 Insights:
    {result}
    """

    # - Impressões: {data['data'][0]['values'][0]['value']}
    # - Alcance: {data['data'][1]['values'][0]['value']}
    # - Visualizações de Perfil: {data['data'][2]['values'][0]['value']}
    print(f"reportt: {report}")
