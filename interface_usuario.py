# Arquivo: interface_usuario.py
import sys
from PyQt6.QtWidgets import QApplication
from janela_principal import JanelaPrincipal

class InterfaceUsuario:
    @staticmethod
    def menuInicial():
        """ Inicializa a aplicação gráfica. """
        app = QApplication(sys.argv)
        janela = JanelaPrincipal()
        janela.show()
        sys.exit(app.exec())