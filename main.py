import tkinter as tk
from ui import app

def main():
    # Criar a Janela Raiz
    root = tk.Tk()
    # Configurar Título
    root.title("Sistema de Pedidos")
    
    # Iniciar a janela no modo maximizado
    root.state('zoomed')

    # Chamar a função de configuração da UI definida em app.py
    app.setup(root)

    # Iniciar o loop principal da interface
    root.mainloop()

if __name__ == "__main__":
    main()