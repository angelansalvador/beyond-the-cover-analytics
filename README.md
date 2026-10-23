# 📖 Beyond the Cover Analytics: Inteligência Editorial com NLP & LLMs
> **Solução desenvolvida para o Desafio Técnico & Negocial da A3Data para a Editora**  
> *Transformando 3 dias de exploração manual em segundos de tomada de decisão estratégica com Engenharia de Dados, NLP e Grandes Modelos de Linguagem.*

---

## 📌 1. Visão Geral do Desafio & Problema de Negócio

A editora contratou a **A3Data** para diagnosticar e transformar o processo de exploração de sua base histórica de avaliações de livros. O objetivo é compreender a fundo a performance de autores e gêneros, além de mapear leitores qualificados para entrevistas em profundidade.

### O Gargalo Operacional Anterior (Cenário AS-IS):
* **Processo 100% Manual**: Analistas liam amostras aleatórias de resenhas e compilavam planilhas manualmente para tentar entender a recepção de lançamentos e o comportamento dos gêneros.
* **Tamanho da Equipe**: **5 analistas de dados** dedicados em tempo integral.
* **Custo Salarial Mensal**: 5 analistas × R$ 5.000,00 = **R$ 25.000,00/mês** (**R$ 300.000,00/ano**).
* **Tempo por Análise (Lead Time)**: Cerca de **3 dias úteis** por relatório (**120 horas-homem**).
* **Capacidade Produtiva Restrita**: No máximo 7 análises mensais, gerando lentidão crítica nas decisões de aquisição de direitos, precificação e tiragem do conselho editorial.

### A Transformação Entregue (Cenário TO-BE):
A plataforma **Beyond the Cover Analytics** automatiza a ingestão, mineração semântica, cálculo de índices proprietários e simulação de diretoria:
* ⚡ **Tempo de Resposta**: Reduzido de 3 dias para **menos de 15 segundos** (**redução de 99,98% no tempo de espera**).
* 💰 **Economia Financeira Direta**: Recuperação de **R$ 24.700,00/mês** (**R$ 296.400,00/ano** em ganho de eficiência).
* 👥 **Realocação de Alto Valor**: Os 5 analistas deixam tarefas braçais de compilação de texto e passam a atuar estrategicamente em:
  1. **Curadoria & Negociação de Originais**: Prospecção orientada pelos atritos e desejos reais apontados pelo NLP.
  2. **Relacionamento Qualitativo**: Condução de entrevistas com super-leitores guiadas pelos roteiros personalizados gerados por LLM.
  3. **Marketing Segmentado**: Campanhas sob medida por cluster de sentimento e categorias em ascensão.

---

## 📊 2. Qualidade de Dados, Canonização & Deduplicação

Para garantir que nenhuma análise fosse distorcida por dados sujos ou redundantes, implementamos uma rigorosa etapa de engenharia de dados:

* **Acervo Único & Canonizado**: **207.101 títulos únicos** catalogados (exatamente 1 linha por livro com seu respectivo autor e gênero consolidado, eliminando variantes e pontuações).
* **Avaliações Consolidadas**: **2.004.512 resenhas limpas e estritamente deduplicadas** em memória através de particionamento colunar `(User_id, norm_title_key, timestamp)`. Linhas sem texto ou sem título preenchido foram descartadas conforme especificação.
---

## 🏛️ 3. Módulos da Plataforma Web Interativa

A aplicação foi estruturada em 4 painéis estratégicos desenhados para responder diretamente às perguntas de negócio da editora:

### 📚 Aba 1: Panorama Geral do Mercado Editorial
- **KPIs Macroeconômicos**: Títulos únicos, volume total de avaliações, leitores ativos e nota média global.
- **Série Histórica Macro (1996 a 2013)**: Gráficos anuais de volume de resenhas e evolução da nota média geral.
- **Filtro Dinâmico de Período (Anos)**: Seletor interativo que recalcula instantaneamente tanto a **Distribuição Global de Notas (1 a 5 estrelas)** quanto o **Top 10 Gêneros por Volume de Leitura**.
- **Rankings em Cards Visuais Dinâmicos**: *Mais Lidos/Avaliados*, *Mais Aclamados (5★)*, *Mais Criticados (1-2★)* e *Mais Polêmicos (maior desvio padrão entre leitores)*.

### ✍️ Aba 2: Performance por Autor & Comitê Editorial
- **Rankings Comparativos com Filtro por Faixa de Volume**: Top 10 mais bem avaliados e com menores médias filtráveis por portes de público:
  - `0 a 1.000` avaliações
  - `1.001 a 5.000` avaliações
  - `5.001 a 10.000` avaliações
  - `Mais de 10.000` avaliações
  - `Todas as faixas (Mínimo 40 avaliações)`
