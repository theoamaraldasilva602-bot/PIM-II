import logging
import re
from typing import Any

logger = logging.getLogger(__name__)

def _encontrar_termos(texto: str, lista_termos: list[str]) -> list[str]:

    encontrados = []
    for termo in lista_termos:
        padrao = r"\b" + re.escape(termo) + r"\b"
        if re.search(padrao, texto):
            encontrados.append(termo)
    return encontrados


def _contar_ocorrencias(texto: str, termo: str) -> int:
    padrao = r"\b" + re.escape(termo) + r"\b"
    return len(re.findall(padrao, texto))

def validar_bloco1_exercicio_pleno(
    texto: str, config_bloco: dict[str, Any]
) -> dict[str, Any]:

    resultado = {
        "aprovado": False,
        "termos_encontrados": [],
        "termos_ausentes": [],
        "alertas": [],
        "impedimentos": [],
    }

    impedimentos = _encontrar_termos(
        texto, config_bloco.get("termos_negativos_impeditivos", [])
    )
    if impedimentos:
        resultado["impedimentos"] = impedimentos
        logger.warning(
            "BLOCO 1 — Impedimento detectado: %s", impedimentos
        )
        return resultado 

    termos_positivos = config_bloco.get("termos_positivos", [])
    encontrados = _encontrar_termos(texto, termos_positivos)
    resultado["termos_encontrados"] = encontrados

    ausentes = [t for t in termos_positivos if t not in encontrados]

    if encontrados:
        resultado["aprovado"] = True
    else:
        resultado["termos_ausentes"] = ausentes
        resultado["alertas"].append(
            "Nenhum termo de exercício pleno encontrado. "
            "Verifique se o vínculo do servidor está documentado."
        )

    return resultado

def validar_bloco2_vinculo_institucional(
    texto: str, config_bloco: dict[str, Any]
) -> dict[str, Any]:

    resultado = {
        "aprovado": False,
        "termos_encontrados": [],
        "termos_ausentes": [],
        "alertas": [],
        "impedimentos": [],
    }

    alertas = _encontrar_termos(
        texto, config_bloco.get("termos_de_alerta", [])
    )
    if alertas:
        resultado["alertas"].append(
            f"Termos de atenção encontrados: {alertas}. "
            "Verificar se há comprometimento do vínculo com o IFB."
        )

    termos_positivos = config_bloco.get("termos_positivos", [])
    encontrados = _encontrar_termos(texto, termos_positivos)
    resultado["termos_encontrados"] = encontrados

    if len(encontrados) >= 2:
        resultado["aprovado"] = True
    else:
        resultado["termos_ausentes"] = [
            t for t in termos_positivos if t not in encontrados
        ]
        resultado["alertas"].append(
            "Vínculo institucional fraco: menos de 2 termos identificadores "
            "do IFB encontrados na proposta."
        )

    return resultado

def validar_bloco3_composicao_equipe(
    texto: str,
    config_bloco: dict[str, Any],
    max_coordenadores: int = 1,
) -> dict[str, Any]:

    resultado = {
        "aprovado": False,
        "termos_encontrados": [],
        "termos_ausentes": [],
        "alertas": [],
        "impedimentos": [],
    }

    termos_equipe = config_bloco.get("termos_positivos", [])
    encontrados = _encontrar_termos(texto, termos_equipe)
    resultado["termos_encontrados"] = encontrados

    funcoes_coord = config_bloco.get("funcoes_coordenacao", [])
    total_mencoes_coord = sum(
        _contar_ocorrencias(texto, f) for f in funcoes_coord
    )

    if total_mencoes_coord > max_coordenadores:
        resultado["impedimentos"].append(
            f"Múltiplos coordenadores detectados "
            f"({total_mencoes_coord} menções a funções de coordenação). "
            f"O máximo permitido é {max_coordenadores}."
        )
        logger.warning(
            "BLOCO 3 — %d menções de coordenação detectadas (máx: %d).",
            total_mencoes_coord, max_coordenadores
        )

    termos_tae = config_bloco.get("termos_tecnico_administrativo", [])
    termos_docente = config_bloco.get("termos_docente_orientador", [])

    proponente_e_tae = bool(_encontrar_termos(texto, termos_tae))
    docente_presente = bool(_encontrar_termos(texto, termos_docente))

    if proponente_e_tae and not docente_presente:
        resultado["impedimentos"].append(
            "Proponente identificado como TAE, mas nenhum Docente/Professor "
            "foi encontrado na equipe. A orientação docente é obrigatória "
            "conforme a Resolução nº 42/2020."
        )
        logger.warning("BLOCO 3 — TAE sem docente orientador na equipe.")
    elif proponente_e_tae and docente_presente:
        resultado["alertas"].append(
            "Proponente TAE: docente orientador confirmado na equipe. ✓"
        )

    if resultado["impedimentos"]:
        resultado["aprovado"] = False
    elif len(encontrados) >= 2:
        resultado["aprovado"] = True
    else:
        resultado["termos_ausentes"] = [
            t for t in termos_equipe if t not in encontrados
        ]
        resultado["alertas"].append(
            "Poucos termos de equipe identificados. "
            "Verifique se a seção de equipe executora está bem descrita."
        )

    return resultado


def validar_bloco4_aderencia_edital(
    texto: str, config_bloco: dict[str, Any]
) -> dict[str, Any]:
    
    resultado = {
        "aprovado": False,
        "termos_encontrados": [],
        "termos_ausentes": [],
        "alertas": [],
        "impedimentos": [],
    }

    areas_validas = config_bloco.get("areas_tematicas_validas", [])
    linhas_validas = config_bloco.get("linhas_de_extensao_validas", [])
    modalidades = config_bloco.get("termos_de_modalidade", [])

    areas_encontradas = _encontrar_termos(texto, areas_validas)
    linhas_encontradas = _encontrar_termos(texto, linhas_validas)
    modalidades_encontradas = _encontrar_termos(texto, modalidades)

    resultado["termos_encontrados"] = (
        areas_encontradas + linhas_encontradas + modalidades_encontradas
    )

    if areas_encontradas and modalidades_encontradas:
        resultado["aprovado"] = True
    else:
        if not areas_encontradas:
            resultado["termos_ausentes"].append(
                "Nenhuma área temática válida identificada."
            )
        if not modalidades_encontradas:
            resultado["termos_ausentes"].append(
                "Modalidade da ação (projeto/programa/curso/evento) não identificada."
            )

    if not linhas_encontradas:
        resultado["alertas"].append(
            "Linha de extensão não identificada explicitamente. "
            "Verifique se está descrita no texto da proposta."
        )

    return resultado


def validar_todos_os_blocos(
    texto: str,
    biblioteca: dict[str, Any],
    max_coordenadores: int = 1,
) -> dict[str, Any]:

    resultados = {}

    resultados["bloco_1"] = validar_bloco1_exercicio_pleno(
        texto, biblioteca.get("bloco_1_exercicio_pleno", {})
    )
    resultados["bloco_2"] = validar_bloco2_vinculo_institucional(
        texto, biblioteca.get("bloco_2_vinculo_institucional", {})
    )
    resultados["bloco_3"] = validar_bloco3_composicao_equipe(
        texto,
        biblioteca.get("bloco_3_composicao_equipe", {}),
        max_coordenadores=max_coordenadores,
    )
    resultados["bloco_4"] = validar_bloco4_aderencia_edital(
        texto, biblioteca.get("bloco_4_aderencia_edital", {})
    )

    return resultados