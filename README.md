# 📖 Beyond the Cover Analytics: Inteligência Editorial com NLP & LLMs
> **Solução desenvolvida para o Desafio Técnico & Negocial da A3Data para Editora**  
> Transformando 3 dias de trabalho manual em segundos de tomada de decisão com Inteligência Artificial.

---

## 📌 1. Visão Geral do Desafio & Problema de Negócio

A editora contratou a **A3Data** para explorar uma base histórica com mais de **3.000.000 de avaliações de livros** e **212.404 títulos cadastrados**.

### O Gargalo Operacional (Cenário Anterior - AS-IS):
* **Processo Manual**: A exploração de resenhas para entender a aceitação de autores, performance de gêneros e busca de leitores relevantes para entrevistas qualitativas era feita manualmente.
* **Tamanho da Equipe**: **5 analistas** dedicados em tempo integral.
* **Custo Salarial Mensal Direto**: 5 analistas × R$ 5.000,00 = **R$ 25.000,00 por mês** (**R$ 300.000,00 por ano**).
* **Tempo por Análise (Lead Time)**: Cerca de **3 dias úteis por relatório** (equivalente a **120 horas-homem** de trabalho analítico).
* **Capacidade Produtiva**: No máximo 7 relatórios por mês, limitando a agilidade do comitê editorial.

### A Solução Entregue (Cenário Automatizado - TO-BE):
A plataforma **Beyond the Cover Analytics** automatiza a ingestão, mineração semântica e síntese estratégica das avaliações:
* ⚡ **Tempo por Análise**: Reduzido de 3 dias para **menos de 15 segundos** (**redução de 99,98% no tempo de resposta**).
* 💰 **Impacto Financeiro Direto**: Economia operacional de **R$ 24.700,00/mês** (**R$ 296.400,00/ano**).
* 👥 **Realocação Estratégica da Equipe**: Os 5 analistas são liberados de tarefas operacionais repetitivas para atuarem em frentes de alto valor:
  1. *Curadoria Editorial*: Prospecção e aquisição de direitos autorais baseadas nas dores dos leitores identificadas pelo NLP.
  2. *Relacionamento com a Comunidade*: Condução de entrevistas presenciais/remotas com super-leitores guiadas pelos roteiros de LLM.
  3. *Marketing Estratégico*: Campanhas segmentadas por cluster de sentimento e categorias em alta.

---

## 🧠 2. Tecnologias & Diferencial Técnico

A solução foi projetada especificamente para rodar com **altíssimo desempenho em hardware local** (CPU e GPU integrada Intel Iris Xe de 4GB compartilhados):

1. **Engenharia de Dados com DuckDB**:
   - Banco analítico colunar embutido (**OLAP**). Permite consultar e agregar 3 milhões de resenhas (2,7 GB) direto do disco consumindo menos de 400 MB de memória RAM e respondendo em menos de 50 milissegundos.
2. **Processamento de Linguagem Natural (NLP)**:
   - **VADER (*Valence Aware Dictionary and sEntiment Reasoner*)**: Mineração de sentimentos veloz e especializada em linguagem coloquial de resenhas (Positivo, Neutro ou Negativo/Crítico).
   - **TF-IDF (*Term Frequency-Inverse Document Frequency*) com N-Grams**: Identificação automatizada dos temas, aspectos narrativos e palavras-chave mais discutidos de cada autor ou gênero literário.
   - **Algoritmo de Priorização para Entrevistas Qualitativas**: Pontua cada resenha de 0 a 100 (*Interview Priority Score*) ponderando profundidade textual (reviews ricas entre 150 e 400 palavras), nuance crítica (notas moderadas com prós e contras detalhados) e qualidade de síntese do resumo.
3. **Grandes Modelos de Linguagem (LLMs - Diferencial Competitivo)**:
   - **Síntese Executiva Automatizada**: Geração de briefings estratégicos para a diretoria contendo diagnóstico de forças, pontos de fricção e recomendações de catálogo.
   - **Gerador de Roteiro de Entrevista Personalizado**: Cria um roteiro estruturado em 4 blocos de perguntas investigativas customizadas para o histórico exato do leitor selecionado no Radar de Entrevistas.
   - **Arquitetura Resiliente**: Funciona 100% offline via motor semântico estruturado local e suporta conexão com APIs (OpenAI / Gemini / Ollama).
4. **Aplicação Web Interativa (Streamlit & Plotly)**:
   - Dashboard moderno, intuitivo e responsivo com 4 abas estratégicas: Visão Geral & ROI, Performance de Autores, Análise de Gêneros e Radar de Entrevistas Qualitativas.

---

## 📂 3. Estrutura do Repositório

```text
beyond-the-cover-analytics/
├── app.py                      # Aplicação Web Interativa (Streamlit)
├── requirements.txt            # Dependências Python do projeto
├── README.md                   # Esta documentação
├── data/
│   ├── books_data.csv          # Base de livros (212.404 títulos)
│   ├── Books_ratings.csv       # Base de resenhas (3.000.000 registros)
│   └── analytics.duckdb        # Banco colunar indexado de alta performance
├── src/
│   ├── business_metrics.py     # Modelo quantitativo de ROI e custos operacionais
│   ├── data_loader.py          # Camada analítica colunar com DuckDB
│   ├── nlp_engine.py           # Análise de sentimento VADER, TF-IDF e Score de Entrevista
│   └── llm_engine.py           # Síntese executiva e roteiros de entrevista via LLM
├── notebooks/
│   └── exploratory_analysis.ipynb # Notebook com análise exploratória e experimentos
└── reports/
    └── executive_summary.md    # Relatório executivo formal de negócios
```

---

## 🚀 4. Como Executar o Projeto Localmente

### Pré-requisitos
* Python 3.10+
* Ambiente Virtual (VENV) ativado

### Passo a Passo

1. **Ative o ambiente virtual:**
   ```bash
   source .venv/bin/activate
   # No Windows PowerShell:
   # .venv\Scripts\Activate.ps1
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Inicie a Aplicação Web Interativa:**
   ```bash
   streamlit run app.py
   ```

4. **Acesse no seu navegador:**
   - URL Local: `http://localhost:8501`

---

## 📚 5. Glossário de Siglas e Termos Técnicos

* **NLP (*Natural Language Processing*)**: Processamento de Linguagem Natural. Área da Inteligência Artificial focada em interpretar e minerar dados textuais.
* **LLM (*Large Language Models*)**: Grandes Modelos de Linguagem. Redes neurais avançadas capazes de gerar sínteses, resumos e análises semânticas profundas.
* **ROI (*Return on Investment*)**: Retorno sobre o Investimento. Métrica financeira que demonstra o retorno financeiro e a economia gerada por uma solução.
* **TF-IDF (*Term Frequency-Inverse Document Frequency*)**: Frequência do Termo – Inverso da Frequência nos Documentos. Métrica estatística que pontua o quão característico é um termo em um conjunto de textos.
* **VADER (*Valence Aware Dictionary and sEntiment Reasoner*)**: Modelo de NLP baseado em regras e intensidade léxica para aferir a polaridade de resenhas.
* **DuckDB**: Banco de dados relacional colunar embutido de altíssimo desempenho, ideal para processamento analítico (OLAP) em larga escala.
* **RAM (*Random Access Memory*)**: Memória de Acesso Aleatório do computador.
* **GPU (*Graphics Processing Unit*)**: Unidade de Processamento Gráfico.
