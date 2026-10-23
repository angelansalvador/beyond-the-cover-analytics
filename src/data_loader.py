"""
Modulo: data_loader.py (Versao 4.0 Definitiva)
Descricao: Camada analitica com DuckDB para:
1. Panorama Geral com EDA robusta (Evolucao temporal, distribuicao de estrelas, generos)
2. Performance por Autor com comparativo geral (melhores e piores avaliados) e serie temporal individual
3. Analise de Generos com series temporais (Ano x Reviews e Ano x Nota Media)
4. Scoreboard dos 4 Pilares de Entrevista e busca das 3 reviews representativas
"""

import os
from typing import List, Dict, Any, Optional, Tuple
import duckdb
import pandas as pd
import numpy as np


class DataLoader:
    """
    Orquestrador analitico colunar DuckDB de alta performance.
    """

    def __init__(self, data_dir: str = "/home/angisalva/desafio_a3data/beyond-the-cover-analytics/data"):
        self.data_dir = data_dir
        self.db_path = os.path.join(data_dir, "analytics.duckdb")
        self.conn = duckdb.connect(self.db_path)
        self.conn.execute("SET memory_limit = '3GB';")
        self.conn.execute("SET threads = 4;")

    def get_metricas_gerais(self) -> Dict[str, Any]:
        """Estatisticas globais do catalogo."""
        query = """
            SELECT 
                (SELECT count(*) FROM books) AS total_livros,
                (SELECT count(*) FROM ratings) AS total_avaliacoes,
                (SELECT count(DISTINCT User_id) FROM ratings) AS total_usuarios,
                (SELECT round(avg(score), 2) FROM ratings WHERE score IS NOT NULL) AS media_score_global
        """
        res = self.conn.execute(query).fetchone()
        return {
            "total_livros": res[0] if res else 0,
            "total_avaliacoes": res[1] if res else 0,
            "total_usuarios": res[2] if res else 0,
            "media_score_global": res[3] if res else 0.0
        }

    # =========================================================================
    # EDA: PANORAMA GERAL DO MERCADO
    # =========================================================================
    def get_eda_tempo_geral(self) -> pd.DataFrame:
        """Evolucao temporal do mercado: Volume de resenhas e Nota media por Ano."""
        query = """
            SELECT 
                TRY_CAST(strftime(to_timestamp(time), '%Y') AS INTEGER) AS ano,
                count(*) AS total_reviews,
                round(avg(score), 2) AS score_medio
            FROM ratings
            WHERE time IS NOT NULL 
              AND time > 788918400   -- 1995
              AND time < 1420070400  -- 2014
            GROUP BY ano
            HAVING ano IS NOT NULL
            ORDER BY ano ASC;
        """
        return self.conn.execute(query).df()

    def get_distribuicao_estrelas(self) -> pd.DataFrame:
        """Distribuicao percentual e absoluta de estrelas (1 a 5)."""
        query = """
            WITH total AS (
                SELECT count(*) AS total_geral FROM ratings WHERE score IS NOT NULL
            )
            SELECT 
                CAST(score AS INTEGER) AS "Estrelas",
                count(*) AS "Total Avaliações",
                round(count(*) * 100.0 / (SELECT total_geral FROM total), 1) AS "Percentual"
            FROM ratings
            WHERE score IS NOT NULL AND score BETWEEN 1 AND 5
            GROUP BY 1
            ORDER BY 1 ASC;
        """
        return self.conn.execute(query).df()

    def get_top_generos_geral(self, limit: int = 10) -> pd.DataFrame:
        """Top generos em volume de avaliacoes e acervo."""
        query = f"""
            SELECT 
                b.categories AS "Gênero",
                count(r.score) AS "Total Avaliações",
                count(DISTINCT b.Title) AS "Títulos Únicos",
                round(avg(r.score), 2) AS "Nota Média"
            FROM ratings r
            JOIN books b ON r.norm_title_key = b.norm_title_key
            WHERE b.categories IS NOT NULL AND b.categories != 'Geral / Outros'
            GROUP BY b.categories
            ORDER BY "Total Avaliações" DESC
            LIMIT {limit};
        """
        return self.conn.execute(query).df()

    def get_livros_mais_avaliados(self, limit: int = 6) -> pd.DataFrame:
        """Livros Mais Lidos / Avaliados."""
        query = f"""
            SELECT 
                r.Title AS "Título",
                round(avg(r.score), 2) AS "Nota Média",
                count(r.score) AS "Total Avaliações",
                first(b.authors) AS "Autor",
                first(b.categories) AS "Gênero"
            FROM ratings r
            LEFT JOIN books b ON r.norm_title_key = b.norm_title_key
            GROUP BY r.Title
            ORDER BY count(r.score) DESC
            LIMIT {limit};
        """
        return self.conn.execute(query).df()

    def get_livros_mais_positivos(self, limit: int = 6) -> pd.DataFrame:
        """Livros com maior numero absoluto de 5 estrelas."""
        query = f"""
            SELECT 
                r.Title AS "Título",
                count(CASE WHEN r.score = 5.0 THEN 1 END) AS "Resenhas 5 Estrelas",
                count(r.score) AS "Total Avaliações",
                round(avg(r.score), 2) AS "Nota Média",
                first(b.authors) AS "Autor",
                first(b.categories) AS "Gênero"
            FROM ratings r
            LEFT JOIN books b ON r.norm_title_key = b.norm_title_key
            GROUP BY r.Title
            ORDER BY count(CASE WHEN r.score = 5.0 THEN 1 END) DESC
            LIMIT {limit};
        """
        return self.conn.execute(query).df()

    def get_livros_mais_negativos(self, limit: int = 6) -> pd.DataFrame:
        """Livros com maior concentracao de resenhas criticas (1 e 2 estrelas)."""
        query = f"""
            SELECT 
                r.Title AS "Título",
                count(CASE WHEN r.score <= 2.0 THEN 1 END) AS "Resenhas Críticas (1-2★)",
                count(r.score) AS "Total Avaliações",
                round(avg(r.score), 2) AS "Nota Média",
                first(b.authors) AS "Autor",
                first(b.categories) AS "Gênero"
            FROM ratings r
            LEFT JOIN books b ON r.norm_title_key = b.norm_title_key
            GROUP BY r.Title
            ORDER BY count(CASE WHEN r.score <= 2.0 THEN 1 END) DESC
            LIMIT {limit};
        """
        return self.conn.execute(query).df()

    def get_livros_mais_polemicos(self, limit: int = 6) -> pd.DataFrame:
        """Livros mais polarizados (maior desvio padrao)."""
        query = f"""
            SELECT 
                r.Title AS "Título",
                round(stddev(r.score), 2) AS "Índice de Polarização",
                count(r.score) AS "Total Avaliações",
                round(avg(r.score), 2) AS "Nota Média",
                first(b.authors) AS "Autor",
                first(b.categories) AS "Gênero"
            FROM ratings r
            LEFT JOIN books b ON r.norm_title_key = b.norm_title_key
            GROUP BY r.Title
            HAVING count(r.score) >= 80
            ORDER BY stddev(r.score) DESC
            LIMIT {limit};
        """
        return self.conn.execute(query).df()

    # =========================================================================
    # EDA: PERFORMANCE POR AUTOR
    # =========================================================================
    def get_ranking_geral_autores(self, min_avaliacoes: int = 40, limit: int = 10) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Retorna os autores mais bem avaliados e os menos bem avaliados (com filtro de volume minimo).
        Consulta instantanea sobre a tabela author_stats.
        """
        base_query = f"""
            SELECT 
                autor AS "Autor",
                total_avaliacoes AS "Total Avaliações",
                nota_media AS "Nota Média",
                pct_5 AS "Pct 5★",
                pct_criticas AS "Pct Críticas (1-2★)"
            FROM author_stats
            WHERE total_avaliacoes >= {min_avaliacoes}
        """
        df_melhores = self.conn.execute(f"{base_query} ORDER BY nota_media DESC, total_avaliacoes DESC LIMIT {limit};").df()
        df_piores = self.conn.execute(f"{base_query} ORDER BY nota_media ASC, total_avaliacoes DESC LIMIT {limit};").df()
        return df_melhores, df_piores

    def get_top_autores(self, limit: int = 60) -> List[Dict[str, Any]]:
        """Autores com maior volume de avaliacoes para selecao no dropdown."""
        query = f"""
            SELECT 
                autor,
                total_avaliacoes,
                nota_media
            FROM author_stats
            ORDER BY total_avaliacoes DESC
            LIMIT {limit};
        """
        return self.conn.execute(query).df().to_dict(orient="records")

    def get_todas_reviews_autor(self, autor_nome: str) -> pd.DataFrame:
        """Busca todas as resenhas do autor selecionado sem cortes artificiais."""
        query = f"""
            WITH autor_books AS (
                SELECT norm_title_key, authors, categories as genero
                FROM books
                WHERE authors ILIKE '%{autor_nome}%'
            )
            SELECT 
                r.Id,
                r.Title,
                b.authors,
                b.genero,
                r.User_id,
                r.profileName,
                r.score,
                r.time,
                r.summary,
                r.text
            FROM ratings r
            JOIN autor_books b ON r.norm_title_key = b.norm_title_key
            ORDER BY r.time DESC;
        """
        return self.conn.execute(query).df()

    def get_evolucao_temporal_autor(self, autor_nome: str) -> pd.DataFrame:
        """Evolucao das notas de avaliacoes do autor ao longo do tempo (Ano x Score e Reviews)."""
        query = f"""
            WITH autor_books AS (
                SELECT norm_title_key
                FROM books
                WHERE authors ILIKE '%{autor_nome}%'
            )
            SELECT 
                TRY_CAST(strftime(to_timestamp(r.time), '%Y') AS INTEGER) AS ano,
                count(*) AS total_reviews,
                round(avg(r.score), 2) AS score_medio
            FROM ratings r
            JOIN autor_books b ON r.norm_title_key = b.norm_title_key
            WHERE r.time IS NOT NULL 
              AND r.time > 788918400 AND r.time < 1420070400
            GROUP BY ano
            HAVING ano IS NOT NULL
            ORDER BY ano ASC;
        """
        return self.conn.execute(query).df()

    # =========================================================================
    # ANALISE DE GENEROS
    # =========================================================================
    def get_series_temporais_generos(self) -> pd.DataFrame:
        """Retorna a serie historica pre-calculada de generos por ano."""
        query = """
            SELECT genero, ano, total_reviews, score_medio
            FROM genre_yearly_stats
            ORDER BY total_reviews DESC, ano ASC;
        """
        return self.conn.execute(query).df()

    def get_metricas_generos(self, limit: int = 35) -> pd.DataFrame:
        """Indicadores de mercado dos generos baseados estritamente em notas e volumes."""
        query = f"""
            SELECT 
                genero AS "Gênero",
                total_avaliacoes,
                nota_media,
                desvio_padrao,
                pct_5_estrelas,
                pct_baixas
            FROM genre_stats
            ORDER BY total_avaliacoes DESC
            LIMIT {limit};
        """
        df = self.conn.execute(query).df()

        mediana_vol = df["total_avaliacoes"].median()
        df["Índice Paixão de Nicho"] = (
            (df["nota_media"] - 3.5).clip(lower=0) * 40.0 +
            (df["pct_5_estrelas"] * 40.0) +
            (np.where(df["total_avaliacoes"] < mediana_vol, 20.0, 5.0))
        ).round(1)

        df["Índice Polêmica / Hype"] = (
            (df["desvio_padrao"].fillna(1.0) / 1.5).clip(0, 1) * 50.0 +
            (np.log10(df["total_avaliacoes"]) / 5.0).clip(0, 1) * 30.0 +
            (df["pct_baixas"] * 20.0)
        ).round(1)

        df["Consistência de Agradecimento"] = (
            (df["nota_media"] / 5.0) * 60.0 +
            (1.0 - (df["desvio_padrao"].fillna(1.0) / 2.0)).clip(0, 1) * 40.0
        ).round(1)

        return df

    # Alias para compatibilidade
    def get_metricas_generos_irreverente(self, limit: int = 35) -> pd.DataFrame:
        return self.get_metricas_generos(limit=limit)

    # =========================================================================
    # RADAR DE ENTREVISTAS COM LEITORES
    # =========================================================================
    def get_scoreboard_entrevistas(self, top_n: int = 15) -> pd.DataFrame:
        """Top N pelo Indice Ajustado + Especialistas de Pico."""
        query = f"""
            WITH top_geral AS (
                SELECT * FROM interview_candidates
                ORDER BY indice_ajustado DESC
                LIMIT {top_n}
            ),
            picos AS (
                SELECT * FROM interview_candidates
                WHERE especialista_pico != 'Geral'
            )
            SELECT DISTINCT * FROM (
                SELECT * FROM top_geral
                UNION ALL
                SELECT * FROM picos
            )
            ORDER BY indice_ajustado DESC;
        """
        return self.conn.execute(query).df()

    def get_candidate_sample_reviews(self, sample_ids_str: str) -> List[Dict[str, Any]]:
        """Busca as 3 reviews representativas do candidato para validacao manual."""
        if not sample_ids_str:
            return []
        ids = tuple(sample_ids_str.split(","))
        query = f"""
            SELECT 
                r.Id,
                r.Title,
                r.score,
                strftime(to_timestamp(r.time), '%d/%m/%Y') as data_avaliacao,
                r.summary,
                r.text
            FROM ratings r
            WHERE r.Id IN {ids}
            LIMIT 3;
        """
        return self.conn.execute(query).df().to_dict(orient="records")


if __name__ == "__main__":
    loader = DataLoader()
    print("DataLoader v4.0 pronto.")
    melhores, piores = loader.get_ranking_geral_autores()
    print("Top 3 melhores autores:")
    print(melhores.head(3))
