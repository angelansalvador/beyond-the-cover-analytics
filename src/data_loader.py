"""
Modulo: data_loader.py (Versao 5.0 Definitiva)
Descricao: Camada analitica colunar de alta performance utilizando DuckDB para:
1. Panorama Geral do Mercado com filtro de periodo (anos) para distribuicao de notas e top generos.
2. Performance por Autor com filtros de faixa de volume, tooltips com contagem de reviews e dropdown completo (40+ reviews).
3. Analise de Generos com series temporais instrutivas (tracao anual e nota media) e matriz completa de indices com explicacoes.
4. Scoreboard dos 4 Pilares de Entrevista e busca de reviews representativas.
"""

import os
import time
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
import duckdb
import pandas as pd
import numpy as np


class DataLoader:
    """
    Orquestrador analitico colunar DuckDB de alta performance (Modo Read-Only).
    """

    def __init__(self, data_dir: str = "/home/angisalva/desafio_a3data/beyond-the-cover-analytics/data"):
        self.data_dir = data_dir
        self.db_path = os.path.join(data_dir, "analytics.duckdb")
        # Abre em modo read_only para evitar conflitos de lock de arquivo
        self.conn = duckdb.connect(self.db_path, read_only=True)
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

    def get_distribuicao_estrelas(self, ano_min: Optional[int] = None, ano_max: Optional[int] = None) -> pd.DataFrame:
        """
        Distribuicao percentual e absoluta de estrelas (1 a 5), com filtro opcional de intervalo de anos.
        """
        where_clauses = ["score IS NOT NULL", "score BETWEEN 1 AND 5"]
        if ano_min is not None and ano_max is not None:
            t_min = int(time.mktime(datetime(ano_min, 1, 1).timetuple()))
            t_max = int(time.mktime(datetime(ano_max + 1, 1, 1).timetuple()))
            where_clauses.append(f"time >= {t_min}")
            where_clauses.append(f"time < {t_max}")

        where_sql = " AND ".join(where_clauses)

        query = f"""
            WITH filtered AS (
                SELECT score FROM ratings WHERE {where_sql}
            ),
            total AS (
                SELECT count(*) AS total_geral FROM filtered
            )
            SELECT 
                CAST(score AS INTEGER) AS "Estrelas",
                count(*) AS "Total Avaliações",
                round(count(*) * 100.0 / NULLIF((SELECT total_geral FROM total), 0), 1) AS "Percentual"
            FROM filtered
            GROUP BY 1
            ORDER BY 1 ASC;
        """
        return self.conn.execute(query).df()

    def get_top_generos_geral(self, limit: int = 10, ano_min: Optional[int] = None, ano_max: Optional[int] = None) -> pd.DataFrame:
        """
        Top generos em volume de avaliacoes, com filtro opcional de intervalo de anos.
        """
        time_filter = ""
        if ano_min is not None and ano_max is not None:
            t_min = int(time.mktime(datetime(ano_min, 1, 1).timetuple()))
            t_max = int(time.mktime(datetime(ano_max + 1, 1, 1).timetuple()))
            time_filter = f"AND r.time >= {t_min} AND r.time < {t_max}"

        query = f"""
            SELECT 
                b.categories AS "Gênero",
                count(r.score) AS "Total Avaliações",
                count(DISTINCT b.Title) AS "Títulos Únicos",
                round(avg(r.score), 2) AS "Nota Média"
            FROM ratings r
            JOIN books b ON r.norm_title_key = b.norm_title_key
            WHERE b.categories IS NOT NULL 
              AND b.categories != 'Geral / Outros'
              {time_filter}
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
    def get_ranking_geral_autores(
        self, 
        faixa_volume: str = "Todas as faixas (Mínimo 40 avaliações)", 
        limit: int = 10
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Retorna os autores mais bem avaliados e os com menor media conforme faixa de quantidade de reviews:
        - '0 a 1000' (ou '0 a 1.000')
        - '1001 a 5000' (ou '1.001 a 5.000')
        - '5001 a 10000' (ou '5.001 a 10.000')
        - 'mais de 10000' (ou 'Mais de 10.000')
        """
        # Mapeamento robusto da condicao de filtro de volume
        faixa_norm = faixa_volume.lower().replace(".", "").replace(" ", "")
        
        if "0a1000" in faixa_norm:
            where_vol = "total_avaliacoes BETWEEN 20 AND 1000"
        elif "1001a5000" in faixa_norm:
            where_vol = "total_avaliacoes BETWEEN 1001 AND 5000"
        elif "5001a10000" in faixa_norm:
            where_vol = "total_avaliacoes BETWEEN 5001 AND 10000"
        elif "maisde10000" in faixa_norm or ">10000" in faixa_norm:
            where_vol = "total_avaliacoes > 10000"
        else:
            where_vol = "total_avaliacoes >= 40"

        base_query = f"""
            SELECT 
                autor AS "Autor",
                total_avaliacoes AS "Total Avaliações",
                nota_media AS "Nota Média",
                pct_elogios AS "Pct Elogios (4-5★)",
                pct_criticas AS "Pct Críticas (1-2★)"
            FROM author_stats
            WHERE {where_vol}
        """
        df_melhores = self.conn.execute(f"{base_query} ORDER BY nota_media DESC, total_avaliacoes DESC LIMIT {limit};").df()
        df_piores = self.conn.execute(f"{base_query} ORDER BY nota_media ASC, total_avaliacoes DESC LIMIT {limit};").df()
        return df_melhores, df_piores

    def get_autores_para_selecao(self, min_avaliacoes: int = 40) -> List[Dict[str, Any]]:
        """
        Retorna TODOS os autores com mais de min_avaliacoes (padrao 40) para preencher a lista de selecao.
        Ordenados por volume decrescente de avaliacoes.
        """
        query = f"""
            SELECT 
                autor,
                total_avaliacoes,
                nota_media
            FROM author_stats
            WHERE total_avaliacoes >= {min_avaliacoes}
            ORDER BY total_avaliacoes DESC;
        """
        return self.conn.execute(query).df().to_dict(orient="records")

    def get_top_autores(self, limit: int = 60) -> List[Dict[str, Any]]:
        """Mantido para compatibilidade retroativa."""
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
        """Busca todas as resenhas do autor selecionado."""
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
        """
        Indicadores de mercado dos generos com calculo dos indices proprietarios.
        """
        query = f"""
            SELECT 
                genero AS "Gênero",
                total_avaliacoes AS "Total Avaliações",
                nota_media AS "Nota Média",
                desvio_padrao AS "Desvio Padrão",
                pct_5_estrelas,
                pct_baixas
            FROM genre_stats
            ORDER BY total_avaliacoes DESC
            LIMIT {limit};
        """
        df = self.conn.execute(query).df()

        mediana_vol = df["Total Avaliações"].median()
        df["Índice Paixão de Nicho"] = (
            (df["Nota Média"] - 3.5).clip(lower=0) * 40.0 +
            (df["pct_5_estrelas"] * 40.0) +
            (np.where(df["Total Avaliações"] < mediana_vol, 20.0, 5.0))
        ).round(1)

        df["Índice Polêmica / Hype"] = (
            (df["Desvio Padrão"].fillna(1.0) / 1.5).clip(0, 1) * 50.0 +
            (np.log10(df["Total Avaliações"]) / 5.0).clip(0, 1) * 30.0 +
            (df["pct_baixas"] * 20.0)
        ).round(1)

        df["Consistência de Agradecimento"] = (
            (df["Nota Média"] / 5.0) * 60.0 +
            (1.0 - (df["Desvio Padrão"].fillna(1.0) / 2.0)).clip(0, 1) * 40.0
        ).round(1)

        return df

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
    print("DataLoader v5.0 inicializado com sucesso!")
    melhores, piores = loader.get_ranking_geral_autores()
    print("Top 3 melhores autores:")
    print(melhores.head(3))
