class Nota:
    """Entidade de Domínio: Representa uma avaliação individual e seu peso."""
    def __init__(self, valor: float, peso: float, id: int = None, materia_id: int = None):
        self.id = id
        self.materia_id = materia_id
        self.valor = valor
        self.peso = peso
    
    def to_dict(self):
        return {
            "id": self.id,
            "materia_id": self.materia_id,
            "valor": self.valor,
            "peso": self.peso
        }
