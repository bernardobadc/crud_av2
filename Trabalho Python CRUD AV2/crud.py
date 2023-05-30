import tkinter as tk
from tkinter import messagebox
import sqlite3

# Criar banco de dados e tabelas

conn = sqlite3.connect('banco_de_dados.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS usuarios
             (username TEXT, password TEXT)''')
conn.commit()

c.execute('''CREATE TABLE IF NOT EXISTS produtos
             (nome TEXT, quantidade INTEGER)''')
conn.commit()

# Função para o login

def realizar_login():
    username = usuario_entry.get()
    password = senha_entry.get()

    c.execute("SELECT * FROM usuarios WHERE username=? AND password=?", (username, password))
    result = c.fetchone()

    if result:
        tela_produtos()
    else:
        messagebox.showerror("Erro de login", "Usuário ou senha incorretos")

# Função para criar uma nova conta

def criar_conta():

    username = usuario_entry.get()
    password = senha_entry.get()

    c.execute("SELECT * FROM usuarios WHERE username=?", (username,))
    result = c.fetchone()

    if result:
        messagebox.showerror("Erro de cadastro", "Nome de usuário já existe")
    else:
        c.execute("INSERT INTO usuarios VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Sucesso", "Conta criada com sucesso")

# Função para abrir a tela de cadastro de produtos

def tela_produtos():
    janela.destroy()

    janela_produtos = tk.Tk()
    janela_produtos.title("Cadastro de Produtos")

    # Função para adicionar um produto

    def adicionar_produto():
        nome = nome_produto_entry.get()
        quantidade = quantidade_produto_entry.get()

        c.execute("INSERT INTO produtos VALUES (?, ?)", (nome, quantidade))
        conn.commit()
        messagebox.showinfo("Produto adicionado", "Produto cadastrado com sucesso")

    # Função para atualizar um produto

    def atualizar_produto():
        nome = nome_produto_entry.get()
        quantidade = quantidade_produto_entry.get()

        c.execute("UPDATE produtos SET quantidade=? WHERE nome=?", (quantidade, nome))
        conn.commit()
        messagebox.showinfo("Atualizado", "Produto atualizado com sucesso")

    # Função para excluir um produto

    def excluir_produto():
        nome = nome_produto_entry.get()

        c.execute("DELETE FROM produtos WHERE nome=?", (nome,))
        conn.commit()
        messagebox.showinfo("Produto excluído", "Produto excluído com sucesso")

    # Função para consultar um produto

    def consultar_produto():
        nome = nome_produto_entry.get()

        c.execute("SELECT * FROM produtos WHERE nome=?", (nome,))
        result = c.fetchone()

        if result:
            messagebox.showinfo("Produto encontrado", f"Nome: {result[0]}\nQuantidade: {result[1]}")
        else:
            messagebox.showinfo("Produto inexistente", "Produto não encontrado")

    # Widgets da tela de produtos

    nome_produto_label = tk.Label(janela_produtos, text="Nome do Produto")
    nome_produto_label.grid(row=0, column=0)

    nome_produto_entry = tk.Entry(janela_produtos)
    nome_produto_entry.grid(row=0, column=1)

    quantidade_produto_label = tk.Label(janela_produtos, text="Quantidade")
    quantidade_produto_label.grid(row=1, column=0)

    quantidade_produto_entry = tk.Entry(janela_produtos)
    quantidade_produto_entry.grid(row=1, column=1)

    adicionar_button = tk.Button(janela_produtos, text="Adicionar", command=adicionar_produto)
    adicionar_button.grid(row=2, column=0)

    atualizar_button = tk.Button(janela_produtos, text="Atualizar", command=atualizar_produto)
    atualizar_button.grid(row=2, column=1)

    excluir_button = tk.Button(janela_produtos, text="Excluir", command=excluir_produto)
    excluir_button.grid(row=3, column=0)

    consultar_button = tk.Button(janela_produtos, text="Consultar", command=consultar_produto)
    consultar_button.grid(row=3, column=1)

    janela_produtos.mainloop()

# Tela de login

janela = tk.Tk()
janela.title("Tela de Login")
janela.geometry('250x100')
janela.resizable(width=False, height=False)

usuario_label = tk.Label(janela, text="Usuário")
usuario_label.grid(row=0, column=0)

usuario_entry = tk.Entry(janela)
usuario_entry.grid(row=0, column=1)

senha_label = tk.Label(janela, text="Senha")
senha_label.grid(row=1, column=0)

senha_entry = tk.Entry(janela, show="*")
senha_entry.grid(row=1, column=1)

login_button = tk.Button(janela, text="Login", command=realizar_login)
login_button.grid(row=6, column=4)

cadastro_button = tk.Button(janela, text="Cadastrar-se", command=criar_conta)
cadastro_button.grid(row=6, column=0)

janela.mainloop()
