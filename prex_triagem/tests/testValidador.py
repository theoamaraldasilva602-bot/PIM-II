import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from prex_triagem.src.validador import (
    validar_bloco1_exercicio_pleno,
    validar_bloco2_vinculo_institucional,
    validar_bloco3_composicao_equipe,
    validar_bloco4_aderencia_edital,
)


CONFIG_BLOCO1 = {
    "termos_positivos": ["em exercicio", "servidor ativo", "docente efetivo"],
    "termos_negativos_impeditivos": [
        "afastado para pos-graduacao", "licenca premio"
    ],
}

CONFIG_BLOCO2 = {
    "termos_positivos": ["instituto federal de brasilia", "ifb", "campus", "proponente"],
    "termos_de_alerta": ["outra instituicao"],
}

CONFIG_BLOCO3 = {
    "termos_positivos": ["equipe executora", "coordenador", "discente", "colaborador"],
    "termos_docente_orientador": ["docente", "professor"],
    "termos_tecnico_administrativo": ["tecnico administrativo", "tae"],
    "funcoes_coordenacao": ["coordenador", "coordenadora"],
}

CONFIG_BLOCO4 = {
    "areas_tematicas_validas": ["educacao", "saude", "meio ambiente"],
    "linhas_de_extensao_validas": ["educacao profissional e tecnologica"],
    "termos_de_modalidade": ["projeto de extensao", "programa de extensao"],
}


class TestBloco1ExercicioPleno(unittest.TestCase):

    def test_aprovado_com_termo_positivo(self):
        texto = "o proponente esta em exercicio pleno no campus plano piloto"
        resultado = validar_bloco1_exercicio_pleno(texto, CONFIG_BLOCO1)
        self.assertTrue(resultado["aprovado"])
        self.assertIn("em exercicio", resultado["termos_encontrados"])
        self.assertEqual(resultado["impedimentos"], [])

    def test_inapto_com_impedimento_afastamento_pos(self):
        """Termo de afastamento deve gerar impedimento imediato."""
        texto = "servidor afastado para pos-graduacao desde 2023"
        resultado = validar_bloco1_exercicio_pleno(texto, CONFIG_BLOCO1)
        self.assertFalse(resultado["aprovado"])
        self.assertTrue(len(resultado["impedimentos"]) > 0)

    def test_inapto_com_licenca_premio(self):
        """Licença prêmio deve gerar impedimento."""
        texto = "servidor em licenca premio aprovada pelo conselho"
        resultado = validar_bloco1_exercicio_pleno(texto, CONFIG_BLOCO1)
        self.assertFalse(resultado["aprovado"])
        self.assertIn("licenca premio", resultado["impedimentos"])

    def test_alerta_sem_termos(self):
        texto = "este documento descreve a proposta de trabalho da equipe"
        resultado = validar_bloco1_exercicio_pleno(texto, CONFIG_BLOCO1)
        self.assertFalse(resultado["aprovado"])
        self.assertEqual(resultado["impedimentos"], [])
        self.assertTrue(len(resultado["alertas"]) > 0)



class TestBloco2VinculoInstitucional(unittest.TestCase):

    def test_aprovado_com_dois_termos(self):
        texto = "proposta submetida ao instituto federal de brasilia campus taguatinga"
        resultado = validar_bloco2_vinculo_institucional(texto, CONFIG_BLOCO2)
        self.assertTrue(resultado["aprovado"])

    def test_alerta_com_apenas_um_termo(self):
        texto = "proposta vinculada ao ifb somente"
        resultado = validar_bloco2_vinculo_institucional(texto, CONFIG_BLOCO2)
        self.assertFalse(resultado["aprovado"])

    def test_alerta_com_termo_de_alerta(self):
        texto = "proposta em parceria com outra instituicao como executora principal ifb campus"
        resultado = validar_bloco2_vinculo_institucional(texto, CONFIG_BLOCO2)
        self.assertTrue(len(resultado["alertas"]) > 0)

class TestBloco3ComposicaoEquipe(unittest.TestCase):

    def test_aprovado_equipe_completa(self):
        texto = (
            "equipe executora composta pelo coordenador prof joao, "
            "discente maria e colaborador carlos"
        )
        resultado = validar_bloco3_composicao_equipe(texto, CONFIG_BLOCO3)
        self.assertTrue(resultado["aprovado"])
        self.assertEqual(resultado["impedimentos"], [])

    def test_impedimento_multiplos_coordenadores(self):
        texto = (
            "coordenador prof joao e coordenadora profa ana "
            "sao responsaveis pela equipe executora discente pedro"
        )
        resultado = validar_bloco3_composicao_equipe(
            texto, CONFIG_BLOCO3, max_coordenadores=1
        )
        self.assertFalse(resultado["aprovado"])
        self.assertTrue(len(resultado["impedimentos"]) > 0)

    def test_impedimento_tae_sem_docente(self):
        texto = (
            "o tecnico administrativo jose coordena o projeto "
            "com equipe executora de discentes"
        )
        resultado = validar_bloco3_composicao_equipe(texto, CONFIG_BLOCO3)
        impedimentos_str = " ".join(resultado["impedimentos"])
        self.assertIn("TAE", impedimentos_str)

    def test_tae_com_docente_aprovado(self):
        texto = (
            "o tecnico administrativo jose propoe o projeto "
            "sob orientacao do professor carlos, com equipe executora e discente"
        )
        resultado = validar_bloco3_composicao_equipe(texto, CONFIG_BLOCO3)
        impedimentos_str = " ".join(resultado["impedimentos"])
        self.assertNotIn("TAE", impedimentos_str)


class TestBloco4AderenciaEdital(unittest.TestCase):

    def test_aprovado_com_area_e_modalidade(self):
        texto = (
            "este projeto de extensao visa promover acoes na area de educacao "
            "voltadas para a comunidade do entorno"
        )
        resultado = validar_bloco4_aderencia_edital(texto, CONFIG_BLOCO4)
        self.assertTrue(resultado["aprovado"])

    def test_reprovado_sem_modalidade(self):
        texto = "acao voltada para educacao e saude da populacao local"
        resultado = validar_bloco4_aderencia_edital(texto, CONFIG_BLOCO4)
        self.assertFalse(resultado["aprovado"])

    def test_reprovado_sem_area_tematica(self):
        texto = "desenvolvemos um programa de extensao voltado para a comunidade"
        resultado = validar_bloco4_aderencia_edital(texto, CONFIG_BLOCO4)
        self.assertFalse(resultado["aprovado"])

if __name__ == "__main__":
    print("Executando testes unitários do Validador PREX/IFB...\n")
    unittest.main(verbosity=2)