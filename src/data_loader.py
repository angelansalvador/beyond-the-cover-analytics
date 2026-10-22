"""
Modulo: data_loader.py
Descricao: Camada de Engenharia de Dados de Alta Performance utilizando DuckDB
para manipulacao analitica (OLAP - Online Analytical Processing) de 3 milhoes de resenhas
sem sobrecarregar a memoria RAM do computador local.
"""

import os
import time
from typing import List, Dict, Any, Optional
import duckdb
import pandas as pd


class DataLoader:
    """
    Carregador e orquestrador de dados otimizado com DuckDB.
    
    Por que DuckDB?
    - Processa 3.000.000 de resenhas colunarmente de forma vetorizada direto do disco.
    - Consome menos de 400MB de RAM mesmo agregando milhoes de registros.
    """

    def __init__(self, data_dir: str = "/home/angisalva/desafio_a3data/beyond-the-cover-analytics/data"):
        self.data_dir = data_dir
        self.books_csv = os.path.join(data_dir, "books_data.csv")
        self.ratings_csv = os.path.join(data_dir, "Books_ratings.csv")
        self.db_path = os.path.join(data_dir, "analytics.duckdb")
        
        # Conexao persistente
        self.conn = duckdb.connect(self.db_path)
        self.conn.execute("SET memory_limit = '3GB';")
        self.conn.execute("SET threads = 4;")

    def inicializar_banco(self):
        """
        Cria tabelas indexadas no arquivo analytics.duckdb se ainda nao existirem.
        Uma vez criadas, consultas rodam em < 50ms.
        """
        tabelas = [t[0] for t in self.conn.execute("SHOW TABLES").fetchall()]
        
        if "books" not in tabelas:
            print("Criando tabela otimizada de livros...")
            self.conn.execute(f"""
                CREATE TABLE books AS
                SELECT 
                    Title,
                    description,
                    authors,
                    publisher,
                    publishedDate,
                    categories,
                    TRY_CAST(ratingsCount AS DOUBLE) AS ratingsCount
                FROM read_csv_auto('{self.books_csv}', ignore_errors=true);
            """)
            self.conn.execute("CREATE INDEX idx_books_title ON books(Title);")
            print("Tabela books criada com sucesso!")

        if "ratings" not in tabelas:
            print("Criando tabela otimizada de ratings (3 milhoes de linhas)...")
            self.conn.execute(f"""
                CREATE TABLE ratings AS
                SELECT 
                    Id,
                    Title,
                    TRY_CAST(Price AS DOUBLE) AS Price,
                    User_id,
                    profileName,
                    TRY_CAST(score AS DOUBLE) AS score,
                    TRY_CAST(time AS BIGINT) AS time,
                    summary,
                    text
                FROM read_csv_auto('{self.ratings_csv}', ignore_errors=true);
            """)
            self.conn.execute("CREATE INDEX idx_ratings_title ON ratings(Title);")
            print("Tabela ratings criada com sucesso!")

    def get_metricas_gerais(self) -> Dict[str, Any]:
        """
        Retorna indicadores-chave de performance (KPIs) globais da base.
        """
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

    def get_top_autores(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Retorna os autores com maior volume de avaliacoes.
        """
        query = f"""
            SELECT 
                b.authors AS autor_raw,
                count(r.score) AS total_avaliacoes,
                round(avg(r.score), 2) AS nota_media,
                count(DISTINCT b.Title) AS total_livros
            FROM books b
            JOIN ratings r ON b.Title = r.Title
            WHERE b.authors IS NOT NULL AND b.authors != '' AND b.authors != '[]'
            GROUP BY b.authors
            HAVING count(r.score) >= 15
            ORDER BY total_avaliacoes DESC
            LIMIT {limit};
        """
        df = self.conn.execute(query).df()
        df["autor"] = df["autor_raw"].astype(str).str.replace(r"[\[\]']", "", regex=True)
        return df.to_dict(orient="records")

    def get_top_categorias(self, limit: int = 40) -> List[Dict[str, Any]]:
        """
        Retorna os generos/categorias com maior volume de avaliacoes.
        """
        query = f"""
            SELECT 
                b.categories AS categoria_raw,
                count(r.score) AS total_avaliacoes,
                round(avg(r.score), 2) AS nota_media,
                count(DISTINCT b.Title) AS total_livros
            FROM books b
            JOIN ratings r ON b.Title = r.Title
            WHERE b.categories IS NOT NULL AND b.categories != '' AND b.categories != '[]'
            GROUP BY b.categories
            HAVING count(r.score) >= 15
            ORDER BY total_avaliacoes DESC
            LIMIT {limit};
        """
        df = self.conn.execute(query).df()
        df["categoria"] = df["categoria_raw"].astype(str).str.replace(r"[\[\]']", "", regex=True)
        return df.to_dict(orient="records")

    def get_reviews_por_autor(self, autor_nome: str, limit: int = 300) -> pd.DataFrame:
        """
        Busca resenhas para um determinado autor.
        """
        query = f"""
            SELECT 
                r.Id,
                r.Title,
                b.authors,
                b.categories,
                r.User_id,
                r.profileName,
                r.score,
                r.time,
                r.summary,
                r.text
            FROM books b
            JOIN ratings r ON b.Title = r.Title
            WHERE b.authors ILIKE '%{autor_nome}%'
            ORDER BY r.time DESC
            LIMIT {limit};
        """
        return self.conn.execute(query).df()

    def get_reviews_por_categoria(self, categoria_nome: str, limit: int = 300) -> pd.DataFrame:
        """
        Busca resenhas para uma determinada categoria.
        """
        query = f"""
            SELECT 
                r.Id,
                r.Title,
                b.authors,
                b.categories,
                r.User_id,
                r.profileName,
                r.score,
                r.time,
                r.summary,
                r.text
            FROM books b
            JOIN ratings r ON b.Title = r.Title
            WHERE b.categories ILIKE '%{categoria_nome}%'
            ORDER BY r.time DESC
            LIMIT {limit};
        """
        return self.conn.execute(query).df()


if __name__ == "__main__":
    loader = DataLoader()
    loader.inicializar_banco()
    print("KPIs:", loader.get_metricas_gerais())
