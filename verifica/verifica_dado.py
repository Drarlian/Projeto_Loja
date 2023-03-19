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
