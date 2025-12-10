from banco_dados import BancoDados
from interface_usuario import InterfaceUsuario

import sys
import os
import builtins

"""Função que permite que as pastas sejam acessiveis pelo executável"""
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

builtins.resource_path = resource_path

def main():
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
        os.chdir(application_path)

    BancoDados.fazPreCadastro()
    InterfaceUsuario.menuInicial()

if __name__ == "__main__":
    main()