- **Tooltips Interativos com Volume de Reviews**: Passar o mouse sobre as barras revela instantaneamente a quantidade exata de resenhas (`Total de Reviews: X.XXX`), nota média e taxas de aprovação/crítica.
- **Dropdown Abrangente**: Seletor com **todos os 6.115 autores com 40+ avaliações** na base, com busca textual instantânea.
- **Histórico Anual do Autor**: Gráficos temporais de Nota Média por Ano e Volume de Resenhas por Ano.
- **Relatório Executivo Editorial Afiado & Irreverente**: Diagnóstico executivo sem clichês corporativos, estruturado em:
  1. ⚡ *O Veredito Nu e Cru* (genialidade narrativa vs. conforto de fórmula);
  2. ⚠️ *A Neurose do Leitor: Onde a Obra Engasga* (análise objetiva de quem deu 1 e 2 estrelas);
  3. 🎯 *Diretrizes para a Mesa Editorial (Segunda-Feira, 9h)* (ações práticas de tiragem, edições de luxo e prevenção contra quebra de expectativa).
- **Termos Recorrentes nas Resenhas (NLP)**: Extração de **15+ termos contextuais** para elogios e para críticas, apresentados em formato discreto entre o relatório e o debate.
- **🏛️ Mesa-Redonda Estratégica (Conselho Editorial & 3 Personas)**: Simulação viva da plenária entre as **3 Personas Literárias** (Marta Albuquerque, Diego Ramos e Helena Souza), o **Diretor Executivo (CEO)** e o **Diretor Financeiro (CFO)**, culminando no **Consenso Unificado da Diretoria** (estratégia de formatos, precificação, tiragem e plano de marketing).

### 📊 Aba 3: Análise Estratégica de Gêneros
- **Evolução Histórica Instrutiva para a Editora**: Gráficos temporais de alta clareza analítica:
  1. *Tração de Mercado:* Volume Anual de Leituras por Gênero (demanda, expansão e arrefecimento).
  2. *Satisfação do Leitor:* Evolução da Nota Média por Gênero (retenção de qualidade e desgaste de formato).
  - Inclui multiselect para selecionar e comparar quaisquer gêneros do catálogo.
- **Matriz de Gêneros & Índices Proprietários (com explicações ℹ️)**:
  - 💎 **ℹ️ Índice Paixão de Nicho (0 a 100)**: Fervor devocional e propensão a pagar caro por edições especiais em categorias hiperengajadas.
  - ⚡ **ℹ️ Índice Polêmica / Hype (0 a 100)**: Polarização acentuada entre 1★ e 5★ com alto volume (alerta para risco de devoluções por quebra de expectativa).
  - 🛡️ **ℹ️ Consistência de Agradecimento (0 a 100)**: Previsibilidade comercial e baixa rejeição, ideal para catálogo de fundo (backlist seguro).
- **Parecer Estratégico-Financeiro**: Diagnóstico de margem de contribuição e risco operacional assinado pelo Analista Financeiro da Editora.

### 🎯 Aba 4: Radar de Entrevistas com Leitores (Scoreboard dos 4 Pilares)
Identificação científica dos leitores mais lúcidos e analíticos da base através de 4 dimensões percentílicas:
1. **🧠 Perspicácia (Peso 35%)**: Mede densidade argumentativa técnica (ritmo, escrita, estrutura, coerência) por 100 palavras (**o tamanho bruto do texto não pontua**), validação social bayesiana, dissenso informado e coerência nota-texto. Possui **porta de qualidade eliminatória no percentil 40**.
2. **💎 Descobridores de Pérolas (Peso 25%)**: Descoberta precoce de livros de cauda longa ($1 / \log_2(vol + 2)$), notas $\ge 4$ bem fundamentadas e filtro antifraude (penalidade se $>30\%$ das resenhas forem de um mesmo autor).
3. **📈 Detectores de Tendências (Peso 20%)**: Avaliações precoces em obras que posteriormente se tornaram sucessos de público (percentil 95), com encolhimento bayesiano e lift.
4. **🌐 Versatilidade (Peso 20%)**: Entropia de Shannon sobre categorias com $\ge 2$ reviews, diversidade de autores e consistência argumentativa mínima entre os 3 principais gêneros do leitor.

$$\text{Índice Final} = 0.35 \cdot \text{Perspicácia} + 0.25 \cdot \text{Pérolas} + 0.20 \cdot \text{Tendências} + 0.20 \cdot \text{Versatilidade}$$
$$\text{Índice Ajustado} = \text{Índice Final} \times \min\left(1, \sqrt{\frac{n\_reviews}{30}}\right)$$

- **Validação Manual com 3 Reviews Reais**: Radiografia em gráfico radar e leitura de 3 resenhas reais do candidato antes de disparar a entrevista.
- **Gerador de Roteiro de Entrevista Personalizado**: Roteiro sob medida criado por LLM para guiar a conversa do analista com o leitor selecionado.

---

## 🛠️ 4. Tecnologias & Engenharia de Dados

