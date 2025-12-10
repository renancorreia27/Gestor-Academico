from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout
from PyQt6 import uic
from PyQt6.QtCore import Qt
from banco_dados import BancoDados 
import os

class CardSemestre(QWidget):
    """Widget reponsável por exibir status, Gerenciar Semestres e permitir a alteração do status"""
    def __init__(self, nome_semestre, situacao, parent_window):
        super().__init__()
        
        # Define tamanho mínimo
        self.setMinimumHeight(140) 
        self.setMinimumWidth(250)

        self.nome = nome_semestre
        self.parent_window = parent_window 
        self.situacao_atual = situacao
        
        # Carrega UI
        ui_carregado = False
        caminhos_tentativa = [
            "UI/Widget - card.semestre.ui",
            "Widget - card.semestre.ui",
            "v2/UI/Widget - card.semestre.ui",
            "../UI/Widget - card.semestre.ui"
        ]

        for caminho in caminhos_tentativa:
            try:
                if os.path.exists(caminho):
                    uic.loadUi(caminho, self)
                    ui_carregado = True
                    print(f"[DEBUG] Card UI carregado de: {caminho}")
                    break
            except:
                continue
        
        # Se NÃO achou o arquivo .ui, cria widgets temp
        if not ui_carregado:
            print(f"[ERRO CRÍTICO] Não foi possível carregar o UI do Card para {nome_semestre}. Criando fallback.")
            self.setStyleSheet("background-color: #e0e0e0; border: 1px solid red; border-radius: 10px;")
            layout_fallback = QVBoxLayout(self)
            self.label_nome = QLabel(nome_semestre)
            self.label_situacao = QLabel(situacao)
            self.label_nome.setStyleSheet("font-size: 16px; font-weight: bold; color: black;")
            layout_fallback.addWidget(self.label_nome)
            layout_fallback.addWidget(self.label_situacao)
            
            # Botões de emergência
            self.btn_iniciar_semestre = QPushButton("Iniciar")
            self.btn_finaliza_semestre = QPushButton("Finalizar")
            self.btn_delete_semestre = QPushButton("Excluir")
            layout_fallback.addWidget(self.btn_iniciar_semestre)
            layout_fallback.addWidget(self.btn_finaliza_semestre)
            layout_fallback.addWidget(self.btn_delete_semestre)

        #Conexões
        if hasattr(self, 'label_nome'): 
            self.label_nome.setText(nome_semestre)
        
        self.atualizar_interface(situacao)

        # Complementar conexões de botões de status
        if hasattr(self, 'btn_iniciar_semestre'): 
            self.btn_iniciar_semestre.clicked.connect(self.marcar_em_andamento)
        if hasattr(self, 'btn_finaliza_semestre'): 
            self.btn_finaliza_semestre.clicked.connect(self.marcar_finalizado)
        
        # Conexão do botão de deletar
        btn_del = getattr(self, 'btn_delete_semestre', None)
        if not btn_del:
            for btn in self.findChildren(QPushButton):
                nome_obj = btn.objectName().lower()
                if "delete" in nome_obj or "lixeira" in nome_obj or "excluir" in nome_obj:
                    btn_del = btn
                    break
        if btn_del:
            btn_del.clicked.connect(self.clicar_excluir)

    def marcar_em_andamento(self):
        """Atualiza o status do semestre para 'em andamento' no banco_dados e UI """
        if BancoDados.atualizar_status_semestre(self.nome, "Em Andamento"):
            self.atualizar_interface("Em Andamento")

    def marcar_finalizado(self):
        """Atualiza o status do semestre para 'finalizado' no banco_dados e UI """
        if BancoDados.atualizar_status_semestre(self.nome, "Finalizado"):
            self.atualizar_interface("Finalizado")

    def clicar_excluir(self):
        """Pergunta na tela principal a confirmação de exclusão do semestre"""
        if hasattr(self.parent_window, 'excluir_semestre_especifico'):
            self.parent_window.excluir_semestre_especifico(self.nome)

    def atualizar_interface(self, situacao):
        """Controla os botões de ação como cor e status"""
        if hasattr(self, 'label_situacao'):
            self.label_situacao.setText(situacao)
            
            style_amarelo = "color: #f1c40f; font-weight: bold;"
            style_verde = "color: #2ecc71; font-weight: bold;"
            style_cinza = "color: #7f8c8d; font-weight: bold;"

            if hasattr(self, 'btn_iniciar_semestre') and hasattr(self, 'btn_finaliza_semestre'):
                if situacao == "Em Andamento":
                    self.btn_iniciar_semestre.hide()
                    self.btn_finaliza_semestre.show()
                    self.label_situacao.setStyleSheet(style_amarelo)
                elif situacao == "Finalizado":
                    self.btn_iniciar_semestre.hide() 
                    self.btn_finaliza_semestre.hide()
                    self.label_situacao.setStyleSheet(style_verde)
                else: 
                    self.btn_finaliza_semestre.hide()   
                    self.btn_iniciar_semestre.show()
                    self.label_situacao.setStyleSheet(style_cinza)