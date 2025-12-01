from modelos import Usuario, Semestre, Materia #importei para no futuro utilizarmos no banco de dados

class BancoDados:
    # Listas em memória para simular o banco
    # Depois vamos usar JSON
    lista_materias = []
    lista_semestres = []

    def fazPreCadastro():
        """ Simula o carregamento inicial de dados"""
        print("[BancoDados] Realizando pré-cadastro de dados...")
        
        # Simulando Matérias cadastradas
        BancoDados.lista_materias = [
            {"nome": "Engenharia de Software", "media": 10.0, "faltas": 0, "max": 20},
            {"nome": "Banco de Dados", "media": 7.5, "faltas": 4, "max": 20},
            {"nome": "Inteligência Artificial", "media": 8.0, "faltas": 2, "max": 15},
        ]

        # Simulando Semestres cadastrados
        BancoDados.lista_semestres = [
            {"nome": "1º Semestre", "situacao": "Finalizado"},
            {"nome": "2º Semestre", "situacao": "Em Andamento"},          
        ]
        
        print("[BancoDados] Dados carregados com sucesso!")

    def get_materias():
        return BancoDados.lista_materias

    def get_semestres():
        return BancoDados.lista_semestres

    def adicionar_materia(nome, carga):
        # Aqui futuramente conectamos com o JSON
        nova = {"nome": nome, "media": 0.0, "faltas": 0, "max": 20}
        BancoDados.lista_materias.append(nova)
        print(f"[BancoDados] Matéria '{nome}' salva com sucesso.")

#adicionar demais metodos de get e set 