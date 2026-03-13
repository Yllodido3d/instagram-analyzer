import requests
from datetime import datetime
import json
import config


def coletar_instagram(username):
    try:
        URL = "https://api.apify.com/v2/acts/apify~instagram-profile-scraper/run-sync-get-dataset-items"
        params = {"token": config.apify_token}
        payload = {
            "usernames": [username],
            "resultLimit": 15
        }

        dados_raw = requests.post(
            URL, params=params, json=payload)  # pedindo request
        dados_raw.raise_for_status()  # erro se falhar

        # faltou o json() <- isso eu resolvi sozinho :D
        perfil = dados_raw.json()[0]
        # pegando os dados especificos dos ultimos 10 posts
        ultimos_posts = []
        for c in range(10):
            post = {
                "legenda": perfil["latestPosts"][c]["caption"],
                "curtidas": perfil["latestPosts"][c]["likesCount"],
                "numerodecomentarios": perfil["latestPosts"][c]["commentsCount"],
                "tempo?": perfil["latestPosts"][c]["timestamp"],
                "tipo": perfil["latestPosts"][c]["type"]
            }
            ultimos_posts.append(post)

        # preguiça do carai de lembrar como faz em list comprehension KKKKK
        # a ideia do dict com as chaves foi do copilot (ele saiou da soneca), mas eu apaguei e fiz sozinho depois
        dados_perfil = {
            "seguidores": perfil["followersCount"],
            "seguindo": perfil["followsCount"],
            "total_posts": perfil["postsCount"],
            "bio": perfil["biography"],
            "posts_recentes": ultimos_posts

        }
        return dados_perfil

    except Exception as e:
        return {"erro": f"falha ao coletar instagram: {str(e)}"}


def gerar_insights_gemini(dados_instagram):
    try:
        gemini_key = config.gemini_key
        URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"

        json_template = '''{
            "resumo_executivo": "string com resumo geral",
            "presenca_digital": {
                "pontos_fortes": ["item1", "item2"],
                "pontos_fracos": ["item1", "item2"]
            },
            "estrategia_conteudo": {
                "tom_de_voz": "string",
                "frequencia_estimada": "string",
                "temas_principais": ["tema1", "tema2"]
            },
            "engajamento": {
                "avaliacao": "string com análise de engajamento"
            },
            "oportunidades": ["item1", "item2"],
            "recomendacoes": ["item1", "item2"]
            }'''

        prompt = f"""You are a professional Instagram account analyst.
        Analyze the data below and return a strategic report in English.

        Data: {dados_instagram}

        Return ONLY a valid JSON object with no text outside it, following this structure:
        {json_template}
        IMPORTANT: Respond exclusively in English. Do not use any other language."""

        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }

        resposta = requests.post(URL, json=payload)
        texto = resposta.json()["candidates"][0]["content"]["parts"][0]["text"]
        texto = texto.strip()
        if texto.startswith("```"):
            texto = texto.split("```")[1]
            if texto.startswith("json"):
                texto = texto[4:]
        return json.loads(texto.strip())

    except Exception as e:
        return {"erro": f"falha ao Analisar: {str(e)}"}
