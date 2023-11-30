import tkinter as tk
from tkinter import ttk

class AutocompleteEntry(ttk.Entry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.lista_sugestoes = tk.Listbox(master)
        self.lista_sugestoes.bind("<Double-Button-1>", self.selecionar_sugestao)
        self.bind("<KeyRelease>", self.atualizar_sugestoes)

    def atualizar_sugestoes(self, event):
        # Aqui você adiciona a lógica para buscar nomes de clientes
        # baseados no texto atual do entry
        # Por enquanto, vamos apenas mostrar algumas sugestões estáticas
        sugestoes = ["Cliente A", "Cliente B", "Cliente C"]
        self.lista_sugestoes.delete(0, tk.END)
        for sugestao in sugestoes:
            self.lista_sugestoes.insert(tk.END, sugestao)
        self.lista_sugestoes.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())

    def selecionar_sugestao(self, event):
        selecionado = self.lista_sugestoes.get(tk.ACTIVE)
        self.delete(0, tk.END)
        self.insert(0, selecionado)
        self.lista_sugestoes.place_forget()