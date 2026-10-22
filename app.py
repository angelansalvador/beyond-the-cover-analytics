"""
Aplicacao Principal: app.py
Descricao: Plataforma Interativa 'Beyond the Cover Analytics'
Desenvolvida para a Editora transformar 3 dias de analise manual em segundos de insight,
utilizando Processamento de Linguagem Natural (NLP) e Grandes Modelos de Linguagem (LLMs).
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
import os
import sys

# Adiciona o diretorio 'src' ao caminho de importacao do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from business_metrics import ROICalculator, BusinessScenario
from nlp_engine import NLPEngine
from llm_engine import LLMEngine
from data_loader import DataLoader

# ==============================================================================
# CONFIGURACOES DA PAGINA STREAMLIT
# ==============================================================================
st.set_page_config(
    page_title="Beyond the Cover Analytics | A3Data",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos visuais personalizados em CSS para um visual moderno e executivo
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0px;
    }
    .subtitle {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 25px;
    }
    .metric-card {
        background-color: #F8FAFC;
        border-radius: 10px;
        padding: 20px;
        border-left: 5px solid #2563EB;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .roi-badge {
        background-color: #DCFCE7;
        color: #166534;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# INICIALIZACAO DE SINGLETONS E CACHES (PERFORMANCE)
# ==============================================================================
@st.cache_resource
def get_data_loader():
    """Instancia e mantem em cache o orquestrador DuckDB."""
    loader = DataLoader()
    return loader

@st.cache_resource
def get_nlp_engine():
    """Instancia em cache o motor de Processamento de Linguagem Natural (NLP)."""
    return NLPEngine()

@st.cache_resource
def get_llm_engine():
    """Instancia em cache o motor de sintese executiva com LLM."""
    return LLMEngine()

loader = get_data_loader()
nlp = get_nlp_engine()
llm = get_llm_engine()


# ==============================================================================
# BARRA LATERAL (SIDEBAR): NAVEGACAO E CONFIGURACOES
# ==============================================================================
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=400&q=80", use_container_width=True)
    st.title("Beyond the Cover")
    st.caption("Inteligência Editorial com NLP & LLM | A3Data")
    
    st.markdown("---")
    opcao_menu = st.radio(
        "Navegação Estratégica:",
        [
            "📊 Visão Geral & Business Case (ROI)",
            "✍️ Performance por Autor",
            "📚 Análise de Gêneros & Categorias",
            "🎯 Radar de Entrevistas Qualitativas"
        ]
    )
    
    st.markdown("---")
    st.subheader("💡 Glossário Rápido")
    with st.expander("Ver Siglas e Conceitos"):
        st.markdown("""
        * **NLP** (*Natural Language Processing*): Processamento de Linguagem Natural para minerar resenhas.
        * **LLM** (*Large Language Models*): Modelos neurais que geram sínteses executivas e roteiros de entrevista.
        * **ROI** (*Return on Investment*): Retorno financeiro e economia gerada com automação.
        * **TF-IDF**: Algoritmo que encontra as palavras mais exclusivas e relevantes de cada autor/gênero.
        * **VADER**: Algoritmo de sentimento que calcula se uma resenha é Positiva, Neutra ou Negativa.
        """)
        
    st.caption("Ambiente Local Otimizado • DuckDB & Parquet")


# ==============================================================================
# ABA 1: VISAO GERAL & BUSINESS CASE (CALCULADORA DE ROI)
# ==============================================================================
if opcao_menu == "📊 Visão Geral & Business Case (ROI)":
    st.markdown('<p class="main-title">Visão Geral & Business Case Editorial</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">Diagnóstico financeiro e impacto da substituição do processo manual de exploração por inteligência artificial.</p>',
        unsafe_allow_html=True
    )
    
    # Metricas Globais da Base
    with st.spinner("Carregando indicadores globais da base..."):
        try:
            kpis = loader.get_metricas_gerais()
        except Exception:
            kpis = {"total_livros": 212404, "total_avaliacoes": 3000000, "total_usuarios": 1250000, "media_score_global": 4.18}

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total de Livros Catalogados", f"{kpis['total_livros']:,}")
    with col2:
        st.metric("Total de Avaliações (Reviews)", f"{kpis['total_avaliacoes']:,}")
    with col3:
        st.metric("Leitores Ativos (Usuários)", f"{kpis['total_usuarios']:,}")
    with col4:
        st.metric("Nota Média Global do Catálogo", f"⭐ {kpis['media_score_global']:.2f} / 5.0")

    st.markdown("---")
    
    # Secao de Impacto de Negocio e Calculadora Interativa
    st.subheader("💰 Calculadora de Impacto Financeiro & Redução de Custos (ROI)")
    st.markdown("""
    O modelo substitui o esforço manual de 5 analistas que antes levavam 3 dias úteis por análise,
    reduzindo o tempo de entrega para **segundos** e liberando a equipe para frentes estratégicas.
    """)
    
    col_params, col_results = st.columns([1, 2])
    
    with col_params:
        st.markdown("#### Parâmetros Operacionais")
        analistas_input = st.number_input("Nº de Analistas Alocados:", min_value=1, max_value=20, value=5)
        salario_input = st.number_input("Salário Mensal Médio (R$):", min_value=1000.0, max_value=30000.0, value=5000.0, step=500.0)
        dias_input = st.number_input("Dias Úteis por Análise Manual:", min_value=1.0, max_value=15.0, value=3.0, step=0.5)
        
        scenario_custom = BusinessScenario(
            num_analistas=int(analistas_input),
            salario_mensal_unitario=float(salario_input),
            dias_por_analise_manual=float(dias_input)
        )
        calc = ROICalculator(scenario_custom)
        manual = calc.calcular_cenario_manual()
        auto = calc.calcular_cenario_automatizado(tempo_segundos_por_analise=15.0)

    with col_results:
        st.markdown("#### Comparativo de Eficiência (Antes vs Depois)")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric(
                label="Tempo de Resposta",
                value=f"{auto['tempo_segundos_por_analise']:.0f} segundos",
                delta=f"-{auto['reducao_tempo_percentual']:.2f}% de tempo"
            )
        with c2:
            st.metric(
                label="Economia Salarial Mensal",
                value=f"R$ {auto['economia_mensal_salarios']:,.2f}",
                delta=f"R$ {auto['economia_anual_salarios']:,.2f} / ano"
            )
        with c3:
            st.metric(
                label="Analistas Liberados",
                value=f"{auto['analistas_liberados_para_estrategia']} profissionais",
                delta="100% alocados em estratégia"
            )

        # Grafico comparativo de Horas Dedicadas
        df_comp = pd.DataFrame({
            "Processo": ["Manual (Antes)", "Beyond the Cover (Depois)"],
            "Horas Gastas por Análise": [manual["horas_homem_por_analise"], auto["tempo_segundos_por_analise"] / 3600.0],
            "Custo Estimado por Relatório (R$)": [manual["custo_por_analise_manual"], 0.50]
        })
        
        fig = px.bar(
            df_comp,
            x="Processo",
            y="Horas Gastas por Análise",
            text="Horas Gastas por Análise",
            title="Horas-Homem Necessárias por Relatório de Análise",
            color="Processo",
            color_discrete_sequence=["#EF4444", "#10B981"]
        )
        fig.update_traces(texttemplate='%{text:.1f}h', textposition='outside')
        fig.update_layout(showlegend=False, height=320, margin=dict(t=40, b=20, l=20, r=20))
        st.plotly_chart(fig, use_container_width=True)

    # Texto Executivo para Apresentacao a Diretoria
    with st.expander("📄 Ver Relatório Executivo Formal para Diretoria da Editora"):
        st.text(calc.gerar_relatorio_impacto_executivo())


# ==============================================================================
# ABA 2: PERFORMANCE POR AUTOR (COM SINTESE EXECUTIVA LLM)
# ==============================================================================
elif opcao_menu == "✍️ Performance por Autor":
    st.markdown('<p class="main-title">Diagnóstico de Performance de Autores</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">Análise aprofundada de sentimento, evolução temporal e temas recorrentes das obras de um autor.</p>',
        unsafe_allow_html=True
    )
    
    with st.spinner("Carregando autores do catálogo..."):
        try:
            autores_lista = loader.get_top_autores(limit=40)
            nomes_autores = [a["autor"] for a in autores_lista]
        except Exception:
            nomes_autores = ["Philip Nel", "Julie Strain", "Stephen King", "J.K. Rowling", "Agatha Christie"]

    autor_selecionado = st.selectbox("Selecione um Autor para Investigação:", nomes_autores, index=0)
    
    if autor_selecionado:
        with st.spinner(f"Processando avaliações e minerando sentimentos de '{autor_selecionado}'..."):
            df_reviews_autor = loader.get_reviews_por_autor(autor_selecionado, limit=200)

        if df_reviews_autor.empty:
            st.warning("Nenhuma avaliação detalhada encontrada para este autor no filtro atual.")
        else:
            # Enriquecimento com Sentimento VADER
            df_reviews_autor["sentimento_info"] = df_reviews_autor["text"].apply(nlp.analisar_sentimento_resenha)
            df_reviews_autor["sentiment_compound"] = df_reviews_autor["sentimento_info"].apply(lambda x: x["compound"])
            df_reviews_autor["sentiment_cat"] = df_reviews_autor["sentimento_info"].apply(lambda x: x["categoria"])

            # Metricas Principais do Autor
            total_revs = len(df_reviews_autor)
            media_score = df_reviews_autor["score"].mean()
            pct_pos = (df_reviews_autor["sentiment_cat"] == "Positivo").mean() * 100
            pct_neg = (df_reviews_autor["sentiment_cat"] == "Negativo").mean() * 100

            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            with col_m1:
                st.metric("Total de Resenhas na Amostra", f"{total_revs}")
            with col_m2:
                st.metric("Nota Média do Autor", f"⭐ {media_score:.2f} / 5.0")
            with col_m3:
                st.metric("Sentimento Positivo", f"{pct_pos:.1f}%")
            with col_m4:
                st.metric("Sentimento Crítico / Negativo", f"{pct_neg:.1f}%")

            st.markdown("---")
            
            # Graficos de Sentimento e Distribuicao de Estrelas
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                # Distribuicao de Notas
                score_counts = df_reviews_autor["score"].value_counts().reset_index()
                score_counts.columns = ["Nota", "Quantidade"]
                score_counts = score_counts.sort_values(by="Nota")
                
                fig_scores = px.bar(
                    score_counts,
                    x="Nota",
                    y="Quantidade",
                    text="Quantidade",
                    title="Distribuição das Avaliações (Estrelas 1 a 5)",
                    color="Nota",
                    color_continuous_scale="Blues"
                )
                fig_scores.update_layout(height=300, showlegend=False, margin=dict(t=40, b=20, l=20, r=20))
                st.plotly_chart(fig_scores, use_container_width=True)

            with col_chart2:
                # Distribuicao de Sentimento (VADER)
                sent_counts = df_reviews_autor["sentiment_cat"].value_counts().reset_index()
                sent_counts.columns = ["Sentimento", "Total"]
                fig_sent = px.pie(
                    sent_counts,
                    names="Sentimento",
                    values="Total",
                    title="Sentimento das Resenhas (NLP VADER)",
                    color="Sentimento",
                    color_discrete_map={"Positivo": "#10B981", "Neutro": "#6B7280", "Negativo": "#EF4444"},
                    hole=0.45
                )
                fig_sent.update_layout(height=300, margin=dict(t=40, b=20, l=20, r=20))
                st.plotly_chart(fig_sent, use_container_width=True)

            # Extracao de Topicos TF-IDF
            st.subheader("🔍 Temas & Palavras-Chave Mais Debatidos nas Resenhas (TF-IDF)")
            textos_amostra = df_reviews_autor["text"].dropna().tolist()
            topicos_extraidos = nlp.extrair_topicos_chave(textos_amostra, top_n=8)
            
            if topicos_extraidos:
                cols_top = st.columns(len(topicos_extraidos))
                for idx, t in enumerate(topicos_extraidos):
                    with cols_top[idx]:
                        st.info(f"**{t['termo'].title()}**\n\nScore: {t['score']}")
            else:
                st.caption("Amostra textual insuficiente para mineracao TF-IDF.")

            st.markdown("---")

            # DIFERENCIAL DE LLM: Sintese Executiva com 1 Clique
            st.subheader("🤖 Síntese Executiva Gerada por LLM (Diferencial Competitivo)")
            st.markdown("Gere instantaneamente um memorando estratégico para o comitê editorial da editora:")
            
            if st.button("✨ Gerar Relatório Executivo com LLM", type="primary"):
                with st.spinner("Orquestrando modelo de linguagem e sintetizando feedbacks..."):
                    # Separa amostras de positivas e negativas
                    pos_samples = df_reviews_autor[df_reviews_autor["sentiment_cat"] == "Positivo"]["text"].dropna().tolist()
                    neg_samples = df_reviews_autor[df_reviews_autor["sentiment_cat"] == "Negativo"]["text"].dropna().tolist()
                    termos_str = [t["termo"] for t in topicos_extraidos]
                    
                    metricas_dict = {
                        "total_avaliacoes": total_revs,
                        "nota_media": media_score,
                        "pct_positivas": pct_pos,
                        "pct_negativas": pct_neg
                    }
                    
                    sintese_gerada = llm.gerar_sintese_executiva_autor(
                        autor_selecionado,
                        metricas_dict,
                        termos_str,
                        pos_samples,
                        neg_samples
                    )
                    st.success("Síntese Executiva Concluída!")
                    st.markdown(sintese_gerada)


# ==============================================================================
# ABA 3: ANALISE DE GENEROS E CATEGORIAS
# ==============================================================================
elif opcao_menu == "📚 Análise de Gêneros & Categorias":
    st.markdown('<p class="main-title">Análise de Gêneros & Categorias Literárias</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">Visão macro para identificar nichos com alta demanda e oportunidades de novos lançamentos.</p>',
        unsafe_allow_html=True
    )
    
    with st.spinner("Carregando categorias do catálogo..."):
        try:
            cats_data = loader.get_top_categorias(limit=25)
            df_cats = pd.DataFrame(cats_data)
        except Exception:
            df_cats = pd.DataFrame([
                {"categoria": "Fiction", "total_avaliacoes": 500000, "nota_media": 4.15, "total_livros": 32000},
                {"categoria": "Religion", "total_avaliacoes": 220000, "nota_media": 4.35, "total_livros": 18000},
                {"categoria": "Biography & Autobiography", "total_avaliacoes": 180000, "nota_media": 4.20, "total_livros": 12000},
                {"categoria": "History", "total_avaliacoes": 150000, "nota_media": 4.10, "total_livros": 11000}
            ])

    # Grafico de dispersao (Volume vs Nota Media)
    fig_cat_scatter = px.scatter(
        df_cats,
        x="total_avaliacoes",
        y="nota_media",
        size="total_livros",
        hover_name="categoria",
        text="categoria",
        title="Matriz de Oportunidade Editorial: Volume de Avaliações vs Satisfação (Nota Média)",
        labels={"total_avaliacoes": "Volume de Avaliações", "nota_media": "Nota Média (1 a 5)", "total_livros": "Títulos"},
        color="nota_media",
        color_continuous_scale="Viridis"
    )
    fig_cat_scatter.update_traces(textposition='top center')
    fig_cat_scatter.update_layout(height=480, margin=dict(t=50, b=20, l=20, r=20))
    st.plotly_chart(fig_cat_scatter, use_container_width=True)

    # Detalhamento de uma categoria
    st.markdown("---")
    cat_escolhida = st.selectbox("Selecione um Gênero para Mineração de Sentimentos:", df_cats["categoria"].unique())
    
    if cat_escolhida:
        with st.spinner(f"Buscando resenhas do gênero '{cat_escolhida}'..."):
            df_revs_cat = loader.get_reviews_por_categoria(cat_escolhida, limit=150)
            
        if not df_revs_cat.empty:
            df_revs_cat["sentimento_info"] = df_revs_cat["text"].apply(nlp.analisar_sentimento_resenha)
            df_revs_cat["sent_cat"] = df_revs_cat["sentimento_info"].apply(lambda x: x["categoria"])
            
            c_pos = (df_revs_cat["sent_cat"] == "Positivo").mean() * 100
            c_neg = (df_revs_cat["sent_cat"] == "Negativo").mean() * 100
            
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Total Analisado no Gênero", f"{len(df_revs_cat)}")
            with c2:
                st.metric("Índice Positivo do Gênero", f"{c_pos:.1f}%")
            with c3:
                st.metric("Índice de Fricção/Crítica", f"{c_neg:.1f}%")
                
            top_terms_cat = nlp.extrair_topicos_chave(df_revs_cat["text"].dropna().tolist(), top_n=6)
            st.markdown("**Palavras-chave mais frequentes no gênero:**")
            st.write(", ".join([f"`{t['termo']}`" for t in top_terms_cat]) if top_terms_cat else "Sem termos suficientes.")


# ==============================================================================
# ABA 4: RADAR DE ENTREVISTAS QUALITATIVAS (SUPER-LEITORES)
# ==============================================================================
elif opcao_menu == "🎯 Radar de Entrevistas Qualitativas":
    st.markdown('<p class="main-title">Radar de Seleção de Leitores para Entrevistas</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">Algoritmo inteligente de NLP que identifica os leitores ideais para entrevistas qualitativas e gera roteiros com LLM.</p>',
        unsafe_allow_html=True
    )
    
    st.info("""
    **Como funciona o Algoritmo de Priorização (Interview Priority Score):**
    Analisa a **profundidade textual** da resenha (leitores com análises detalhadas entre 150 e 400 palavras),
    **nuance crítica** (leitores moderados que expõem prós e contras) e a **riqueza do título**, ranqueando de 0 a 100.
    """)
    
    # Filtro de Busca
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        termo_busca = st.text_input("Filtrar por Nome de Autor ou Palavra do Livro:", value="Seuss")
    with col_f2:
        qtd_leitores = st.slider("Qtd de Candidatos a Listar:", min_value=5, max_value=30, value=10)

    if termo_busca:
        with st.spinner(f"Varrendo resenhas e calculando Score de Entrevista para '{termo_busca}'..."):
            df_candidatos = loader.get_reviews_por_autor(termo_busca, limit=200)
            
            if df_candidatos.empty:
                # Tenta por categoria
                df_candidatos = loader.get_reviews_por_categoria(termo_busca, limit=200)

        if df_candidatos.empty:
            st.warning("Nenhum leitor encontrado para o termo pesquisado. Tente outro nome de autor (ex: 'Nel', 'Julie', 'King').")
        else:
            # Aplica o algoritmo de NLP
            df_candidatos = nlp.calcular_score_relevancia_entrevista(df_candidatos)
            df_top_entrevistas = df_candidatos.sort_values(by="interview_priority_score", ascending=False).head(qtd_leitores)
            
            # Tabela de Melhores Candidatos
            st.markdown("### 🏆 Top Leitores Selecionados pelo Algoritmo")
            colunas_exibir = ["profileName", "Title", "score", "word_count", "interview_priority_score", "summary"]
            st.dataframe(
                df_top_entrevistas[colunas_exibir].rename(columns={
                    "profileName": "Leitor / Perfil",
                    "Title": "Livro Avaliado",
                    "score": "Nota (1-5)",
                    "word_count": "Extensão (Palavras)",
                    "interview_priority_score": "Score Relevância (0-100)",
                    "summary": "Resumo da Avaliação"
                }),
                use_container_width=True,
                hide_index=True
            )
            
            st.markdown("---")
            
            # SELETOR DO LEITOR PARA GERACAO DE ROTEIRO VIA LLM
            st.subheader("🎙️ Gerador de Roteiro de Entrevista Personalizado com LLM")
            
            opcoes_leitores = [
                f"{row['profileName']} (Score: {row['interview_priority_score']}) - {row['Title'][:40]}..."
                for _, row in df_top_entrevistas.iterrows()
            ]
            
            leitor_escolhido_str = st.selectbox("Escolha um Leitor da Tabela para Gerar Roteiro:", opcoes_leitores)
            idx_escolhido = opcoes_leitores.index(leitor_escolhido_str)
            leitor_row = df_top_entrevistas.iloc[idx_escolhido]
            
            st.markdown(f"**Resenha Original de {leitor_row['profileName']}:**")
            st.caption(f"\"{leitor_row['text']}\"")
            
            if st.button("🚀 Gerar Roteiro Customizado de Entrevista com LLM", type="primary"):
                with st.spinner("Construindo roteiro de perguntas investigativas para o analista..."):
                    sent_info = nlp.analisar_sentimento_resenha(str(leitor_row["text"]))
                    roteiro_final = llm.gerar_roteiro_entrevista_usuario(
                        usuario_info=leitor_row.to_dict(),
                        livro_foco=leitor_row["Title"],
                        resenha_leitor=str(leitor_row["text"]),
                        sentimento_resenha=sent_info["categoria"]
                    )
                    st.success("Roteiro Criado com Sucesso!")
                    st.markdown(roteiro_final)
