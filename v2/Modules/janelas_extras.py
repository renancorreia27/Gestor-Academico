from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, QDate
from PyQt6 import uic

from banco_dados import BancoDados 

class DialogAdicionarNota(QDialog):
    def __init__(self, nome_da_materia):
        super().__init__()
        try:
            uic.loadUi("UI/Dialog - add.nota.ui", self)
        except:
            uic.loadUi("Dialog - add.nota.ui", self)
        
        self.configurar_janela()
        self.label_card_materia.setText(f"Adicionar Nota para {nome_da_materia}")
        self.btn_salvar.clicked.connect(self.accept) 
        self.btn_cancelar.clicked.connect(self.reject) 

    def get_dados(self):
        return {
            "nota": self.doubleSpinBox_nota.value(),
            "peso": self.doubleSpinBox_peso_nota.value(),
            "descricao": getattr(self, 'lineEdit_descricao', None).text() if hasattr(self, 'lineEdit_descricao') else "Avaliação"
        }
    
    def configurar_janela(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

class DialogAdicionarFalta(QDialog):
    def __init__(self, nome_da_materia):
        super().__init__()
        try:
            uic.loadUi("UI/Dialog - add.falta.ui", self)
        except:
            uic.loadUi("Dialog - add.falta.ui", self)
        
        self.configurar_janela()
        
        if hasattr(self, 'label_card_falta'):
            self.label_card_falta.setText(f"Adicionar Falta para {nome_da_materia}")
        else:
            self.setWindowTitle(f"Adicionar Falta para {nome_da_materia}")

        # Define a data atual como padrão
        if hasattr(self, 'dateEdit_data_falta'):
             self.dateEdit_data_falta.setDate(QDate.currentDate())
             
        self.btn_salvar.clicked.connect(self.accept) 
        self.btn_cancelar.clicked.connect(self.reject) 

    def get_dados(self):
        """ Retorna a quantidade de faltas e a data digitada. """
        data_falta = QDate.currentDate().toString(Qt.DateFormat.ISODate)
        if hasattr(self, 'dateEdit_data_falta'):
            data_falta = self.dateEdit_data_falta.date().toString(Qt.DateFormat.ISODate) 
            
        return {
            "falta": self.spinBox_falta.value(), 
            "data": data_falta
        }

    def configurar_janela(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)


class DialogCalcularIEA(QDialog):
    def __init__(self):
        super().__init__()
        
        self.ui_loaded = False 
        
        try:
            uic.loadUi("UI/Dialog - calcular.iea.ui", self)
            self.ui_loaded = True 
        except Exception as e:
            print(f"[ERRO CRÍTICO UI] Falha ao carregar Dialog - calcular.iea.ui: {e}")
            self.reject()
            return

        self.configurar_janela()
        
        if self.ui_loaded:
             self.realizar_calculo() 

        if hasattr(self, 'btn_fechar'): self.btn_fechar.clicked.connect(self.accept)
        elif hasattr(self, 'btn_fechar_iea'): self.btn_fechar_iea.clicked.connect(self.accept)
        
        if hasattr(self, 'btn_calcular'): 
            self.btn_calcular.clicked.connect(self.realizar_calculo) 

    def realizar_calculo(self):
        # Chama o backend para obter os resultados
        resultados = BancoDados.calcular_iea_geral()
        
        if hasattr(self, 'label_iech'): 
            self.label_iech.setText(f"IECH: {resultados['IECH']:.2f}")

        if hasattr(self, 'label_iepl'):
            self.label_iepl.setText(f"IEPL: {resultados['IEPL']:.2f}")
            
        iea_score_text = f"IEA: {resultados['IEA']:.2f}"
        
        if hasattr(self, 'label_iea_resultado'):
            self.label_iea_resultado.setText(iea_score_text)
        elif hasattr(self, 'label_iea'):
             self.label_iea.setText(iea_score_text)
        else:
             print("[ERRO CRÍTICO] Label de IEA não encontrado na UI!")


    def configurar_janela(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)


class DialogConfirmarExclusao(QDialog):
    def __init__(self, item_nome):
        super().__init__()
        
        try:
            uic.loadUi("UI/Dialog - confirmar.exclusao.ui", self)
            self.ui_loaded = True
        except Exception as e:
            self.ui_loaded = False
            self.setWindowTitle("Confirmar Exclusão")
            self.layout = QVBoxLayout(self)
            self.label = QLabel(f"Confirma a exclusão de **{item_nome}**?")
            self.btn_confirmar = QPushButton("Sim, Excluir")
            self.btn_cancelar = QPushButton("Cancelar")
            
            self.layout.addWidget(self.label)
            self.layout.addWidget(self.btn_confirmar)
            self.layout.addWidget(self.btn_cancelar)

            self.btn_confirmar.clicked.connect(self.accept)
            self.btn_cancelar.clicked.connect(self.reject)
            return
        self.configurar_janela()
        
        if hasattr(self, 'label_mensagem'):
            self.label_mensagem.setText(f"Tem certeza que deseja excluir '{item_nome}'?")

        if hasattr(self, 'btn_confirmar'):
            self.btn_confirmar.clicked.connect(self.accept)
        if hasattr(self, 'btn_cancelar'):
            self.btn_cancelar.clicked.connect(self.reject)

    def configurar_janela(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)