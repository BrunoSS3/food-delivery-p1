pedidos_ativos = []
pedidos_finalizados = []
todos_os_pedidos = []
itens = []
# gerador de códigos (incrementar)
sequencia_cod = 1
sequencia_cod_pedido = 1

# Filas

pedido_aguardando_aprovacao = []
pedido_aceito = []
pedido_fazendo = []
pedido_feito = []
pedido_esperando_entregador = []
pedido_saiu_entrega = []
pedido_entregue = []
pedido_rejeitado = []
pedido_cancelado = []

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

    cupom = ''
    status = 'AGUARDANDO APROVACAO'
    pedido_itens = []
    valor_total = 0.0 # Começa em 0 para somar
    
    global sequencia_cod_pedido
    pedido = [sequencia_cod_pedido]
    
    print("\nItens disponíveis:")
    for item in itens:
        print(f"Código: {item[1]}, Nome: {item[0]}, Preço: R$ {item[2]}")

    # loop para adicionar itens ao pedido
    while True:
        comprar = []
        quantidade = None
        codigo = input("Digite o código do item desejado. Para finalizar, digite 'fim'. ")
        if codigo.lower() == "fim":
            break

        encontrado = False
        for item in itens:
            if str(item[1]) == codigo:
                while type(quantidade) != int:
                    try:
                        quantidade = int(input("Quantidade: "))
                    except:
                        print('\n-----Insira um número válido!-----\n')

                if quantidade > 0 and quantidade <= item[4]:
                    # --- INÍCIO DAS CORREÇÕES ---
                    
                    subtotal_item = item[2] * quantidade
                    valor_total += subtotal_item           
                    
                    comprar.append(codigo)
                    comprar.append(item[0])
                    comprar.append(quantidade)
                    comprar.append(subtotal_item)         
                    
                    # --- FIM DAS CORREÇÕES ---
                    
                    pedido_itens.append(comprar)
                    item[4] -= quantidade  # reduz o estoque
                    print(f"{quantidade} unidades de {item[0]} adicionado(s) ao pedido.")
                elif quantidade <= 0:
                    print("A quantidade deve ser maior que zero.")
                else:
                    print(f"Estoque insuficiente para '{item[0]}'. Apenas {item[4]} disponível(is).")
                
                encontrado = True
                break
        
        if not encontrado:
            print("Código não encontrado. Tente novamente.")

    # pedido não pode ser vazio
    if len(pedido_itens) == 0:
        print("Pedido cancelado pois nenhum item foi adicionado.")
        return

    # Colocar as compras do cliente no pedido
    pedido.append(pedido_itens)

    # Tratamento do cupom;
    valor_com_desconto = valor_total # Inicia com o valor total
    while True:
        cupom = input("CUPOM (se não tiver, deixe em branco): ")
        if cupom == "DESCONTO10":
            valor_com_desconto = valor_total * 0.9  # aplica 10% de desconto
            print("Cupom aplicado: 10% de desconto.")
            break
        elif cupom == "DESCONTO20":
            valor_com_desconto = valor_total * 0.8  # aplica 20% de desconto
            print("Cupom aplicado: 20% de desconto.")
            break
        elif cupom == '':
            break
        else:
            print("Cupom inválido ou não inserido.")

    # Valor Total
    pedido.append(valor_com_desconto)

    # Cupom
    pedido.append(cupom)

    # status
    pedido.append(status)

    pedidos_ativos.append(pedido)
    todos_os_pedidos.append(pedido)
    sequencia_cod_pedido += 1
    print(f"\nPedido #{pedido[0]:02d} criado com sucesso!")
    print(f"Status: {pedido[4]}")
    print(f"Valor total: R$ {pedido[2]:.2f}")

def imprimir_detalhes_pedido(pedido):
    """Função auxiliar para imprimir um único pedido de forma formatada."""
    print("\n-----------------------------------------")
    print(f"Pedido Código: #{pedido[0]:02d}")
    print(f"Status: {pedido[4]}")
    print("Itens:")
    
    # Itera sobre a lista de itens dentro do pedido
    for item_comprado in pedido[1]:
        # item_comprado = ['código', 'nome', quantidade, subtotal]
        codigo_prod = item_comprado[0]
        nome_prod = item_comprado[1]
        quantidade = item_comprado[2]
        subtotal = item_comprado[3]
        print(f"  - {quantidade}x {nome_prod} (Cód: {codigo_prod}) - Subtotal: R$ {subtotal:.2f}")

    if pedido[3]: # Se houver um cupom
        print(f"Cupom Aplicado: {pedido[3]}")
        
    print(f"Valor Total: R$ {pedido[2]:.2f}")
    print("-----------------------------------------")

