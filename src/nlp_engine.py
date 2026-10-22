"""
Modulo: nlp_engine.py
Descricao: Motor de Processamento de Linguagem Natural (NLP - Natural Language Processing)
para mineracao de sentimentos, extracao de topicos e algoritmo de priorizacao
de leitores para entrevistas qualitativas da editora.
"""

import re
from typing import List, Dict, Any, Tuple
import pandas as pd
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer


class NLPEngine:
    """
    Motor central de NLP para analise de resenhas textuais de livros.
    
    Siglas e Conceitos:
    - NLP: Natural Language Processing (Processamento de Linguagem Natural)
    - VADER: Valence Aware Dictionary and sEntiment Reasoner (Avaliador de Sentimento Baseado em Lexico)
    - TF-IDF: Term Frequency-Inverse Document Frequency (Frequencia do Termo - Inverso da Frequencia nos Documentos)
    """

    def __init__(self):
        # Inicializa o analisador lexico VADER (otimizado para resenhas em ingles)
        self.analyzer = SentimentIntensityAnalyzer()
        self.stop_words = "english"

    def limpar_texto(self, texto: str) -> str:
        """
        Limpa caracteres indesejados, tags HTML e espacos extras do texto da resenha.
        """
        if not isinstance(texto, str) or not texto.strip():
            return ""
        
        texto_limpo = re.sub(r"<[^>]+>", " ", texto)
        texto_limpo = re.sub(r"[\r\n\t]+", " ", texto_limpo)
        texto_limpo = re.sub(r"\s+", " ", texto_limpo).strip()
        return texto_limpo

    def analisar_sentimento_resenha(self, texto: str) -> Dict[str, Any]:
        """
        Calcula o sentimento de uma resenha usando VADER.
        
        Retorna:
        - compound: Score normalizado entre -1.0 (muito negativo) e +1.0 (muito positivo)
        - pos, neu, neg: Proporcoes dos termos
        - categoria: 'Positivo', 'Neutro' ou 'Negativo'
        """
        if not isinstance(texto, str) or not texto.strip():
            return {
                "compound": 0.0,
                "pos": 0.0,
                "neu": 1.0,
                "neg": 0.0,
                "categoria": "Neutro"
            }
        
        scores = self.analyzer.polarity_scores(texto)
        compound = scores["compound"]
        
        if compound >= 0.05:
            categoria = "Positivo"
        elif compound <= -0.05:
            categoria = "Negativo"
        else:
            categoria = "Neutro"

        return {
            "compound": compound,
            "pos": scores["pos"],
            "neu": scores["neu"],
            "neg": scores["neg"],
            "categoria": categoria
        }

    def extrair_topicos_chave(
        self,
        textos: List[str],
        top_n: int = 10,
        ngram_range: Tuple[int, int] = (1, 2)
    ) -> List[Dict[str, Any]]:
        """
        Extrai os termos e expressoes mais relevantes (n-grams) usando TF-IDF.
        """
        textos_filtrados = [self.limpar_texto(t) for t in textos if isinstance(t, str) and len(t.strip()) > 10]
        
        if not textos_filtrados or len(textos_filtrados) < 2:
            return []
        
        vectorizer = TfidfVectorizer(
            stop_words=self.stop_words,
            ngram_range=ngram_range,
            max_df=0.85,
            min_df=2,
            max_features=1000
        )
        
        try:
            tfidf_matrix = vectorizer.fit_transform(textos_filtrados)
            feature_names = vectorizer.get_feature_names_out()
            scores = np.asarray(tfidf_matrix.sum(axis=0)).ravel()
            top_indices = scores.argsort()[::-1][:top_n]
            
            resultados = [
                {"termo": feature_names[i], "score": round(float(scores[i]), 2)}
                for i in top_indices
            ]
            return resultados
        except Exception:
            return []

    def calcular_score_relevancia_entrevista(
        self,
        df_reviews: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Algoritmo de Priorizacao de Leitores para Entrevistas Qualitativas.
        
        Pilares do Algoritmo:
        1. Profundidade Textual: Reviews com 150 a 450 palavras fornecem detalhes criticos
        2. Qualidade do Resumo (Summary): Titulos de resenha informativos demonstram capacidade de sintese
        3. Nuance Critica: Avaliacoes moderadas (scores de 2 a 4 estrelas) ou com sentimento
           elaborado revelam dores reais do leitor com a obra
        4. Frequencia: Leitores com engajamento constante na base
        
        Retorna o DataFrame com a coluna 'interview_priority_score' (0 a 100).
        """
        df = df_reviews.copy()
        
        # Extensao textual da resenha (Word count)
        df["word_count"] = df["text"].fillna("").apply(lambda x: len(str(x).split()))
        df["summary_len"] = df["summary"].fillna("").apply(lambda x: len(str(x).split()))
        
        # 1. Score de Profundidade Textual (normalizado entre 0 e 1)
        # 300 palavras atinge o teto maximo de qualidade
        df["depth_score"] = np.clip(df["word_count"] / 300.0, 0.0, 1.0)
        
        # 2. Score de Qualidade do Titulo/Resumo (0 a 1)
        df["summary_score"] = np.clip(df["summary_len"] / 10.0, 0.0, 1.0)
        
        # 3. Nuance Critica (notas 2, 3 e 4 tem maior valor diagnostico para a editora)
        notas = df["score"].fillna(3.0)
        df["critical_nuance"] = np.where(notas.isin([2.0, 3.0, 4.0]), 1.0, 0.75)
        
        # 4. Score Composto de Entrevista (0 a 100):
        # 60% profundidade do texto + 25% nuance critica + 15% resumo informativo
        df["interview_priority_score"] = (
            (df["depth_score"] * 0.60) +
            (df["critical_nuance"] * 0.25) +
            (df["summary_score"] * 0.15)
        ) * 100.0
        
        df["interview_priority_score"] = df["interview_priority_score"].round(1)
        
        return df


if __name__ == "__main__":
    nlp = NLPEngine()
    df_ex = pd.DataFrame([{
        "User_id": "U123",
        "profileName": "Carlos Leitor",
        "score": 3.0,
        "summary": "Great premise, but sluggish ending",
        "text": "I really enjoyed the beginning of the book. The characters are vivid and the setting is breathtaking. However, the last third felt rushed and unresolved."
    }])
    df_res = nlp.calcular_score_relevancia_entrevista(df_ex)
    print(df_res[["profileName", "interview_priority_score", "word_count"]])
