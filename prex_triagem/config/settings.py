import os
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent

PASTA_PDFS = ROOT_DIR / "data" / "pdfs_entrada"
PASTA_EDITAIS_JSON = ROOT_DIR / "data" / "editais_json"
PASTA_RELATORIOS = ROOT_DIR / "relatorios"
PASTA_LOGS = ROOT_DIR / "logs"
ARQUIVO_BIBLIOTECA = ROOT_DIR / "biblioteca_termos.json"
RELATORIO_CONSOLIDADO = PASTA_RELATORIOS / "consolidado.csv"
ARQUIVO_LOG = PASTA_LOGS / "triagem.log"
MAX_COORDENADORES = 1
LIMIAR_ALTO_MERITO = 25
LIMIAR_MEDIO_MERITO = 12
EXTENSOES_ACEITAS = [".pdf"]
TAMANHO_MINIMO_TEXTO = 100
ENCODING_SAIDA = "utf-8"
VERBOSE = True
LARGURA_SEPARADOR = 70