def consultar_pedido():
    if not todos_os_pedidos:
        print("\n--- Não há pedidos registrados. ---")
        return

    # Passo 1: Imprimir todos os pedidos de forma formatada
    print("\n======== Histórico de Todos os Pedidos ========")
    for pedido in todos_os_pedidos:
        imprimir_detalhes_pedido(pedido)


    # Passo 2: Oferecer opções para filtrar por status
    while True:
        print("\nFiltrar pedidos por Status:\n"
              "(1) AGUARDANDO APROVACAO\n"
              "(2) ACEITO\n"
              "(3) FAZENDO\n"
              "(4) FEITO\n"
              "(5) ESPERANDO ENTREGADOR\n"
              "(6) SAIU PARA ENTREGA\n"
              "(7) ENTREGUE\n"
              "(8) CANCELADO\n"
              "(9) REJEITADO\n"
              "(0) VOLTAR AO MENU PRINCIPAL")

        sub_opcao = input("Escolha uma opção de filtro: ")
        status_desejado = None

        if sub_opcao == "0":
            print("Voltando ao menu principal...")
            return
        elif sub_opcao == "1":
            status_desejado = "AGUARDANDO APROVACAO"
        elif sub_opcao == "2":
            status_desejado = "ACEITO"
        elif sub_opcao == "3":
            status_desejado = "FAZENDO"
        elif sub_opcao == "4":
            status_desejado = "FEITO"
        elif sub_opcao == "5":
            status_desejado = "ESPERANDO ENTREGADOR"
        elif sub_opcao == "6":
            status_desejado = "SAIU PARA ENTREGA"
        elif sub_opcao == "7":
            status_desejado = "ENTREGUE"
        elif sub_opcao == "8":
            status_desejado = "CANCELADO"
        elif sub_opcao == "9":
            status_desejado = "REJEITADO"
        else:
            print("Opção de status inválida.")
            continue

        if status_desejado:
            print(f"\n--- Pedidos com status: {status_desejado} ---")
            encontrou_pedido = False
            for pedido in todos_os_pedidos:
                if pedido[4] == status_desejado:
                    imprimir_detalhes_pedido(pedido)
                    encontrou_pedido = True
            
            if not encontrou_pedido:
                print(f"\nNenhum pedido encontrado com o status '{status_desejado}'.")

def mostrar_pedidos_por_status(status_desejado, flag=0):
    encontrou_lista = False

    for pedido in pedidos_ativos:
        if pedido[4] == status_desejado:
            print(f"  - ID: {pedido[0]}, Valor: R$ {pedido[2]}")
            encontrou_lista = True
            
        
    if not encontrou_lista and flag != 0:
        print("\n---- Nenhum pedido encontrado com este status ----\n")
    
    return encontrou_lista

def buscar_primeiro_pedido_por_status(status_desejado):
    """Encontra o pedido mais antigo (o primeiro da lista) com um status específico."""
    for pedido in pedidos_ativos:
        if pedido[4] == status_desejado:
            return pedido  # Retorna o primeiro que encontrar
    return None # Retorna None se nenhum pedido com esse status for encontrado

