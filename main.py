import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QGridLayout, QMessageBox, QWidget, QListView, QStackedWidget)
from PyQt6.QtCore import Qt
from PyQt6 import uic

# Widgets e Janelas
from Modules.card_materia import CardMateria
from Modules.card_semestre import CardSemestre
from Modules.janelas_extras import DialogCalcularIEA

class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/MainWindow - eng.software.ui", self)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.semestres_carregados = False 
        self.setup_ui() # Configura botões e navegação
        self.carregar_dashboard() # Carrega dados iniciais

    def carregar_dashboard(self):
        """ Configura a grid de matérias na tela inicial """
        
        # Configura o layout da grid
        self.layout_grid = QGridLayout()
        self.layout_grid.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        container = self.scrollArea_materias.widget()
        if not container:
             container = QWidget()
             self.scrollArea_materias.setWidget(container)
             self.scrollArea_materias.setWidgetResizable(True)
        container.setLayout(self.layout_grid)

        # Dados para teste (substituir pela integração real)
        dados_mock = [
            {"nome": "Engenharia de Software", "media": 10.0, "faltas": 0, "max": 20},
            {"nome": "Banco de Dados", "media": 7.5, "faltas": 4, "max": 20},
        ]

        # Gera os cards visuais
        row, col = 0, 0
        for m in dados_mock:
            card = CardMateria(m["nome"], m["media"], m["faltas"], m["max"])
            self.layout_grid.addWidget(card, row, col)
            
            # Lógica de 2 colunas
            col += 1 
            if col == 2: 
                col, row = 0, row + 1

    def salvar_nova_materia(self):
        """ Captura o formulário e salva """
        nome = self.nomeDaMateria_lineEdit.text()
        carga = self.cargaHoraria_spinBox.value()

        if not nome:
            return

        # Aqui entra a lógica de salvar os dados
        print(f"Salvando: {nome}, {carga}h")
        
        self.nomeDaMateria_lineEdit.clear()
        self.mudar_pagina(0) # Volta para o dashboard
        self.carregar_dashboard() # Atualiza a lista visual

    def abrir_tela_semestres(self):
        """ Carrega lista de semestres """
        self.mudar_pagina(1)
        if self.semestres_carregados: return

        # Prepara layout
        container = QWidget()
        grid = QGridLayout()
        grid.setAlignment(Qt.AlignmentFlag.AlignTop)
        container.setLayout(grid)
        self.scrollArea_semestre.setWidget(container)
        self.scrollArea_semestre.setWidgetResizable(True)

        # Lista de semestres (dados de teste)
        semestres = [
            {"nome": "1º Semestre", "situacao": "Finalizado"},
            {"nome": "2º Semestre", "situacao": "Futuro"},          
        ]

        for i, item in enumerate(semestres):
            row, col = divmod(i, 2)
            grid.addWidget(CardSemestre(item["nome"], item["situacao"]), row, col)
        
        self.semestres_carregados = True

    # --- Configuração de Navegação e Botões ---
    def setup_ui(self):
        self.stack = self.findChild(QStackedWidget) or self.stackedWidget
        
        # Botões do Menu Lateral
        if hasattr(self, 'btn_dashboard_principal'): self.btn_dashboard_principal.clicked.connect(lambda: self.mudar_pagina(0))
        if hasattr(self, 'btn_semestres'): self.btn_semestres.clicked.connect(self.abrir_tela_semestres)
        if hasattr(self, 'btn_usuario'): self.btn_usuario.clicked.connect(lambda: self.mudar_pagina(2))
        if hasattr(self, 'btn_registrar_materia'): self.btn_registrar_materia.clicked.connect(lambda: self.mudar_pagina(3))
        
        # Botões de Ação
        if hasattr(self, 'btn_salvar_materia'): self.btn_salvar_materia.clicked.connect(self.salvar_nova_materia)
        if hasattr(self, 'btn_calcular_iea'): self.btn_calcular_iea.clicked.connect(lambda: DialogCalcularIEA().exec())
        if hasattr(self, 'btn_fechar'): self.btn_fechar.clicked.connect(self.close)
        if hasattr(self, 'comboBox_semestre'): self.comboBox_semestre.setView(QListView())

    def mudar_pagina(self, index):
        self.stack.setCurrentIndex(index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JanelaPrincipal()
    window.show()
    sys.exit(app.exec())