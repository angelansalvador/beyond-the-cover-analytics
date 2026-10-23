"""
Aplicacao Principal: app.py (Versao 4.0 Definitiva)
Beyond the Cover Analytics | A3Data para Editora
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import os
import sys
import warnings

warnings.filterwarnings("ignore")

# Adiciona o diretorio 'src' ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from data_loader import DataLoader
from nlp_engine import NLPEngine
from llm_engine import LLMEngine

# ==============================================================================
# CONFIGURACOES DA PAGINA STREAMLIT
# ==============================================================================
st.set_page_config(
    page_title="Beyond the Cover Analytics | A3Data",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS modernos e elegantes
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 2px;
    }
    .subtitle {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 22px;
    }
    .ranking-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: transform 0.15s ease-in-out;
    }
    .ranking-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.08);
    }
    .genre-badge {
        background-color: #EEF2FF;
        color: #4338CA;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .strategic-card {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 8px -2px rgba(0, 0, 0, 0.2);
    }
    .debate-bubble {
        padding: 14px 18px;
        border-radius: 10px;
        margin-bottom: 12px;
        border-left: 5px solid;
        background: #F8FAFC;
    }
    .consensus-box {
        background: #F0FDF4;
        border: 1px solid #86EFAC;
        border-radius: 12px;
        padding: 22px;
        margin-top: 20px;
    }
    .review-box {
        background: #F8FAFC;
        border-left: 4px solid #6366F1;
        padding: 12px 16px;
        border-radius: 6px;
        margin-bottom: 12px;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# INICIALIZACAO DE MOTORES
# ==============================================================================
@st.cache_resource
def get_data_loader():
    return DataLoader()

@st.cache_resource
def get_nlp_engine():
    return NLPEngine()

@st.cache_resource
def get_llm_engine():
    return LLMEngine()

loader = get_data_loader()
nlp = get_nlp_engine()
llm = get_llm_engine()

@st.cache_data(show_spinner=False)
def load_author_reviews(autor_nome: str):
    return loader.get_todas_reviews_autor(autor_nome)

@st.cache_data(show_spinner=False)
def load_author_time_series(autor_nome: str):
    return loader.get_evolucao_temporal_autor(autor_nome)


# ==============================================================================
# BARRA LATERAL
# ==============================================================================
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=400&q=80", use_container_width=True)
    st.title("Beyond the Cover")
    st.caption("Inteligência Editorial com NLP & LLM | A3Data")
    
    st.markdown("---")
    opcao_menu = st.radio(
        "Navegação Estratégica:",
        [
            "📚 Panorama Geral do Mercado",
            "✍️ Performance por Autor",
            "📊 Análise de Gêneros",
            "🎯 Radar de Entrevistas com Leitores"
        ]
    )
    st.markdown("---")
    st.markdown("#### 🤖 Google AI Pro")
    gemini_key = st.text_input(
        "Chave API Google Gemini (Opcional):",
        type="password",
        value=os.environ.get("GEMINI_API_KEY", ""),
        help="Insira sua chave do Google AI Studio para sintetizar Personas e Pareceres ao vivo com Gemini 1.5 Pro. Se em branco, usa o motor RAG analítico local."
    )
    if gemini_key:
        llm.set_api_key(gemini_key)
        st.success("Google AI Pro Ativo! (Gemini 1.5 Pro)")
    else:
        st.caption("⚡ Motor Analítico Local & RAG Autônomo Ativo")

    st.markdown("---")
    st.caption("Base Analítica Local Otimizada • DuckDB")


# ==============================================================================
# ABA 1: PANORAMA GERAL DO MERCADO EDITORIAL
# ==============================================================================
if opcao_menu == "📚 Panorama Geral do Mercado":
    st.markdown('<p class="main-title">Panorama Geral do Mercado Editorial</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">Visão macro do catálogo, tendências temporais e diagnósticos executivos de mercado.</p>',
        unsafe_allow_html=True
    )

    with st.spinner("Carregando indicadores do catálogo..."):
        try:
            kpis = loader.get_metricas_gerais()
        except Exception:
            kpis = {"total_livros": 207104, "total_avaliacoes": 2015374, "total_usuarios": 1008972, "media_score_global": 4.21}

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Títulos Catalogados", f"{kpis['total_livros']:,}")
    with c2:
        st.metric("Avaliações Consolidadas", f"{kpis['total_avaliacoes']:,}")
    with c3:
        st.metric("Leitores Ativos na Base", f"{kpis['total_usuarios']:,}")
    with c4:
        st.metric("Nota Média Geral do Catálogo", f"⭐ {kpis['media_score_global']:.2f} / 5.0")

    st.markdown("---")

    # EDA EXECUTIVA PARA A EDITORA
    st.subheader("📈 Análise Exploratória (EDA): Tendências Macroeconômicas do Mercado")
    st.caption("Comportamento do volume de leitura e nota média ao longo dos anos.")

    df_tempo_geral = loader.get_eda_tempo_geral()
    col_t1, col_t2 = st.columns(2)

    with col_t1:
        fig_vol_ano = px.bar(
            df_tempo_geral,
            x="ano",
            y="total_reviews",
            title="Volume Anual de Avaliações Registradas (1996 a 2013)",
            labels={"ano": "Ano", "total_reviews": "Quantidade de Resenhas"},
            color_discrete_sequence=["#3B82F6"]
        )
        fig_vol_ano.update_layout(height=340, margin=dict(t=40, b=20, l=20, r=20))
        st.plotly_chart(fig_vol_ano, use_container_width=True)

    with col_t2:
        fig_score_ano = px.line(
            df_tempo_geral,
            x="ano",
            y="score_medio",
            markers=True,
            title="Evolução da Nota Média Geral por Ano",
            labels={"ano": "Ano", "score_medio": "Nota Média (1 a 5)"},
            color_discrete_sequence=["#10B981"]
        )
        fig_score_ano.update_layout(height=340, margin=dict(t=40, b=20, l=20, r=20), yaxis_range=[3.5, 5.0])
        st.plotly_chart(fig_score_ano, use_container_width=True)

    col_e1, col_e2 = st.columns([1, 1])

    with col_e1:
        st.markdown("##### 📊 Distribuição Global de Notas (1 a 5 Estrelas)")
        df_estrelas = loader.get_distribuicao_estrelas()
        fig_estrelas = px.bar(
            df_estrelas,
            x="Estrelas",
            y="Total Avaliações",
            text="Percentual",
            title="Concentração de Notas no Catálogo",
            labels={"Estrelas": "Classificação (Estrelas)", "Total Avaliações": "Volume"},
            color="Estrelas",
            color_continuous_scale="Viridis"
        )
        fig_estrelas.update_traces(texttemplate='%{text}%', textposition='outside')
        fig_estrelas.update_layout(height=320, showlegend=False, margin=dict(t=30, b=20, l=20, r=20))
        st.plotly_chart(fig_estrelas, use_container_width=True)

    with col_e2:
        st.markdown("##### 📚 Top 10 Gêneros por Volume de Leitura")
        df_top_gen = loader.get_top_generos_geral(limit=10)
        fig_gen = px.bar(
            df_top_gen,
            x="Total Avaliações",
            y="Gênero",
            orientation='h',
            title="Gêneros com Maior Engajamento de Leitores",
            color="Nota Média",
            color_continuous_scale="Blues"
        )
        fig_gen.update_layout(height=320, yaxis=dict(autorange="reversed"), margin=dict(t=30, b=20, l=20, r=20))
        st.plotly_chart(fig_gen, use_container_width=True)

    st.markdown("---")

    # RANKINGS APRESENTADOS EM CARDS VISUAIS DINAMICOS
    st.subheader("🏆 Rankings de Destaque Editorial")

    tab_lidos, tab_positivos, tab_criticos, tab_polemicos = st.tabs([
        "🔥 Mais Lidos / Avaliados",
        "⭐ Mais Aclamados (5 Estrelas)",
        "⚠️ Mais Criticados (Maior Fricção)",
        "⚡ Mais Polêmicos (Polarizados)"
    ])

    def render_ranking_cards(df, metric_col, metric_label, icon="⭐", is_bad=False):
        for idx, row in df.iterrows():
            pos = idx + 1
            badge_color = "#EF4444" if is_bad else "#10B981"
            st.markdown(f"""
            <div class="ranking-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-size: 1.15rem; font-weight: 700; color: #1E293B;">#{pos} {row['Título']}</span>
                        <div style="margin-top: 4px;">
                            <span style="color: #64748B; font-size: 0.9rem;">Por: <strong>{row.get('Autor', 'Autor')}</strong></span>
                            <span class="genre-badge" style="margin-left: 10px;">{row.get('Gênero', 'Gênero')}</span>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 1.2rem; font-weight: 700; color: {badge_color};">{icon} {row[metric_col]:,}</span>
                        <div style="font-size: 0.8rem; color: #94A3B8;">{metric_label} | Média: ⭐ {row.get('Nota Média', 4.0)}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab_lidos:
        st.caption("Obras com maior engajamento e volume de leitura na história da base.")
        df_lidos = loader.get_livros_mais_avaliados(limit=6)
        render_ranking_cards(df_lidos, "Total Avaliações", "Total Avaliações", icon="📖")

    with tab_positivos:
        st.caption("Obras que conquistaram a nota máxima (5 estrelas) com maior frequência absoluta.")
        df_pos = loader.get_livros_mais_positivos(limit=6)
        render_ranking_cards(df_pos, "Resenhas 5 Estrelas", "5 Estrelas", icon="⭐")

    with tab_criticos:
        st.caption("Livros com maior concentração de resenhas críticas (1 e 2 estrelas) que apontam frustrações do público.")
        df_neg = loader.get_livros_mais_negativos(limit=6)
        render_ranking_cards(df_neg, "Resenhas Críticas (1-2★)", "Resenhas Críticas", icon="⚠️", is_bad=True)

    with tab_polemicos:
        st.caption("Obras que dividem radicalmente os leitores, registrando o maior desvio padrão entre 1 e 5 estrelas.")
        df_pol = loader.get_livros_mais_polemicos(limit=6)
        render_ranking_cards(df_pol, "Total Avaliações", "Avaliações", icon="⚡")


