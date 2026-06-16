class Usuario:
    """Entidade de Domínio: Representa o aluno e suas configurações acadêmicas globais."""
    def __init__(self, nome: str, curso: str, carga_horaria_total: int, semestres_totais: int, ira: float = 0.0, semestres_cursados: int = 0, id: int = None):
        self.id = id
        self.nome = nome
        self.curso = curso
        self.carga_horaria_total = carga_horaria_total
        self.semestres_totais = semestres_totais
        self.ira = ira
        self.semestres_cursados = semestres_cursados
    
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "curso": self.curso,
            "carga_horaria_total": self.carga_horaria_total,
            "semestres_totais": self.semestres_totais,
            "ira": self.ira,
            "semestres_cursados": self.semestres_cursados,
        }
