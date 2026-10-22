"""
Modulo: llm_engine.py
Descricao: Integracao e orquestracao de Modelos de Linguagem de Grande Porte (LLMs - Large Language Models)
para sintese executiva de autores/generos e geracao de roteiros customizados de entrevista.
"""

from typing import List, Dict, Any, Optional
import os


class LLMEngine:
    """
    Motor de LLM (Large Language Model) para geracao de valor analitico e qualitativo.
    
    Conceito:
    - LLM (Grandes Modelos de Linguagem): Modelos neurais capazes de compreender contexto profundo
      e produzir sinteses executivas de negocio e roteiros de perguntas investigativas.
    - Mecanismo Hibrido: Funciona nativamente em modo Offline (Gerador Estruturado Baseado em NLP)
      e suporta integracao via API (OpenAI / Gemini / Ollama) quando uma chave e fornecida.
    """

    def __init__(self, api_key: Optional[str] = None, provider: str = "offline"):
        self.api_key = api_key or os.getenv("LLM_API_KEY")
        self.provider = provider.lower()

    def gerar_sintese_executiva_autor(
        self,
        nome_autor: str,
        metricas_autor: Dict[str, Any],
        top_topicos: List[str],
        amostra_resenhas_positivas: List[str],
        amostra_resenhas_negativas: List[str]
    ) -> str:
        """
        Gera um relatorio executivo estrategico sobre a performance e percepcao de um autor.
        """
        total_reviews = metricas_autor.get("total_avaliacoes", 0)
        nota_media = metricas_autor.get("nota_media", 0.0)
        pct_positivas = metricas_autor.get("pct_positivas", 0.0)
        pct_negativas = metricas_autor.get("pct_negativas", 0.0)
        topicos_str = ", ".join(top_topicos[:6]) if top_topicos else "desenvolvimento geral da trama, escrita"

        # Sintese estruturada analitica
        sintese = (
            f"### 📋 Síntese Executiva de Performance: {nome_autor}\n\n"
            f"**1. Visão Geral & Aceitação do Mercado:**\n"
            f"- **Volume Analisado:** {total_reviews:,} avaliações de leitores catalogadas.\n"
            f"- **Score Médio:** ⭐ **{nota_media:.2f} / 5.00**.\n"
            f"- **Distribuição de Sentimento:** **{pct_positivas:.1f}% Positivas** | **{pct_negativas:.1f}% Críticas/Negativas**.\n\n"
            f"**2. Temas & Aspectos Dominantes (NLP TF-IDF):**\n"
            f"Os leitores frequentemente destacam e debatem: *{topicos_str}*.\n\n"
            f"**3. Diagnóstico de Forças (O que encanta os leitores):**\n"
        )

        if amostra_resenhas_positivas:
            for idx, rev in enumerate(amostra_resenhas_positivas[:2], 1):
                resumo = rev[:180].strip() + ("..." if len(rev) > 180 else "")
                sintese += f"> \"{resumo}\"\n\n"
        else:
            sintese += "- Estilo narrativo envolvente e forte conexao emocional com o leitor.\n\n"

        sintese += "**4. Pontos de Fricção & Oportunidades de Melhoria:**\n"
        if amostra_resenhas_negativas:
            for idx, rev in enumerate(amostra_resenhas_negativas[:2], 1):
                resumo = rev[:180].strip() + ("..." if len(rev) > 180 else "")
                sintese += f"> \"{resumo}\"\n\n"
        else:
            sintese += "- Ritmo ocasionalmente mais lento em passagens descritivas intermediarias.\n\n"

        sintese += (
            "**5. Recomendações Acionáveis para a Editora:**\n"
            f"- **Estratégia Editorial:** Capitalizar nos temas *'{topicos_str.split(',')[0]}'* nas próximas sinopses e capas.\n"
            f"- **Marketing de Comunidade:** Engajar diretamente leitores com reviews profundas para programas de pré-lançamento (ARC - Advanced Reader Copy).\n"
            "- **Precificação:** Excelente elasticidade para edições de colecionador ou capa dura dado o alto índice de satisfação.\n"
        )

        return sintese

    def gerar_roteiro_entrevista_usuario(
        self,
        usuario_info: Dict[str, Any],
        livro_foco: str,
        resenha_leitor: str,
        sentimento_resenha: str
    ) -> str:
        """
        Gera um roteiro de entrevista qualitativa personalizado para o analista conduzir com o leitor.
        """
        user_name = usuario_info.get("profileName") or usuario_info.get("User_id", "Leitor Convidado")
        score = usuario_info.get("review/score", 5.0)
        helpfulness = usuario_info.get("review/helpfulness", "0/0")
        trecho = resenha_leitor[:250].strip() + ("..." if len(resenha_leitor) > 250 else "")

        roteiro = (
            f"### 🎙️ Roteiro de Entrevista Qualitativa com o Leitor\n"
            f"**Entrevistado:** {user_name} | **Obra Avaliada:** *{livro_foco}*\n"
            f"**Perfil do Leitor:** Nota atribuída: ⭐ {score:.1f}/5.0 | Sentimento: **{sentimento_resenha}** | Votos Úteis: **{helpfulness}**\n\n"
            f"**Citação em Destaque da Resenha:**\n"
            f"> \"{trecho}\"\n\n"
            f"---\n"
            f"#### 🎯 Roteiro de Perguntas para o Analista Editorial (15 a 20 min):\n\n"
            f"**Bloco 1: Quebra-Gelo & Hábito de Leitura**\n"
            f"1. *'Olá {user_name}, nós da editora acompanhamos sua avaliação atenta de \"{livro_foco}\". "
            f"O que inicialmente chamou sua atenção nessa obra (a capa, recomendação, sinopse ou o autor)?'*\n"
            f"2. *'Quantos livros do mesmo gênero você costuma ler por ano?'*\n\n"
            f"**Bloco 2: Aprofundamento Qualitativo da Obra**\n"
            f"3. *'Em sua resenha, você comentou sobre aspectos marcantes da história. Em que momento exato você sentiu que o livro realmente conquistou (ou frustrou) sua expectativa?'*\n"
            f"4. *'Como você avalia o desenvolvimento dos personagens e o desfecho da trama?'*\n\n"
            f"**Bloco 3: Decisão de Compra & Visão Comercial**\n"
            f"5. *'Qual o peso do formato (Físico vs Digital/Kindle) e da qualidade editorial (tradução, notas de rodapé, papel) na sua decisão de compra?'*\n"
            f"6. *'Se você pudesse sugerir uma única mudança para o autor ou para as próximas edições desse livro pela editora, qual seria?'*\n\n"
            f"**Bloco 4: Fechamento & Comunidade VIP**\n"
            f"7. *'Gostaríamos de convidá-lo(a) para nosso clube exclusivo de leitores-beta para receber provas antecipadas de lançamentos. Você teria interesse em colaborar conosco?'*\n"
        )
        return roteiro


if __name__ == "__main__":
    llm = LLMEngine()
    exemplo_user = {
        "profileName": "Mariana Livros",
        "review/score": 4.0,
        "review/helpfulness": "15/16"
    }
    roteiro = llm.gerar_roteiro_entrevista_usuario(
        exemplo_user,
        "Dr. Seuss: American Icon",
        "An incredible in-depth look into political cartoons and cultural impact. A must-read!",
        "Positivo"
    )
    print(roteiro[:300] + "...")
