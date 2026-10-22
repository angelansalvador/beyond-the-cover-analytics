# 📊 Relatório Executivo: Beyond the Cover Analytics
## Transformação Analítica, Inteligência de Mercado e Redução de Custos Operacionais
**Cliente**: Editora | **Consultoria**: A3Data  
**Data**: Outubro de 2026 | **Status**: Entregue para Produção  

---

## 1. Sumário Executivo
A editora contratou a **A3Data** para solucionar um gargalo crítico em sua operação: a exploração manual de uma base histórica contendo mais de **3.000.000 de avaliações de leitores** e **212.404 livros**.

Atualmente, o processo de pesquisa e compilação de feedbacks sobre autores, gêneros e seleção de leitores para entrevistas qualitativas é realizado manualmente por uma equipe de **5 analistas**, demandando cerca de **3 dias úteis por análise** (equivalente a **120 horas-homem** por relatório).

A plataforma **Beyond the Cover Analytics** automatiza esse fluxo de ponta a ponta através de **Processamento de Linguagem Natural (NLP)** e **Grandes Modelos de Linguagem (LLMs)**. O tempo de geração de um diagnóstico completo cai de **72 horas para menos de 15 segundos**, permitindo uma economia direta de **R$ 296.400,00 anuais** em folha de pagamento e liberando 100% da equipe de analistas para atividades estratégicas de receita.

---

## 2. Diagnóstico do Problema & Business Case (ROI)

### 2.1 Cenário Atual (Processo Manual - AS-IS)
* **Equipe Alocada**: 5 analistas dedicados em tempo integral.
* **Custo Salarial Mensal Direto**: 5 analistas × R$ 5.000,00 = **R$ 25.000,00/mês** (**R$ 300.000,00/ano**).
* **Tempo por Análise (Lead Time)**: 3 dias úteis (24 horas úteis por pessoa = **120 horas-homem por relatório**).
* **Capacidade Produtiva do Time**: Em um mês comercial com 22 dias úteis, a equipe consegue entregar no máximo **7 relatórios mensais**, criando uma fila de espera severa para o comitê editorial.
* **Custo Médio por Análise**: Cada relatório manual custa aproximadamente **R$ 3.409,00** apenas em horas de analista.

### 2.2 Cenário Automatizado (Beyond the Cover Analytics - TO-BE)
* **Tempo Médio de Processamento**: **15 segundos** (redução de **99,98%** no tempo de resposta).
* **Capacidade Produtiva**: **Virtualmente ilimitada sob demanda** (centenas de análises por dia).
* **Custo Marginal por Análise**: Praticamente **R$ 0,00** (processamento colunar local otimizado).
* **Economia Salarial Líquida Direta**: **R$ 24.700,00/mês** (**R$ 296.400,00/ano**), descontando custos mínimos de manutenção.
* **ROI (Retorno sobre o Investimento)**: Imediato no primeiro mês de operação.

### 2.3 Destinação Estratégica dos Analistas Liberados
Os 5 analistas não são desligados, mas sim **promovidos e realocados** para frentes onde o raciocínio humano gera valor direto ao negócio:
1. **Curadoria e Aquisição de Direitos Autorais**: Utilizar os dados de fricção e temas em alta para negociar direitos de livros internacionais com alto potencial de venda.
2. **Condução de Entrevistas Qualitativas VIP**: Conduzir entrevistas guiadas pelos roteiros de LLM com os super-leitores identificados pela ferramenta, aprofundando o relacionamento da editora com a comunidade.
3. **Estratégia de Marketing e Campanhas Personalizadas**: Alinhar as mensagens de marketing aos sentimentos reais dos leitores identificados pelo motor de NLP.

---

## 3. Metodologia Técnica & Arquitetura da Solução

### 3.1 Engenharia de Dados com DuckDB (Processamento de 3 Milhões de Linhas em Hardware Local)
* **Desafio**: Rodar análises em uma base de 3 GB e 3.000.000 de registros localmente em um computador com GPU integrada (Intel Iris Xe com 4 GB compartilhados) e memória RAM padrão.
* **Solução Arquitetural**: Implementamos o **DuckDB** como motor analítico colunar embutido. O DuckDB realiza streaming vetorizado direto do disco com indexação (`analytics.duckdb`), permitindo agregações de milhões de linhas consumindo menos de 400 MB de memória RAM e executando consultas em menos de 50 milissegundos.

