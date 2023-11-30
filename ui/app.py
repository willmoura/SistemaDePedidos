import tkinter as tk
from tkinter import ttk, messagebox
from database import db_connection
from business_logic import crud_operations
from ui.autocomplete_entry import AutocompleteEntry


global label_total_itens, label_valor_total

# Funções auxiliares
def buscar_clientes(nome):
    conn = db_connection.create_connection(r"C:\Users\dayan\OneDrive\Documentos\Sistema Pedidos\database\pedidos.db")
    resultados = crud_operations.buscar_clientes_por_nome(conn, nome)
    conn.close()
    return [(resultado[1], resultado[2]) for resultado in resultados]

def selecionar_cliente(nome_cliente, entry_var_cliente, entry_telefone):
    conn = db_connection.create_connection(r"C:\Users\dayan\OneDrive\Documentos\Sistema Pedidos\database\pedidos.db")
    cliente_info = crud_operations.buscar_clientes_por_nome(conn, nome_cliente)
    conn.close()
    if cliente_info:
        entry_var_cliente.set(cliente_info[0][0])  # Nome do cliente
        entry_telefone.set(cliente_info[0][1])     # Telefone do cliente




def setup(root):
    global label_total_itens, label_valor_total

    # Frame para o cabeçalho do pedido
    frame_header = ttk.Frame(root, padding="10")
    frame_header.pack(side='top', fill='x')

    # Botões Cancelar e Salvar
    btn_cancel = ttk.Button(frame_header, text="CANCELAR")
    btn_cancel.pack(side='right', padx=5)
    btn_save = ttk.Button(frame_header, text="SALVAR")
    btn_save.pack(side='right', padx=5)

    # Frame para os dados do cliente
    frame_customer = ttk.Frame(root, padding="10")
    frame_customer.pack(side='top', fill='x')

    ttk.Label(frame_customer, text="Cliente").pack(side='left')

    # Aqui, criamos uma instância simples da AutocompleteEntry
    entry_cliente = AutocompleteEntry(frame_customer)
    entry_cliente.pack(side='left', fill='x', expand=True)

    # Variáveis para os campos de entrada
    # entry_var_cliente = tk.StringVar()
    # entry_var_telefone = tk.StringVar()

    # Configuração do AutocompleteEntry para o campo cliente
    # entry_cliente = AutocompleteEntry(
      #  master=frame_customer, 
       # entry_var=entry_var_cliente, 
       # search_callback=lambda nome: buscar_clientes(nome)
    #)
   # entry_cliente.pack(side='left', fill='x', expand=True)

    # Campo de entrada para 'Telefone'
   # ttk.Label(frame_customer, text="Telefone").pack(side='left', padx=5)
   # entry_telefone = ttk.Entry(frame_customer, textvariable=entry_var_telefone)
    # entry_telefone.pack(side='left', fill='x', expand=True)

    ttk.Label(frame_customer, text="Condição de pagamento").pack(side='left', padx=5)
    combo_pagamento = ttk.Combobox(frame_customer, values=["PIX", "Cartão de débito", "Cartão de crédito", "Dinheiro", "Crediário"])
    combo_pagamento.pack(side='left', fill='x', expand=True)

    ttk.Label(frame_customer, text="Data do pedido").pack(side='left', padx=5)
    entry_data_pedido = ttk.Entry(frame_customer)
    entry_data_pedido.pack(side='left', fill='x', expand=True)

    # Frame para os itens do pedido
    frame_order_items = ttk.Frame(root, padding="10")
    frame_order_items.pack(side='top', fill='both', expand=True)

    # Tabela para itens do pedido
    colunas = ('Item', 'CodItem', 'Descricao', 'Un', 'Qtde', 'Desc', 'ValorUn', 'ValorTotal')
    tree = ttk.Treeview(frame_order_items, columns=colunas, show='headings')
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(side='top', fill='both', expand=True)

    # Botões para adicionar/remover itens
    btn_add_item = ttk.Button(frame_order_items, text="Adicionar outro item")
    btn_add_item.pack(side='left', padx=5)
    btn_remove_item = ttk.Button(frame_order_items, text="Remover item selecionado")
    btn_remove_item.pack(side='left', padx=5)

    # Frame para os totais
    frame_totals = ttk.Frame(root, padding="10")
    frame_totals.pack(side='top', fill='x')

    # Labels e Entries para os totais
    ttk.Label(frame_totals, text="Total de Itens:").pack(side='left', padx=5)
    label_total_itens = ttk.Label(frame_totals, text="0")  # Inicializar com 0
    label_total_itens.pack(side='left', padx=5)

    ttk.Label(frame_totals, text="Valor Total:").pack(side='left', padx=5)
    label_valor_total = ttk.Label(frame_totals, text="R$ 0,00")  # Inicializar com R$ 0,00
    label_valor_total.pack(side='left', padx=5)

    # Lógica para o AutocompleteEntry
    # entry_cliente.set_callback(lambda nome: selecionar_cliente(nome, entry_var_cliente, entry_var_telefone))

    # Lógica para botões e outros elementos interativos
    btn_add_item.configure(command=lambda: adicionar_item(tree))
    btn_remove_item.configure(command=lambda: remover_item_selecionado(tree))
    btn_save.configure(command=lambda: salvar_pedido(entry_cliente, entry_telefone, combo_pagamento, entry_data_pedido, tree))
    btn_cancel.configure(command=limpar_formulario)

    
    # Adicionar o evento de clique à função on_click
    tree.bind("<Button-1>", on_click)

