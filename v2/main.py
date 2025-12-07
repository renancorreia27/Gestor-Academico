from banco_dados import BancoDados
from interface_usuario import InterfaceUsuario

def main():
    # 1. Carrega/Prepara os dados do sistema
    BancoDados.fazPreCadastro()
    # 2. Inicia a Interface Gráfica
    InterfaceUsuario.menuInicial()

if __name__ == "__main__":
    main()