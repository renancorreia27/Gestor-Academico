from .nota import Nota

class Materia:
    """Entidade de Domínio: Representa uma disciplina cursada."""
    def __init__(self, nome: str, semestre: str, carga_horaria: int, media: float = 0.0, faltas: int = 0, max_faltas: int = 0, media_necessaria: float = 7.0, notas: list = None, id: int = None, semestre_id: int = None):
        self.id = id
        self.semestre_id = semestre_id
        self.nome = nome
        self.semestre = semestre
        self.carga_horaria = carga_horaria
        self.media = media
        self.faltas = faltas
        self.max_faltas = max_faltas
        self.media_necessaria = media_necessaria
        self.notas = notas if notas is not None else []
        
    def calcular_media(self) -> float:
        soma_pesos = sum(nota.peso for nota in self.notas)
        if soma_pesos == 0:
            self.media = 0.0
            return 0.0
        soma_ponderada = sum(nota.valor * nota.peso for nota in self.notas)
        self.media = round(soma_ponderada / soma_pesos, 2)
        return self.media

    def adicionar_nota(self, nota: Nota):
        self.notas.append(nota)
        self.calcular_media()
        
    def to_dict(self):
        return {
            "id": self.id,
            "semestre_id": self.semestre_id,
            "nome": self.nome, 
            "semestre": self.semestre,
            "carga_horaria": self.carga_horaria,
            "media": self.media, 
            "faltas": self.faltas, 
            "max_faltas": self.max_faltas,
            "media_necessaria": self.media_necessaria,
            "notas": [n.to_dict() for n in self.notas]
        }
