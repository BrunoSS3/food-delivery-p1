molde = ['id', 'Nome', 'Descrição', 'Preço', 'Estoque']
itens = []


while True:

    print ('=== MENU === \n'
        '(1) Cadastrar Item\n'
        '(2) Atualizar Item\n'
        '(3) Consultar Itens\n')

    while True:
        try:
            usuario = int(input('Insira sua opção: '))
            break
        except:
            print('insira um numero inteiro ou valido')

    def CadastrarItem():
        sublista = []
        caracteristica = None

        # Gerador de codigo
        if itens != []:
            caracteristica = itens[-1][0] + 1
        else:
            caracteristica = 1
        sublista.append(caracteristica)

        caracteristica = input('Nome: ')
        sublista.append(caracteristica)

        caracteristica = input('Descrição: ')
        sublista.append(caracteristica)

        caracteristica = input('Preço: ')
        sublista.append(caracteristica)

        caracteristica = input('Estoque: ')
        sublista.append(caracteristica)

        itens.append(sublista)

        return formatarSaida(sublista)

    def atualizarItem():
        if itens == []:
            return ('Não há itens cadastrados')

        contador = 0
        validar = 0

        while validar != 1:
            try:
                id_produto = int(input('Insira o id do produto que você quer editar: '))
            except:
                print('Insira um numero inteiro')

            for i in itens:
                if i[0] == id_produto:
                    validar = 1
                    for j in range(0, (len(i)-1)):
                        itens[contador][j+1] = input(f'{molde[j+1]}: ') 
                        
                    return formatarSaida(i)
                contador += 1

            if validar != 1:
                print('Insira um número válido')
            
    def consultarItens(codigo=0):
        if codigo == 0:
            return formatarSaida(itens)
        else:
            for i in itens:
                if i[0] == codigo:
                    return formatarSaida(i)

    def formatarSaida(identificador):
    
        if type(identificador) == list:
            print(f"{'ID':<5}{'Nome':<15}{'Descrição':<20}{'Preço':<10}{'Estoque':<10}")
            print('-'*60)
            for i in itens:
                print(f"{i[0]:<5}{i[1]:<15}{i[2]:<20}{i[3]:<10}{i[4]:<10}")
        elif type(identificador) == int:
                print(f"{'ID':<5}{'Nome':<15}{'Descrição':<20}{'Preço':<10}{'Estoque':<10}")
                for i in itens:
                    if identificador == i[0]:
                        print(f"{i[0]:<5}{i[1]:<15}{i[2]:<20}{i[3]:<10}{i[4]:<10}")
        else:
            print('Entrada não suportada!')

    if usuario == 1:
        print(CadastrarItem())
    elif usuario == 2:
        print(atualizarItem())
    elif usuario == 3:
        print(consultarItens())