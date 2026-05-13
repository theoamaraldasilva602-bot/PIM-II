import json
import logging
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config.settings import (
    PASTA_PDFS,
    PASTA_RELATORIOS,
    ARQUIVO_BIBLIOTECA,
    RELATORIO_CONSOLIDADO,
    ARQUIVO_LOG,
    EXTENSOES_ACEITAS,
    MAX_COORDENADORES,
    VERBOSE,
)
from prex_triagem.src.pipeline import processar_proposta
from prex_triagem.src.relatorio import inicializar_csv_consolidado

def configurar_logging(nivel_console: int = logging.INFO) -> None:

    ARQUIVO_LOG.parent.mkdir(parents=True, exist_ok=True)

    formato = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    data_formato = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(
        level=logging.DEBUG,  
        format=formato,
        datefmt=data_formato,
        handlers=[
            logging.FileHandler(ARQUIVO_LOG, encoding="utf-8", mode="a"),
            logging.StreamHandler(sys.stdout),
        ],
    )

    logging.getLogger().handlers[1].setLevel(
        logging.DEBUG if VERBOSE else nivel_console
    )

    logging.getLogger("pdfminer").setLevel(logging.WARNING)
    logging.getLogger("pdfplumber").setLevel(logging.WARNING)
    logging.getLogger("PyPDF2").setLevel(logging.WARNING)

def carregar_biblioteca(caminho: Path) -> dict:
    if not caminho.exists():
        logging.critical(
            "Arquivo de biblioteca não encontrado: %s\n"
            "Verifique se 'biblioteca_termos.json' está na raiz do projeto.",
            caminho
        )
        sys.exit(1)

    try:
        with open(caminho, encoding="utf-8") as f:
            dados = json.load(f)
        logging.info("Biblioteca carregada: %s", caminho)
        return dados
    except json.JSONDecodeError as erro:
        logging.critical(
            "Erro ao ler '%s': JSON inválido.\nDetalhe: %s", caminho, erro
        )
        sys.exit(1)

def listar_pdfs(pasta: Path) -> list[Path]:

    if not pasta.exists():
        logging.warning(
            "Pasta de PDFs não encontrada: %s\n"
            "Crie a pasta e adicione os PDFs das propostas.",
            pasta
        )
        return []

    pdfs = sorted([
        arq for arq in pasta.iterdir()
        if arq.suffix.lower() in EXTENSOES_ACEITAS
    ])

    logging.info("PDFs encontrados em '%s': %d arquivo(s).", pasta, len(pdfs))
    return pdfs

def exibir_resumo_final(resultados: list[dict]) -> None:
    total = len(resultados)
    aptos = sum(1 for r in resultados if r["status"] == "APTO")
    alertas = sum(1 for r in resultados if r["status"] == "ALERTA")
    inaptos = sum(1 for r in resultados if r["status"] == "INAPTO")

    print("\n" + "=" * 70)
    print("  RESUMO DA TRIAGEM — PREX/IFB")
    print("=" * 70)
    print(f"  Total de propostas analisadas : {total}")
    print(f"  ✅ APTAS                       : {aptos}")
    print(f"  ⚠️  ALERTA                      : {alertas}")
    print(f"  ❌ INAPTAS                      : {inaptos}")
    print("=" * 70)

    if resultados:
        ranking = sorted(
            resultados, key=lambda r: r["pontuacao_merito"], reverse=True
        )[:5]

        print("\n  🏆 Top 5 por Pontuação de Mérito:")
        print("-" * 70)
        for pos, item in enumerate(ranking, start=1):
            print(
                f"  {pos}. {item['arquivo'][:45]:<45} "
                f"{item['pontuacao_merito']:>3} pts  "
                f"({item['classificacao_merito']})"
            )

    print("\n  📁 Relatórios individuais salvos em: relatorios/")
    print(f"  📊 Relatório consolidado: {RELATORIO_CONSOLIDADO}")
    print(f"  📝 Log completo: {ARQUIVO_LOG}")
    print("=" * 70)

def main() -> None:

    configurar_logging()
    logger = logging.getLogger(__name__)

    inicio = datetime.now()
    logger.info("=" * 60)
    logger.info("INÍCIO DA TRIAGEM — %s", inicio.strftime("%d/%m/%Y %H:%M:%S"))
    logger.info("=" * 60)

    print("\n" + "=" * 70)
    print("  🏛️  SISTEMA DE TRIAGEM DE EDITAIS — PREX/IFB")
    print(f"  Base legal: Resolução nº 42/2020")
    print(f"  Execução: {inicio.strftime('%d/%m/%Y às %H:%M')}")
    print("=" * 70)

    biblioteca = carregar_biblioteca(ARQUIVO_BIBLIOTECA)

    pdfs = listar_pdfs(PASTA_PDFS)

    if not pdfs:
        print(
            f"\n  ⚠️  Nenhum PDF encontrado em '{PASTA_PDFS}'.\n"
            "  Adicione os arquivos e execute novamente.\n"
        )
        return

    print(f"\n  📂 {len(pdfs)} proposta(s) encontrada(s). Iniciando triagem...\n")
    print("-" * 70)

    PASTA_RELATORIOS.mkdir(parents=True, exist_ok=True)
    inicializar_csv_consolidado(RELATORIO_CONSOLIDADO)

    resultados = []
    for indice, caminho_pdf in enumerate(pdfs, start=1):
        print(f"  [{indice:>3}/{len(pdfs)}] Analisando: {caminho_pdf.name}")

        resultado = processar_proposta(
            caminho_pdf=caminho_pdf,
            biblioteca=biblioteca,
            pasta_relatorios=PASTA_RELATORIOS,
            caminho_csv_consolidado=RELATORIO_CONSOLIDADO,
            max_coordenadores=MAX_COORDENADORES,
        )

        if resultado:
            resultados.append(resultado)

    fim = datetime.now()
    duracao = (fim - inicio).total_seconds()

    logger.info(
        "TRIAGEM CONCLUÍDA em %.1f segundos. %d/%d propostas processadas.",
        duracao, len(resultados), len(pdfs)
    )

    exibir_resumo_final(resultados)
    print(f"\n  ⏱️  Tempo total: {duracao:.1f} segundos\n")


if __name__ == "__main__":
    main()