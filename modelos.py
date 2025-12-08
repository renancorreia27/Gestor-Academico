class Nota:
    def __init__(self, valor: float, peso: float, descricao: str):
        self.valor = valor
        self.peso = peso
        self.descricao = descricao
    
    def to_dict(self):
        return {"valor": self.valor, "peso": self.peso, "descricao": self.descricao}

class Falta:
    def __init__(self, quantidade: int, data: str):
        self.quantidade = quantidade
        self.data = data

    def to_dict(self):
        return {"quantidade": self.quantidade, "data": self.data}

class Materia:
    def __init__(self, nome: str, semestre: str, carga_horaria: int, media: float = 0.0, faltas: int = 0, max_faltas: int = 0, media_necessaria: float = 7.0, notas: list = None):
        self.nome = nome
        self.semestre = semestre
        self.carga_horaria = carga_horaria
        self.media = media
        self.faltas = faltas
        self.max_faltas = max_faltas
        self.media_necessaria = media_necessaria
        self.notas = notas if notas is not None else []
        
    def calcular_media(self):
        soma_pesos = sum(nota.peso for nota in self.notas)
        if soma_pesos == 0:
            self.media = 0.0
            return 0.0
        soma_ponderada = sum(nota.valor * nota.peso for nota in self.notas)
        self.media = soma_ponderada / soma_pesos
        return self.media

    def adicionar_nota(self, nota: Nota):
        self.notas.append(nota)
        self.calcular_media()
        
    def to_dict(self):
        return {
            "nome": self.nome, 
            "semestre": self.semestre,
            "carga_horaria": self.carga_horaria,
            "media": self.media, 
            "faltas": self.faltas, 
            "max_faltas": self.max_faltas,
            "media_necessaria": self.media_necessaria,
            "notas": [n.to_dict() for n in self.notas]
        }

class Semestre:
    def __init__(self, nome: str, situacao: str):
        self.nome = nome
        self.situacao = situacao
    
    def to_dict(self):
        return {"nome": self.nome, "situacao": self.situacao}

class Usuario:
    def __init__(self, nome: str, curso: str, carga_horaria_total: int, semestres_totais: int, iea: float = 0.0, semestres_cursados: int = 0):
        self.nome = nome
        self.curso = curso
        self.carga_horaria_total = carga_horaria_total
        self.semestres_totais = semestres_totais
        self.iea = iea
        self.semestres_cursados = semestres_cursados
    
    def to_dict(self):
        return {
            "nome": self.nome,
            "curso": self.curso,
            "carga_horaria_total": self.carga_horaria_total,
            "semestres_totais": self.semestres_totais,
            "iea": self.iea,
            "semestres_cursados": self.semestres_cursados,
        }