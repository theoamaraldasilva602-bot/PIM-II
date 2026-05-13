import logging
import re
import unicodedata 
from pathlib import Path
from typing import Optional

try:
    import pdfplumber
    PDFPLUMBER_DISPONIVEL = True
except ImportError:
    PDFPLUMBER_DISPONIVEL = False

try:
    import pypdf 
    PYPDF_DISPONIVEL = True
except ImportError:
    PYPDF_DISPONIVEL = False

logger = logging.getLogger(__name__)

def extrair_texto_pdfplumber(caminho_pdf: Path) -> str:

    texto_paginas = []

    with pdfplumber.open(str(caminho_pdf)) as pdf:
        for numero_pagina, pagina in enumerate(pdf.pages, start=1):
            texto = pagina.extract_text()
            if texto:
                texto_paginas.append(texto)
            else:
                logger.debug(
                    "Página %d de '%s' não retornou texto (pode ser imagem).",
                    numero_pagina, caminho_pdf.name
                )

    return "\n".join(texto_paginas)


def extrair_texto_pypdf(caminho_pdf: Path) -> str:

    texto_paginas = []

    with open(caminho_pdf, "rb") as arquivo:
        leitor = pypdf.PdfReader(arquivo)
        for numero_pagina, pagina in enumerate(leitor.pages, start=1):
            texto = pagina.extract_text()
            if texto:
                texto_paginas.append(texto)
            else:
                logger.debug(
                    "pypdf — Página %d de '%s' sem texto.",
                    numero_pagina, caminho_pdf.name
                )

    return "\n".join(texto_paginas)


def extrair_texto(caminho_pdf: Path) -> Optional[str]:

    if not caminho_pdf.exists():
        logger.error("Arquivo não encontrado: %s", caminho_pdf)
        return None

    if PDFPLUMBER_DISPONIVEL:
        try:
            texto = extrair_texto_pdfplumber(caminho_pdf)
            if texto.strip():
                logger.info(
                    "Texto extraído com pdfplumber: %d caracteres — '%s'",
                    len(texto), caminho_pdf.name
                )
                return texto
            logger.warning(
                "pdfplumber retornou texto vazio para '%s'. Tentando pypdf.",
                caminho_pdf.name
            )
        except Exception as erro:
            logger.warning(
                "pdfplumber falhou em '%s': %s. Tentando pypdf.",
                caminho_pdf.name, erro
            )

    if PYPDF_DISPONIVEL:
        try:
            texto = extrair_texto_pypdf(caminho_pdf)
            if texto.strip():
                logger.info(
                    "Texto extraído com pypdf: %d caracteres — '%s'",
                    len(texto), caminho_pdf.name
                )
                return texto
            logger.warning(
                "pypdf também retornou texto vazio para '%s'.",
                caminho_pdf.name
            )
        except Exception as erro:
            logger.error(
                "pypdf falhou em '%s': %s.", caminho_pdf.name, erro
            )

    logger.error(
        "Impossível extrair texto de '%s'. O PDF pode ser baseado em imagens.",
        caminho_pdf.name
    )
    return None

def normalizar_texto(texto: str) -> str:

    if not texto:
        return ""

    texto = texto.lower()
    texto = (
        unicodedata.normalize("NFKD", texto)
        .encode("ascii", "ignore")
        .decode("ascii")
    )

    texto = re.sub(r"[\r\n\t]+", " ", texto)
    texto = re.sub(r" {2,}", " ", texto)

    texto = re.sub(r"[^\x20-\x7e]", " ", texto)

    return texto.strip()


def preparar_documento(caminho_pdf: Path) -> Optional[str]:

    texto_bruto = extrair_texto(caminho_pdf)

    if texto_bruto is None:
        return None

    texto_normalizado = normalizar_texto(texto_bruto)

    if len(texto_normalizado) < 100:
        logger.warning(
            "Texto muito curto (%d chars) em '%s'. "
            "O PDF pode ser escaneado (imagem sem OCR).",
            len(texto_normalizado), caminho_pdf.name
        )

    return texto_normalizado