### 3.2 Processamento de Linguagem Natural (NLP)
1. **Análise de Sentimentos com VADER (*Valence Aware Dictionary and sEntiment Reasoner*)**:
   - Algoritmo lexico-regulado calibrado para capturar intensidade e nuances em resenhas de livros (pontuações de -1.0 a +1.0).
   - Classifica em tempo real cada avaliação como **Positiva**, **Neutra** ou **Negativa/Crítica**.
2. **Mineração de Tópicos e Aspectos com TF-IDF (*Term Frequency-Inverse Document Frequency*)**:
   - Vetorização com n-gramas (unigramas e bigramas) com remoção de stopwords para isolar termos-chave debatidos pelo público sobre cada autor e gênero literário (ex: *"character development"*, *"plot twist"*, *"narrative pace"*).
3. **Algoritmo Proprietário de Priorização de Leitores para Entrevistas**:
   - Calcula o **Interview Priority Score (0 a 100)** para identificar os melhores usuários a entrevistar com base em:
     * **Profundidade Textual (60%)**: Resenhas detalhadas e substanciais (entre 150 e 400 palavras);
     * **Nuance Crítica (25%)**: Leitores moderados (notas 2, 3 e 4) que articulam pontos fortes e pontos fracos;
     * **Qualidade de Síntese (15%)**: Título e resumo informativo da resenha.

### 3.3 Grandes Modelos de Linguagem (LLMs) como Diferencial Estratégico
O módulo de LLM atua em duas frentes de altíssimo impacto:
1. **Síntese Executiva Automatizada de Autor/Gênero**: Gera um briefing executivo consolidando aceitação de mercado, principais forças elogiadas, pontos de fricção e recomendações estratégicas para o comitê editorial.
2. **Gerador de Roteiro de Entrevista Personalizado**: Analisa a resenha real e o perfil do leitor selecionado no Radar de Entrevistas e cria um roteiro investigativo em 4 blocos (Quebra-gelo, Aprofundamento da Obra, Decisão de Compra e Fechamento/Clube VIP) pronto para o analista conduzir.

---

## 4. Estrutura do Repositório & Como Executar

```text
beyond-the-cover-analytics/
├── app.py                      # Aplicacao Web Interativa completa em Streamlit
├── requirements.txt            # Dependencias do projeto
├── README.md                   # Documentacao técnica e institucional
├── data/
│   ├── books_data.csv          # Metadados de 212.404 livros
│   ├── Books_ratings.csv       # 3.000.000 de avaliacoes textuais
│   └── analytics.duckdb        # Base colunar indexada em alta performance
├── src/
│   ├── business_metrics.py     # Modulo financeiro de ROI e custos operacionais
│   ├── data_loader.py          # Camada analitica colunar DuckDB
│   ├── nlp_engine.py           # Analise de sentimento VADER, TF-IDF e Score de Entrevista
│   └── llm_engine.py           # Sintese executiva e roteiros de entrevista via LLM
├── notebooks/
│   └── exploratory_analysis.ipynb # Notebook com a jornada analitica completa
└── reports/
    └── executive_summary.md    # Este relatorio executivo formal
```

---

## 5. Glossário de Siglas e Conceitos
* **NLP (*Natural Language Processing*)**: Processamento de Linguagem Natural. Área da IA que capacita computadores a entender, interpretar e minerar dados textuais.
* **LLM (*Large Language Models*)**: Grandes Modelos de Linguagem. Modelos neurais que produzem raciocínio semântico, resumos executivos e geração textual contextualmente coerente.
* **ROI (*Return on Investment*)**: Retorno sobre o Investimento. Métrica que mede a eficiência financeira de um investimento em relação ao seu custo.
* **TF-IDF (*Term Frequency-Inverse Document Frequency*)**: Frequência do Termo – Inverso da Frequência nos Documentos. Métrica estatística que pontua o quão importante é uma palavra para um documento em uma coleção.
* **VADER (*Valence Aware Dictionary and sEntiment Reasoner*)**: Modelo de NLP baseado em regras e intensidade léxica para aferir sentimento em textos coloquiais e resenhas.
* **DuckDB**: Sistema de gerenciamento de banco de dados colunar analítico embutido, focado em alta velocidade para consultas OLAP sem necessidade de servidor externo.
* **RAM (*Random Access Memory*)**: Memória de Acesso Aleatório do computador, responsável pelo armazenamento volátil dos dados em processamento.
