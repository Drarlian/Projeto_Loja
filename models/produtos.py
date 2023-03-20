class Produtos:
    def __init__(self):
        self.__estoque: list = []
        self.__carrinho: list = []
        self.__preco_total: float = 0

    @property
    def estoque(self) -> list:
        return self.__estoque

    @estoque.setter
    def estoque(self, estoque: list) -> None:
        self.__estoque = estoque

    @property
    def carrinho(self) -> list:
        return self.__carrinho

    @property
    def preco_total(self) -> float:
        return self.__preco_total

    @preco_total.setter
    def preco_total(self, preco_total: float) -> None:
        self.__preco_total = preco_total

    def cadastrar_produto_estoque(self, item: str, preco: float, quantidade: int = 1) -> None:
        self.estoque.append([item.lower(), preco, quantidade])
        print(f'{item.capitalize()} foi adicionado(a) ao estoque.')

    def remover_produto_estoque(self, item: str, quantidade: int = 1) -> None:
        existe, _ = self.__verifica_produto_existe_estoque(item)
        if existe:
            self.__diminuir_quantidade_estoque(item, quantidade, informa=True)
        else:
            print(f'{item.capitalize()} não existe no estoque.')

    def listar_produtos_estoque(self) -> None:
        if len(self.estoque) > 0:
            print('Produtos Disponíveis:')
            for item, preco, quantidade in self.estoque:
                print(f'Produto: {item} | Preço: R${preco} | Quantidade: {quantidade}')
        else:
            print('O estoque está vazio.')

    def __recadastrar_produto_estoque(self, item: str, preco: float, quantidade: int):
        existe, _ = self.__verifica_produto_existe_estoque(item)
        if existe:
            self.__aumentar_quantidade_estoque(item)
        else:
            self.estoque.append([item, preco, quantidade])

    def adicionar_produto_carrinho(self, item: str) -> None:
        existe_estoque, preco = self.__verifica_produto_existe_estoque(item)
        if existe_estoque:
            self.__diminuir_quantidade_estoque(item)
            self.preco_total += preco

            if self.__verifica_produto_existe_carrinho(item):
                self.__aumentar_quantidade_carrinho(item)
            else:
                self.carrinho.append([item.lower(), preco, 1])

            print(f'{item.capitalize()} foi adicionado(a) ao carrinho.')
        else:
            print('Produto indisponível.')

    def remover_produto_carrinho(self, item: str) -> None:
        if self.__verifica_produto_existe_carrinho(item):
            self.__diminuir_quantidade_carrinho(item)
            print(f'{item.capitalize()}(x1) foi removido(a) do carrinho.')
        else:
            print(f'{item.capitalize()} não existe no carrinho.')

    def visualizar_carrinho(self) -> None:
        if len(self.carrinho) > 0:
            print('Carrinho:')
            for item, preco, quantidade in self.carrinho:
                print(f'{item} | R${preco} | x{quantidade}')
        else:
            print('O carrinho está vazio.')

    def finalizar_carrinho(self) -> None:
        if len(self.carrinho) > 0:
            for item, valor, quantidade in self.carrinho:
                print(f'{item} | R${valor} | x{quantidade}')

            print(f'O valor total é de R${self.preco_total:.2f}')
        else:
            print('O carrinho está vazio.')

    def __verifica_produto_existe_estoque(self, item: str) -> tuple:
        if len(self.estoque) > 0:
            for i in self.estoque:
                if item.lower() == i[0]:
                    return True, i[1]

        return False, None

    def __verifica_produto_existe_carrinho(self, item: str) -> bool:
        if len(self.carrinho) > 0:
            for i in self.carrinho:
                if item.lower() == i[0]:
                    return True

        return False

    def __aumentar_quantidade_carrinho(self, item: str) -> None:
        for i in self.carrinho:
            if item.lower() == i[0]:
                i[2] += 1
                break

    def __diminuir_quantidade_carrinho(self, item) -> None:
        for i in self.carrinho:
            if i[0] == item.lower():
                if i[2] == 1:
                    self.__recadastrar_produto_estoque(i[0], i[1], 1)
                    self.carrinho.remove(i)
                    break
                else:
                    self.__recadastrar_produto_estoque(i[0], i[1], 1)
                    i[2] -= 1
                    break

    def __aumentar_quantidade_estoque(self, item: str) -> None:
        for i in self.estoque:
            if item.lower() == i[0]:
                i[2] += 1
                break

    def __diminuir_quantidade_estoque(self, item, quantidade=1, *, informa: bool = False) -> None:
        for i in self.estoque:
            if item.lower() == i[0]:
                if i[2] == 1:
                    if quantidade > 1:
                        print('Quantidade inválida!')
                        quantidade = 1
                    self.estoque.remove(i)
                    break
                else:
                    if i[2] > quantidade:
                        i[2] -= quantidade
                    elif i[2] == quantidade:
                        self.estoque.remove(i)
                    else:
                        print('Quantidade inválida!')
                        quantidade = 1
                        i[2] -= 1
                    break

        if informa:
            print(f'{item.capitalize()}(x{quantidade}) foi removido(a) do estoque.')

    def guardar_produtos(self) -> None:
        from json import dumps
        from datetime import datetime

        data: datetime = datetime.now()

        with open('dados\\info_estoque.json', 'w', encoding='UTF-8') as arquivo:
            ret: str = dumps({'Produtos': self.estoque, 'Historico': [f'{data.strftime("%d/%m/%Y")}', f'{data.strftime("%H:%M:%S")}']})
            arquivo.write(ret)
        print('Dados do estoque armazenados.')

    def carregar_produtos(self) -> None:
        from verifica.verifica_dado import verifica_decisao
        import json
        import os

        decisao: str = verifica_decisao('Tem certeza que deseja sobrescrever o estoque atual? [S/N] ')

        if decisao == 'S':
            caminho: str = 'dados\\info_estoque.json'
            if os.path.exists(caminho):
                with open(caminho, 'r', encoding='UTF-8') as arquivo:
                    ret: dict = json.load(arquivo)

                self.estoque = ret['Produtos']
                print('Estoque atualizado.')
            else:
                print('Não existem dados armazenados.')
        else:
            print('Ok, o estoque NÃO foi sobrescrito.')
