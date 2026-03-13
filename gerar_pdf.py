from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT


# ─── PALETA DE CORES ──────────────────────────────────────────────────────────
AZUL_ESCURO = colors.HexColor("#1A1F36")
AZUL_MEDIO = colors.HexColor("#2D3561")
AZUL_CLARO = colors.HexColor("#4A6CF7")
CINZA_CLARO = colors.HexColor("#F4F6FB")
CINZA_TEXTO = colors.HexColor("#555B6E")
VERDE = colors.HexColor("#22C55E")
VERMELHO = colors.HexColor("#EF4444")
LARANJA = colors.HexColor("#F59E0B")
BRANCO = colors.white
# ──────────────────────────────────────────────────────────────────────────────


def criar_estilos():
    base = getSampleStyleSheet()

    estilos = {
        "titulo_capa": ParagraphStyle(
            "titulo_capa",
            fontName="Helvetica-Bold",
            fontSize=26,
            textColor=BRANCO,
            alignment=TA_CENTER,
            spaceAfter=8,
        ),
        "subtitulo_capa": ParagraphStyle(
            "subtitulo_capa",
            fontName="Helvetica",
            fontSize=13,
            textColor=colors.HexColor("#B0B8D1"),
            alignment=TA_CENTER,
            spaceAfter=4,
        ),
        "secao_titulo": ParagraphStyle(
            "secao_titulo",
            fontName="Helvetica-Bold",
            fontSize=13,
            textColor=AZUL_ESCURO,
            spaceBefore=18,
            spaceAfter=8,
        ),
        "subsecao": ParagraphStyle(
            "subsecao",
            fontName="Helvetica-Bold",
            fontSize=10,
            textColor=AZUL_MEDIO,
            spaceBefore=10,
            spaceAfter=4,
        ),
        "corpo": ParagraphStyle(
            "corpo",
            fontName="Helvetica",
            fontSize=10,
            textColor=CINZA_TEXTO,
            leading=16,
            spaceAfter=6,
        ),
        "item_lista": ParagraphStyle(
            "item_lista",
            fontName="Helvetica",
            fontSize=10,
            textColor=CINZA_TEXTO,
            leading=16,
            leftIndent=12,
            spaceAfter=3,
        ),
        "label_card": ParagraphStyle(
            "label_card",
            fontName="Helvetica",
            fontSize=8,
            textColor=CINZA_TEXTO,
            alignment=TA_CENTER,
        ),
        "valor_card": ParagraphStyle(
            "valor_card",
            fontName="Helvetica-Bold",
            fontSize=20,
            textColor=AZUL_ESCURO,
            alignment=TA_CENTER,
        ),
        "rodape": ParagraphStyle(
            "rodape",
            fontName="Helvetica",
            fontSize=8,
            textColor=colors.HexColor("#9CA3AF"),
            alignment=TA_CENTER,
        ),
    }
    return estilos


def capa(dados: dict, estilos: dict) -> list:
    """Cria a página de capa com fundo escuro."""
    elementos = []

    # Bloco de capa — fundo azul escuro via tabela
    conteudo_capa = [
        [Paragraph("COMPETITOR ANALYSIS", estilos["subtitulo_capa"])],
        [Paragraph("REPORT", estilos["subtitulo_capa"])],
        [Spacer(1, 0.3 * cm)],
        [Paragraph(dados["nome_concorrente"].upper(), estilos["titulo_capa"])],
        [Spacer(1, 0.2 * cm)],
        [Paragraph(f"Segment: {dados['segmento']}",
                   estilos["subtitulo_capa"])],
        [Spacer(1, 1 * cm)],
        [Paragraph(
            f"Prepared for: <b>{dados['nome_cliente']}</b>", estilos["subtitulo_capa"])],
        [Paragraph(
            f"Generated on: {dados['data_geracao']}", estilos["subtitulo_capa"])],
    ]

    tabela_capa = Table(conteudo_capa, colWidths=[16 * cm])
    tabela_capa.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, -1), AZUL_ESCURO),
        ("TOPPADDING",  (0, 0), (-1, 0),  60),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 60),
        ("LEFTPADDING",  (0, 0), (-1, -1), 30),
        ("RIGHTPADDING", (0, 0), (-1, -1), 30),
        ("ROUNDEDCORNERS", [8]),
    ]))

    elementos.append(Spacer(1, 1.5 * cm))
    elementos.append(tabela_capa)
    elementos.append(PageBreak())
    return elementos


