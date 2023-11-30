

#def buscar_clientes_por_nome(conn, nome):
 #   """
  #  Busca clientes por nome
   # :param conn: Conexão com o banco de dados
    #:param nome: Nome do cliente a ser buscado
    #"""
    #sql = "SELECT nome, telefone FROM Cliente WHERE nome LIKE ?"
    #try:
     #   cur = conn.cursor()
      #  cur.execute(sql, ('%' + nome + '%',))
       # return cur.fetchall()
    # except sqlite3.Error as e:
      #  raise DatabaseError(f"Erro ao buscar cliente: {e}")