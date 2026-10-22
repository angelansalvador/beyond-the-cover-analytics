"""
Modulo: business_metrics.py
Descricao: Calculo quantitativo do impacto financeiro, reducao de custos operacionais
e Retorno sobre o Investimento (ROI - Return on Investment) da solucao automatizada
em comparacao com o processo manual anterior.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class BusinessScenario:
    """
    Parametros do cenario de negocio fornecidos pela editora para analise de ROI:
    - 5 analistas dedicados em tempo integral
    - R$ 5.000,00 de salario mensal individual
    - 3 dias uteis para concluir 1 relatorio manualmente
    """
    num_analistas: int = 5                  # Quantidade de analistas no time atual
    salario_mensal_unitario: float = 5000.0 # Salario individual mensal em Reais (R$)
    dias_por_analise_manual: float = 3.0   # Dias necessarios para concluir 1 analise manualmente
    horas_dia_trabalho: float = 8.0        # Jornada de trabalho padrao em horas por dia
    dias_uteis_mes: int = 22               # Media de dias uteis em um mes comercial


class ROICalculator:
    """
    Calculadora de ROI (Return on Investment / Retorno sobre o Investimento)
    e metricas de produtividade entre o modelo manual e a plataforma automatizada.
    """

    def __init__(self, scenario: BusinessScenario = None):
        # Se nenhum cenario for passado, utiliza o cenario padrao da editora
        self.scenario = scenario if scenario is not None else BusinessScenario()

    def calcular_cenario_manual(self) -> Dict[str, Any]:
        """
        Calcula os custos, horas e capacidade produtiva do processo manual.
        
        Retorna dicionario com:
        - custo_mensal_total: Folha salarial mensal da equipe (R$)
        - custo_anual_total: Folha salarial anual da equipe (R$)
        - horas_homem_por_analise: Total de horas de analista gastas por analise
        - capacidade_analises_mes: Quantidade maxima de relatorios que o time gera por mes
        - custo_por_analise_manual: Custo financeiro estimado por cada relatorio manual
        """
        # Custo salarial direto mensal da equipe: 5 analistas * R$ 5.000 = R$ 25.000,00
        custo_mensal = self.scenario.num_analistas * self.scenario.salario_mensal_unitario
        custo_anual = custo_mensal * 12

        # Horas gastas por analise manual:
        # 3 dias uteis * 8 horas/dia * 5 pessoas = 120 horas-homem (man-hours) por analise
        horas_por_analise = (
            self.scenario.dias_por_analise_manual
            * self.scenario.horas_dia_trabalho
            * self.scenario.num_analistas
        )

        # Capacidade produtiva: 22 dias uteis / 3 dias por analise ~ 7.33 analises por mes
        capacidade_mensal = self.scenario.dias_uteis_mes / self.scenario.dias_por_analise_manual
        
        # Custo por relatorio individual manual (R$ 25.000 / ~7.33 = ~R$ 3.409,00 por relatorio)
        custo_unitario_analise = custo_mensal / capacidade_mensal if capacidade_mensal > 0 else 0

        return {
            "custo_mensal_total": custo_mensal,
            "custo_anual_total": custo_anual,
            "horas_homem_por_analise": horas_por_analise,
            "capacidade_analises_mes": round(capacidade_mensal, 1),
            "custo_por_analise_manual": round(custo_unitario_analise, 2)
        }

    def calcular_cenario_automatizado(
        self,
        tempo_segundos_por_analise: float = 30.0,
        custo_infra_mensal: float = 300.0
    ) -> Dict[str, Any]:
        """
        Calcula os ganhos operacionais com a plataforma automatizada.
        
        Parametros:
        - tempo_segundos_por_analise: Tempo medio de execucao da ferramenta (em segundos)
        - custo_infra_mensal: Custo estimado de servidor / nuvem / APIs (R$)
        
        Retorna dicionario com:
        - reducao_tempo_percentual: Ganho percentual em agilidade
        - economia_mensal_salarios: Valor financeiro mensal recuperado
        - economia_anual_salarios: Valor financeiro anual recuperado
        - horas_economizadas_por_analise: Horas de trabalho liberadas por analise
        - analistas_liberados_para_estrategia: Quantidade de pessoas liberadas para outras areas
        """
        manual = self.calcular_cenario_manual()

        # Tempo manual em segundos: 3 dias * 8 horas * 3600 segundos = 86.400 segundos
        tempo_manual_segundos = self.scenario.dias_por_analise_manual * self.scenario.horas_dia_trabalho * 3600
        
        # Reducao percentual no tempo de espera (SLA - Service Level Agreement)
        reducao_tempo_percentual = (
            (tempo_manual_segundos - tempo_segundos_por_analise) / tempo_manual_segundos
        ) * 100.0

        # Economia financeira liquida direta
        economia_mensal_salarios = manual["custo_mensal_total"] - custo_infra_mensal
        economia_anual_salarios = economia_mensal_salarios * 12

        # Horas economizadas por analise
        horas_economizadas_por_analise = manual["horas_homem_por_analise"] - (tempo_segundos_por_analise / 3600.0)

        return {
            "tempo_segundos_por_analise": tempo_segundos_por_analise,
            "reducao_tempo_percentual": round(reducao_tempo_percentual, 2),
            "economia_mensal_salarios": round(economia_mensal_salarios, 2),
            "economia_anual_salarios": round(economia_anual_salarios, 2),
            "horas_economizadas_por_analise": round(horas_economizadas_por_analise, 1),
            "analistas_liberados_para_estrategia": self.scenario.num_analistas
        }

    def gerar_relatorio_impacto_executivo(self) -> str:
        """
        Gera um relatorio textual formal formatado para decisores da editora.
        """
        manual = self.calcular_cenario_manual()
        auto = self.calcular_cenario_automatizado()

        return (
            "========================================================================\n"
            "RELATORIO EXECUTIVO: IMPACTO FINANCEIRO E EFICIENCIA OPERACIONAL\n"
            "Projeto: Beyond the Cover Analytics | A3Data para Editora\n"
            "========================================================================\n\n"
            "1. DIAGNOSTICO DO PROCESSO MANUAL (AS-IS):\n"
            f"   - Equipe Dedicada: {self.scenario.num_analistas} analistas de dados em tempo integral\n"
            f"   - Folha Salarial: R$ {manual['custo_mensal_total']:,.2f}/mes (R$ {manual['custo_anual_total']:,.2f}/ano)\n"
            f"   - Tempo por Analise (Lead Time): {self.scenario.dias_por_analise_manual:.0f} dias uteis ({manual['horas_homem_por_analise']:.0f} horas-homem)\n"
            f"   - Custo Medio Estimado por Relatorio Manual: R$ {manual['custo_por_analise_manual']:,.2f}\n"
            f"   - Gargalo Produtivo: Limite de aproximadamente {manual['capacidade_analises_mes']} analises mensais\n\n"
            "2. TRANSFORMACAO COM A FERRAMENTA AUTOMATIZADA (TO-BE):\n"
            f"   - Tempo de Resposta: Reduzido de 3 dias para ~{auto['tempo_segundos_por_analise']:.0f} segundos\n"
            f"   - Ganho de Velocidade Operacional: {auto['reducao_tempo_percentual']:.2f}% de reducao no tempo de entrega\n"
            f"   - Economia Salarial Direta Recuperada: R$ {auto['economia_mensal_salarios']:,.2f}/mes (R$ {auto['economia_anual_salarios']:,.2f}/ano)\n"
            f"   - Alocacao de Recursos Humanos: 100% dos analistas ({auto['analistas_liberados_para_estrategia']} profissionais)\n"
            "     liberados de tarefas repetitivas para atuarem em frentes estrategicas:\n"
            "     * Prospeccao e negociacao de direitos autorais de livros promissores;\n"
            "     * Relacionamento qualitativo direto com super-leitores e influencers;\n"
            "     * Campanhas de marketing direcionadas por publico-alvo e cluster de genero.\n"
            "========================================================================\n"
        )


if __name__ == "__main__":
    # Teste rapido do modulo
    calc = ROICalculator()
    print(calc.gerar_relatorio_impacto_executivo())
