# business_logic/order_management.py

from database.db_connection import create_connection
from business_logic.crud_operations import create_pedido, update_pedido, delete_pedido
from ui.widgets import mostrar_erro_copiavel

def adicionar_pedido(nome_cliente, telefone_cliente, data_pedido):
    try:
        conn = create_connection()
        pedido_id = create_pedido(conn, (nome_cliente, telefone_cliente, data_pedido))
        conn.close()
        return pedido_id
    except Exception as e:
        mostrar_erro_copiavel(f"Erro ao adicionar pedido: {e}")

def atualizar_pedido(id_pedido, nome_cliente, telefone_cliente, data_pedido):
    try:
        conn = create_connection()
        update_pedido(conn, (nome_cliente, telefone_cliente, data_pedido, id_pedido))
        conn.close()
    except Exception as e:
        mostrar_erro_copiavel(f"Erro ao atualizar pedido: {e}")

def deletar_pedido(id_pedido):
    try:
        conn = create_connection()
        delete_pedido(conn, id_pedido)
        conn.close()
    except Exception as e:
        mostrar_erro_copiavel(f"Erro ao deletar pedido: {e}")
