# Arquivo: janela_principal.py
from PyQt6.QtWidgets import QMainWindow, QGridLayout, QWidget, QListView, QStackedWidget
from PyQt6.QtCore import Qt
from PyQt6 import uic

# Importando nossos Módulos e o Banco de Dados
from Modules.card_materia import CardMateria
from Modules.card_semestre import CardSemestre
from Modules.janelas_extras import DialogCalcularIEA
from banco_dados import BancoDados

class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/MainWindow - eng.software.ui", self)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.semestres_carregados = False 
        self.setup_ui() 
        self.carregar_dashboard() 

    def carregar_dashboard(self):
        """ Configura a grid de matérias buscando do BancoDados """
        # Limpa o layout anterior se existir (para recarregar)
        if hasattr(self, 'layout_grid'):
            pass
        else:
            self.layout_grid = QGridLayout()
            self.layout_grid.setAlignment(Qt.AlignmentFlag.AlignTop)
            
            container = self.scrollArea_materias.widget()
            if not container:
                container = QWidget()
                self.scrollArea_materias.setWidget(container)
                self.scrollArea_materias.setWidgetResizable(True)
            container.setLayout(self.layout_grid)

        # --- Busca dados do Banco ---
        dados = BancoDados.get_materias() 

        # Gera os cards visuais
        for i in reversed(range(self.layout_grid.count())): 
            self.layout_grid.itemAt(i).widget().setParent(None) # Limpa grid antes de adicionar

        row, col = 0, 0
        for m in dados:
            card = CardMateria(m["nome"], m["media"], m["faltas"], m["max"])
            self.layout_grid.addWidget(card, row, col)
            
            col += 1 
            if col == 2: 
                col, row = 0, row + 1

    def salvar_nova_materia(self):
        """ Captura o formulário e manda para o BancoDados """
        nome = self.nomeDaMateria_lineEdit.text()
        carga = self.cargaHoraria_spinBox.value()

        if not nome:
            return

        # Chama o Banco de Dados para salvar
        BancoDados.adicionar_materia(nome, carga)
        
        # Limpa e recarrega
        self.nomeDaMateria_lineEdit.clear()
        self.mudar_pagina(0) 
        self.carregar_dashboard() 

    def abrir_tela_semestres(self):
        """ Carrega lista de semestres do BancoDados """
        self.mudar_pagina(1)
        
        # Prepara layout (similar ao dashboard)
        if not hasattr(self, 'grid_semestres'):
            self.container_sem = QWidget()
            self.grid_semestres = QGridLayout()
            self.grid_semestres.setAlignment(Qt.AlignmentFlag.AlignTop)
            self.container_sem.setLayout(self.grid_semestres)
            self.scrollArea_semestre.setWidget(self.container_sem)
            self.scrollArea_semestre.setWidgetResizable(True)
        
        # Limpa visualização antiga
        for i in reversed(range(self.grid_semestres.count())): 
            self.grid_semestres.itemAt(i).widget().setParent(None)

        # Busca do Banco
        semestres = BancoDados.get_semestres()

        for i, item in enumerate(semestres):
            row, col = divmod(i, 2)
            self.grid_semestres.addWidget(CardSemestre(item["nome"], item["situacao"]), row, col)
        
        self.semestres_carregados = True

    def setup_ui(self):
        self.stack = self.findChild(QStackedWidget) or self.stackedWidget
        
        # Conexões de Botões
        if hasattr(self, 'btn_dashboard_principal'): self.btn_dashboard_principal.clicked.connect(lambda: self.mudar_pagina(0))
        if hasattr(self, 'btn_semestres'): self.btn_semestres.clicked.connect(self.abrir_tela_semestres)
        if hasattr(self, 'btn_usuario'): self.btn_usuario.clicked.connect(lambda: self.mudar_pagina(2))
        if hasattr(self, 'btn_registrar_materia'): self.btn_registrar_materia.clicked.connect(lambda: self.mudar_pagina(3))
        
        if hasattr(self, 'btn_salvar_materia'): self.btn_salvar_materia.clicked.connect(self.salvar_nova_materia)
        if hasattr(self, 'btn_calcular_iea'): self.btn_calcular_iea.clicked.connect(lambda: DialogCalcularIEA().exec())
        if hasattr(self, 'btn_fechar'): self.btn_fechar.clicked.connect(self.close)
        if hasattr(self, 'comboBox_semestre'): self.comboBox_semestre.setView(QListView())

    def mudar_pagina(self, index):
        self.stack.setCurrentIndex(index)