import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import re  # Para validação de email
from datetime import datetime

# Criar conexão com o banco de dados no volume
conn = sqlite3.connect('/vol/bd/clientes.db')
cursor = conn.cursor()

# Definir a função antes de chamá-la
def exportar_banco_sql():
    try:
        # Nome do arquivo com timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        arquivo_exportacao = f"backup_clientes_{timestamp}.sql"

        # Abrir o arquivo para escrita
        with open(arquivo_exportacao, "w") as f:
            for linha in conn.iterdump():
                f.write(f"{linha}\n")

        print(f"Banco de dados exportado automaticamente para {arquivo_exportacao}.")
    except Exception as e:
        print(f"Erro ao exportar banco de dados: {e}")

# Exportar banco automaticamente ao iniciar
exportar_banco_sql()

cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    apelido TEXT,
                    data_nascimento TEXT NOT NULL,
                    telefone TEXT NOT NULL,
                    email TEXT NOT NULL,
                    endereco TEXT NOT NULL)''')

conn.commit()

# Função para validar data
def validar_data(data):
    try:
        datetime.strptime(data, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def validar_dados(nome, data_nascimento, telefone, email, endereco):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        messagebox.showerror("Erro", "Email inválido.")
        return False

    if not telefone.isdigit():
        messagebox.showerror("Erro", "Telefone deve conter apenas números.")
        return False

    if not validar_data(data_nascimento):
        messagebox.showerror("Erro", "Data de nascimento inválida. Use o formato DD/MM/AAAA.")
        return False

    if not nome or not data_nascimento or not telefone or not email or not endereco:
        messagebox.showwarning("Erro", "Preencha todos os campos obrigatórios.")
        return False

    return True

# Função para cadastrar cliente
def cadastrar_cliente():
    def salvar_cliente():
        nome = entry_nome.get()
        apelido = entry_apelido.get()
        data_nascimento = entry_data_nascimento.get()
        telefone = entry_telefone.get()
        email = entry_email.get()
        endereco = entry_endereco.get()

        if validar_dados(nome, data_nascimento, telefone, email, endereco):
            try:
                cursor.execute("INSERT INTO clientes (nome, apelido, data_nascimento, telefone, email, endereco) VALUES (?, ?, ?, ?, ?, ?)",
                               (nome, apelido, data_nascimento, telefone, email, endereco))
                conn.commit()
                messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro ao salvar cliente: {e}")
            cadastro_window.destroy()

    cadastro_window = tk.Toplevel(root)
    cadastro_window.title("Cadastro de Cliente")

    tk.Label(cadastro_window, text="Nome:").grid(row=0, column=0)
    entry_nome = ttk.Entry(cadastro_window)
    entry_nome.grid(row=0, column=1)

    tk.Label(cadastro_window, text="Apelido:").grid(row=1, column=0)
    entry_apelido = tk.Entry(cadastro_window)
    entry_apelido.grid(row=1, column=1)

    tk.Label(cadastro_window, text="Data de Nascimento (DD/MM/AAAA):").grid(row=2, column=0)
    entry_data_nascimento = tk.Entry(cadastro_window)
    entry_data_nascimento.grid(row=2, column=1)

    tk.Label(cadastro_window, text="Telefone:").grid(row=3, column=0)
    entry_telefone = tk.Entry(cadastro_window)
    entry_telefone.grid(row=3, column=1)

    tk.Label(cadastro_window, text="Email:").grid(row=4, column=0)
    entry_email = tk.Entry(cadastro_window)
    entry_email.grid(row=4, column=1)

    tk.Label(cadastro_window, text="Endereço:").grid(row=5, column=0)
    entry_endereco = tk.Entry(cadastro_window)
    entry_endereco.grid(row=5, column=1)

    tk.Button(cadastro_window, text="Salvar", command=salvar_cliente).grid(row=6, column=1)

# Função para editar cliente
def editar_cliente():
    def salvar_alteracao():
        id_cliente = entry_id.get()
        telefone = entry_novo_telefone.get()
        email = entry_novo_email.get()
        endereco = entry_novo_endereco.get()

        try:
            cursor.execute("SELECT * FROM clientes WHERE id = ?", (id_cliente,))
            if cursor.fetchone() is None:
                messagebox.showerror("Erro", "ID do cliente não encontrado.")
                return

            cursor.execute("UPDATE clientes SET telefone = ?, email = ?, endereco = ? WHERE id = ?", (telefone, email, endereco, id_cliente))
            conn.commit()
            messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
            editar_window.destroy()
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao atualizar cliente: {e}")

    editar_window = tk.Toplevel(root)
    editar_window.title("Edição de Cliente")

    tk.Label(editar_window, text="ID do Cliente:").grid(row=0, column=0)
    entry_id = tk.Entry(editar_window)
    entry_id.grid(row=0, column=1)

    tk.Label(editar_window, text="Novo Telefone:").grid(row=1, column=0)
    entry_novo_telefone = tk.Entry(editar_window)
    entry_novo_telefone.grid(row=1, column=1)

    tk.Label(editar_window, text="Novo Email:").grid(row=2, column=0)
    entry_novo_email = tk.Entry(editar_window)
    entry_novo_email.grid(row=2, column=1)

    tk.Label(editar_window, text="Novo Endereço:").grid(row=3, column=0)
    entry_novo_endereco = tk.Entry(editar_window)
    entry_novo_endereco.grid(row=3, column=1)

    tk.Button(editar_window, text="Salvar Alterações", command=salvar_alteracao).grid(row=4, column=1)

# Função para excluir cliente
def excluir_cliente():
    def confirmar_exclusao():
        id_cliente = entry_excluir.get()
        if messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este cliente?"):
            try:
                cursor.execute("DELETE FROM clientes WHERE id = ?", (id_cliente,))
                conn.commit()
                messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro ao excluir cliente: {e}")
        excluir_window.destroy()

    excluir_window = tk.Toplevel(root)
    excluir_window.title("Exclusão de Cliente")

    tk.Label(excluir_window, text="ID do Cliente:").grid(row=0, column=0)
    entry_excluir = tk.Entry(excluir_window)
    entry_excluir.grid(row=0, column=1)

    tk.Button(excluir_window, text="Excluir Cliente", command=confirmar_exclusao).grid(row=1, column=1)

# Função para procurar cliente
def procurar_cliente():
    def buscar_cliente():
        criterio = entry_criterio.get()
        tipo_busca = combo_tipo_busca.get()

        try:
            if tipo_busca == "ID":
                cursor.execute("SELECT * FROM clientes WHERE id = ?", (criterio,))
            elif tipo_busca == "Nome":
                cursor.execute("SELECT * FROM clientes WHERE nome LIKE ?", (f"%{criterio}%",))
            else:
                messagebox.showerror("Erro", "Selecione um tipo de busca válido.")
                return

            resultado = cursor.fetchall()
            if resultado:
                texto_resultado.delete(1.0, tk.END)
                for cliente in resultado:
                    texto_resultado.insert(tk.END, f"ID: {cliente[0]}\nNome: {cliente[1]}\nApelido: {cliente[2]}\n"
                                                   f"Data de Nascimento: {cliente[3]}\nTelefone: {cliente[4]}\n"
                                                   f"Email: {cliente[5]}\nEndereço: {cliente[6]}\n\n")
            else:
                messagebox.showinfo("Resultado", "Nenhum cliente encontrado.")
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao buscar cliente: {e}")

    procurar_window = tk.Toplevel(root)
    procurar_window.title("Procurar Cliente")

    tk.Label(procurar_window, text="Buscar por:").grid(row=0, column=0)
    combo_tipo_busca = ttk.Combobox(procurar_window, values=["ID", "Nome"], state="readonly")
    combo_tipo_busca.grid(row=0, column=1)
    combo_tipo_busca.set("ID")

    tk.Label(procurar_window, text="Critério:").grid(row=1, column=0)
    entry_criterio = tk.Entry(procurar_window)
    entry_criterio.grid(row=1, column=1)

    tk.Button(procurar_window, text="Buscar", command=buscar_cliente).grid(row=2, column=1)

    texto_resultado = tk.Text(procurar_window, width=50, height=15)
    texto_resultado.grid(row=3, column=0, columnspan=2)

# Criar interface inicial
root = tk.Tk()
root.title("Sistema de Gestão de Clientes")

tk.Label(root, text="Escolha uma ação:").grid(row=0, column=0, columnspan=2)

tk.Button(root, text="Cadastrar Cliente", command=cadastrar_cliente).grid(row=1, column=0)
tk.Button(root, text="Editar Cliente", command=editar_cliente).grid(row=1, column=1)
tk.Button(root, text="Excluir Cliente", command=excluir_cliente).grid(row=2, column=0, columnspan=2)
tk.Button(root, text="Procurar Cliente", command=procurar_cliente).grid(row=3, column=0, columnspan=2)

def on_closing():
    exportar_banco_sql()  # Exporta o banco automaticamente
    conn.close()          # Fecha a conexão com o banco
    root.destroy()         # Fecha a interface gráfica

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
