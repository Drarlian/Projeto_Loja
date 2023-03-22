class Produto:
    contador: int = 1

    def __init__(self, nome: str, preco: float, quantidade: int = 1) -> None:
        self.__id: int = Produto.contador
        self.__nome: str = nome.lower()
        self.__preco: float = preco
        self.__quantidade: int = quantidade
        Produto.contador += 1

        """
        if self.__verificar_arquivo_estoque():
            self.__id: int = self.__pegar_ultimo_id() + 1
        else:
            self.__id: int = Produto.contador
            Produto.contador += 1
        """

    @property
    def id(self) -> int:
        return self.__id

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str) -> None:
        self.__nome = nome

    @property
    def preco(self) -> float:
        return self.__preco

    @preco.setter
    def preco(self, preco: float) -> None:
        self.__preco = preco

    @property
    def quantidade(self) -> int:
        return self.__quantidade

    @quantidade.setter
    def quantidade(self, quantidade: int) -> None:
        self.__quantidade = quantidade

    def __str__(self) -> str:
        return f'Id: {self.id} | Produto: {self.nome} | Preço: R${self.preco} | Quantidade: {self.quantidade}'

    """
    def __verificar_arquivo_estoque(self) -> bool:
        import os

        caminho: str = 'dados\\info_estoque.json'
        if os.path.exists(caminho):
            return True
        return False
    """

    """
    def __pegar_ultimo_id(self) -> int:
        import jsonpickle

        caminho: str = 'dados\\info_estoque.json'
        with open(caminho, 'r', encoding='UTF-8') as arquivo:
            conteudo = arquivo.read()
            ret: Estoque = jsonpickle.decode(conteudo)

        return ret['Produtos'][-1].id
    """

class Estoque:
    def __init__(self) -> None:
        self.__estoque: list = []

    @property
    def estoque(self) -> list:
        return self.__estoque

    @estoque.setter
    def estoque(self, estoque: list) -> None:
        self.__estoque = estoque

    def cadastrar_produto_estoque(self, item: Produto) -> None:
        self.estoque.append(item)
        print(f'{item.nome}(x{item.quantidade}) foi adicionado ao estoque.')

    def remover_produto_estoque(self, nome: str, quantidade: int = 1):
        if self.verificar_produto_existe_estoque(nome):
            self.diminuir_quantidade_estoque(nome, quantidade, informa=True)

    def recadastrar_produto_estoque(self, nome: str, preco: float, quantidade: int, *, exibe_mensagem: bool = True) -> None:
        if self.verificar_produto_existe_estoque(nome, exibe_mensagem=exibe_mensagem):
            self.aumentar_quantidade_estoque(nome, quantidade)
        else:
            prod = Produto(nome, preco, quantidade)
            self.estoque.append(prod)

    def listar_produtos_estoque(self) -> None:
        if len(self.estoque) > 0:
            print('Produtos Disponíveis:')
            for item in self.estoque:
                print(item)
        else:
            print('O estoque está vazio.')

    def aumentar_quantidade_estoque(self, nome: str, quantidade: int = 1) -> None:
        for produto in self.estoque:
            if nome.lower() == produto.nome:
                produto.quantidade += quantidade
                break

    def diminuir_quantidade_estoque(self, nome: str, quantidade: int = 1, *, informa: bool = False) -> None:
        for produto in self.estoque:
            if nome.lower() == produto.nome:
                if (produto.quantidade == 1) or (produto.quantidade == quantidade):
                    if quantidade > produto.quantidade:
                        print('Quantidade inválida!')
                        quantidade = 1
                    self.estoque.remove(produto)
                    break
                else:
                    if produto.quantidade > quantidade:
                        produto.quantidade -= quantidade
                    else:
                        print('Quantidade inválida!')
                        quantidade = 1
                        produto.quantidade -= 1
                break

        if informa:
            print(f'{nome.capitalize()}(x{quantidade}) foi removido(a) do estoque.')

    def verificar_produto_existe_estoque(self, nome: str, *, exibe_mensagem: bool = True) -> bool:
        if len(self.estoque) > 0:
            for produto in self.estoque:
                if nome.lower() == produto.nome:
                    return True

            if exibe_mensagem:
                print(f'{nome.capitalize()} não exite no estoque.')
            return False

        if exibe_mensagem:
            print('O estoque está vazio.')

    def guardar_produtos(self, exibe_mensagem: bool = True) -> None:
        import jsonpickle
        from datetime import datetime

        data: datetime = datetime.now()

        with open('dados\\info_estoque.json', 'w', encoding='UTF-8') as arquivo:
            ret: str = jsonpickle.encode({'Produtos': self.estoque,
                                         'Historico': [f'{data.strftime("%d/%m/%Y")}', f'{data.strftime("%H:%M:%S")}']})
            arquivo.write(ret)

        if exibe_mensagem:
            print('Dados do estoque armazenados.')

    def carregar_produtos(self, *, certeza: bool = True) -> None:
        from verifica.verifica_dado import verifica_decisao
        import jsonpickle
        from os import path

        if certeza:
            decisao: str = verifica_decisao('Tem certeza que deseja sobrescrever o estoque atual? [S/N] ')
        else:
            decisao = 'S'

        if decisao == 'S':
            caminho: str = 'dados\\info_estoque.json'
            if path.exists(caminho):
                with open(caminho, 'r', encoding='UTF-8') as arquivo:
                    conteudo = arquivo.read()
                    ret: Estoque = jsonpickle.decode(conteudo)

                self.estoque = ret['Produtos']
                if certeza:
                    print('Estoque atualizado.')
            else:
                print('Não existem dados armazenados.')
        else:
            print('Ok, o estoque NÃO foi sobrescrito.')

