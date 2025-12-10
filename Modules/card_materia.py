from PyQt6.QtWidgets import QWidget, QPushButton
from PyQt6 import uic
from .janelas_extras import DialogAdicionarNota, DialogAdicionarFalta, DialogConfirmarExclusao
from banco_dados import BancoDados 

import sys
import os
"""Função que permite que as pastas sejam acessiveis pelo executável"""
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class CardMateria(QWidget):
    """Widget responsável por exibir média, notas, faltas, barras de progresso etc."""
    def __init__(self, nome_materia, media, faltas, faltas_max, media_necessaria, parent_window):
        
        super().__init__()
        try:
            uic.loadUi(resource_path("UI/Widget - card.materia.ui"), self)
        except:
            uic.loadUi("Widget - card.materia.ui", self)

        self.nome_materia_atual = nome_materia
        self.parent_window = parent_window
        
        # Visual
        self.label_card_materia.setText(nome_materia)
        self.label_media.setText(f"{media:.1f}") 
        self.label_faltas.setText(f"{faltas}/{faltas_max}")

        # Barras de progressão
        self.progressBar_media.setValue(int(media * 10))
        if media >= media_necessaria:
            self.progressBar_media.setStyleSheet("QProgressBar::chunk { background-color: #2ecc71; }")
            self.progressBar_media.setToolTip(f"Aprovado! Meta: {media_necessaria}")
        else:
            self.progressBar_media.setStyleSheet("QProgressBar::chunk { background-color: #f1c40f; }")
            self.progressBar_media.setToolTip(f"Meta: {media_necessaria}")

        self.progressBar_falta.setMaximum(faltas_max)
        self.progressBar_falta.setValue(faltas)
        if faltas > faltas_max:
            self.progressBar_falta.setValue(faltas_max)

        #Conexões de botão
        self.btn_add_nota.clicked.connect(self.clicar_add_nota)
        self.btn_add_falta.clicked.connect(self.clicar_add_falta)
        
        if hasattr(self, 'btn_delete_materia'):
            self.btn_delete_materia.clicked.connect(self.clicar_remover_materia)

        if hasattr(self, 'btn_editar'):
            self.btn_editar.clicked.connect(self.clicar_editar_materia)

    def clicar_add_nota(self):
        """Abre uma caixa de diálogo pro usuário adicionar nota"""
        dialog = DialogAdicionarNota(self.nome_materia_atual)
        if dialog.exec():
            d = dialog.get_dados()
            if BancoDados.adicionar_nota_materia(self.nome_materia_atual, d["nota"], d["peso"]):
                self.parent_window.recarregar_dashboard() 

    def clicar_add_falta(self):
        """Abre uma caixa de diálogo pro usuário adicionar falta"""
        dialog = DialogAdicionarFalta(self.nome_materia_atual)
        if dialog.exec():
            d = dialog.get_dados()
            if BancoDados.adicionar_falta_materia(self.nome_materia_atual, d["falta"]):
                self.parent_window.recarregar_dashboard()
                
    def clicar_remover_materia(self):
        """Abre uma caixa de diálogo pro usuário remover a matéria"""
        dialog = DialogConfirmarExclusao(self.nome_materia_atual)
        if dialog.exec():
            if BancoDados.deletar_materia(self.nome_materia_atual):
                self.deleteLater() 
                self.parent_window.recarregar_dashboard()

    def clicar_editar_materia(self):
        """Abre na janela principal a tela de edição de dados"""
        self.parent_window.abrir_tela_edicao(self.nome_materia_atual)