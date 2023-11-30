# ui/widgets.py

from tkinter import messagebox

def mostrar_erro_copiavel(mensagem):
    """
    Mostra uma mensagem de erro em uma janela que permite copiar o texto.
    :param mensagem: Mensagem de erro a ser exibida.
    """
    messagebox.showerror("Erro", mensagem)