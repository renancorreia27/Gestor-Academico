from PyQt6.QtWidgets import QWidget, QPushButton
from PyQt6 import uic
from .janelas_extras import DialogAdicionarNota, DialogAdicionarFalta, DialogConfirmarExclusao 

from banco_dados import BancoDados 

class CardMateria(QWidget):
    def __init__(self, nome_materia, media, faltas, faltas_max, parent_window):
        super().__init__()
        try:
            uic.loadUi("UI/Widget - card.materia.ui", self)
        except:
            uic.loadUi("Widget - card.materia.ui", self)

        self.nome_materia_atual = nome_materia
        self.parent_window = parent_window
        
        # Preenchimento visual
        self.label_card_materia.setText(nome_materia)
        self.label_media.setText(f"{media:.2f}") 
        self.label_faltas.setText(f"Faltas: {faltas}/{faltas_max}")

        self.progressBar_media.setMaximum(100) 
        self.progressBar_media.setValue(int(float(media) * 10)) 
        self.progressBar_falta.setMaximum(faltas_max)
        self.progressBar_falta.setValue(faltas)

        # Conexões de Botões
        self.btn_add_nota.clicked.connect(self.clicar_add_nota)
        self.btn_add_falta.clicked.connect(self.clicar_add_falta)
        
        btn_remover = getattr(self, 'btn_remover_materia', None) # 1. Tenta o nome padrão
        
        if btn_remover is None:
            botoes = self.findChildren(QPushButton)
            if botoes:
                btn_remover = botoes[-1]

        if btn_remover:
            btn_remover.clicked.connect(self.clicar_remover_materia) 
            print(f"[DEBUG] Conexão de remoção (Botão '{btn_remover.objectName() or 'sem nome'}') OK.")
        else:
            print(f"[ALERTA] FALHA CRÍTICA: Não foi possível encontrar e conectar o botão de remoção para {nome_materia}.")


    def clicar_add_nota(self):
        """ Abre modal de notas, captura dados e envia para o backend. """
        dialog = DialogAdicionarNota(self.nome_materia_atual)
        
        if dialog.exec():
            dados = dialog.get_dados()
            nota = dados["nota"]
            peso = dados["peso"]
            descricao = dados.get("descricao", "Avaliação Padrão")
            
            sucesso = BancoDados.adicionar_nota_materia(
                self.nome_materia_atual, 
                nota, 
                peso, 
                descricao
            )
            
            if sucesso:
                self.parent_window.recarregar_dashboard() 

    def clicar_add_falta(self):
        """ Abre modal de faltas, captura dados e envia para o backend. """
        dialog = DialogAdicionarFalta(self.nome_materia_atual)
        
        if dialog.exec():
            dados = dialog.get_dados()
            qtd_faltas = dados["falta"]
            data_falta = dados["data"]
            
            sucesso = BancoDados.adicionar_falta_materia(
                self.nome_materia_atual, 
                qtd_faltas, 
                data_falta
            )
            
            if sucesso:
                # Callback: recarrega a tela principal para atualizar faltas
                self.parent_window.recarregar_dashboard()
                
    def clicar_remover_materia(self):
        """ Abre diálogo de confirmação, deleta a matéria e destrói o card localmente. """
        
        dialog = DialogConfirmarExclusao(self.nome_materia_atual)
        
        if dialog.exec():
            # Tenta deletar no backend (lista e JSON)
            sucesso = BancoDados.deletar_materia(self.nome_materia_atual)
            
            if sucesso:
                # 1. DESTRÓI O WIDGET ATUAL (REMOVE-O VISUALMENTE)
                self.deleteLater() 
                
                # 2. FORÇA A RECARGA DA TELA PRINCIPAL (AJUSTA LAYOUT)
                self.parent_window.recarregar_dashboard() 
            else:
                print(f"[ERRO DE BACKEND] Falha ao deletar {self.nome_materia_atual}.")