{
  "_meta": {
    "versao": "1.0",
    "base_legal": "Resolução nº 42/2020 — IFB",
    "ultima_atualizacao": "2025",
    "instrucao": "Edite os termos abaixo conforme o edital vigente. Todos os termos devem estar em MINÚSCULAS e SEM ACENTOS para garantir compatibilidade com o pré-processamento."
  },

  "bloco_1_exercicio_pleno": {
    "descricao": "Verifica se o proponente está em exercício pleno de suas funções no IFB",
    "obrigatorio": true,
    "termos_positivos": [
      "em exercicio",
      "servidor ativo",
      "docente efetivo",
      "professor efetivo",
      "tecnico administrativo",
      "em atividade",
      "lotado no campus",
      "lotado na reitoria",
      "vinculo ativo",
      "quadro permanente"
    ],
    "termos_negativos_impeditivos": [
      "afastado para pos-graduacao",
      "afastado para doutorado",
      "afastado para mestrado",
      "licenca premio",
      "licenca capacitacao",
      "cedido para",
      "em afastamento",
      "licenca medica prolongada",
      "exonerado",
      "aposentado",
      "redistribuido"
    ],
    "peso": 1
  },

  "bloco_2_vinculo_institucional": {
    "descricao": "Confirma o vínculo do proponente e da proposta com o IFB",
    "obrigatorio": true,
    "termos_positivos": [
      "instituto federal de brasilia",
      "ifb",
      "campus",
      "reitoria",
      "cnpj 10.724.560",
      "proponente",
      "coordenador",
      "servidor do ifb",
      "docente do ifb",
      "tecnico do ifb"
    ],
    "termos_negativos_impeditivos": [],
    "termos_de_alerta": [
      "outra instituicao",
      "instituicao parceira exclusiva",
      "sem vinculo"
    ],
    "peso": 1
  },

  "bloco_3_composicao_equipe": {
    "descricao": "Valida a composição mínima da equipe executora",
    "obrigatorio": true,
    "termos_positivos": [
      "equipe executora",
      "coordenador",
      "discente",
      "aluno",
      "estudante",
      "colaborador",
      "membro da equipe",
      "equipe de trabalho"
    ],
    "termos_docente_orientador": [
      "docente",
      "professor",
      "professora",
      "docente orientador",
      "professor orientador",
      "coordenador docente"
    ],
    "termos_tecnico_administrativo": [
      "tecnico administrativo",
      "tecnico-administrativo",
      "servidor tecnico",
      "tae"
    ],
    "funcoes_coordenacao": [
      "coordenador",
      "coordenadora",
      "coord.",
      "proponente coordenador"
    ],
    "peso": 1
  },

  "bloco_4_aderencia_edital": {
    "descricao": "Verifica se a proposta atende às áreas temáticas e linhas de extensão previstas no edital",
    "obrigatorio": true,
    "areas_tematicas_validas": [
      "comunicacao",
      "cultura",
      "direitos humanos e justica",
      "educacao",
      "meio ambiente",
      "saude",
      "tecnologia e producao",
      "trabalho",
      "ciencia e tecnologia",
      "desenvolvimento regional"
    ],
    "linhas_de_extensao_validas": [
      "alfabetizacao e letramento",
      "desenvolvimento sustentavel",
      "educacao profissional e tecnologica",
      "empreendedorismo",
      "formacao de professores",
      "inclusao digital",
      "seguranca alimentar",
      "saude da familia",
      "tecnologias assistivas",
      "inovacao tecnologica"
    ],
    "termos_de_modalidade": [
      "projeto de extensao",
      "programa de extensao",
      "curso de extensao",
      "evento de extensao",
      "prestacao de servico"
    ],
    "peso": 1
  },

  "bloco_5_merito": {
    "descricao": "Avalia indicadores de qualidade e impacto da proposta (não eliminatório — gera ranking)",
    "obrigatorio": false,
    "termos_de_merito": {
      "impacto_social": {
        "termos": [
          "impacto social",
          "transformacao social",
          "beneficio a comunidade",
          "beneficio para a comunidade",
          "retorno a sociedade",
          "retorno para a sociedade",
          "populacao vulneravel",
          "inclusao social"
        ],
        "pontos_por_ocorrencia": 2,
        "max_pontos": 10
      },
      "indissociabilidade": {
        "termos": [
          "indissociabilidade",
          "ensino pesquisa extensao",
          "tríade",
          "triade",
          "articulacao ensino",
          "integracao curriculo",
          "creditacao"
        ],
        "pontos_por_ocorrencia": 3,
        "max_pontos": 9
      },
      "sustentabilidade": {
        "termos": [
          "sustentabilidade",
          "acao continuada",
          "permanencia",
          "continuidade da acao",
          "replicabilidade",
          "multiplicadores"
        ],
        "pontos_por_ocorrencia": 2,
        "max_pontos": 8
      },
      "metodologia": {
        "termos": [
          "metodologia",
          "cronograma",
          "etapas de execucao",
          "plano de trabalho",
          "indicadores de resultado",
          "metas",
          "avaliacao de impacto"
        ],
        "pontos_por_ocorrencia": 1,
        "max_pontos": 7
      },
      "parcerias": {
        "termos": [
          "parceria",
          "convenio",
          "termo de cooperacao",
          "rede de parceiros",
          "interinstitucional",
          "articulacao com",
          "colaboracao com"
        ],
        "pontos_por_ocorrencia": 2,
        "max_pontos": 8
      }
    },
    "pontuacao_maxima_total": 42,
    "limiares": {
      "alto_merito": 25,
      "medio_merito": 12,
      "baixo_merito": 0
    },
    "peso": 0
  }
}