from verifica.verifica_dado import verifica_int, verifica_float
from models.produtos import Produtos
from time import sleep


def menu_base(prod: Produtos = None):
    if prod is None:
        prod = Produtos()

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
            menu_funcionario(prod)
        elif opcao == 2:
            menu_cliente(prod)
        elif opcao == 3:
            break
        else:
            print('Opção inválida!')


def menu_funcionario(prod: Produtos):
    while True:
        print('-' * 60)

        print('Selecione uma opção:')
        print('1 - Cadastrar produto')
        print('2 - Listar produtos')
        print('3 - Remover produto')
        print('4 - Carregar produtos do sistema')
        print('5 - Guardar produtos no sistema')
        print('6 - Voltar')
        print('7 - Sair do sistema')

        opcao: int = verifica_int('Digite a opção: ')

        if opcao == 1:
            produto: str = str(input('Digite o nome do produto: '))
            preco: float = verifica_float('Digite o preço do produto: ')
            quantidade: int = verifica_int('Digite a quantidade: ')
            prod.cadastrar_produto_estoque(produto, preco, quantidade)
            sleep(2)
        elif opcao == 2:
            prod.listar_produtos_estoque()
            sleep(2)
        elif opcao == 3:
            produto: str = str(input('Digite o nome do produto: '))
            quantidade: int = verifica_int('Digite a quantidade: ')
            prod.remover_produto_estoque(produto, quantidade)
        elif opcao == 4:
            pass
        elif opcao == 5:
            pass
        elif opcao == 6:
            menu_base(prod)
        elif opcao == 7:
            print('Volte sempre :)')
            sleep(1)
            exit()
        else:
            print('Opção inválida!')


def menu_cliente(prod: Produtos):
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
            prod.listar_produtos_estoque()
            sleep(2)
        elif opcao == 2:
            produto: str = str(input('Digite o nome do produto: '))
            prod.adicionar_produto_carrinho(produto)
            sleep(2)
        elif opcao == 3:
            produto: str = str(input('Digite o nome do produto: '))
            prod.remover_produto_carrinho(produto)
        elif opcao == 4:
            prod.visualizar_carrinho()
            sleep(2)
        elif opcao == 5:
            prod.finalizar_carrinho()
            print('Volte sempre :)')
            sleep(1)
            exit()
        elif opcao == 6:
            menu_base(prod)
        elif opcao == 7:
            print('Volte sempre :)')
            sleep(1)
            exit()
        else:
            print('Opção inválida!')
