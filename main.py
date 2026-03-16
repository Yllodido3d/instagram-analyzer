from analisador import coletar_instagram, gerar_insights_gemini
from datetime import datetime
from gerar_pdf import gerar_relatorio

date_now = datetime.now().strftime("%m/%d/%Y at %H:%M")
username = str(input("Type the Instagram name(withoud @)> "))
segmento = input("Account niche/segment (ex: gaming, fitness, food)> ")
client_name = input("Your name or agency name> ")


data = coletar_instagram(username)
if not data:
    print("fail to get data, check the logs")
    exit()
insight = gerar_insights_gemini(data)


dados = {
    "nome_concorrente": username,
    "data_geracao": date_now,
    "insights": insight,
    "instagram": username,
    "instagram_dados": data,
    "segmento": segmento,
    "nome_cliente": client_name
}

nome_arquivo = f"report_{username}.pdf"
gerar_relatorio(dados, nome_arquivo)
print(f"Report generated: {nome_arquivo}")
