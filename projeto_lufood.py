'''
bibliografia:

produto:
0 nome
1 sequencia_cod
2 preco
3 descricao
4 quantidade_estoque

pedido:
0 codigo
1 itens
2 valor_total
3 cupom
4 status

'''

# Base do projeto
"""
menu de itens
cadastro -> atualização -> consulta
detalhes do itens

"""
# Lista para guardar todos os itens que forem cadastrados.
pedidos_pendentes = []
pedidos_aceitos = []
pedidos_prontos = []
todos_pedidos = []
itens = []
# gerador de códigos (incrementar)
sequencia_cod = 1

def cadastrar_item():
    nome = input("Nome do item: ")
    descricao = input("Descrição do item: ")
    preco = None
    quantidade_estoque = None

    # Tratar preco e quantidade para ser float e int
    while type(preco) != float:
        try:
            preco = float(input("Preço do item: "))
        except:
            print('\n-----Insira um número válido!-----\n')
    
    while type(quantidade_estoque) != int:
        try:
            quantidade_estoque = int(input("Quantidade em estoque: "))
        except:
            print('\n-----Insira um número válido!-----\n')

    global sequencia_cod

    produto = [nome, sequencia_cod, preco, descricao, quantidade_estoque]

    itens.append(produto) # adiciona o produto na lista de itens (final)
    sequencia_cod += 1 # incrementa +1 na variável global 'sequencia_cod'
    print(f"Novo item: {produto[0]}. Cadastrado com sucesso!")
    return produto

def modificar_itens():
    # novamente verifica se há itens cadastrados, se não houver, retorna essa mensagem mensagem e sai da função
    if len(itens) == 0:
        print("Sem dados de cadastro no item.")
        return
    # mostra todos os itens cadastrados e que podem sofrer modificção
    print("Itens cadastrados:") # for (para) cada item na lista de itens (in itens) buscar as informações abaixo
    for item in itens:
        print(f"Código: {item[1]}, Nome: {item[0]}, Preço: {item[2]}, Descrição: {item[3]}, Quantidade em estoque: {item[4]}")
    # pede para o usuário digitar o código do item que deseja modificar e logo depois percorre a lista de itens buscando o código digitado; SE ENCONTRAR, entra no bloco if
    codigo = input("Digite o código do item que deseja modificar: ")
    for item in itens:
        if str(item[1]) == codigo:
            print(f"Modificando item: {item[0]}")
            novo_nome = input(f"Novo nome (Nome atual: '{item[0]}'): ")
            novo_preco = input(f"Novo preço (Valor atual: '{item[2]}'): ")
            nova_descricao = input(f"Nova descrição (Descrição atual: '{item[3]}'): ")
            nova_quantidade = input(f"Nova quantidade em estoque (Atual: '{item[4]}'): ")
            # se o usuário não digitar nada, mantém o valor atual.. se digitar altera no dicionário (dados primeiro são convertidos para o tipo correto e depois atribuídos)
            if novo_nome:
                item[0] = novo_nome
            if novo_preco:
                item[2] = float(novo_preco)
            if nova_descricao:
                item[3] = nova_descricao
                # para a quantidade em estoque, tenta converter o valor para inteiro, se não conseguir (ValueError) mostra uma mensagem de erro e mantém o valor atual
            if nova_quantidade:
                try:
                    item[4] = int(nova_quantidade)
                except ValueError:
                    print("Quantidade inválida. Valor não alterado.")

            print(f"Item {item[1]} atualizado com sucesso!")
            return

    print("Código não encontrado.")

def consultar_itens():
    # mais uma vez verifica se há ou não itens cadastrados
    if len(itens) == 0:
        print("Sem dados de cadastro no item.")
        return
    # mostra todos os itens cadastrados em caso de retorno positivo
    print("Itens cadastrados:")
    for item in itens:
        print(f"Código: {item[1]}, Nome: {item[0]}, Preço: {item[2]}, Descrição: {item[3]}, Quantidade em estoque: {item[4]}")