def new_func():
    global entry_cliente, entry_telefone

# Global variable to keep track of the next item ID
next_item_id = 1

    # Função para adicionar uma nova linha em branco ao Treeview para inserção de dados pelo usuário
def adicionar_item(tree):
    global next_item_id
    # Insere uma nova linha em branco com valores vazios onde o usuário pode digitar os dados do novo item
    tree.insert('', 'end', values=(next_item_id, "", "", "", "", "", "", ""))
    next_item_id += 1

def iniciar_novo_pedido(tree, entry_cliente, entry_telefone, combo_pagamento, entry_data_pedido):
    global next_item_id
    # Reiniciar o contador de IDs de itens para um novo pedido
    next_item_id = 1
    # Limpar a Treeview e quaisquer outros campos relevantes
    limpar_formulario(tree, entry_cliente, entry_telefone, combo_pagamento, entry_data_pedido)

# Função para atualizar os totais após adicionar/remover itens
def atualizar_totais(tree):
    global label_total_itens, label_valor_total
    # Esta função recalcula os totais cada vez que um item é adicionado ou removido
    total_itens = 0
    valor_total = 0.0
    for child in tree.get_children():
        item = tree.item(child)['values']
        total_itens += int(item[4])  # Quantidade
        valor_total += float(item[7])  # Valor Total
    label_total_itens.config(text=str(total_itens))
    label_valor_total.config(text=f'R$ {valor_total:.2f}')

# Função para remover o item selecionado do Treeview
def remover_item_selecionado(tree):
    selected_item = tree.selection()
    if selected_item:
        tree.delete(selected_item)
        atualizar_totais(tree)

# Função para salvar o pedido no banco de dados
def salvar_pedido(entry_cliente, entry_telefone, combo_pagamento, entry_data_pedido, tree):
    # Obter os valores dos campos de entrada
    nome_cliente = entry_cliente.get()
    telefone_cliente = entry_telefone.get()
    condicao_pagamento = combo_pagamento.get()
    data_pedido = entry_data_pedido.get()

    # Validar os dados de entrada
    if not (nome_cliente and telefone_cliente and condicao_pagamento and data_pedido):
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
        return

    # Salvar o cabeçalho do pedido no banco de dados
    conn = db_connection.create_connection(r"C:\Users\dayan\OneDrive\Documentos\Sistema Pedidos\database\pedidos.db")
    pedido_id = crud_operations.create_pedido_cabecalho(conn, nome_cliente, telefone_cliente, condicao_pagamento, data_pedido)

    # Salvar os itens do pedido
    for child in tree.get_children():
        item = tree.item(child)['values']
        if item[0]:  # Verificar se a linha não está vazia (considerando que a primeira coluna não estará vazia se o item for válido)
            crud_operations.create_pedido_item(conn, pedido_id, *item[1:])

    # Fechar a conexão com o banco de dados
    conn.close()
    messagebox.showinfo("Sucesso", "Pedido salvo com sucesso.")
    limpar_formulario(tree, entry_cliente, entry_telefone, combo_pagamento, entry_data_pedido)

# Função para limpar o formulário
def limpar_formulario(tree, entry_cliente, entry_telefone, combo_pagamento, entry_data_pedido):
    # Limpar os campos do formulário
    entry_cliente.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)
    combo_pagamento.set('')
    entry_data_pedido.delete(0, tk.END)

    # Limpar a Treeview
    tree.delete(*tree.get_children())
# Função para permitir a edição de células na Treeview ao clicar
# Função para permitir a edição de células na Treeview ao clicar
def on_click(event):
    # Fechar qualquer Entry existente
    if hasattr(tree, 'entry_editor'):
        tree.entry_editor.destroy()

    # Obter a referência da célula clicada
    region = tree.identify("region", event.x, event.y)
    if region == "cell":
        row_id = tree.identify_row(event.y)
        column = tree.identify_column(event.x)
        x, y, width, height = tree.bbox(row_id, column)

        # Obter o valor da célula
        value = tree.set(row_id, column)

        # Criar e posicionar um Entry para edição da célula
        entry_editor = ttk.Entry(tree)
        entry_editor.place(x=x, y=y, width=width, height=height)
        entry_editor.insert(0, value)
        entry_editor.focus()

        # Definir o que acontece quando pressionamos Enter
        def on_enter(event):
            tree.set(row_id, column, entry_editor.get())
            entry_editor.destroy()
            # Atualizar os totais, se necessário
            atualizar_totais(tree)

        entry_editor.bind('<Return>', on_enter)
        entry_editor.bind('<Escape>', lambda event: entry_editor.destroy())

        # Guardar o editor na Treeview para referência futura
        tree.entry_editor = entry_editor
