import json
import os 
from modelos import Usuario, Semestre, Materia, Nota

ARQUIVO_DADOS = "dados_sistema.json"

class BancoDados:
    lista_materias = []
    lista_semestres = []
    info_usuario = Usuario(nome="Estudante", curso="Engenharia", carga_horaria_total=3600, semestres_totais=8)

    @staticmethod
    def _salvar_dados():
        """ Salva imediatamente no JSON. """
        dados_a_salvar = {
            "materias": [m.to_dict() for m in BancoDados.lista_materias],
            "semestres": [s.to_dict() for s in BancoDados.lista_semestres],
            "usuario": BancoDados.info_usuario.to_dict()
        }
        try:
            with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as f:
                json.dump(dados_a_salvar, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"[BancoDados] Erro ao salvar: {e}")

    @staticmethod
    def fazPreCadastro():
        if os.path.exists(ARQUIVO_DADOS):
            try:
                with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    
                    BancoDados.lista_materias = []
                    for m in dados.get("materias", []):
                        notas_objs = [Nota(n['valor'], n['peso']) for n in m.get('notas', [])]
                        semestre_m = m.get('semestre', "1º Semestre")
                        
                        nova_mat = Materia(
                            nome=m['nome'],
                            semestre=semestre_m,
                            carga_horaria=m.get('carga_horaria', 60), 
                            media=m.get('media', 0.0), 
                            faltas=m.get('faltas', 0), 
                            max_faltas=m.get('max_faltas', 15),
                            media_necessaria=m.get('media_necessaria', 7.0),
                            notas=notas_objs
                        )
                        BancoDados.lista_materias.append(nova_mat)
                        
                    BancoDados.lista_semestres = [Semestre(s['nome'], s['situacao']) for s in dados.get("semestres", [])]

                    u = dados.get("usuario", {})
                    BancoDados.info_usuario = Usuario(
                        nome=u.get("nome", "Estudante"),
                        curso=u.get("curso", "Geral"),
                        carga_horaria_total=u.get("carga_horaria_total", 3000),
                        semestres_totais=u.get("semestres_totais", 8),
                        iea=u.get("iea", 0.0),
                        semestres_cursados=u.get("semestres_cursados", 0)
                    )
            except:
                BancoDados._criar_dados_iniciais()
        else:
            BancoDados._criar_dados_iniciais()

    @staticmethod
    def _criar_dados_iniciais():
        BancoDados.lista_materias = []
        BancoDados.lista_semestres = [Semestre("1º Semestre", "Em Andamento")]
        BancoDados.info_usuario = Usuario("Estudante", "Engenharia", 3600, 8)
        BancoDados._salvar_dados()

    # Getters
    @staticmethod
    def get_materias(filtro_semestre=None):
        if filtro_semestre is None: return BancoDados.lista_materias
        return [m for m in BancoDados.lista_materias if m.semestre == filtro_semestre]

    @staticmethod
    def get_materia(nome_materia):
        for m in BancoDados.lista_materias:
            if m.nome == nome_materia: return m
        return None

    @staticmethod
    def get_semestres():
        return BancoDados.lista_semestres

    @staticmethod
    def get_usuario():
        return BancoDados.info_usuario

    # Métodos

    @staticmethod
    def criar_proximo_semestre():
        qtd = len(BancoDados.lista_semestres)
        nome = f"{qtd + 1}º Semestre"
        BancoDados.lista_semestres.append(Semestre(nome, "Não Iniciado"))
        BancoDados._salvar_dados()
        return nome

    @staticmethod
    def deletar_semestre(nome_semestre):
        BancoDados.lista_materias = [m for m in BancoDados.lista_materias if m.semestre != nome_semestre]
        for i, s in enumerate(BancoDados.lista_semestres):
            if s.nome == nome_semestre:
                BancoDados.lista_semestres.pop(i)
                BancoDados._salvar_dados()
                return True
        return False

    @staticmethod
    def atualizar_status_semestre(nome_semestre, novo_status):
        for s in BancoDados.lista_semestres:
            if s.nome == nome_semestre:
                s.situacao = novo_status
                BancoDados._salvar_dados()
                return True
        return False

    @staticmethod
    def adicionar_materia(nome, semestre, carga, max_faltas, media_nec):
        nova = Materia(nome, semestre, carga, 0.0, 0, max_faltas, media_nec)
        BancoDados.lista_materias.append(nova)
        BancoDados._salvar_dados()

    @staticmethod
    def editar_materia(nome_antigo, novo_nome, nova_carga, novo_max_faltas, nova_media_nec):
        for m in BancoDados.lista_materias:
            if m.nome == nome_antigo:
                m.nome = novo_nome
                m.carga_horaria = nova_carga
                m.max_faltas = novo_max_faltas
                m.media_necessaria = nova_media_nec
                BancoDados._salvar_dados()
                return True
        return False
    
    @staticmethod
    def deletar_materia(nome_materia):
        for i, m in enumerate(BancoDados.lista_materias):
            if m.nome == nome_materia:
                BancoDados.lista_materias.pop(i)
                BancoDados._salvar_dados()
                return True
        return False

    @staticmethod
    def adicionar_nota_materia(nome_materia, valor, peso):
        for m in BancoDados.lista_materias:
            if m.nome == nome_materia:
                m.adicionar_nota(Nota(valor, peso))
                BancoDados._salvar_dados()
                return True
        return False

    @staticmethod
    def adicionar_falta_materia(nome_materia, qtd):
        for m in BancoDados.lista_materias:
            if m.nome == nome_materia:
                m.faltas += qtd
                BancoDados._salvar_dados()
                return True
        return False

    @staticmethod
    def salvar_configuracoes_usuario(nome, curso, carga, semestres):
        u = BancoDados.info_usuario
        u.nome = nome
        u.curso = curso
        u.carga_horaria_total = carga
        u.semestres_totais = semestres
        BancoDados._salvar_dados()

    # Cálculo do IEA

    @staticmethod
    def get_materias_aprovadas():
        return [m for m in BancoDados.lista_materias if m.media >= m.media_necessaria]

    @staticmethod
    def calcular_iech(materias: list):
        soma_ponderada = 0.0
        soma_cargas = 0

        for m in materias:
            if m.carga_horaria > 0:
                soma_ponderada += (m.media * m.carga_horaria)
                soma_cargas += m.carga_horaria

        if soma_cargas == 0:
            return 0.0

        iech = soma_ponderada / soma_cargas
        return round(iech, 2)
    
    @staticmethod
    def calcular_iepl():
        usuario = BancoDados.get_usuario()
        total = usuario.semestres_totais
        
        cursados = len([s for s in BancoDados.lista_semestres if s.situacao == "Finalizado"])
        
        if total <= 0:
            return 0.0
        
        iepl = (cursados / total) * 10.0
        
        return round(iepl, 2)
        
    @staticmethod
    def calcular_iea_geral():
        materias_aprovadas = BancoDados.get_materias_aprovadas()
        
        iech = BancoDados.calcular_iech(materias_aprovadas)
        
        iepl = BancoDados.calcular_iepl()
        
        iea_final = (iech + iepl) / 2.0
        
        BancoDados.info_usuario.iea = round(iea_final, 2)
        BancoDados._salvar_dados()
        
        return {
            "IECH": iech,
            "IEPL": iepl, 
            "IEA": round(iea_final, 2)
        }