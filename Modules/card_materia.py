from PyQt6.QtWidgets import QWidget
from PyQt6 import uic
from .janelas_extras import DialogAdicionarNota
from .janelas_extras import DialogAdicionarFalta

from banco_dados import BancoDados #para linkar o banco de dados no futuro

class CardMateria(QWidget):
    def __init__(self, nome_materia, media, faltas, faltas_max):
        super().__init__()
        try:
            uic.loadUi("UI/Widget - card.materia.ui", self)
        except:
            uic.loadUi("Widget - card.materia.ui", self)

        self.nome_materia_atual = nome_materia
        
        # Preenchimento visual
        self.label_card_materia.setText(nome_materia)
        self.label_media.setText(str(media))
        self.label_faltas.setText(f"Faltas: {faltas}/{faltas_max}")

        # Barras de Progresso
        self.progressBar_media.setMaximum(100) 
        self.progressBar_media.setValue(int(float(media) * 10)) # Ex: 7.5 vira 75%

        self.progressBar_falta.setMaximum(faltas_max)
        self.progressBar_falta.setValue(faltas)

        # Botões
        self.btn_add_nota.clicked.connect(self.clicar_add_nota)
        self.btn_add_falta.clicked.connect(self.clicar_add_falta)

    def clicar_add_nota(self):
        """ Abre modal de notas e envia para o backend """
        dialog = DialogAdicionarNota(self.nome_materia_atual)
        
        if dialog.exec(): # Se o usuário clicou em Salvar
            dados = dialog.get_dados()
            nota = dados["nota"]
            peso = dados["peso"]

            # Lógica de Persistência
            print(f"[BACKEND] Inserir Nota -> Matéria: {self.nome_materia_atual} | Nota: {nota} | Peso: {peso}")
            # Sugestão: Após salvar, recalcular a média da matéria e atualizar a tela

    def clicar_add_falta(self):
        """ Abre modal de faltas e envia para o backend """
        dialog = DialogAdicionarFalta(self.nome_materia_atual)
        
        if dialog.exec():
            dados = dialog.get_dados()
            qtd_faltas = dados["falta"]
            
            # Lógica de Persistência
            print(f"[BACKEND] Somar Faltas -> Matéria: {self.nome_materia_atual} | +{qtd_faltas} faltas")