def cards_instagram(dados_instagram: dict, estilos: dict) -> list:
    """Cards com os números do Instagram."""
    elementos = []

    if "erro" in dados_instagram or "aviso" in dados_instagram:
        return elementos

    seguidores = dados_instagram.get("seguidores", 0)
    total_posts = dados_instagram.get("total_posts", 0)
    posts = dados_instagram.get("posts_recentes", [])

    media_curtidas = 0
    if posts:
        media_curtidas = int(sum(p.get("curtidas", 0)
                             for p in posts) / len(posts))

    def formatar_numero(n):
        if n >= 1_000_000:
            return f"{n/1_000_000:.1f}M"
        if n >= 1_000:
            return f"{n/1_000:.1f}K"
        return str(n)

    dados_cards = [
        ("👥 Followers",      formatar_numero(seguidores)),
        ("📸 Total Posts",  formatar_numero(total_posts)),
        ("❤️ Avg. Likes",  formatar_numero(media_curtidas)),
    ]

    celulas = []
    for label, valor in dados_cards:
        celula = Table(
            [
                [Paragraph(label, estilos["label_card"])],
                [Paragraph(valor, estilos["valor_card"])],
            ],
            colWidths=[4.8 * cm]
        )
        celula.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), CINZA_CLARO),
            ("TOPPADDING",    (0, 0), (-1, -1), 14),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
            ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
            ("ROUNDEDCORNERS", [6]),
        ]))
        celulas.append(celula)

    tabela_cards = Table([celulas], colWidths=[5.1 * cm, 5.1 * cm, 5.1 * cm])
    tabela_cards.setStyle(TableStyle([
        ("ALIGN",   (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",  (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING",  (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
    ]))

    elementos.append(tabela_cards)
    elementos.append(Spacer(1, 0.5 * cm))
    return elementos


def secao_lista(titulo: str, itens: list, estilos: dict, cor_bullet=AZUL_CLARO) -> list:
    """Cria uma seção com título e lista de itens com bullet colorido."""
    elementos = []
    elementos.append(Paragraph(titulo, estilos["secao_titulo"]))
    elementos.append(HRFlowable(width="100%", thickness=1,
                     color=CINZA_CLARO, spaceAfter=6))

    for item in itens:
        elementos.append(Paragraph(
            f"<font color='#{cor_bullet.hexval()[2:]}'>▸</font>  {item}", estilos["item_lista"]))

    return elementos


def tabela_pontos(pontos_fortes: list, pontos_fracos: list, estilos: dict) -> list:
    """Tabela lado a lado com pontos fortes e fracos."""
    elementos = []
    elementos.append(
        Paragraph("Strong and Weak Points", estilos["secao_titulo"]))
    elementos.append(HRFlowable(width="100%", thickness=1,
                     color=CINZA_CLARO, spaceAfter=8))

    # Cabeçalho
    header = [
        Paragraph("✅  STRENGTHS", ParagraphStyle(
            "h", fontName="Helvetica-Bold", fontSize=10, textColor=VERDE)),
        Paragraph("⚠️  WEAKNESSES",  ParagraphStyle(
            "h", fontName="Helvetica-Bold", fontSize=10, textColor=VERMELHO)),
    ]

    # Equaliza as listas
    max_len = max(len(pontos_fortes), len(pontos_fracos))
    pontos_fortes = pontos_fortes + [""] * (max_len - len(pontos_fortes))
    pontos_fracos = pontos_fracos + [""] * (max_len - len(pontos_fracos))

    linhas = [header]
    for forte, fraco in zip(pontos_fortes, pontos_fracos):
        linhas.append([
            Paragraph(f"• {forte}" if forte else "", estilos["item_lista"]),
            Paragraph(f"• {fraco}" if fraco else "", estilos["item_lista"]),
        ])

    tabela = Table(linhas, colWidths=[7.8 * cm, 7.8 * cm])
    tabela.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (0, 0), colors.HexColor("#DCFCE7")),
        ("BACKGROUND",    (1, 0), (1, 0), colors.HexColor("#FEE2E2")),
        ("BACKGROUND",    (0, 1), (0, -1), colors.HexColor("#F9FEFB")),
        ("BACKGROUND",    (1, 1), (1, -1), colors.HexColor("#FFF9F9")),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ("GRID",          (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
    ]))

    elementos.append(tabela)
    elementos.append(Spacer(1, 0.5 * cm))
    return elementos


def gerar_relatorio(dados: dict, nome_arquivo: str):
    """Função principal — monta e salva o PDF."""

    doc = SimpleDocTemplate(
        nome_arquivo,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    estilos = criar_estilos()
    insights = dados.get("insights", {})
    elementos = []

    # ── 1. CAPA ──────────────────────────────────────────────────────────────
    elementos += capa(dados, estilos)

    # ── 2. RESUMO EXECUTIVO ──────────────────────────────────────────────────
    elementos.append(Paragraph("Executive Summary", estilos["secao_titulo"]))
    elementos.append(HRFlowable(width="100%", thickness=1,
                     color=CINZA_CLARO, spaceAfter=8))
    elementos.append(Paragraph(insights.get(
        "resumo_executivo", "—"), estilos["corpo"]))
    elementos.append(Spacer(1, 0.4 * cm))

    # ── 3. CARDS INSTAGRAM ───────────────────────────────────────────────────
    if dados.get("instagram") != "Não informado":
        elementos.append(
            Paragraph("Instagram Presence", estilos["secao_titulo"]))
        elementos.append(HRFlowable(width="100%", thickness=1,
                         color=CINZA_CLARO, spaceAfter=8))
        elementos += cards_instagram(dados.get("instagram_dados", {}), estilos)

    # ── 4. PONTOS FORTES E FRACOS ────────────────────────────────────────────
    presenca = insights.get("presenca_digital", {})
    elementos += tabela_pontos(
        presenca.get("pontos_fortes", []),
        presenca.get("pontos_fracos", []),
        estilos
    )

    # ── 5. ESTRATÉGIA DE CONTEÚDO ────────────────────────────────────────────
    estrategia = insights.get("estrategia_conteudo", {})
    elementos.append(Paragraph("Content Strategy", estilos["secao_titulo"]))
    elementos.append(HRFlowable(width="100%", thickness=1,
                     color=CINZA_CLARO, spaceAfter=8))
    elementos.append(Paragraph(
        f"<b>Tone of voice:</b> {estrategia.get('tom_de_voz', '—')}", estilos["corpo"]))
    elementos.append(Paragraph(
        f"<b>Estimated frequency:</b> {estrategia.get('frequencia_estimada', '—')}", estilos["corpo"]))

    temas = estrategia.get("temas_principais", [])
    if temas:
        elementos.append(Paragraph("<b>Main themes:</b>", estilos["corpo"]))
        for tema in temas:
            elementos.append(Paragraph(f"▸  {tema}", estilos["item_lista"]))
    elementos.append(Spacer(1, 0.4 * cm))

    # ── 6. ENGAJAMENTO ───────────────────────────────────────────────────────
    eng = insights.get("engajamento", {})
    elementos.append(Paragraph("Engagement Analysis", estilos["secao_titulo"]))
    elementos.append(HRFlowable(width="100%", thickness=1,
                     color=CINZA_CLARO, spaceAfter=8))
    elementos.append(Paragraph(eng.get("avaliacao", "—"), estilos["corpo"]))
    elementos.append(Spacer(1, 0.4 * cm))

    # ── 7. OPORTUNIDADES ─────────────────────────────────────────────────────
    elementos += secao_lista(
        "Opportunities to Explore",
        insights.get("oportunidades", []),
        estilos,
        cor_bullet=VERDE
    )
    elementos.append(Spacer(1, 0.4 * cm))

    # ── 8. RECOMENDAÇÕES ─────────────────────────────────────────────────────
    elementos += secao_lista(
        "Strategic Recommendations",
        insights.get("recomendacoes", []),
        estilos,
        cor_bullet=AZUL_CLARO
    )

    # ── RODAPÉ ───────────────────────────────────────────────────────────────
    elementos.append(Spacer(1, 1 * cm))
    elementos.append(HRFlowable(width="100%", thickness=0.5,
                     color=CINZA_CLARO, spaceAfter=8))
    elementos.append(Paragraph(
        f"Report automatically generated on {dados['data_geracao']} · {dados['nome_cliente']}",
        estilos["rodape"]
    ))

    doc.build(elementos)
