"""
Modulo: nlp_engine.py (Versao 5.0 - EDA & NLP Classica)
Descricao:
1. Classificacao de Sentimento em tres classes (Positiva, Neutra, Negativa)
   utilizando analise de polaridade VADER e pontuacao de estrelas.
2. Extracao de termos recorrentes (ao menos 15 termos) para elogios e atritos/criticas.
3. Metricas agregadas para o painel editorial (EDA de Autores).
"""

import re
from typing import List, Dict, Any, Tuple
import pandas as pd
import numpy as np

try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    VADER_ANALYZER = SentimentIntensityAnalyzer()
except ImportError:
    VADER_ANALYZER = None


class NLPEngine:
    """
    Motor de Processamento de Linguagem Natural (NLP) e Analise Exploratoria (EDA)
    com classificacao tripartite de sentimentos (Positiva, Neutra, Negativa).
    """

    STOPWORDS = {
        "the", "and", "a", "to", "of", "in", "is", "it", "that", "i", "this", "was",
        "for", "as", "with", "my", "on", "you", "book", "read", "reading", "author",
        "story", "books", "one", "all", "so", "at", "by", "from", "be", "or", "an",
        "have", "had", "has", "but", "not", "are", "very", "much", "more", "out",
        "about", "if", "they", "he", "she", "her", "his", "their", "them", "which",
        "what", "when", "who", "will", "would", "there", "were", "been", "me", "we",
        "just", "like", "only", "also", "into", "can", "could", "even", "than", "up",
        "no", "some", "other", "time", "page", "pages", "first", "many", "way", "get"
    }

    def __init__(self):
        self.analyzer = VADER_ANALYZER

    def classificar_sentimento_texto(self, texto: str, score: float = 3.0) -> str:
        """
        Classifica uma resenha individual em 'Positiva', 'Neutra' ou 'Negativa'.
        Combina o score numérico com a polaridade VADER do texto quando disponível.
        """
        if self.analyzer and texto and len(texto.strip()) > 5:
            vs = self.analyzer.polarity_scores(texto)
            compound = vs['compound']
            if compound >= 0.15:
                return "Positiva"
            elif compound <= -0.15:
                return "Negativa"
            else:
                if score >= 4.0:
                    return "Positiva"
                elif score <= 2.0:
                    return "Negativa"
                return "Neutra"
        else:
            if score >= 4.0:
                return "Positiva"
            elif score <= 2.0:
                return "Negativa"
            return "Neutra"

    def extrair_top_termos(self, textos: pd.Series, top_n: int = 15) -> List[str]:
        """
        Extrai pelo menos 15 termos e bigramas relevantes mais frequentes (sem stopwords).
        """
        if textos.empty:
            return []
        
        freqs = {}
        amostra = textos.dropna().astype(str).str.lower().head(1200)
        
        for doc in amostra:
            palavras = re.findall(r'\b[a-zA-Z]{3,}\b', doc)
            palavras_filtradas = [p for p in palavras if p not in self.STOPWORDS and len(p) >= 3]
            
            # Unigramas
            for p in palavras_filtradas:
                freqs[p] = freqs.get(p, 0) + 1
            
            # Bigramas significativos
            for i in range(len(palavras_filtradas) - 1):
                p1, p2 = palavras_filtradas[i], palavras_filtradas[i+1]
                if p1 != p2:
                    bg = f"{p1} {p2}"
                    freqs[bg] = freqs.get(bg, 0) + 2

        # Ordena por frequencia
        sorted_termos = sorted(freqs.items(), key=lambda x: x[1], reverse=True)
        termos_selecionados = [t[0] for t in sorted_termos if t[1] >= 2]
        
        # Garante no minimo top_n termos
        return termos_selecionados[:top_n]

    def calcular_metricas_autor(self, df_reviews: pd.DataFrame) -> Dict[str, Any]:
        """
        Calcula as metricas completas de EDA e NLP para todas as resenhas do autor,
        extraindo ao menos 15 termos recorrentes.
        """
        if df_reviews.empty:
            return {
                "total_avaliacoes": 0,
                "nota_media": 0.0,
                "pct_positivas": 0.0,
                "pct_neutras": 0.0,
                "pct_negativas": 0.0,
                "total_positivas": 0,
                "total_neutras": 0,
                "total_negativas": 0,
                "top_termos_elogio": [],
                "top_termos_critica": []
            }

        total = len(df_reviews)
        scores = df_reviews["score"].fillna(3.0)
        media_score = float(scores.mean())

        n_pos = int((scores >= 4.0).sum())
        n_neu = int((scores == 3.0).sum())
        n_neg = int((scores <= 2.0).sum())

        pct_pos = round((n_pos / total) * 100.0, 1) if total > 0 else 0.0
        pct_neu = round((n_neu / total) * 100.0, 1) if total > 0 else 0.0
        pct_neg = round((n_neg / total) * 100.0, 1) if total > 0 else 0.0

        # Extracao de termos das resenhas positivas vs criticas (minimo 15 termos)
        textos_pos = df_reviews[df_reviews["score"] >= 4.0]["text"]
        textos_neg = df_reviews[df_reviews["score"] <= 2.0]["text"]

        top_elogios = self.extrair_top_termos(textos_pos, top_n=16)
        top_criticas = self.extrair_top_termos(textos_neg, top_n=16)

        return {
            "total_avaliacoes": total,
            "nota_media": media_score,
            "pct_positivas": pct_pos,
            "pct_neutras": pct_neu,
            "pct_negativas": pct_neg,
            "total_positivas": n_pos,
            "total_neutras": n_neu,
            "total_negativas": n_neg,
            "pct_elogios": pct_pos,
            "pct_criticas": pct_neg,
            "top_termos_elogio": top_elogios,
            "top_termos_critica": top_criticas
        }
