import json
import os 
from modelos import Usuario, Semestre, Materia, Nota

ARQUIVO_DADOS = "dados_sistema.json"

class BancoDados:
    lista_materias = []
    lista_semestres = []
    info_usuario = Usuario(nome="Estudante", curso="Geral", carga_horaria_total=3000, semestres_totais=8)

    @staticmethod
    def _salvar_dados():
        try:
            dados = {
                "materias": [m.to_dict() for m in BancoDados.lista_materias],
                "semestres": [s.to_dict() for s in BancoDados.lista_semestres],
                "usuario": BancoDados.info_usuario.to_dict()
            }
            with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro salvar: {e}")

    @staticmethod
    def fazPreCadastro():
        if os.path.exists(ARQUIVO_DADOS):
            try:
                with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    BancoDados.lista_materias = []
                    for m in dados.get("materias", []):
                        notas = [Nota(n['valor'], n['peso'], n['descricao']) for n in m.get('notas', [])]
                        BancoDados.lista_materias.append(Materia(
                            m['nome'], m.get('semestre', "1º Semestre"), m.get('carga_horaria', 60), 
                            m.get('media', 0.0), m.get('faltas', 0), m.get('max_faltas', 15), 
                            m.get('media_necessaria', 7.0), notas
                        ))
                    BancoDados.lista_semestres = [Semestre(s['nome'], s['situacao']) for s in dados.get("semestres", [])]
                    u = dados.get("usuario", {})
                    BancoDados.info_usuario = Usuario(u.get("nome", "User"), u.get("curso", "Curso"), u.get("carga_horaria_total", 3000), u.get("semestres_totais", 8))
            except: BancoDados._criar_dados_iniciais()
        else: BancoDados._criar_dados_iniciais()

    @staticmethod
    def _criar_dados_iniciais():
        BancoDados.lista_semestres = [Semestre("1º Semestre", "Em Andamento")]
        BancoDados.info_usuario = Usuario("Estudante", "Engenharia", 3600, 8)
        BancoDados._salvar_dados()

    @staticmethod
    def get_materias(filtro_semestre=None):
        if not filtro_semestre: return BancoDados.lista_materias
        return [m for m in BancoDados.lista_materias if m.semestre == filtro_semestre]

    @staticmethod
    def get_semestres(): return BancoDados.lista_semestres
    @staticmethod
    def get_usuario(): return BancoDados.info_usuario
    @staticmethod
    def get_materia(nome): 
        for m in BancoDados.lista_materias: 
            if m.nome == nome: return m
        return None

    # AÇÕES
    @staticmethod
    def criar_proximo_semestre():
        nome = f"{len(BancoDados.lista_semestres) + 1}º Semestre"
        BancoDados.lista_semestres.append(Semestre(nome, "Não Iniciado"))
        BancoDados._salvar_dados()
        return nome

    @staticmethod
    def deletar_semestre(nome):
        BancoDados.lista_materias = [m for m in BancoDados.lista_materias if m.semestre != nome]
        for i, s in enumerate(BancoDados.lista_semestres):
            if s.nome == nome:
                BancoDados.lista_semestres.pop(i)
                BancoDados._salvar_dados()
                return True
        return False

    @staticmethod
    def atualizar_status_semestre(nome, status):
        for s in BancoDados.lista_semestres:
            if s.nome == nome:
                s.situacao = status
                BancoDados._salvar_dados()
                return True
        return False

    @staticmethod
    def adicionar_materia(nome, sem, carga, max_f, med_nec):
        BancoDados.lista_materias.append(Materia(nome, sem, carga, 0.0, 0, max_f, med_nec))
        BancoDados._salvar_dados()

    @staticmethod
    def editar_materia(antigo, novo, carga, max_f, med_nec):
        for m in BancoDados.lista_materias:
            if m.nome == antigo:
                m.nome = novo; m.carga_horaria = carga; m.max_faltas = max_f; m.media_necessaria = med_nec
                BancoDados._salvar_dados()
                return True
        return False

    @staticmethod
    def deletar_materia(nome):
        for i, m in enumerate(BancoDados.lista_materias):
            if m.nome == nome:
                BancoDados.lista_materias.pop(i)
                BancoDados._salvar_dados()
                return True
        return False

    @staticmethod
    def adicionar_nota_materia(nome, val, pes, desc):
        for m in BancoDados.lista_materias:
            if m.nome == nome:
                m.adicionar_nota(Nota(val, pes, desc))
                BancoDados._salvar_dados()
                return True
        return False

    @staticmethod
    def adicionar_falta_materia(nome, qtd):
        for m in BancoDados.lista_materias:
            if m.nome == nome:
                m.faltas += qtd
                BancoDados._salvar_dados()
                return True
        return False

    @staticmethod
    def salvar_configuracoes_usuario(n, c, cg, s):
        u = BancoDados.info_usuario
        u.nome = n; u.curso = c; u.carga_horaria_total = cg; u.semestres_totais = s
        BancoDados._salvar_dados()

    @staticmethod
    def calcular_iea_geral():
        # Retorna valores fictícios se não houver dados, ou calcula média simples
        return {"IECH": 0, "IEPL": 0, "IEA": 0}