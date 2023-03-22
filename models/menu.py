from verifica.verifica_dado import verifica_int, verifica_float
from models.produtos import Produto, Estoque, Carrinho
from time import sleep


def menu_base():
    while True:
        print('-' * 60)
        print('Mercadinho Hype'.center(60, '-'))
        print('-' * 60)

        print('Selecione uma opção:')
        print('1 - Funcionário')
        print('2 - Cliente')
        print('3 - Sair')

        opcao: int = verifica_int('Digite a opção: ')

        if opcao == 1:
            menu_funcionario()
        elif opcao == 2:
            menu_cliente()
        elif opcao == 3:
            break
        else:
            print('Opção inválida!')


def menu_funcionario():
    estoque: Estoque = Estoque()

    while True:
        print('-' * 60)

        print('Selecione uma opção:')
        print('1 - Cadastrar produto')
        print('2 - Listar produtos')
        print('3 - Remover produto')
        print('4 - Guardar produtos no sistema')
        print('5 - Carregar produtos do sistema')
        print('6 - Voltar')
        print('7 - Sair do sistema')

        opcao: int = verifica_int('Digite a opção: ')

        if opcao == 1:
            nome: str = str(input('Digite o nome do produto: '))
            preco: float = verifica_float('Digite o preço do produto: ')
            quantidade: int = verifica_int('Digite a quantidade: ')
            produto = Produto(nome, preco, quantidade)
            estoque.cadastrar_produto_estoque(produto)
            sleep(2)
        elif opcao == 2:
            estoque.listar_produtos_estoque()
            sleep(2)
        elif opcao == 3:
            produto: str = str(input('Digite o nome do produto: '))
            quantidade: int = verifica_int('Digite a quantidade: ')
            estoque.remover_produto_estoque(produto, quantidade)
        elif opcao == 4:
            estoque.guardar_produtos()
            sleep(2)
        elif opcao == 5:
            estoque.carregar_produtos()
            sleep(2)
        elif opcao == 6:
            menu_base()
        elif opcao == 7:
            print('Volte sempre :)')
            sleep(1)
            exit()
        else:
            print('Opção inválida!')


def menu_cliente():
    carrinho: Carrinho = Carrinho()

    while True:
        print('-' * 60)

        print('Selecione uma opção:')
        print('1 - Visualizar produtos')
        print('2 - Adicionar produto no carrinho')
        print('3 - Remover produto do carrinho')
        print('4 - Visualizar carrinho')
        print('5 - Fechar pedido')
        print('6 - Voltar')
        print('7 - Sair')

        opcao: int = verifica_int('Digite a opção: ')

        if opcao == 1:
            carrinho.estoque.listar_produtos_estoque()
            sleep(2)
        elif opcao == 2:
            produto: str = str(input('Digite o nome do produto: '))
            quantidade = verifica_int('Digite a quantidade: ')
            carrinho.adicionar_produto_carrinho(produto, quantidade)
            sleep(2)
        elif opcao == 3:
            produto: str = str(input('Digite o nome do produto: '))
            quantidade = verifica_int('Digite a quantidade: ')
            carrinho.remover_produto_carrinho(produto, quantidade)
        elif opcao == 4:
            carrinho.visualizar_carrinho()
            sleep(2)
        elif opcao == 5:
            carrinho.finalizar_carrinho()
            print('Volte sempre :)')
            sleep(1)
            exit()
        elif opcao == 6:
            menu_base()
        elif opcao == 7:
            print('Volte sempre :)')
            sleep(1)
            exit()
        else:
            print('Opção inválida!')
