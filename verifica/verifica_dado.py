def verifica_int(mensagem: str) -> int:
    while True:
        try:
            valor = int(input(mensagem))
        except (ValueError, TypeError):
            print('Digite uma opção válida!')
        except KeyboardInterrupt:
            print('\nO usuário optou por não continuar.')
            exit()
        else:
            return valor


def verifica_float(mensagem: str) -> float:
    while True:
        try:
            valor = float(input(mensagem))
        except (ValueError, TypeError):
            print('Digite uma opção válida!')
        except KeyboardInterrupt:
            print('\nO usuário optou por não continuar.')
            exit()
        else:
            return valor


def verifica_decisao(mensagem: str) -> str:
    while True:
        try:
            opcao = str(input(mensagem)).strip().upper()[0]
        except (TypeError, ValueError):
            print('Digite uma opção válida!')
        except KeyboardInterrupt:
            print('\nO usuário escolheu não continuar.')
            exit()
        else:
            if opcao == 'S' or opcao == 'N':
                return opcao
            else:
                print('Digite uma opção válida!')