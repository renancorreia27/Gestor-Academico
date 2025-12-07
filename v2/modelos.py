#Ta sendo usado a def to_dict pra garantir que o json consiga salvar textos mais simples
#to_dict retorna os atributos como dicionario

class Nota:
    def __init__(self, valor: float, peso: float, descricao: str):
        self.valor = valor
        self.peso = peso
        self.descricao = descricao
    
    def to_dict(self):
        return {
            "valor": self.valor,
            "peso": self.peso,
            "descricao": self.descricao
        }

class Falta:
    def __init__(self, quantidade: int, data: str):
        self.quantidade = quantidade
        self.data = data

    def to_dict(self):
        return {
            "quantidade": self.quantidade,
            "data": self.data
        }

class Materia:
    def __init__(self, nome: str, carga_horaria: int, media: float = 0.0, faltas: int = 0, max_faltas: int = 0, notas: list = None):
        self.nome = nome
        self.carga_horaria = carga_horaria # Adicionamos carga horária
        self.media = media
        self.faltas = faltas
        self.max_faltas = max_faltas
        self.notas = notas if notas is not None else [] # Lista de objetos Nota
        
    def calcular_media(self):
        """Calcula a média ponderada da matéria com base nas notas e pesos."""
        soma_pesos = sum(nota.peso for nota in self.notas)
        
        # Evita divisão por zero
        if soma_pesos == 0:
            self.media = 0.0
            return 0.0

        soma_ponderada = sum(nota.valor * nota.peso for nota in self.notas)
        self.media = soma_ponderada / soma_pesos
        return self.media

    def adicionar_nota(self, nota: Nota):
        """Adiciona uma nota e recalcula a média."""
        self.notas.append(nota)
        self.calcular_media()
        
    def to_dict(self):
        notas_dict = [nota.to_dict() for nota in self.notas]
        return {
            "nome": self.nome, 
            "carga_horaria": self.carga_horaria,
            "media": self.media, 
            "faltas": self.faltas, 
            "max": self.max_faltas,
            "notas": notas_dict
        }
class Semestre:
    def __init__(self, nome: str, situacao: str):
        self.nome = nome
        self.situacao = situacao
    
    def to_dict(self):
        return {
            "nome": self.nome,
            "situacao": self.situacao
        }

class Usuario:
    def __init__(self, nome: str, matricula: str, iea: float = 0.0, semestres_totais: int = 8, semestres_cursados: int = 0):
        self.nome = nome
        self.matricula = matricula
        self.iea = iea
        self.semestres_totais = semestres_totais
        self.semestres_cursados = semestres_cursados
    
    def to_dict(self):
        return {
            "nome": self.nome,
            "matricula": self.matricula,
            "iea": self.iea,
            "semestres_totais": self.semestres_totais,
            "semestres_cursados": self.semestres_cursados,
        }