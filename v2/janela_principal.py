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

    def recarregar_dashboard(self):
        """ Método público usado como callback para forçar a atualização da tela. """
        self.carregar_dashboard()
        self.preencher_combo_materias() 
        print("[JanelaPrincipal] Dashboard Recarregado após ação do usuário.")

    def carregar_dashboard(self):
        """ Configura a grid de matérias buscando do BancoDados """
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
            item = self.layout_grid.itemAt(i)
            if item and item.widget():
                item.widget().setParent(None) 

        row, col = 0, 0
        for m in dados:
            # PASSANDO 'self' (referência para JanelaPrincipal)
            card = CardMateria(m.nome, m.media, m.faltas, m.max_faltas, self) 
            self.layout_grid.addWidget(card, row, col)
            
            col += 1 
            if col == 2: 
                col, row = 0, row + 1

    def salvar_nova_materia(self):
        """ Captura o formulário e manda para o BancoDados """
        nome = self.nomeDaMateria_lineEdit.text()
        carga = self.cargaHoraria_spinBox.value()
        NOME_WIDGET_LIMITE = "limiteFaltas_spinBox" 
        
        max_faltas = int(carga * 0.25) #25% da carga
        
        try:
             # Tenta obter o valor do widget
             max_faltas = getattr(self, NOME_WIDGET_LIMITE).value()
             print(f"[DEBUG] Limite de Faltas LIDO do widget '{NOME_WIDGET_LIMITE}': {max_faltas}")
        except AttributeError:
             # Entra aqui se o nome do widget estiver errado
             print(f"[ERRO DE WIDGET] O sistema não encontrou o widget '{NOME_WIDGET_LIMITE}' para ler o limite.")
             print(f"[INFO] Usando o valor de fallback: {max_faltas}")
             
        if not nome:
            return

        # Passa o valor (do usuário ou o fallback)
        print(f"[DEBUG] Valor FINAL ENVIADO ao backend: {max_faltas}")
        BancoDados.adicionar_materia(nome, carga, max_faltas)
        
        # Limpa e recarrega
        self.nomeDaMateria_lineEdit.clear()
        self.cargaHoraria_spinBox.setValue(0)
        
        # Limpa o campo do novo limite, se ele existir
        if hasattr(self, NOME_WIDGET_LIMITE):
            getattr(self, NOME_WIDGET_LIMITE).setValue(0)
            
        self.mudar_pagina(0) 
        self.recarregar_dashboard() 

    def abrir_tela_semestres(self):
        """ Carrega lista de semestres do BancoDados """
        self.mudar_pagina(1)
        
        if not hasattr(self, 'grid_semestres'):
            self.container_sem = QWidget()
            self.grid_semestres = QGridLayout()
            self.grid_semestres.setAlignment(Qt.AlignmentFlag.AlignTop)
            self.container_sem.setLayout(self.grid_semestres)
            self.scrollArea_semestre.setWidget(self.container_sem)
            self.scrollArea_semestre.setWidgetResizable(True)
        
        for i in reversed(range(self.grid_semestres.count())): 
            item = self.grid_semestres.itemAt(i)
            if item and item.widget():
                item.widget().setParent(None)

        semestres = BancoDados.get_semestres()

        for i, item in enumerate(semestres):
            row, col = divmod(i, 2)
            self.grid_semestres.addWidget(CardSemestre(item.nome, item.situacao), row, col) 
        
        self.semestres_carregados = True

    def exibir_iea(self):
        """ Calcula o IEA/IECH no backend e abre o diálogo. """
        
        resultados = BancoDados.calcular_iea_geral()
        
        try:
            DialogCalcularIEA().exec() 
            print(f"[JanelaPrincipal] IEA calculado (IECH): {resultados['IECH']}")
        except Exception as e:
            print(f"ERRO ao abrir diálogo IEA. Causa: {e}")

    def preencher_combo_materias(self):
        """ Carrega todas as matérias cadastradas no ComboBox de seleção de notas. """
        if hasattr(self, 'comboBox_materias'):
            self.comboBox_materias.clear()
            materias = BancoDados.get_materias()
            
            for m in materias:
                self.comboBox_materias.addItem(m.nome)

    def salvar_nova_nota(self):
        """ Captura os dados da nota da interface e envia para o BancoDados. """
        
        try:
            materia_selecionada = self.comboBox_materias.currentText()
            valor = self.valor_nota_spinBox.value() 
            peso = self.peso_nota_spinBox.value()
            descricao = self.descricao_lineEdit.text()
        except AttributeError:
            print("[JanelaPrincipal] ERRO: Verifique os nomes dos widgets de entrada de notas.")
            return

        if not materia_selecionada or not valor or not peso:
            return

        BancoDados.adicionar_nota_materia(materia_selecionada, valor, peso, descricao)
        
        self.valor_nota_spinBox.setValue(0.0)
        self.peso_nota_spinBox.setValue(0.0)
        self.descricao_lineEdit.clear()
        
        self.recarregar_dashboard() 

    def setup_ui(self):
        self.stack = self.findChild(QStackedWidget) or self.stackedWidget
        
        if hasattr(self, 'btn_dashboard_principal'): self.btn_dashboard_principal.clicked.connect(lambda: self.mudar_pagina(0))
        if hasattr(self, 'btn_semestres'): self.btn_semestres.clicked.connect(self.abrir_tela_semestres)
        if hasattr(self, 'btn_usuario'): self.btn_usuario.clicked.connect(lambda: self.mudar_pagina(2))
        if hasattr(self, 'btn_registrar_materia'): self.btn_registrar_materia.clicked.connect(lambda: self.mudar_pagina(3))
        
        if hasattr(self, 'btn_salvar_materia'): self.btn_salvar_materia.clicked.connect(self.salvar_nova_materia)
        if hasattr(self, 'btn_calcular_iea'): self.btn_calcular_iea.clicked.connect(self.exibir_iea)
        if hasattr(self, 'btn_salvar_nota'): self.btn_salvar_nota.clicked.connect(self.salvar_nova_nota)
        
        if hasattr(self, 'btn_fechar'): self.btn_fechar.clicked.connect(self.close)
        if hasattr(self, 'comboBox_semestre'): self.comboBox_semestre.setView(QListView())
        
        self.preencher_combo_materias()

    def mudar_pagina(self, index):
        self.stack.setCurrentIndex(index)