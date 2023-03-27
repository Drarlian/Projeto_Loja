class Produto:
    def __init__(self, nome: str, preco: float, quantidade: int = 1) -> None:
        if self.verificar_produto_existe_no_estoque(nome):
            produto = self.__pegar_dados_produto(nome)
            self.__id: int = produto.id
            self.__nome: str = nome.lower()
            self.__preco: float = preco
            self.__quantidade: int = produto.quantidade + quantidade
        else:
            self.__id: int = self.__gerar_id_produto()
            self.__nome: str = nome.lower()
            self.__preco: float = preco
            self.__quantidade: int = quantidade

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
        return f'Id: {self.id} | Produto: {self.nome} | Preço: R${self.preco:.2f} | Quantidade: {self.quantidade}'


    def verificar_produto_existe_no_estoque(self, nome: str) -> bool:
        """
        Verifico se o produto com o nome informado existe no arquivo "info_estoque.json"
        """
        from os import path
        from jsonpickle import decode

        caminho: str = 'dados\\info_estoque.json'

        if path.exists(caminho):
            with open(caminho, 'r', encoding='UTF-8') as arquivo:
                conteudo: str = arquivo.read()
            if conteudo != '':
                ret: dict = decode(conteudo)
                for produto in ret['Produtos']:
                    if produto.nome == nome.lower():
                        return True
        return False

    def __pegar_dados_produto(self, nome: str):
        from jsonpickle import decode

        caminho: str = 'dados\\info_estoque.json'

        with open(caminho, 'r', encoding='UTF-8') as arquivo:
            conteudo: str = arquivo.read()
            ret: dict = decode(conteudo)
            for produto in ret['Produtos']:
                if produto.nome == nome.lower():
                    return produto
        return False

    def __gerar_id_produto(self) -> int:
        from os import path
        from jsonpickle import decode

        caminho = 'dados\\info_estoque.json'

        if path.exists(caminho):
            with open(caminho, 'r', encoding='UTF-8') as arquivo:
                conteudo: str = arquivo.read()
            if conteudo != '':
                ret: dict = decode(conteudo)
                maior_id: int = None
                comeco: bool = True
                for produto in ret['Produtos']:
                    if comeco:
                        maior_id = produto.id
                        comeco = False
                    else:
                        if produto.id > maior_id:
                            maior_id = produto.id
                return maior_id + 1
        return 1


class Estoque:
    def __init__(self) -> None:
        self.__estoque: list = None
        self.carregar_produtos(certeza=False)

    @property
    def estoque(self) -> list:
        return self.__estoque

    @estoque.setter
    def estoque(self, estoque: list) -> None:
        self.__estoque = estoque

    def cadastrar_produto_estoque(self, nome: str, preco: float, quantidade: int = 1) -> None:
        if self.verificar_produto_existe_estoque(nome.lower(), exibe_mensagem=False):
            self.__atualizar_preco_produto(nome, preco)
            self.aumentar_quantidade_estoque(nome.lower(), quantidade)
            print(f'{nome.lower()} já existia no estoque, foram adicionadas x{quantidade} unidades')
        else:
            produto = Produto(nome, preco, quantidade)
            self.estoque.append(produto)
            print(f'{nome.lower()}(x{quantidade}) foi adicionado ao estoque.')
            self.guardar_produtos(exibe_mensagem=False)

    def remover_produto_estoque(self, nome: str, quantidade: int = 1):
        if self.verificar_produto_existe_estoque(nome):
            self.diminuir_quantidade_estoque(nome, quantidade, informa=True)

    def recadastrar_produto_estoque(self, nome: str, preco: float, quantidade: int, *, exibe_mensagem: bool = True) -> None:
        if self.verificar_produto_existe_estoque(nome, exibe_mensagem=exibe_mensagem):
            self.aumentar_quantidade_estoque(nome, quantidade)
        else:  # -> Esse else não vai acontecer nunca, pois os produtos não são mais removidos do estoque.
            prod = Produto(nome, preco, quantidade)
            self.estoque.append(prod)
            self.guardar_produtos(exibe_mensagem=False)

    def __atualizar_preco_produto(self, nome: str, preco: float) -> None:
        for produto in self.__estoque:
            if produto.nome == nome:
                produto.preco = preco

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
        self.guardar_produtos(exibe_mensagem=False)

    def diminuir_quantidade_estoque(self, nome: str, quantidade: int = 1, *, informa: bool = False) -> None:
        for produto in self.estoque:
            if nome.lower() == produto.nome:
                if (produto.quantidade == 1) or (produto.quantidade == quantidade):
                    if quantidade > produto.quantidade:
                        print('Quantidade inválida!')
                        quantidade = 1
                    produto.quantidade = 0
                    break
                elif produto.quantidade == 0:
                    informa = False
                    print(f'Não existem unidades de {nome.lower()} no estoque.')
                else:
                    if produto.quantidade > quantidade:
                        produto.quantidade -= quantidade
                    else:
                        print('Quantidade inválida!')
                        quantidade = 1
                        produto.quantidade -= 1
                break
        self.guardar_produtos(exibe_mensagem=False)

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

    def verificar_quantidade_produto_igual_zero(self, nome: str) -> bool:
        for produto in self.estoque:
            if produto.nome == nome.lower():
                if produto.quantidade == 0:
                    return True
                else:
                    return False

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
                if conteudo != '':
                    ret: Estoque = jsonpickle.decode(conteudo)

                    self.estoque = ret['Produtos']
                    if certeza:
                        print('Estoque atualizado.')
                else:
                    print('Não existem dados no estoque.')
            else:
                print('Não existem dados armazenados.')
        else:
            print('Ok, o estoque NÃO foi sobrescrito.')

class Carrinho:
    def __init__(self) -> None:
        self.__estoque: Estoque = Estoque()
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
            if not self.estoque.verificar_quantidade_produto_igual_zero(nome):
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
                print('Produto esgotado.')
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