def gerenciar_status_pedido():
    while True:
        print("\n--- Gerenciador de Status de Pedidos ---")
        print("O sistema sempre processará o pedido mais antigo de cada etapa.")
        print("(1) AGUARDANDO APROVACAO")
        print("(2) ACEITO")
        print("(3) FAZENDO")
        print("(4) FEITO")
        print("(5) ESPERANDO ENTREGADOR")
        print("(6) SAIU PARA ENTREGA")
        print("(7) CANCELAR")
        print("(0) Voltar ao Menu Principal")
        
        sub_opcao = input("Escolha uma ação: ")

        if sub_opcao == "0":
            print("Voltando ao menu principal")
            return

        pedido_alvo = None
        acao_invalida = False

        if sub_opcao == '1':
            pedido_alvo = buscar_primeiro_pedido_por_status('AGUARDANDO APROVACAO')
            if not pedido_alvo:
                print("\nNenhum pedido aguardando aprovação.")
                continue
            
            print("\nProcessando pedidos:")
            imprimir_detalhes_pedido(pedido_alvo)
            decisao = input("Aceitar (A) ou Rejeitar (R) o pedido? ").upper()
            if decisao == "A":
                pedido_alvo[4] = "ACEITO"
                print(f"Pedido #{pedido_alvo[0]:02d} ACEITO.")
            elif decisao == "R":
                pedido_alvo[4] = "REJEITADO"
                pedidos_ativos.remove(pedido_alvo)
                pedidos_finalizados.append(pedido_alvo)
                print(f"Pedido #{pedido_alvo[0]:02d} REJEITADO e movido para finalizados.")
            else:
                print("Opção inválida. Nenhuma ação tomada.")

        elif sub_opcao == '2':
            pedido_alvo = buscar_primeiro_pedido_por_status('ACEITO')
            if not pedido_alvo:
                print("\nNenhum pedido aceito.")
                continue

            print("\nIniciando preparo:")
            imprimir_detalhes_pedido(pedido_alvo)
            decisao = input("Confirmar início do preparo (S/N)? ").upper()
            if decisao == 'S':
                pedido_alvo[4] = "FAZENDO"
                print(f"Pedido #{pedido_alvo[0]:02d} agora está sendo FEITO.")
            else:
                print("Ação cancelada.")

        elif sub_opcao == '3':
            pedido_alvo = buscar_primeiro_pedido_por_status('FAZENDO')
            if not pedido_alvo:
                print("\nNenhum pedido em preparação.")
                continue
            
            print("\nFinalizando preparo:")
            imprimir_detalhes_pedido(pedido_alvo)
            decisao = input("Confirmar finalização do preparo (S/N)? ").upper()
            if decisao == 'S':
                pedido_alvo[4] = "FEITO"
                print(f"Pedido #{pedido_alvo[0]} foi FEITO e está pronto.")
            else:
                print("Ação cancelada.")
        
        elif sub_opcao == '4':
            pedido_alvo = buscar_primeiro_pedido_por_status('FEITO')
            if not pedido_alvo:
                print("\nNenhum pedido pronto para entrega.")
                continue
            
            print("\nMovendo pedido para aguardar entregador:")
            imprimir_detalhes_pedido(pedido_alvo)
            decisao = input("Confirmar (S/N)? ").upper()
            if decisao == 'S':
                pedido_alvo[4] = "ESPERANDO ENTREGADOR"
                print(f"Pedido #{pedido_alvo[0]:02d} agora está ESPERANDO ENTREGADOR.")
            else:
                print("Ação cancelada.")

        elif sub_opcao == '5':
            pedido_alvo = buscar_primeiro_pedido_por_status('ESPERANDO ENTREGADOR')
            if not pedido_alvo:
                print("\nNenhum pedido aguardando entregador.")
                continue
            
            print("\nDespachando pedido para entrega:")
            imprimir_detalhes_pedido(pedido_alvo)
            decisao = input("Confirmar saída para entrega (S/N)? ").upper()
            if decisao == 'S':
                pedido_alvo[4] = "SAIU PARA ENTREGA"
                print(f"Pedido #{pedido_alvo[0]:02d} SAIU PARA ENTREGA.")
            else:
                print("Ação cancelada.")

        elif sub_opcao == '6':
            pedido_alvo = buscar_primeiro_pedido_por_status('SAIU PARA ENTREGA')
            if not pedido_alvo:
                print("\nNenhum pedido em rota de entrega.")
                continue

            print("\nFinalizando entrega do pedido:")
            imprimir_detalhes_pedido(pedido_alvo)
            decisao = input("Confirmar entrega (S/N)? ").upper()
            if decisao == 'S':
                pedido_alvo[4] = "ENTREGUE"
                pedidos_ativos.remove(pedido_alvo)
                pedidos_finalizados.append(pedido_alvo)
                print(f"Pedido #{pedido_alvo[0]:02d} finalizado como ENTREGUE.")
            else:
                print("Ação cancelada.")

        elif sub_opcao == '7':
            codigo_pedido = input('Insira o ID do pedido que deseja cancelar: ')
            pedido_encontrado = None
            for p in pedidos_ativos:
                if str(p[0]) == codigo_pedido:
                    pedido_encontrado = p
                    break
            
            if not pedido_encontrado:
                print(f"Pedido com ID {codigo_pedido} não encontrado nos pedidos ativos.")
                continue

            if pedido_encontrado[4] in ["AGUARDANDO APROVACAO", "ACEITO"]:
                pedido_encontrado[4] = "CANCELADO"
                pedidos_ativos.remove(pedido_encontrado)
                pedidos_finalizados.append(pedido_encontrado)
                print(f"Pedido #{pedido_encontrado[0]:02d} CANCELADO.")
            else:
                print(f"Erro: Pedido não pode mais ser cancelado. Status atual: {pedido_encontrado[4]}")

        else:
            print("Opção inválida. Tente novamente.")

while True:

    print("Menu Principal\n"
      "(1) Cadastrar Produtos\n"
      "(2) Atualizar Produtos\n"
      "(3) Consultar Produtos\n"
      "(4) Criar Pedido\n"
      "(5) Processar Pedidos\n"
      "(6) Consultar Pedidos\n"
      "(0) SAIR")


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
        gerenciar_status_pedido()
    elif opcao == "6":
        consultar_pedido()
    elif opcao == "0":
        print("Saindo do programa")
        exit()
    else:  
        print("Opção inválida. Tente novamente.")