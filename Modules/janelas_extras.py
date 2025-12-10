from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFormLayout, QLineEdit, QSpinBox, 
                             QDoubleSpinBox, QDialogButtonBox)
from PyQt6.QtCore import Qt, QDate
from PyQt6 import uic
from banco_dados import BancoDados 



class DialogAdicionarNota(QDialog):
    """Diálogo para registrar nova nota incluindo seu valor e peso em uma matéria"""
    def __init__(self, nome_da_materia):
        super().__init__()
        try:
            uic.loadUi("UI/Dialog - add.nota.ui", self)
        except:
            try:
                uic.loadUi("Dialog - add.nota.ui", self)
            except:
                print("ERRO: Arquivo UI de nota não encontrado.")
        
        self.configurar_janela()
        if hasattr(self, 'label_card_materia'):
            self.label_card_materia.setText(f"Nota: {nome_da_materia}")
            
        self.btn_salvar.clicked.connect(self.accept) 
        self.btn_cancelar.clicked.connect(self.reject) 

    def get_dados(self):
        """Retorna valor e peso da nota"""
        desc = self.lineEdit_descricao.text() if hasattr(self, 'lineEdit_descricao') else "Avaliação"
        if not desc: desc = "Avaliação"
        
        return {
            "nota": self.doubleSpinBox_nota.value(),
            "peso": self.doubleSpinBox_peso_nota.value(),
            "descricao": desc
        }
    
    def configurar_janela(self):
        """Aplica config visuais nos frames"""
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

class DialogAdicionarFalta(QDialog):
    """Diálogo para registrar faltas incluindo sua quantidade uma matéria"""
    def __init__(self, nome_da_materia):
        super().__init__()
        try:
            uic.loadUi("UI/Dialog - add.falta.ui", self)
        except:
             try:
                uic.loadUi("Dialog - add.falta.ui", self)
             except:
                print("ERRO: Arquivo UI de falta não encontrado.")
        
        self.configurar_janela()
        if hasattr(self, 'label_card_falta'):
            self.label_card_falta.setText(f"Falta: {nome_da_materia}")

        if hasattr(self, 'dateEdit_data_falta'):
             self.dateEdit_data_falta.setDate(QDate.currentDate())
             
        self.btn_salvar.clicked.connect(self.accept) 
        self.btn_cancelar.clicked.connect(self.reject) 

    def get_dados(self):
        """Retorna os dados como faltas e data"""
        data_str = QDate.currentDate().toString("yyyy-MM-dd")
        if hasattr(self, 'dateEdit_data_falta'):
            data_str = self.dateEdit_data_falta.date().toString("yyyy-MM-dd")
            
        return {
            "falta": self.spinBox_falta.value(), 
            "data": data_str
        }

    def configurar_janela(self):
        """Aplica config visuais nos frames"""
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)


class DialogCalcularIEA(QDialog):
    """Dialógo para exibir os resultados do cálculo de IEA, IECH e IEPL"""
    def __init__(self):
        super().__init__()
        try:
            uic.loadUi("UI/Dialog - calcular.iea.ui", self)
        except:
             try:
                uic.loadUi("Dialog - calcular.iea.ui", self)
             except:
                 pass

        self.configurar_janela()
        
        if hasattr(self, 'btn_fechar'): self.btn_fechar.clicked.connect(self.accept)
        elif hasattr(self, 'btn_fechar_iea'): self.btn_fechar_iea.clicked.connect(self.accept)
        
        if hasattr(self, 'btn_calcular'): 
            self.btn_calcular.clicked.connect(self.realizar_calculo) 
            
        self.realizar_calculo()

    def realizar_calculo(self):
        """Chama a função feita la no banco_dados para receber e mostrar o resultado"""
        resultados = BancoDados.calcular_iea_geral()
        if hasattr(self, 'label_iech'): self.label_iech.setText(f"IECH = {resultados['IECH']:.2f}")
        if hasattr(self, 'label_iepl'): self.label_iepl.setText(f"IEPL = {resultados['IEPL']:.2f}")
        
        texto_iea = f"IEA = {resultados['IEA']:.2f}"
        if hasattr(self, 'label_iea_resultado'): self.label_iea_resultado.setText(texto_iea)
        elif hasattr(self, 'label_iea'): self.label_iea.setText(texto_iea)

    def configurar_janela(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)


class DialogConfirmarExclusao(QDialog):
    """Diálogo para confirmar a exclusão de um elemento"""
    def __init__(self, item_nome):
        super().__init__()
        self.setWindowTitle("Confirmar Exclusão")
        self.setFixedWidth(350)
        self.setStyleSheet("""
            QDialog { background-color: #f0f0f0; border-radius: 10px; border: 2px solid #bdc3c7; }
            QLabel { font-size: 14px; color: #333; font-weight: bold; }
            QPushButton { border-radius: 5px; padding: 8px; font-weight: bold; }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        self.label_mensagem = QLabel(f"Tem certeza que deseja excluir permanentemente:\n'{item_nome}'?")
        self.label_mensagem.setWordWrap(True)
        self.label_mensagem.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_mensagem)
        
        hbox = QHBoxLayout()
        
        self.btn_confirmar = QPushButton("Sim, Excluir")
        self.btn_confirmar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_confirmar.setStyleSheet("background-color: #e74c3c; color: white;")
        
        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_cancelar.setStyleSheet("background-color: #95a5a6; color: white;")
        
        hbox.addWidget(self.btn_confirmar)
        hbox.addWidget(self.btn_cancelar)
        
        layout.addLayout(hbox)

        self.btn_confirmar.clicked.connect(self.accept)
        self.btn_cancelar.clicked.connect(self.reject)
        
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

    def get_dados(self):
        return {
            "nome": self.input_nome.text(),
            "carga": self.input_carga.value(),
            "max_faltas": self.input_faltas.value(),
            "media_nec": self.input_media.value()
        }