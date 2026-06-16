class Semestre:
    """Entidade de Domínio: Representa um período letivo."""
    def __init__(self, nome: str, situacao: str, id: int = None):
        self.id = id
        self.nome = nome
        self.situacao = situacao
    
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "situacao": self.situacao
        }
