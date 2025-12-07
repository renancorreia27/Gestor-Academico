# Arquivo: interface_usuario.py
import sys
from PyQt6.QtWidgets import QApplication
from janela_principal import JanelaPrincipal

class InterfaceUsuario:
    def menuInicial():
        # Cria a instância da aplicação
        app = QApplication(sys.argv)
        # Cria e exibe a janela principal
        window = JanelaPrincipal()
        window.show()
        sys.exit(app.exec())