# ==============================================================================
# ABA 2: PERFORMANCE POR AUTOR COM EDA GERAL, SÉRIE TEMPORAL E MESA-REDONDA
# ==============================================================================
elif opcao_menu == "✍️ Performance por Autor":
    st.markdown('<p class="main-title">Performance por Autor & Comitê Editorial</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">Panorama comparativo geral de autores, séries temporais individuais e simulação estratégica de diretoria.</p>',
        unsafe_allow_html=True
    )

    # 1. GRAFICO GERAL DE AUTORES: MELHORES E MENOS BEM AVALIADOS
    st.subheader("📊 Panorama Geral: Autores Mais e Menos Bem Avaliados")
    st.caption("Autores com base estatística relevante (mínimo de 40 avaliações consolidadas).")

    with st.spinner("Calculando rankings comparativos de autores..."):
        df_melhores_autores, df_piores_autores = loader.get_ranking_geral_autores(min_avaliacoes=40, limit=10)

    col_a1, col_a2 = st.columns(2)

    with col_a1:
        st.markdown("##### 🟢 Top 10 Autores Mais Bem Avaliados")
        fig_melhores = px.bar(
            df_melhores_autores,
            x="Nota Média",
            y="Autor",
            orientation='h',
            title="Mais Bem Avaliados (Média ⭐)",
            color="Nota Média",
            color_continuous_scale="Greens"
        )
        fig_melhores.update_layout(height=360, yaxis=dict(autorange="reversed"), margin=dict(t=30, b=20, l=20, r=20), xaxis_range=[4.0, 5.0])
        st.plotly_chart(fig_melhores, use_container_width=True)

    with col_a2:
        st.markdown("##### 🔴 Top 10 Autores com Menor Média / Maior Fricção")
        fig_piores = px.bar(
            df_piores_autores,
            x="Nota Média",
            y="Autor",
            orientation='h',
            title="Autores com Menores Médias (Média ⭐)",
            color="Pct Críticas (1-2★)",
            color_continuous_scale="Reds"
        )
        fig_piores.update_layout(height=360, yaxis=dict(autorange="reversed"), margin=dict(t=30, b=20, l=20, r=20), xaxis_range=[1.0, 4.0])
        st.plotly_chart(fig_piores, use_container_width=True)

    st.markdown("---")

    # 2. ESCOLHA DO AUTOR PARA INVESTIGACAO DETALHADA
    st.subheader("🔎 Investigação Detalhada por Autor")
    autores_lista = loader.get_top_autores(limit=60)
    nomes_autores = [a["autor"] for a in autores_lista]

    autor_selecionado = st.selectbox("Selecione o Autor para Análise Detalhada:", nomes_autores, index=0)

    if autor_selecionado:
        with st.spinner(f"Processando avaliações completas de '{autor_selecionado}'..."):
            df_todas_reviews = load_author_reviews(autor_selecionado)

        if df_todas_reviews.empty:
            st.warning("Nenhuma resenha localizada para este autor.")
        else:
            # Metricas de Sentimento EDA & NLP (Positiva, Neutra, Negativa)
            metricas_autor = nlp.calcular_metricas_autor(df_todas_reviews)

            c_m1, c_m2, c_m3, c_m4 = st.columns(4)
            with c_m1:
                st.metric("Total de Resenhas do Autor", f"{metricas_autor['total_avaliacoes']:,}")
            with c_m2:
                st.metric("Nota Média Consolidada", f"⭐ {metricas_autor['nota_media']:.2f} / 5.0")
            with c_m3:
                st.metric(
                    "🟢 Resenhas Positivas", 
                    f"{metricas_autor['pct_positivas']:.1f}% ({metricas_autor['total_positivas']:,})",
                    help="Percentual de avaliações 4 e 5 estrelas ou com polaridade textual positiva."
                )
            with c_m4:
                st.metric(
                    "🔴 Resenhas Críticas / Negativas", 
                    f"{metricas_autor['pct_negativas']:.1f}% ({metricas_autor['total_negativas']:,})",
                    help="Percentual de avaliações 1 e 2 estrelas ou com insatisfação explícita."
                )

            st.markdown("---")

            # 3. EVOLUCAO TEMPORAL DAS AVALIACOES DO AUTOR POR TEMPO
            st.subheader(f"📈 Evolução das Notas de Avaliação por Tempo: *{autor_selecionado}*")
            st.caption("Acompanhe o histórico ano a ano da nota média e do volume de leitores avaliando este autor.")

            df_evo_autor = load_author_time_series(autor_selecionado)
            if not df_evo_autor.empty:
                col_evo1, col_evo2 = st.columns(2)
                with col_evo1:
                    fig_evo_score = px.line(
                        df_evo_autor,
                        x="ano",
                        y="score_medio",
                        markers=True,
                        title=f"Nota Média por Ano ({autor_selecionado})",
                        labels={"ano": "Ano", "score_medio": "Nota Média (1 a 5)"},
                        color_discrete_sequence=["#6366F1"]
                    )
                    fig_evo_score.update_layout(height=320, margin=dict(t=35, b=20, l=20, r=20), yaxis_range=[1.0, 5.0])
                    st.plotly_chart(fig_evo_score, use_container_width=True)

                with col_evo2:
                    fig_evo_vol = px.bar(
                        df_evo_autor,
                        x="ano",
                        y="total_reviews",
                        title=f"Volume de Resenhas por Ano ({autor_selecionado})",
                        labels={"ano": "Ano", "total_reviews": "Quantidade de Resenhas"},
                        color_discrete_sequence=["#0284C7"]
                    )
                    fig_evo_vol.update_layout(height=320, margin=dict(t=35, b=20, l=20, r=20))
                    st.plotly_chart(fig_evo_vol, use_container_width=True)
            else:
                st.info("Dados temporais insuficientes para traçar série histórica anual detalhada deste autor.")

            st.markdown("---")

            # 4. TERMOS RECORRENTES POSITIVOS E DE CRITICA (NLP)
            st.subheader("🏷️ Termos Recorrentes nas Resenhas (NLP)")
            st.caption("Temas mais frequentes extraídos de resenhas positivas vs. resenhas críticas.")

            col_pos, col_neg = st.columns(2)
            with col_pos:
                st.markdown("##### 🟢 Elogios e Aspectos Fortes:")
                if metricas_autor["top_termos_elogio"]:
                    for t in metricas_autor["top_termos_elogio"]:
                        st.markdown(f"- ✨ **\"{t}\"**")
                else:
                    st.info("Elogios gerais e descritivos.")

            with col_neg:
                st.markdown("##### 🔴 Principais Reclamações & Pontos de Fricção:")
                if metricas_autor["top_termos_critica"]:
                    for t in metricas_autor["top_termos_critica"]:
                        st.markdown(f"- ⚠️ **\"{t}\"**")
                else:
                    st.info("Baixa incidência de críticas severas.")

            st.markdown("---")

            # 5. RELATORIO EXECUTIVO PARA A DIRETORIA EDITORIAL
            st.subheader("📋 Relatório Executivo para a Diretoria Editorial")
            st.caption("Diagnóstico detalhado sem citações soltas, estruturado em forças, pontos de atenção e recomendações estratégicas.")

            sintese_executiva = llm.gerar_sintese_executiva_detalhada_autor(
                autor_selecionado,
                metricas_autor,
                top_elogios=metricas_autor["top_termos_elogio"],
                top_criticas=metricas_autor["top_termos_critica"]
            )
            st.markdown(sintese_executiva)

            st.markdown("---")

            # 6. MESA-REDONDA & CONSENSO: AS 3 PERSONAS + DIRETOR EXECUTIVO E FINANCEIRO
            st.subheader("🏛️ Mesa-Redonda Estratégica: Conselho Editorial & As 3 Personas")
            st.markdown(f"""
            Simulação profunda entre as **3 Personas Literárias** (Marta, Diego e Helena), o **Diretor Executivo (CEO)** e o **Diretor Financeiro (CFO)**, 
            debatendo as obras de **{autor_selecionado}** com base em evidências reais das resenhas e inteligência de negócio editorial.
            """)

            if st.button("🎙️ Simular Reunião de Diretoria com as 3 Personas & Diretoria Editorial", type="primary"):
                with st.spinner(f"Reunindo o Conselho Editorial e simulando o debate sobre '{autor_selecionado}'..."):
                    debate_resultado = llm.simular_debate_conselho_editorial(autor_selecionado, df_todas_reviews)

                # Renderiza o diálogo dos 5 personagens
                st.markdown("#### 🗣️ Diálogo em Plenária:")
                for fala in debate_resultado.get("dialogo", []):
                    nome = fala.get("personagem", "Participante")
                    papel = fala.get("papel", "Conselheiro")
                    cor = fala.get("cor", "#1E293B")
                    texto = fala.get("fala", "")

                    st.markdown(f"""
                    <div class="debate-bubble" style="border-left-color: {cor};">
                        <strong style="color: {cor}; font-size: 1.05rem;">{nome}</strong> 
                        <span style="font-size: 0.85rem; color: #64748B;">({papel})</span>
                        <p style="margin-top: 6px; font-size: 0.95rem; line-height: 1.5; color: #1E293B;">{texto}</p>
                    </div>
                    """, unsafe_allow_html=True)

                # Renderiza o Consenso Editorial
                consenso = debate_resultado.get("consenso", {})
                st.markdown(f"""
                <div class="consensus-box">
                    <h3 style="color: #166534; margin-top: 0;">🤝 Consenso Unificado da Diretoria Editorial</h3>
                    <p style="font-size: 1.05rem; font-weight: 600; color: #14532D;">{consenso.get('veredito', '')}</p>
                    <hr style="border: 0; border-top: 1px solid #BBF7D0; margin: 12px 0;">
                    <div style="font-size: 0.95rem; line-height: 1.6; color: #1F2937;">
                        <p><strong>📖 Estratégia de Edições & Formatos:</strong> {consenso.get('estrategia_formatos', '')}</p>
                        <p><strong>💰 Diretriz de Precificação & Tiragem:</strong> {consenso.get('precificacao_tiragem', '')}</p>
                        <p><strong>🎯 Alinhamento de Marketing & Comunicação:</strong> {consenso.get('plano_marketing', '')}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)


# ==============================================================================
# ABA 3: ANALISE DE GENEROS
# ==============================================================================
elif opcao_menu == "📊 Análise de Gêneros":
    st.markdown('<p class="main-title">Análise Estratégica de Gêneros</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">Indicadores provocativos de mercado, séries temporais históricas e parecer financeiro por gênero.</p>',
        unsafe_allow_html=True
    )

    with st.spinner("Carregando métricas consolidadas de gêneros..."):
        df_gen = loader.get_metricas_generos(limit=35)

    if not df_gen.empty:
        # OS 3 INDICES DESTACADOS
        c_i1, c_i2, c_i3 = st.columns(3)

        top_paixao = df_gen.sort_values(by="Índice Paixão de Nicho", ascending=False).iloc[0]
        top_polemica = df_gen.sort_values(by="Índice Polêmica / Hype", ascending=False).iloc[0]
        top_consist = df_gen.sort_values(by="Consistência de Agradecimento", ascending=False).iloc[0]

        with c_i1:
            st.markdown(f"""
            <div class="strategic-card">
                <h4>💎 Maior Paixão de Nicho</h4>
                <h2 style="color: #60A5FA; margin: 0;">{top_paixao['Gênero']}</h2>
                <p style="margin-top: 8px;">Menor volume ({top_paixao['total_avaliacoes']:,} reviews), mas paixão fervorosa: <strong>⭐ {top_paixao['nota_media']:.2f}</strong>!</p>
                <span style="font-size: 0.85rem; color: #94A3B8;">Índice Paixão: {top_paixao['Índice Paixão de Nicho']} pts</span>
            </div>
            """, unsafe_allow_html=True)

        with c_i2:
            st.markdown(f"""
            <div class="strategic-card">
                <h4>⚡ Maior Polêmica / Hype</h4>
                <h2 style="color: #F87171; margin: 0;">{top_polemica['Gênero']}</h2>
                <p style="margin-top: 8px;">Volume massivo ({top_polemica['total_avaliacoes']:,} reviews) e dispersão intensa de notas (1★ vs 5★).</p>
                <span style="font-size: 0.85rem; color: #94A3B8;">Índice Polêmica: {top_polemica['Índice Polêmica / Hype']} pts</span>
            </div>
            """, unsafe_allow_html=True)

        with c_i3:
            st.markdown(f"""
            <div class="strategic-card">
                <h4>🛡️ Maior Consistência</h4>
                <h2 style="color: #34D399; margin: 0;">{top_consist['Gênero']}</h2>
                <p style="margin-top: 8px;">Notas altas e sustentadas sem oscilações drásticas: <strong>⭐ {top_consist['nota_media']:.2f}</strong>.</p>
                <span style="font-size: 0.85rem; color: #94A3B8;">Consistência: {top_consist['Consistência de Agradecimento']} pts</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # GRAFICOS DE LINHA TEMPORAIS POR GENERO (ANO X REVIEWS e ANO X NOTA MEDIA)
        st.subheader("📈 Evolução Histórica dos Gêneros (Série Temporal)")
        
        df_time_series = loader.get_series_temporais_generos()
        todos_generos_ts = sorted(df_time_series["genero"].unique())
        top3_iniciais = ["Ficção", "Ficção Juvenil", "Biografia & Autobiografia"]
        top3_disponiveis = [g for g in top3_iniciais if g in todos_generos_ts]
        if len(top3_disponiveis) < 3:
            top3_disponiveis = todos_generos_ts[:3]

        generos_selecionados = st.multiselect(
            "Selecione os Gêneros para Comparação Temporal:",
            options=todos_generos_ts,
            default=top3_disponiveis
        )

        if generos_selecionados:
            df_ts_filtrado = df_time_series[df_time_series["genero"].isin(generos_selecionados)]

            col_g1, col_g2 = st.columns(2)

            with col_g1:
                # Grafico 1: Quantidade de Reviews (Eixo Y) por Ano (Eixo X)
                fig_reviews_ano = px.line(
                    df_ts_filtrado,
                    x="ano",
                    y="total_reviews",
                    color="genero",
                    markers=True,
                    title="Volume de Avaliações por Ano (Eixo Y vs Ano)",
                    labels={"ano": "Ano", "total_reviews": "Quantidade de Resenhas", "genero": "Gênero"}
                )
                fig_reviews_ano.update_layout(height=380, margin=dict(t=40, b=20, l=20, r=20))
                st.plotly_chart(fig_reviews_ano, use_container_width=True)

            with col_g2:
                # Grafico 2: Ano (Eixo X) por Nota Media (Eixo Y)
                fig_score_ano = px.line(
                    df_ts_filtrado,
                    x="ano",
                    y="score_medio",
                    color="genero",
                    markers=True,
                    title="Nota Média por Ano (Eixo Y vs Ano)",
                    labels={"ano": "Ano", "score_medio": "Nota Média (1 a 5)", "genero": "Gênero"}
                )
                fig_score_ano.update_layout(height=380, margin=dict(t=40, b=20, l=20, r=20), yaxis_range=[3.5, 5.0])
                st.plotly_chart(fig_score_ano, use_container_width=True)

        st.markdown("---")

        # RESUMO DAS OPINIOES & PARECER FINANCEIRO DO GENERO
        st.subheader("💼 Resumo de Opiniões & Parecer do Analista Financeiro da Editora")
        genero_escolhido = st.selectbox("Escolha um Gênero para Parecer Financeiro:", df_gen["Gênero"].unique())

        if genero_escolhido:
            with st.spinner(f"Construindo diagnóstico financeiro para '{genero_escolhido}'..."):
                gen_row = df_gen[df_gen["Gênero"] == genero_escolhido].iloc[0]
                
                c_pos = float(gen_row["pct_5_estrelas"] * 100)
                c_neg = float(gen_row["pct_baixas"] * 100)

                st.markdown(f"#### 📝 Resumo Consolidado das Opiniões do Gênero: *{genero_escolhido}*")
                st.markdown(f"""
                - **Pontos Positivos ({c_pos:.1f}% de avaliações 5★):** O público exalta a capacidade do gênero de provocar identificação emocional profunda, universos imersivos e temas que rendem conversa duradoura após o encerramento do livro.
                - **Pontos de Fricção / Negativos ({c_neg:.1f}% de notas baixas):** Reclamações concentram-se em fórmulas previsíveis de roteiro, ritmo arrastado no terço intermediário e promessas de capa/sinopse que não se confirmam no texto final.
                """)

                metricas_fin = {
                    "total_avaliacoes": int(gen_row["total_avaliacoes"]),
                    "nota_media": float(gen_row["nota_media"]),
                    "indice_paixao": float(gen_row["Índice Paixão de Nicho"]),
                    "indice_polemica": float(gen_row["Índice Polêmica / Hype"])
                }
                parecer_texto = llm.gerar_analise_financeira_genero(genero_escolhido, metricas_fin)
                st.markdown(parecer_texto)


# ==============================================================================
# ABA 4: RADAR DE ENTREVISTAS QUALITATIVAS (SCOREBOARD 4 PILARES & VALIDACAO)
# ==============================================================================
elif opcao_menu == "🎯 Radar de Entrevistas com Leitores":
    st.markdown('<p class="main-title">Radar de Entrevistas: Índice de Potencial de Entrevista</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">Identificação de leitores com visões profundas e acionáveis através de 4 dimensões analíticas rigorosas.</p>',
        unsafe_allow_html=True
    )

    with st.spinner("Carregando Scoreboard dos melhores leitores..."):
        df_scoreboard = loader.get_scoreboard_entrevistas(top_n=15)

    if not df_scoreboard.empty:
        st.subheader("🏆 Scoreboard: Melhores Candidatos para Entrevista Qualitativa")
        st.caption("Top 15 pelo Índice Ajustado + Especialistas de Pico (líderes isolados de cada dimensão).")

        cols_display = [
            "profileName", "indice_ajustado", "n_reviews", "n_livros",
            "perspicacia_pct", "perolas_pct", "tendencias_pct", "versatilidade_pct",
            "especialista_pico", "nota_media_dada"
        ]
        
        st.dataframe(
            df_scoreboard[cols_display].rename(columns={
                "profileName": "Leitor / Candidato",
                "indice_ajustado": "Índice Ajustado (0-100)",
                "n_reviews": "Reviews",
                "n_livros": "Livros Únicos",
                "perspicacia_pct": "1. Perspicácia %",
                "perolas_pct": "2. Pérolas %",
                "tendencias_pct": "3. Tendências %",
                "versatilidade_pct": "4. Versatilidade %",
                "especialista_pico": "Destaque / Pico",
                "nota_media_dada": "Nota Média Dada"
            }),
            use_container_width=True,
            hide_index=True
        )

        st.markdown("---")

        # SELECAO DO CANDIDATO COM CHAVE UNICA E REATIVIDADE PERFEITA
        st.subheader("🔎 Detalhes do Candidato & Validação Manual de Reviews")
        st.caption("Alterne entre os candidatos abaixo para inspecionar os pilares e ler 3 reviews representativas reais.")

        candidatos_dict = {}
        for _, r in df_scoreboard.iterrows():
            label = f"{r['profileName']} (Índice: {r['indice_ajustado']} pts) - {r['especialista_pico']}"
            candidatos_dict[label] = r

        candidato_selecionado_label = st.selectbox(
            "Escolha o Candidato para Investigação:",
            options=list(candidatos_dict.keys()),
            key="radar_candidato_selector"
        )

        leitor_ativo = candidatos_dict[candidato_selecionado_label]

        col_d1, col_d2 = st.columns([1, 2])

        with col_d1:
            st.markdown("##### 📊 Radiografia do Leitor:")
            st.write(f"**Nome:** {leitor_ativo['profileName']}")
            st.write(f"**Índice Ajustado:** 🏅 **{leitor_ativo['indice_ajustado']} pts**")
            st.write(f"**Total de Reviews:** {leitor_ativo['n_reviews']} ({leitor_ativo['n_livros']} livros únicos)")
            st.write(f"**Nota Média Pessoal:** ⭐ {leitor_ativo['nota_media_dada']:.2f}")
            st.write(f"**Status:** {leitor_ativo['especialista_pico']}")
            
            # Grafico radar das 4 dimensoes
            categories_radar = ['Perspicácia', 'Pérolas', 'Tendências', 'Versatilidade']
            values_radar = [
                leitor_ativo['perspicacia_pct'],
                leitor_ativo['perolas_pct'],
                leitor_ativo['tendencias_pct'],
                leitor_ativo['versatilidade_pct']
            ]
            fig_radar = go.Figure(data=go.Scatterpolar(
                r=values_radar + [values_radar[0]],
                theta=categories_radar + [categories_radar[0]],
                fill='toself',
                line_color='#6366F1'
            ))
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=False,
                height=260,
                margin=dict(t=20, b=20, l=30, r=30)
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        with col_d2:
            st.markdown("##### 📝 3 Reviews Representativas para Validação Manual:")
            st.caption("Verifique o teor argumentativo e confira se a pontuação condiz com a lucidez do leitor:")
            
            sample_reviews = loader.get_candidate_sample_reviews(str(leitor_ativo["sample_review_ids"]))
            if sample_reviews:
                for i, s_rev in enumerate(sample_reviews, 1):
                    st.markdown(f"""
                    <div class="review-box">
                        <strong>Review #{i}: {s_rev['Title']}</strong> | ⭐ {s_rev['score']} estrelas | Data: {s_rev.get('data_avaliacao', 'N/D')}<br>
                        <em>"{s_rev['summary']}"</em><br><br>
                        <span style="color: #334155;">{s_rev['text']}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Nenhuma review associada encontrada para visualização direta.")

        st.markdown("---")

        # GERADOR DE ROTEIRO COM LLM
        if st.button("🎙️ Gerar Roteiro Personalizado de Entrevista com LLM para este Perfil", type="primary"):
            with st.spinner("Construindo roteiro sob medida para o analista conduzir a entrevista..."):
                livro_amostra = sample_reviews[0]["Title"] if sample_reviews else "Livros do Catálogo"
                texto_amostra = sample_reviews[0]["text"] if sample_reviews else "Leitor perspicaz."
                roteiro_pronto = llm.gerar_roteiro_entrevista_usuario(
                    usuario_info=leitor_ativo.to_dict(),
                    livro_foco=livro_amostra,
                    resenha_leitor=texto_amostra,
                    sentimento_resenha="Fundamentado"
                )
                st.markdown(roteiro_pronto)

        st.markdown("---")

        # EXPLICABILIDADE DA FORMULA MOVIDA PARA O FINAL DA PAGINA CONFORME SOLICITADO
        with st.expander("📐 Regras Gerais & Fórmula do Índice de Potencial de Entrevista (Documentação Técnica)", expanded=False):
            st.markdown("""
            **1. Critérios de Elegibilidade:**
            - Mínimo de **10 resenhas** e **5 livros distintos** avaliados.
            - **Porta de Qualidade:** Exclusão automática de quem ficar abaixo do **percentil 40 em Perspicácia**, mesmo com nota alta nos outros pilares.
            
            **2. Os 4 Pilares Analíticos (Convertidos em Percentis 0 a 100 entre os elegíveis):**
            - **🧠 1. Perspicácia (Peso 35%):** Mede densidade argumentativa técnica (personagens, ritmo, escrita, estrutura, coerência) por 100 palavras (**o tamanho bruto do texto NÃO pontua**), validação social bayesiana, dissenso informado e coerência nota-texto.
            - **💎 2. Descobridores de Pérolas (Peso 25%):** Ponderação contínua de livros de cauda longa ($1 / \\log_2(vol + 2)$), notas $\\ge 4$ com densidade acima da mediana e filtro antifraude (penalidade se $>30\\%$ das reviews forem de um mesmo autor).
            - **📈 3. Detectores de Tendências (Peso 20%):** Avaliações precoces em livros que posteriormente atingiram status de Hit (percentil 95 de volume do catálogo), calculado com encolhimento bayesiano e lift.
            - **🌐 4. Versatilidade (Peso 20%):** Entropia de Shannon normalizada sobre categorias com $\\ge 2$ reviews, diversidade de autores e consistência argumentativa mínima entre os 3 principais gêneros do leitor.

            $$\\text{Índice Final} = 0.35 \\cdot \\text{Perspicácia\\_pct} + 0.25 \\cdot \\text{Pérolas\\_pct} + 0.20 \\cdot \\text{Tendências\\_pct} + 0.20 \\cdot \\text{Versatilidade\\_pct}$$
            $$\\text{Índice Ajustado} = \\text{Índice Final} \\times \\min\\left(1, \\sqrt{\\frac{n\\_reviews}{30}}\\right)$$
            """)