def criar_pedido():
    # verifica a existência de itens cadastrados; pedidos não podem ser feitos sem itens
    if len(itens) == 0:
        print("Itens não cadastrados.")
        return

    codigo = None
    valor_total = None
    cupom = None
    status = 'AGUARDANDO APROVACAO'
    pedido_itens = []
    valor_total = 0.0

    print("\nItens disponíveis:")
    for item in itens:
        print(f"Código: {item[1]}, Nome: {item[0]}, Preço: R$ {item[2]}")

    # loop para adicionar itens ao pedido, enquanto não digitar 'fim' ele continua solicitando código.
    while True:
        codigo = input("Digite os códigos dos itens desejados. Para finalizar, digite 'fim'. ")
        if codigo.lower() == "fim":
            break

        encontrado = False
        # percorre a lista buscando o código digitado, e adiciona ao pedido apenas aquilo que existe de fato no estoque.
        for item in itens:
            if str(item[1]) == codigo:
                if item[4] > 0:
                    pedido_itens.append(item)
                    valor_total += item[2]
                    item[4] -= 1  # reduz o estoque
                    print(f"Item '{item[0]}' adicionado ao pedido.")
                else:
                    print(f"Item '{item[0]}' acabou. Insira outro código ou finalize.")
                encontrado = True
                break

        if not encontrado:
            print("Código não encontrado. Tente novamente.")

    # pedido não pode ser vazio
    if len(pedido_itens) == 0:
        print("Pedido precisa ter pelo menos um item.")
        return

    # Tratamento do cupom; nesse caso temos 2 possibilidades ofertadas fora isso é inválido
    while True:
        cupom = input("CUPOM (se não tiver, deixe em branco): ")
        if cupom == "DESCONTO10":
            valor_total *= 0.9  # aplica 10% de desconto
            print("Cupom aplicado: 10% de desconto.")
            break
        elif cupom == "DESCONTO20":
            valor_total *= 0.8  # aplica 20% de desconto
            print("Cupom aplicado: 20% de desconto.")
            break
        elif cupom == '':
            break
        else:
            print("Cupom inválido ou não inserido.")


    # dicionário de pedido coletado que será adicionado a fila de pendentes

    pedido = [codigo, itens, valor_total, cupom, status]

    pedidos_pendentes.append(pedido)
    print(f"\nPedido #0{pedido[0]} criado com sucesso!")
    print(f"Status: {pedido[4]}")
    print(f"Valor total: R$ {pedido[2]}")

def processar_pedidos():
    # verifica se tem pedidos pendentes para processamento de fila
    if not pedidos_pendentes:
        print("Sem pendências.")
        return
    
    # pega o primeiro pedido da fila - o 0 é o primeiro - (first in, first out) e pergunta se aceita ou rejeita.
    pedido = pedidos_pendentes.pop(0)
    print(f"Processando Pedido #{pedido[0]} - Valor: R$ {pedido[2]}")
    decisao = input("Aceitar pedido (A) ou Rejeitar pedido (R)? ").upper() #deixa resposta em maíusculo
    
    if decisao == "A":
        pedido[4] = "FAZENDO"
        pedidos_aceitos.append(pedido)
        # o .append adiciona o pedido no final da lista de aceitos
        print("Pedido aceito e movido para preparo.")
    elif decisao == "R":
        pedido[4] = "REJEITADO"
        print("Pedido rejeitado.")
    else:
        print("Opção inválida. Pedido mantido como pendente.")
        # se a opção for inválida, o pedido volta para o início da fila de pendentes
        pedidos_pendentes.insert(0, pedido)

def finalizar_preparo():
    if not pedidos_aceitos:
        print("Nenhum pedido em preparo.")
        return

    # pega o primeiro pedido da fila de aceitos e finaliza o preparo
    pedido = pedidos_aceitos.pop(0)
    pedido[4] = "Aguardando retirada do entregador."
    pedidos_prontos.append(pedido)
    print(f"Pedido #{pedido[0]} finalizado e aguardando entregador.")

def atualizar_status():
    id_busca = input("Digite o ID do pedido: ")
    for lista in [pedidos_pendentes, pedidos_aceitos, pedidos_prontos]:
        for pedido in lista:
            if str(pedido[0]) == id_busca:
                print(f"Status atual: {pedido[4]}")
                novo_status = input("Novo status: ").upper()
                pedido[4] = novo_status
                print("Status atualizado.")
                return
    print("Pedido não existe.")

def cancelar_pedido():
    id_busca = input("Digite o ID do pedido para cancelar: ")
    for fila in [pedidos_pendentes, pedidos_aceitos]:
        for pedido in fila:
            if str(pedido[0]) == id_busca:
                if pedido[4] in ["AGUARDANDO APROVACAO", "FAZENDO"]:
                    pedido[4] = "CANCELADO"
                    fila.remove(pedido)
                    print("Pedido cancelado!")
                    return
    print("Pedido não pode ser cancelado ou não foi encontrado.")

def consultar_pedido():
    pass



 # MENU DE ITENS
while True: # loop infinito para o menu de itens

    print("Menu Principal")
    print(f"{'(1) Cadastrar Produtos'}")
    print(f"{'(2) Atualizar Produtos'}")
    print(f"{'(3) Consultar Produtos'}")
    print(f"{'(4) Criar Pedido'}")
    print(f"{'(5) Processar Pedidos'}")
    print(f"{'(6) Cancelar Pedido'}")
    print(f"{'(7) Finalizar Preparação do Pedido'}")
    print(f"{'(8) Atualizar Status do Pedido'}")
    print(f"{'(9) Consultar Pedidos'}")
    print(f"{'(0) SAIR'}")

    opcao = input("Escolha a opção desejada: ")
    if opcao == "1":
        cadastrar_item()
    elif opcao == "2":
        modificar_itens()
    elif opcao == "3":
        consultar_itens()
    elif opcao == "4":
        criar_pedido()
    elif opcao == "5":
        processar_pedidos()
    elif opcao == "6":
        cancelar_pedido()
    elif opcao == "7":
        finalizar_preparo()
    elif opcao == "8":
        atualizar_status()
    elif opcao == '9':
        consultar_pedido()
    elif opcao == "0":
        print("Saindo do programa...")
        exit() # encerra o programa e o loop do "while"
    else:  
        print("Opção inválida. Tente novamente.")