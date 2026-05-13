import logging
from pathlib import Path
from typing import Any, Optional

from prex_triagem.src.extrator import preparar_documento
from prex_triagem.src.validador import validar_todos_os_blocos
from prex_triagem.src.pontuador import calcular_pontuacao_merito
from prex_triagem.src.relatorio import (
    determinar_status,
    gerar_relatorio_individual,
    registrar_no_csv_consolidado,
)

logger = logging.getLogger(__name__)


def processar_proposta(
    caminho_pdf: Path,
    biblioteca: dict[str, Any],
    pasta_relatorios: Path,
    caminho_csv_consolidado: Path,
    max_coordenadores: int = 1,
) -> Optional[dict[str, Any]]:
 
    nome_arquivo = caminho_pdf.name
    logger.info(">>> Iniciando triagem: %s", nome_arquivo)

    texto_normalizado = preparar_documento(caminho_pdf)

    if not texto_normalizado:
        logger.error(
            "Não foi possível extrair texto de '%s'. Proposta ignorada.",
            nome_arquivo
        )
        return None

    if len(texto_normalizado) < 100:
        logger.warning(
            "'%s' possui texto muito curto (%d chars). "
            "Pode ser um PDF escaneado sem OCR.",
            nome_arquivo, len(texto_normalizado)
        )

    resultados_blocos = validar_todos_os_blocos(
        texto_normalizado, biblioteca, max_coordenadores=max_coordenadores
    )

    config_bloco5 = biblioteca.get("bloco_5_merito", {})
    resultado_merito = calcular_pontuacao_merito(texto_normalizado, config_bloco5)

    caminho_relatorio = gerar_relatorio_individual(
        nome_arquivo=nome_arquivo,
        resultados_blocos=resultados_blocos,
        resultado_merito=resultado_merito,
        pasta_saida=pasta_relatorios,
    )

    registrar_no_csv_consolidado(
        caminho_csv=caminho_csv_consolidado,
        nome_arquivo=nome_arquivo,
        resultados_blocos=resultados_blocos,
        resultado_merito=resultado_merito,
    )


    status = determinar_status(resultados_blocos, resultado_merito)
    icone = {"APTO": "✅", "ALERTA": "⚠️ ", "INAPTO": "❌"}.get(status, "?")

    print(
        f"  {icone} {status:<8} | "
        f"Mérito: {resultado_merito['pontuacao_total']:>3}pts "
        f"({resultado_merito['classificacao']}) | "
        f"{nome_arquivo}"
    )

    logger.info(
        "<<< Triagem concluída: %s | Status: %s | Mérito: %d pts",
        nome_arquivo, status, resultado_merito["pontuacao_total"]
    )

    return {
        "arquivo": nome_arquivo,
        "status": status,
        "pontuacao_merito": resultado_merito["pontuacao_total"],
        "classificacao_merito": resultado_merito["classificacao"],
        "caminho_relatorio": str(caminho_relatorio),
    }