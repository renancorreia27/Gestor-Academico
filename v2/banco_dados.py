import json
from modelos import Usuario, Semestre, Materia, Nota, Falta 
import os 

ARQUIVO_DADOS = "dados_sistema.json"
MEDIA_MINIMA_APROVACAO = 7.0

class BancoDados:
    # Listas para OBJETOS (Materia, Semestre)
    lista_materias = []
    lista_semestres = []
    
    # Atributo para armazenar as informações do usuário
    info_usuario = Usuario(nome="Usuário Padrão", matricula="000000", semestres_totais=8)


    @staticmethod
    def _salvar_dados():
        """ Salva a lista de objetos Materia, Semestre e o objeto Usuario no arquivo JSON. """
        
        # Converte os objetos para dicionários
        dados_a_salvar = {
            "materias": [materia.to_dict() for materia in BancoDados.lista_materias],
            "semestres": [semestre.to_dict() for semestre in BancoDados.lista_semestres],
            "usuario": BancoDados.info_usuario.to_dict() # Salva dados do usuário
        }
        
        with open(ARQUIVO_DADOS, 'w') as f:
            json.dump(dados_a_salvar, f, indent=4)
        print(f"[BancoDados] Dados salvos em '{ARQUIVO_DADOS}'.")

    @staticmethod
    def fazPreCadastro():
        """ Tenta carregar dados do arquivo JSON. Se não existir, usa o pré-cadastro inicial. """
        if os.path.exists(ARQUIVO_DADOS):
            try:
                with open(ARQUIVO_DADOS, 'r') as f:
                    dados = json.load(f)
                    print(f"[BancoDados] Dados carregados do arquivo '{ARQUIVO_DADOS}'.")
                    
                    # Carrega Matérias
                    materias_dicts = dados.get("materias", [])
                    BancoDados.lista_materias = []
                    for m in materias_dicts:
                        notas_objetos = [Nota(n['valor'], n['peso'], n['descricao']) for n in m.get('notas', [])]
                        materia = Materia(
                            nome=m['nome'], 
                            carga_horaria=m['carga_horaria'], 
                            media=m.get('media', 0.0), 
                            faltas=m.get('faltas', 0), 
                            max_faltas=m.get('max', 0),
                            notas=notas_objetos
                        )
                        BancoDados.lista_materias.append(materia)
                        
                    # Carrega Semestres
                    semestres_dicts = dados.get("semestres", [])
                    BancoDados.lista_semestres = [
                        Semestre(s['nome'], s['situacao']) for s in semestres_dicts
                    ]

                    # Carrega Usuário (Dados IEPL)
                    usuario_dict = dados.get("usuario")
                    if usuario_dict:
                        BancoDados.info_usuario = Usuario(
                            nome=usuario_dict.get("nome", "Usuário Padrão"),
                            matricula=usuario_dict.get("matricula", "000000"),
                            iea=usuario_dict.get("iea", 0.0),
                            semestres_totais=usuario_dict.get("semestres_totais", 8),
                            semestres_cursados=usuario_dict.get("semestres_cursados", 0)
                        )
                    
            except Exception as e:
                print(f"[BancoDados] ERRO ao carregar JSON: {e}. Usando pré-cadastro padrão.")
                BancoDados._criar_dados_iniciais()
        else:
            BancoDados._criar_dados_iniciais()

    @staticmethod
    def _criar_dados_iniciais():
        """ Cria dados padrão se o JSON não existir. """
        print("[BancoDados] Realizando pré-cadastro de dados iniciais...")
        
        # Dados Padrão de Matérias
        BancoDados.lista_materias = [
            Materia(nome="Engenharia de Software", carga_horaria=80, media=10.0, faltas=0, max_faltas=20),
            Materia(nome="Banco de Dados", carga_horaria=80, media=7.5, faltas=4, max_faltas=20),
            Materia(nome="Inteligência Artificial", carga_horaria=60, media=8.0, faltas=2, max_faltas=15),
        ]
        
        # Dados Padrão de Semestres
        BancoDados.lista_semestres = [
            Semestre(nome="1º Semestre", situacao="Finalizado"),
            Semestre(nome="2º Semestre", situacao="Em Andamento"),          
        ]
        
        # Dados iniciais do usuário para cálculo do IEPL
        BancoDados.info_usuario = Usuario(
            nome="Aluno Padrão", 
            matricula="2024-1", 
            semestres_totais=8, 
            semestres_cursados=1 
        )
        
        BancoDados._salvar_dados() 
        print("[BancoDados] Dados padrão criados com sucesso!")


    @staticmethod
    def get_materias():
        return BancoDados.lista_materias

    @staticmethod
    def get_semestres():
        return BancoDados.lista_semestres

    @staticmethod
    def get_usuario():
        """ Retorna o objeto Usuario. """
        return BancoDados.info_usuario

    @staticmethod
    def adicionar_materia(nome, carga, max_faltas):
        """ Cria um novo objeto Materia com max_faltas fornecido pelo usuário e o salva no banco. """
        
        
        # O valor de max_faltas já vem do usuário.
        nova = Materia(nome=nome, carga_horaria=carga, max_faltas=max_faltas)
        
        BancoDados.lista_materias.append(nova)
        BancoDados._salvar_dados() 
        print(f"[BancoDados] Matéria '{nome}' salva. Máx. Faltas definido pelo usuário: {max_faltas}")

    @staticmethod
    def deletar_materia(nome_materia: str):
        """ Remove uma matéria da lista e salva. """
        materia_alvo = None
        for i, m in enumerate(BancoDados.lista_materias):
            if m.nome == nome_materia:
                materia_alvo = m
                BancoDados.lista_materias.pop(i)
                break

        if materia_alvo:
            BancoDados._salvar_dados()
            print(f"[BancoDados] Matéria '{nome_materia}' deletada com sucesso.")
            return True
        else:
            print(f"[BancoDados] ERRO: Matéria '{nome_materia}' não encontrada para deletar.")
            return False

    @staticmethod
    def adicionar_nota_materia(nome_materia: str, valor: float, peso: float, descricao: str = "Avaliação Padrão"):
        """ Adiciona uma nota à matéria, recalcula a média e salva. """
        materia_alvo = None
        for m in BancoDados.lista_materias:
            if m.nome == nome_materia:
                materia_alvo = m
                break
        
        if materia_alvo:
            nova_nota = Nota(valor, peso, descricao)
            materia_alvo.adicionar_nota(nova_nota) 
            BancoDados._salvar_dados()
            print(f"[BancoDados] Nota {valor} (Peso {peso}) adicionada a '{nome_materia}'. Nova média: {materia_alvo.media:.2f}")
            return True
        else:
            print(f"[BancoDados] ERRO: Matéria '{nome_materia}' não encontrada.")
            return False
            
    @staticmethod
    def adicionar_falta_materia(nome_materia: str, quantidade: int, data: str):
        """ Adiciona faltas à matéria e salva. """
        materia_alvo = None
        for m in BancoDados.lista_materias:
            if m.nome == nome_materia:
                materia_alvo = m
                break

        if materia_alvo:
            materia_alvo.faltas += quantidade
            BancoDados._salvar_dados()
            print(f"[BancoDados] {quantidade} falta(s) adicionada(s) a '{nome_materia}' em {data}. Total de faltas: {materia_alvo.faltas}")
            return True
        else:
            print(f"[BancoDados] ERRO: Matéria '{nome_materia}' não encontrada.")
            return False

    @staticmethod
    def atualizar_status_semestre(nome_semestre: str, novo_status: str):
        """ Altera a situação de um semestre específico e salva no JSON. """
        
        semestre_alvo = None
        for s in BancoDados.lista_semestres:
            if s.nome == nome_semestre:
                semestre_alvo = s
                break

        if semestre_alvo:
            semestre_alvo.situacao = novo_status
            BancoDados._salvar_dados()
            print(f"[BancoDados] Status do semestre '{nome_semestre}' atualizado para: {novo_status}")
            return True
        else:
            print(f"[BancoDados] ERRO: Semestre '{nome_semestre}' não encontrado.")
            return False

    @staticmethod
    def get_materias_aprovadas(media_minima=MEDIA_MINIMA_APROVACAO):
        """ Filtra e retorna apenas as matérias onde a média é igual ou superior à média mínima. """
        return [materia for materia in BancoDados.lista_materias if materia.media >= media_minima]

    @staticmethod
    def calcular_iech(materias: list):
        """ Calcula o Índice de Eficiência em Carga Horária (IECH). """
        
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
        """ Calcula o Índice de Eficiência em Prazo Legal (IEPL). """
        
        usuario = BancoDados.get_usuario()
        total = usuario.semestres_totais
        cursados = usuario.semestres_cursados
        
        if total <= 0:
            return 0.0
        
        # IEPL = (Semestres Cursados / Semestres Totais) * 10
        iepl = (cursados / total) * 10.0
        
        return round(iepl, 2)
        
    @staticmethod
    def calcular_iea_geral():
        """ Calcula o IEA Geral (IECH, IEPL, IEA). """
        materias_aprovadas = BancoDados.get_materias_aprovadas(media_minima=MEDIA_MINIMA_APROVACAO)
        
        # 1. Calcula o IECH
        iech = BancoDados.calcular_iech(materias_aprovadas)
        
        # 2. Calcula o IEPL (Agora dinâmico)
        iepl = BancoDados.calcular_iepl()
        
        # 3. Calcula o IEA Final (Média entre Desempenho e Prazo)
        iea_final = (iech + iepl) / 2.0
        
        # Atualiza o IEA no objeto usuário para ser salvo
        BancoDados.info_usuario.iea = round(iea_final, 2)
        BancoDados._salvar_dados()
        
        return {
            "IECH": iech,
            "IEPL": iepl, 
            "IEA": round(iea_final, 2)
        }