| Camada | Tecnologia | Função no Projeto |
| :--- | :--- | :--- |
| **Banco de Dados OLAP** | **DuckDB** | Processamento analítico colunar vetorizado direto do disco de 2M+ resenhas em < 0.05s, consumindo menos de 400MB de RAM. |
| **Processamento de Linguagem Natural** | **VADER & N-Grams** | Mineração de polaridade (Positiva, Neutra, Negativa) e extração de termos e bigramas recorrentes contextuais. |
| **Grandes Modelos de Linguagem** | **Google AI Pro (Gemini 1.5 Pro)** | Síntese de relatórios irreverentes, debate do Conselho Editorial e geração de roteiros de entrevista personalizados (com fallback analítico autônomo local). |
| **Interface de Usuário** | **Streamlit & Plotly** | Dashboard moderno, reativo, com layout customizado e visualização interativa de dados. |
| **Modelagem Financeira** | **Python (ROICalculator)** | Cálculo quantitativo de lead time, horas-homem e viabilidade econômica AS-IS vs TO-BE. |

---

## 📂 5. Estrutura do Repositório

```text
beyond-the-cover-analytics/
├── app.py                      # Aplicação Web Interativa (Streamlit)
├── requirements.txt            # Dependências Python do projeto
├── README.md                   # Documentação completa do projeto
├── .gitignore                  # Arquivos ignorados pelo Git (dados e logs)
├── data/
│   ├── books_data.csv          # Base bruta de livros (212.404 títulos)
│   ├── Books_ratings.csv       # Base bruta de resenhas (3.000.000 registros)
│   └── analytics.duckdb        # Banco colunar indexado e deduplicado (207k livros / 2M ratings)
├── src/
│   ├── business_metrics.py     # Modelo quantitativo de ROI e custos operacionais
│   ├── data_loader.py          # Camada analítica colunar com DuckDB (modo read-only)
│   ├── nlp_engine.py           # Classificação de sentimento tripartite e termos recorrentes
│   └── llm_engine.py           # RAG, síntese executiva, personas literárias e conselho editorial
├── notebooks/
│   └── exploratory_analysis.ipynb # Notebook com análise exploratória e experimentos validados
└── reports/
    └── executive_summary.md    # Relatório executivo formal de negócios
```

---

## 🚀 6. Como Executar o Projeto Localmente

### Pré-requisitos
* Python 3.10 ou superior
* Sistema operacional: Linux / WSL2 (Ubuntu) ou Windows PowerShell

### Passo a Passo

1. **Clone o repositório e acesse a pasta:**
   ```bash
   git clone https://github.com/angisalva/beyond-the-cover-analytics.git
   cd beyond-the-cover-analytics
   ```

2. **Crie e ative o ambiente virtual:**
   ```bash
   # No Linux / WSL2:
   python3 -m venv .venv
   source .venv/bin/activate

   # No Windows PowerShell:
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Inicie a Aplicação Web:**
   ```bash
   streamlit run app.py
   ```

5. **Acesse no seu navegador:**
   - URL Local: **`http://localhost:8501`**

> **💡 Dica (Opcional):** Para habilitar o modo ao vivo com o **Google AI Pro (Gemini 1.5 Pro)**, insira sua chave do Google AI Studio no campo dedicado na barra lateral da aplicação ou defina a variável de ambiente:
> ```bash
> export GEMINI_API_KEY="sua_chave_aqui"
> ```
> Caso nenhuma chave seja informada, o sistema operará perfeitamente com seu motor analítico local autônomo.

---

## 📓 7. Execução do Jupyter Notebook

Para reproduzir todos os experimentos, gráficos de validação de *The Hobbit*, séries temporais de gêneros e cálculos de ROI passo a passo:

```bash
jupyter notebook notebooks/exploratory_analysis.ipynb
```
*Todas as 18 células do notebook estão configuradas para execução sequencial de ponta a ponta sem falhas.*

---

## 📚 8. Glossário de Conceitos Técnicos & Negociais

* **OLAP (*Online Analytical Processing*)**: Processamento analítico em tempo real focado em agregações colunares velozes de grandes volumes de dados.
* **DuckDB**: Banco relacional colunar embutido projetado para ciência de dados e consultas analíticas de alta performance sem necessidade de servidor dedicado.
* **NLP (*Natural Language Processing*)**: Subárea da Inteligência Artificial voltada à compreensão, mineração e extração de significado de textos escritos por humanos.
* **LLM (*Large Language Models*)**: Redes neurais de bilhões de parâmetros capazes de sintetizar textos complexos, raciocinar sobre evidências e simular personas contextuais.
* **VADER (*Valence Aware Dictionary and sEntiment Reasoner*)**: Classificador léxico de sentimento ajustado para gírias, pontuações e intensificadores típicos de avaliações online.
* **RAG (*Retrieval-Augmented Generation*)**: Arquitetura que ancora as respostas do LLM em fatos e registros reais recuperados dinamicamente do banco de dados, eliminando alucinações.
* **ROI (*Return on Investment*)**: Métrica de retorno financeiro que comprova o valor gerado pela substituição do gargalo operacional manual pela ferramenta automatizada.
* **Cauda Longa (Long Tail)**: Conceito editorial que descreve títulos de vendas perenes em pequenas quantidades individuais que, somados, representam parcela substancial da receita da editora.
* **Backlist**: Catálogo perene de livros publicados há mais de um ano que continuam vendendo regularmente sem depender de investimentos pesados de marketing inicial.
