from PyQt6.QtWidgets import QMainWindow, QGridLayout, QVBoxLayout, QWidget, QStackedWidget, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6 import uic

from Modules.card_materia import CardMateria
from Modules.card_semestre import CardSemestre
from Modules.janelas_extras import DialogCalcularIEA, DialogConfirmarExclusao 
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

class JanelaPrincipal(QMainWindow):
    "Controlador principal do programa, tem a função de controlar todas as janelas"
    def __init__(self):
        super().__init__()
        try:
            uic.loadUi(resource_path("UI/MainWindow - eng.software.ui"), self)
        except:
            uic.loadUi("MainWindow - eng.software.ui", self)
            
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.materia_em_edicao = None 
        
        self.setup_ui() 
        self.carregar_dados_usuario()
        
        # Load antes de começar o programa
        self.atualizar_combo_semestres()
        self.carregar_dashboard()
        self.carregar_semestres() 

    def setup_ui(self):
        """Conecta os clicks nos butões com as funções corretas"""
        self.stack = self.findChild(QStackedWidget, "pages") or self.stackedWidget
        
        # Navegação
        if hasattr(self, 'btn_dashboard_principal'): self.btn_dashboard_principal.clicked.connect(lambda: self.mudar_pagina(0))
        if hasattr(self, 'btn_semestres'): self.btn_semestres.clicked.connect(self.abrir_tela_semestres)
        if hasattr(self, 'btn_usuario'): self.btn_usuario.clicked.connect(lambda: self.mudar_pagina(2))
        
        # Matéria
        if hasattr(self, 'btn_registrar_materia'): self.btn_registrar_materia.clicked.connect(self.preparar_novo_cadastro)
        if hasattr(self, 'btn_salvar_materia'): self.btn_salvar_materia.clicked.connect(self.salvar_materia)
        
        # Config
        if hasattr(self, 'btn_salvar_config'): self.btn_salvar_config.clicked.connect(self.salvar_configuracoes)
        if hasattr(self, 'btn_calcular_iea'): self.btn_calcular_iea.clicked.connect(self.exibir_iea)
            
        # Semestres
        if hasattr(self, 'btn_add_semestre'):
            self.btn_add_semestre.clicked.connect(self.adicionar_novo_semestre)
        
        if hasattr(self, 'btn_salvar_semestre'):
            self.btn_salvar_semestre.hide()

        # Dashboard
        if hasattr(self, 'comboBox_semestre'):
            self.comboBox_semestre.currentIndexChanged.connect(self.recarregar_dashboard)

        if hasattr(self, 'btn_fechar'): self.btn_fechar.clicked.connect(self.close)

    def mudar_pagina(self, index):
        self.stack.setCurrentIndex(index)


    # CONFIG DE USER


    def carregar_dados_usuario(self):
        """Carrega os dados do usuário do banco_dados"""
        u = BancoDados.get_usuario()
        if hasattr(self, 'nomeDeUsuarioLineEdit'): self.nomeDeUsuarioLineEdit.setText(u.nome)
        if hasattr(self, 'nomeDoCursoLineEdit'): self.nomeDoCursoLineEdit.setText(u.curso)
        if hasattr(self, 'cargaHorariaDoCursoSpinBox'): self.cargaHorariaDoCursoSpinBox.setValue(u.carga_horaria_total)
        if hasattr(self, 'cargaHorariaDoCursoSpinBox_2'): self.cargaHorariaDoCursoSpinBox_2.setValue(u.semestres_totais)
        
        if hasattr(self, 'btn_usuario'):
            txt = u.nome if u.nome.strip() else "Usuário"
            self.btn_usuario.setText(txt)

    def salvar_configuracoes(self):
        """Salva as configurações do usuário no banco_dados"""
        nome = self.nomeDeUsuarioLineEdit.text()
        curso = self.nomeDoCursoLineEdit.text()
        carga = self.cargaHorariaDoCursoSpinBox.value()
        sem = self.cargaHorariaDoCursoSpinBox_2.value() if hasattr(self, 'cargaHorariaDoCursoSpinBox_2') else 8
        
        BancoDados.salvar_configuracoes_usuario(nome, curso, carga, sem)
        
        if hasattr(self, 'btn_usuario'):
            txt = nome if nome.strip() else "Usuário"
            self.btn_usuario.setText(txt)
            
        self.mudar_pagina(0)

    def exibir_iea(self):
        DialogCalcularIEA().exec()

    
    #CONFIG DE SEMESTRES
    

    def abrir_tela_semestres(self):
        """Entra na tela de semestres"""
        self.mudar_pagina(1)
        self.carregar_semestres() 

    def carregar_semestres(self):
        """Cria e redimensiona o CardSemestre para seu respectivo semestre"""
        if not hasattr(self, 'scrollArea_semestre'): return

        novo_container = QWidget()
        novo_container.setStyleSheet("background-color: #F8F9FD; border: none;") 
        
        layout_grade = QGridLayout() 
        layout_grade.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout_grade.setSpacing(15)
        layout_grade.setContentsMargins(10, 10, 10, 10)
        novo_container.setLayout(layout_grade)

        semestres = BancoDados.get_semestres()
        colunas = 2
        for i, s in enumerate(semestres):
            row, col = divmod(i, colunas)
            card = CardSemestre(s.nome, s.situacao, self)
            layout_grade.addWidget(card, row, col)
            card.show()

        self.scrollArea_semestre.setWidget(novo_container)
        self.scrollArea_semestre.setWidgetResizable(True)

    def adicionar_novo_semestre(self):
        """Cria um novo semestre na UI"""
        nome = BancoDados.criar_proximo_semestre()
        self.atualizar_combo_semestres()
        self.carregar_semestres()
        if hasattr(self, 'comboBox_semestre'):
            idx = self.comboBox_semestre.findText(nome)
            if idx >= 0: self.comboBox_semestre.setCurrentIndex(idx)

    def excluir_semestre_especifico(self, nome_semestre):
        """ Deleta semestre usando o Dialog estilizado. """
        
        try:
            dialog = DialogConfirmarExclusao(nome_semestre)
            confirmou = dialog.exec()
        except:
            res = QMessageBox.question(self, "Excluir", f"Deseja excluir **{nome_semestre}**?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            confirmou = (res == QMessageBox.StandardButton.Yes)

        if confirmou:
            if BancoDados.deletar_semestre(nome_semestre):
                self.carregar_semestres()
                self.atualizar_combo_semestres()
                self.recarregar_dashboard()

    def atualizar_combo_semestres(self):
        """Prenche o QcomboBox com semestres disponíveis"""
        if not hasattr(self, 'comboBox_semestre'): return
        self.comboBox_semestre.blockSignals(True)
        self.comboBox_semestre.clear()
        for s in BancoDados.get_semestres():
            self.comboBox_semestre.addItem(s.nome)
        self.comboBox_semestre.blockSignals(False)

  
    #CONFIG DE MATÉRIAS


    def preparar_novo_cadastro(self):
        """Prepara tela para entrada de dados de uma nova matéria"""
        self.materia_em_edicao = None 
        if hasattr(self, 'nomeDaMateria_lineEdit'): self.nomeDaMateria_lineEdit.clear()
        if hasattr(self, 'cargaHoraria_spinBox'): self.cargaHoraria_spinBox.setValue(0)
        if hasattr(self, 'label_registrar'): self.label_registrar.setText("Registrar Matéria")
        self.mudar_pagina(3)

    def abrir_tela_edicao(self, nome_materia):
        """Permite a alteração de matérias existentes"""
        m = BancoDados.get_materia(nome_materia)
        if not m: return
        self.materia_em_edicao = nome_materia 
        
        if hasattr(self, 'nomeDaMateria_lineEdit'): self.nomeDaMateria_lineEdit.setText(m.nome)
        if hasattr(self, 'cargaHoraria_spinBox'): self.cargaHoraria_spinBox.setValue(m.carga_horaria)
        
        s_faltas = getattr(self, "limiteFaltas_spinBox", getattr(self, "limiteFatlas_spinBox", None))
        if s_faltas: s_faltas.setValue(m.max_faltas)
        s_media = getattr(self, "mediaMateria_doubleSpinBox", None)
        if s_media: s_media.setValue(m.media_necessaria)

        if hasattr(self, 'label_registrar'): self.label_registrar.setText("Editar Matéria")
        self.mudar_pagina(3)

    def salvar_materia(self):
        """Salva uma nova matéria ou modificações no banco_dados"""
        nome = self.nomeDaMateria_lineEdit.text()
        carga = self.cargaHoraria_spinBox.value()
        try: max_faltas = getattr(self, "limiteFaltas_spinBox", getattr(self, "limiteFatlas_spinBox")).value()
        except: max_faltas = 20
        try: media_nec = self.mediaMateria_doubleSpinBox.value()
        except: media_nec = 7.0

        if not nome: return

        if self.materia_em_edicao:
            BancoDados.editar_materia(self.materia_em_edicao, nome, carga, max_faltas, media_nec)
        else:
            sem = self.comboBox_semestre.currentText()
            if not sem: sem = "1º Semestre"
            BancoDados.adicionar_materia(nome, sem, carga, max_faltas, media_nec)
        
        self.preparar_novo_cadastro()
        self.mudar_pagina(0) 
        self.recarregar_dashboard()

    def recarregar_dashboard(self):
        self.carregar_dashboard()

    def carregar_dashboard(self):
        """Cria e redimensiona o CardMateria para cada semestre"""
        if not hasattr(self, 'scrollArea_materias'): return

        novo_container = QWidget()
        novo_container.setStyleSheet("background-color: #F8F9FD; border: none;") 

        layout_grid = QGridLayout()
        layout_grid.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout_grid.setSpacing(15)
        layout_grid.setContentsMargins(10, 10, 10, 10)
        novo_container.setLayout(layout_grid)

        semestre = "1º Semestre"
        if hasattr(self, 'comboBox_semestre'):
            txt = self.comboBox_semestre.currentText()
            if txt: semestre = txt
            elif self.comboBox_semestre.count() > 0: semestre = self.comboBox_semestre.itemText(0)

        dados = BancoDados.get_materias(filtro_semestre=semestre)
        
        col_count = 2
        for i, m in enumerate(dados):
            row, col = divmod(i, col_count)
            card = CardMateria(m.nome, m.media, m.faltas, m.max_faltas, m.media_necessaria, self)
            layout_grid.addWidget(card, row, col)
            card.show()

        self.scrollArea_materias.setWidget(novo_container)
        self.scrollArea_materias.setWidgetResizable(True)