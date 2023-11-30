import unittest
from database.db_connection import create_connection
from business_logic import crud_operations
from database.db_exceptions import DatabaseError

class TestCrudOperations(unittest.TestCase):

    def setUp(self):
        # Configuração inicial para os testes, como conexão com banco de dados de teste
        self.conn = create_connection(":memory:")

        # Criação de tabelas necessárias para os testes
        self.create_tables()

    def create_tables(self):
        # Cria as tabelas necessárias para os testes
        cur = self.conn.cursor()

        sql_create_pedido_cabecalho_table = """
        CREATE TABLE IF NOT EXISTS Pedido_Cabecalho (
            ID integer PRIMARY KEY,
            NomeCliente text NOT NULL,
            TelefoneCliente text,
            DataPedido text NOT NULL
        );
        """
        cur.execute(sql_create_pedido_cabecalho_table)

        sql_create_pedido_itens_table = """
        CREATE TABLE IF NOT EXISTS Pedido_Itens (
            ID integer PRIMARY KEY,
            PedidoID integer,
            Descricao text,
            Quantidade integer,
            ValorUnitario real,
            ValorTotal real,
            FOREIGN KEY (PedidoID) REFERENCES Pedido_Cabecalho (ID)
        );
        """
        cur.execute(sql_create_pedido_itens_table)

        self.conn.commit()

    def test_update_pedido(self):
        # Preparar dados de teste
            pedido_original = ('Cliente Teste','21589865248', '2023-03-15')
            pedido_id = crud_operations.create_pedido(self.conn, pedido_original)

        # Dados atualizados
            pedido_atualizado = ('Cliente Atualizado', '21589865248', '2023-03-16')
        
        # Atualizar o pedido
            crud_operations.update_pedido(self.conn, pedido_atualizado + (pedido_id,))

        # Verificar se o pedido foi atualizado
            updated_pedido = crud_operations.exibir_pedido(self.conn, pedido_id)
            self.assertEqual(updated_pedido['cabecalho'][1:], pedido_atualizado)

    def test_delete_pedido(self):
        # Preparar dados de teste
            pedido = ('Cliente Teste', '21589865248', '2023-03-15')
            pedido_id = crud_operations.create_pedido(self.conn, pedido)

        # Deletar o pedido
            crud_operations.delete_pedido(self.conn, pedido_id)

        # Verificar se o pedido foi deletado
            try:
                deleted_pedido = crud_operations.exibir_pedido(self.conn, pedido_id)
                self.assertIsNone(deleted_pedido)
            except DatabaseError as e:
                self.assertEqual(str(e), "Pedido não encontrado")

    def test_exibir_pedido(self):
        # Preparar dados de teste
            pedido = ('Cliente Teste', '21589865248', '2023-03-15')
            pedido_id = crud_operations.create_pedido(self.conn, pedido)

        # Exibir o pedido
            result = crud_operations.exibir_pedido(self.conn, pedido_id)

        # Verificar se os dados do pedido estão corretos
            esperado = ('Cliente Teste', '21589865248', '2023-03-15')
            resultado = result['cabecalho'][1:]  # Ignorando o ID do pedido na comparação
            self.assertEqual(resultado, esperado)

    def tearDown(self):
        # Limpeza após cada teste
        self.conn.close()

if __name__ == '__main__':
    unittest.main()