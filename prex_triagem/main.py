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

#Configurar logging para o projeto.
def configurar_logging(nivel_console: int = logging.INFO) -> None:
    """
    Configura o sistema de logging do programa.

    Esta função define como as mensagens de log serão exibidas no console
    e salvas em arquivo, permitindo acompanhar a execução do programa
    durante desenvolvimento e produção.

    Parâmetros:
        nivel_console (int): Nível mínimo de mensagens mostradas no console.
                            Padrão: logging.INFO (mostra INFO, WARNING, ERROR).
                            Se VERBOSE=True, mostra DEBUG.
    """

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

#Carregar a biblioteca de termos.
def carregar_biblioteca(caminho: Path) -> dict:
    """
    Carrega a biblioteca de termos de validação a partir de um arquivo JSON.

    Esta função lê o arquivo 'biblioteca_termos.json' que contém os termos
    positivos, negativos e de alerta para cada bloco de validação.
    Se o arquivo não existir ou for inválido, o programa é encerrado.

    Parâmetros:
        caminho (Path): Caminho absoluto para o arquivo JSON da biblioteca.

    Retorna:
        dict: Dicionário com os dados da biblioteca carregados.
    """
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

#Listar os arquivos PDF na pasta especificada.
def listar_pdfs(pasta: Path) -> list[Path]:
    """
    Lista todos os arquivos PDF válidos em uma pasta específica.

    Esta função verifica a pasta definida em settings.py (normalmente 'data/pdfs_entrada')
    e retorna uma lista ordenada de caminhos para arquivos PDF.
    Apenas extensões aceitas (definidas em EXTENSOES_ACEITAS) são incluídas.

    Parâmetros:
        pasta (Path): Caminho para a pasta onde buscar os PDFs.

    Retorna:
        list[Path]: Lista de caminhos absolutos para os arquivos PDF encontrados.
    """

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

# Listar relatórios individuais gerados.
def listar_relatorios_individuais(pasta_relatorios: Path) -> list[Path]:
    """
    Lista todos os relatórios individuais em TXT gerados na pasta.
    
    Parâmetros:
        pasta_relatorios (Path): Caminho da pasta de relatórios.
    
    Retorna:
        list[Path]: Lista de caminhos para os arquivos *_relatorio.txt encontrados.
    """
    if not pasta_relatorios.exists():
        return []
    
    relatorios = sorted(pasta_relatorios.glob("*_relatorio.txt"))
    return relatorios

# Exibir resultado final da triagem, incluindo estatísticas e ranking.
def exibir_resumo_final(resultados: list[dict], pasta_relatorios: Path = None) -> None:
    """
    Exibe o resumo final da triagem com estatísticas globais e lista limitada de pareceres.
    
    Mostra apenas estatísticas gerais (aptos, alertas, inaptos) e os primeiros 5 pareceres
    individuais gerados, evitando inundação do terminal.
    
    Parâmetros:
        resultados (list[dict]): Lista com os resultados de todas as propostas.
        pasta_relatorios (Path): Caminho da pasta de relatórios para listar pareceres.
    """
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

    if pasta_relatorios:
        relatorios_gerados = listar_relatorios_individuais(pasta_relatorios)
        print("\n  📄 Pareceres Individuais Gerados:")
        print("-" * 70)
        if relatorios_gerados:
            # Mostrar apenas os primeiros 5 para evitar inundação
            max_exibir = 5
            for relatorio in relatorios_gerados[:max_exibir]:
                print(f"     • {relatorio.name}")
            
            restantes = len(relatorios_gerados) - max_exibir
            if restantes > 0:
                print(f"     ... e mais {restantes} parecer(es) salvo(s) no disco")
        else:
            print("     (nenhum parecer encontrado)")

    print("\n  📁 Arquivos salvos em: relatorios/")
    print(f"  📊 Relatório consolidado (CSV): {RELATORIO_CONSOLIDADO}")
    print(f"  📝 Log completo: {ARQUIVO_LOG}")
    print("=" * 70)

def main() -> None:
    """
    Função principal do programa de triagem de editais PREX/IFB.
    
    Coordena o carregamento da biblioteca, listagem dos PDFs, processamento
    individual de cada proposta (gerando pareceres em TXT) e exibição
    das estatísticas globais ao final.
    """

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

    exibir_resumo_final(resultados, PASTA_RELATORIOS)
    
    print(f"\n  ⏱️  Tempo total: {duracao:.1f} segundos\n")


if __name__ == "__main__":
    main()