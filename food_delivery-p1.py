molde_item = ['Código', 'Nome', 'Descrição', 'Preço', 'Estoque']
molde_pedido = ['Código', 'Cliente', ['Item', 'Quantidade'], 'Status', 'Subtotal', 'Total', 'Cupom']
itens = []
pedidos = []


print ('=== MENU === \n'
        '(0) Sair\n'
        '(1) Cadastrar Item\n'
        '(2) Atualizar Item\n'
        '(3) Consultar Itens\n'
        '(4) Detalhar item\n'
        '(5) Criar Pedido')

while True:
        try:
            usuario = int(input('Insira sua opção: '))
            break
        except:
            print('\n-----\nInsira um numero inteiro ou valido\n-----\n')

while usuario != 0:

    def CadastrarItem():
        sublista = []
        caracteristica = None

        # Gerador de codigo
        if itens != []:
            caracteristica = itens[-1][0] + 1
        else:
            caracteristica = 1
        sublista.append(caracteristica)
        '''
        for i in molde_item:
            if i != 'Código':
                caracteristica = input(f'{i}: ')
                sublista.append(caracteristica)
        '''
        # Nome
        while type(caracteristica) != str:
            try:
                caracteristica = input(f'Nome: ')
                caracteristica = float(caracteristica)
                print('O nome não pode conter apenas números!')
            except:
                sublista.append(caracteristica)
        else:
            caracteristica = None
        # Descrição
        while type(caracteristica) != str:
            try:
                caracteristica = input(f'Descrição: ')
                caracteristica = float(caracteristica)
                print('A descrição não pode conter apenas números!')
            except:
                sublista.append(caracteristica)
        else:
            caracteristica = None
        # Preço
        while type(caracteristica) != float:
            try:
                caracteristica = float(input(f'Preço: '))
                sublista.append(caracteristica)
            except:
                print('\n-----\nInsira um número válido!\n-----\n')
        else:
            caracteristica = None
        # Estoque
        while type(caracteristica) != int:
            try:
                caracteristica = int(input(f'Estoque: '))
                sublista.append(caracteristica)
            except:
                print('\n-----\nInsira um número válido!\n-----\n')

        itens.append(sublista)

        #return formatarSaida(sublista, 'item')

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
                        itens[contador][j+1] = input(f'{molde_item[j+1]}: ') 
                        
                    return formatarSaida(i, 'item')
                contador += 1

            if validar != 1:
                print('Insira um número válido')
            
    def consultarItens(codigo=0):
        if codigo == 0:
            return formatarSaida(itens, 'item')
        else:
            for i in itens:
                if i[0] == codigo:
                    return formatarSaida(i, 'item')

    def formatarSaida(identificador, categoria):
        
        if categoria == 'pedido':
            pass

        if categoria == 'item':
            if type(identificador) == list:
                print(f"{'ID':<5}{'Nome':<15}{'Descrição':<20}{'Preço':<10}{'Estoque':<10}")
                print('-'*60)
                for i in itens:
                    print(f"{i[0]:<5}{i[1]:<15}{i[2]:<20}{i[3]:<10}{i[4]:<10}")
            elif type(identificador) == int:
                    print(f"{'ID':<5}{'Nome':<15}{'Descrição':<20}{'Preço':<10}{'Estoque':<10}")
                    print('-'*60)
                    for i in itens:
                        if identificador == i[0]:
                            print(f"{i[0]:<5}{i[1]:<15}{i[2]:<20}{i[3]:<10}{i[4]:<10}")
            else:
                print('Entrada não suportada!')
            
        if categoria == 'carrinho':
            print(f"{'ID':<5}{'Nome':<15}{'Quantidade':<5}")
            print('-'*45)
            for i in identificador:
                print(f"{i[0]:<5}{i[1]:<15}{i[2]:<5}")
            
        return ''

    def criar_pedido():
        sublista = []
        user_pedido = None
        cupons = [
            ["DESC10", 0.10],
            ["DESC20", 0.20],
            ["FRETE5", 0.05], 
            ["DESC30", 0.30],
            ["VALE20", 20.00]  
        ]
        verificar_cupom = 0

        # Código
        if pedidos != []:
            user_pedido = int(pedidos[-1][0]) + 1
        else:
            user_pedido = 1
            sublista.append(user_pedido)

        # Cliente
        user_pedido = str(input('Nome do Cliente: '))
        sublista.append(user_pedido)

        # Item e quantidade
        def comprar(user_pedido):
            carrinho = []
            comprar = []
            print(formatarSaida(itens, 'item'))
            while user_pedido != '0':
                comprar = []
                # Item
                user_pedido = input('Id do Item (0 para sair): ')
                if user_pedido == '0':
                    print('\n-----\nCarrinho Fechado!\n-----')
                else:
                    for i in itens:
                        if str(i[0]) == user_pedido:
                            comprar.append(user_pedido)
                            comprar.append(i[1])
                            user_pedido = input('Quantidade: ')
                            comprar.append(int(user_pedido))
                            carrinho.append(comprar)
                            print(formatarSaida(carrinho, 'carrinho'))
                        else:
                            print('---\nInsira um Id válido!\n---\n')

            sublista.append(carrinho)    
        
        comprar(user_pedido)
            
        # Cupom
        while user_pedido not in ['1','2']:
            user_pedido = input('Você possui cupom de desconto?:\n'
            '(1) Sim\n'
            '(2) Não\n\n'
            'Resposta: ')

            if user_pedido not in ['1','2']:
                print('Insira uma opção válida!')

        if user_pedido == '1':
            while verificar_cupom != 1 or user_pedido == '0':
                user_pedido = input('Insira o cupom (0 para sair): ')
                for i in cupons:
                    if i[0] == user_pedido:
                        verificar_cupom = 1
                        print(f'Desconto aplicado de {i[1] * 100}%')
                if verificar_cupom != 1:
                    print('Cupom inválido, tente novamente!')
            if user_pedido == '0':
                print('Deseja prosseguir sem cupom?'
                '(1) Sim'
                '(2) Cancelar')

        pedidos.append(sublista)
        return f'{sublista}\n\nPedido Concluído!'

    def monstrarPedido():
        return pedidos

    if usuario == 1:
        print(CadastrarItem())
    elif usuario == 2:
        print(atualizarItem())
    elif usuario == 3:
        print(consultarItens())
    elif usuario == 4:
        pass
    elif usuario == 5:
        print(criar_pedido())
    elif usuario == 6:
        monstrarPedido

    print ('=== MENU === \n'
        '(0) Sair\n'
        '(1) Cadastrar Item\n'
        '(2) Atualizar Item\n'
        '(3) Consultar Itens\n'
        '(4) Detalhar item\n'
        '(5) Criar Pedido\n'
        '(6) Mostrar pedidos')

    while True:
        try:
            usuario = int(input('Insira sua opção: '))
            break
        except:
            print('\n-----\nInsira um numero inteiro ou valido\n-----\n')