class Carrinho:
    def __init__(self) -> None:
        self.__estoque: Estoque = Estoque()
        self.__estoque.carregar_produtos(certeza=False)
        self.__carrinho: list = []
        self.__preco_total: float = 0

    @property
    def carrinho(self) -> list:
        return self.__carrinho

    @carrinho.setter
    def carrinho(self, carrinho: list) -> None:
        self.__carrinho = carrinho

    @property
    def preco_total(self) -> float:
        return self.__preco_total

    @preco_total.setter
    def preco_total(self, preco_total: float) -> None:
        self.__preco_total = preco_total

    @property
    def estoque(self) -> Estoque:
        return self.__estoque

    @estoque.setter
    def estoque(self, estoque: Estoque) -> None:
        self.__estoque = estoque

    def adicionar_produto_carrinho(self, nome: str, quantidade: int = 1) -> None:
        import copy
        if self.estoque.verificar_produto_existe_estoque(nome, exibe_mensagem=False):
            if not self.__confirma_quantidade_estoque(nome, quantidade):
                print('Quantidade insuficiente no estoque.')
                print('Quantidade definida como: 1')
                quantidade = 1

            if self.__verifica_produto_existe_carrinho(nome, exibe_mensagem=False):
                self.__aumentar_quantidade_carrinho(nome, quantidade)
            else:
                produto_temporario = copy.deepcopy(self.__converter_nome_para_objeto(nome))
                produto_temporario.quantidade = quantidade
                self.carrinho.append(produto_temporario)

            self.estoque.diminuir_quantidade_estoque(nome, quantidade)
            self.__aumentar_preco_total(nome, quantidade)

            print(f'{nome.capitalize()}(x{quantidade}) foi adicionado(a) ao carrinho.')
        else:
            print('Produto indisponível.')

    def remover_produto_carrinho(self, nome: str, quantidade: int = 1) -> None:
        if self.__verifica_produto_existe_carrinho(nome):
            self.__diminuir_quantidade_carrinho(nome, quantidade)

    def visualizar_carrinho(self):
        if len(self.carrinho) > 0:
            print('Produtos Disponíveis:')
            for item in self.carrinho:
                print(f'Produto: {item.nome} | Preço: {item.preco} | Quantidade: {item.quantidade}')
        else:
            print('O carrinho está vazio.')

    def __verifica_produto_existe_carrinho(self, nome: str, exibe_mensagem: bool = True) -> bool:
        if len(self.carrinho) > 0:
            for item in self.carrinho:
                if nome.lower() == item.nome:
                    return True

            if exibe_mensagem:
                print(f'{nome.capitalize()} não existe no carrinho.')
            return False

        if exibe_mensagem:
            print('O carrinho está vazio.')

    def __confirma_quantidade_estoque(self, nome: str, quantidade: int) -> bool:
        for item in self.estoque.estoque:
            if nome.lower() == item.nome:
                if item.quantidade >= quantidade:
                    return True
        return False

    def __confirma_quantidade_carrinho(self, nome: str, quantidade: int) -> bool:
        for item in self.carrinho:
            if nome.lower() == item.nome:
                if item.quantidade >= quantidade:
                    return True
        return False

    def __aumentar_quantidade_carrinho(self, nome: str, quantidade: int = 1) -> None:
        for item in self.carrinho:
            if nome.lower() == item.nome:
                item.quantidade += quantidade

    def __diminuir_quantidade_carrinho(self, nome: str, quantidade: int = 1) -> None:
        if not self.__confirma_quantidade_carrinho(nome, quantidade):
            print('Quantidade insuficiente no carrinho.')
            print('Quantidade definida como: 1')
            quantidade = 1

        for item in self.carrinho:
            if nome.lower() == item.nome:
                if item.quantidade == quantidade:
                    self.estoque.recadastrar_produto_estoque(item.nome, item.preco, quantidade, exibe_mensagem=False)
                    self.__diminuir_preco_total(nome, quantidade)
                    self.carrinho.remove(item)
                    break
                else:
                    self.estoque.recadastrar_produto_estoque(item.nome, item.preco, quantidade, exibe_mensagem=False)
                    self.__diminuir_preco_total(nome, quantidade)
                    item.quantidade -= quantidade
                    break

        print(f'{nome.capitalize()}(x{quantidade}) foi removido(a) do carrinho.')

    def __aumentar_preco_total(self, nome: str, quantidade: int = 1) -> None:
        for item in self.carrinho:
            if nome.lower() == item.nome:
                self.preco_total += (item.preco * quantidade)
                break

    def __diminuir_preco_total(self, nome: str, quantidade: int = 1) -> None:
        for item in self.carrinho:
            if nome.lower() == item.nome:
                self.preco_total -= (item.preco * quantidade)
                break

    def __converter_nome_para_objeto(self, nome: str) -> Produto:
        for item in self.estoque.estoque:
            if nome.lower() == item.nome:
                return item

    def finalizar_carrinho(self):
        if len(self.carrinho) > 0:
            print('Produtos no carrinho:')
            for item in self.carrinho:
                print(f'{item.nome} | R${item.preco} | x{item.quantidade}')

            print(f'O valor total é de R${self.preco_total:.2f}')
            self.estoque.guardar_produtos(exibe_mensagem=False)
        else:
            print('O carrinho está vazio.')
