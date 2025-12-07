from PyQt6.QtWidgets import QWidget
from PyQt6 import uic

from banco_dados import BancoDados 

class CardSemestre(QWidget):
    def __init__(self, nome_semestre, situacao):
        super().__init__()
        try:
            uic.loadUi("UI/Widget - card.semestre.ui", self)
        except:
            uic.loadUi("Widget - card.semestre.ui", self)

        self.setMinimumHeight(142)
        self.nome = nome_semestre # Armazena o nome para o backend
        
        # Preenche dados
        self.label_nome.setText(nome_semestre)
        self.atualizar_interface(situacao) # Configura botões e cores iniciais

        # Conecta botões aos novos métodos de backend
        self.btn_iniciar_semestre.clicked.connect(self.marcar_em_andamento)
        self.btn_finaliza_semestre.clicked.connect(self.marcar_finalizado)

    def marcar_em_andamento(self):
        """ Ação do botão Iniciar: Atualiza o backend e o visual. """
        # Chama a função de atualização no banco de dados
        if BancoDados.atualizar_status_semestre(self.nome, "Em Andamento"):
            self.atualizar_interface("Em Andamento")

    def marcar_finalizado(self):
        """ Ação do botão Finalizar: Atualiza o backend e o visual. """
        # Chama a função de atualização no banco de dados
        if BancoDados.atualizar_status_semestre(self.nome, "Finalizado"):
            self.atualizar_interface("Finalizado")

    def atualizar_interface(self, situacao):
        """ Lógica visual (Esconde botões e muda cor) """
        self.label_situacao.setText(situacao)
        
        # Controle de visibilidade dos botões e cores
        if situacao == "Em Andamento":
            self.btn_iniciar_semestre.hide()
            self.btn_finaliza_semestre.show()
            self.label_situacao.setStyleSheet("color: #f1c40f; font-weight: bold;") # Amarelo
            
        elif situacao == "Finalizado":
            self.btn_iniciar_semestre.hide() 
            self.btn_finaliza_semestre.hide()
            self.label_situacao.setStyleSheet("color: #2ecc71; font-weight: bold;") # Verde

        else: # Futuro / Não iniciado
            self.btn_finaliza_semestre.hide()   
            self.btn_iniciar_semestre.show()
            self.label_situacao.setStyleSheet("color: #7f8c8d; font-weight: bold;") # Cinza