from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import Qt
from PyQt6 import uic

from banco_dados import BancoDados

class DialogCalcularIEA(QDialog):
    def __init__(self):
        super().__init__()
        try:
            uic.loadUi("UI/Dialog - calcular.iea.ui", self)
        except:
            uic.loadUi("Dialog - calcular.iea.ui", self)

        self.configurar_janela()

        # Botão de Fechar
        if hasattr(self, 'btn_fechar'): self.btn_fechar.clicked.connect(self.accept)
        elif hasattr(self, 'btn_fechar_iea'): self.btn_fechar_iea.clicked.connect(self.accept)

        # Botão de Calcular (Gatilho para o Backend)
        if hasattr(self, 'btn_calcular'): 
            self.btn_calcular.clicked.connect(self.realizar_calculo)

    def realizar_calculo(self):
        """
        Lógica Principal do Backend:
        1. Buscar notas, faltas e carga horária de todas as matérias no Banco.
        2. Aplicar a fórmula do IEA.
        3. Atualizar o label na tela com o resultado.
        """
        print("[BACKEND] Buscando dados de todas as matérias e calculando IEA...")
        
        # Exemplo: Atualiza um label com o resultado (se existir na interface)
        if hasattr(self, 'label_resultado_iea'):
            self.label_resultado_iea.setText("7.8")

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