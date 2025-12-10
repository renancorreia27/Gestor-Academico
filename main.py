from banco_dados import BancoDados
from interface_usuario import InterfaceUsuario

def main():
    BancoDados.fazPreCadastro()
    InterfaceUsuario.menuInicial()

if __name__ == "__main__":
    main()