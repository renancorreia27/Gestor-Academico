from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import Qt
from PyQt6 import uic

from banco_dados import BancoDados #para linkar o banco de dados no futuro

class DialogAdicionarNota(QDialog):
    def __init__(self, nome_da_materia):
        super().__init__()
        try:
            uic.loadUi("UI/Dialog - add.nota.ui", self)
        except:
            uic.loadUi("Dialog - add.nota.ui", self)
        
        self.configurar_janela()
        
        # Mostra no título qual matéria está sendo editada
        self.label_card_materia.setText(f"Adicionar Nota para {nome_da_materia}")

        # Botões
        self.btn_salvar.clicked.connect(self.accept) # Fecha e retorna Sucesso (1)
        self.btn_cancelar.clicked.connect(self.reject) # Fecha e retorna Cancelado (0)

    def get_dados(self):
        """ 
        Chame este método para pegar o que o usuário digitou.
        """
        return {
            "nota": self.doubleSpinBox_nota.value(),
            "peso": self.doubleSpinBox_peso_nota.value()
        }
    
    # --- Configuração Visual (Arrastar janela) ---
    def configurar_janela(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.globalPosition().toPoint() - self.drag_pos)
            self.drag_pos = event.globalPosition().toPoint()
            event.accept()


class DialogAdicionarFalta(QDialog):
    def __init__(self, nome_da_materia):
        super().__init__()
        try:
            uic.loadUi("UI/Dialog - add.falta.ui", self)
        except:
            uic.loadUi("Dialog - add.falta.ui", self)
        
        self.configurar_janela()
        self.label_card_falta.setText(f"Adicionar Falta para {nome_da_materia}")

        self.btn_salvar.clicked.connect(self.accept)
        self.btn_cancelar.clicked.connect(self.reject)

    def get_dados(self):
        """ 
        Retorna a quantidade de faltas digitada.
        """
        return {
            "falta": self.spinBox_falta.value()
        }

    # --- Configuração Visual (Arrastar janela) ---
    def configurar_janela(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.globalPosition().toPoint() - self.drag_pos)
            self.drag_pos = event.globalPosition().toPoint()
            event.accept()


class DialogCalcularIEA(QDialog):
    def __init__(self):
        super().__init__()
        try:
            uic.loadUi("UI/Dialog - calcular.iea.ui", self)
        except:
            uic.loadUi("Dialog - calcular.iea.ui", self)

        self.configurar_janela()

        # Botão fechar
        if hasattr(self, 'btn_fechar'): self.btn_fechar.clicked.connect(self.accept)
        elif hasattr(self, 'btn_fechar_iea'): self.btn_fechar_iea.clicked.connect(self.accept)

        # lógica de cálculo, implementar aqui

    # --- Configuração Visual (Arrastar janela) ---
    def configurar_janela(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.globalPosition().toPoint() - self.drag_pos)
            self.drag_pos = event.globalPosition().toPoint()
            event.accept()