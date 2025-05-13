import tkinter as tk
from tkinter import messagebox
import os
import platform


def bloquear_site():
    url = entry.get().strip()

    if not url:
        messagebox.showerror("Erro", "Por favor, insira um URL.")
        return

    sistema = platform.system()

    if sistema == "Windows":
        caminho_hosts = r"C:\Windows\System32\drivers\etc\hosts"
    elif sistema == "Linux" or sistema == "Darwin": 
        caminho_hosts = "/etc/hosts"
    else:
        messagebox.showerror("Erro", "Sistema não suportado.")
        return

    try:
        with open(caminho_hosts, "r") as hosts_file:
            conteudo = hosts_file.read()

        if f"# Bloqueado pelo programa\n127.0.0.1 {url}" in conteudo:#loopback
            messagebox.showinfo("Informação", f"O site {url} já está bloqueado.")
            return
        
        with open(caminho_hosts, "a") as hosts_file:
            hosts_file.write(f"# Bloqueado pelo programa\n127.0.0.1 {url}\n")
        
        messagebox.showinfo("Sucesso", f"Site {url} bloqueado com sucesso!")
        atualizar_lista_sites_bloqueados()  
    except PermissionError:
        messagebox.showerror("Erro", "Permissões insuficientes. Execute o programa como administrador.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")


def desbloquear_site():
    site_selecionado = lista_sites_bloqueados.curselection()
    if not site_selecionado:
        messagebox.showerror("Erro", "Por favor, selecione um site para desbloquear.")
        return

    site = lista_sites_bloqueados.get(site_selecionado)
   
    sistema = platform.system()

    if sistema == "Windows":
        caminho_hosts = r"C:\Windows\System32\drivers\etc\hosts"
    elif sistema == "Linux" or sistema == "Darwin":
        caminho_hosts = "/etc/hosts"
    else:
        messagebox.showerror("Erro", "Sistema não suportado.")
        return

    try:
        with open(caminho_hosts, "r") as hosts_file:
            linhas = hosts_file.readlines()

        site_bloqueado = f"# Bloqueado pelo programa\n127.0.0.1 {site}\n"

        with open(caminho_hosts, "w") as hosts_file:
            for linha in linhas:
                if linha != site_bloqueado:
                    hosts_file.write(linha)

        lista_sites_bloqueados.delete(site_selecionado)

        messagebox.showinfo("Sucesso", f"Site {site} desbloqueado com sucesso!")
    except PermissionError:
        messagebox.showerror("Erro", "Permissões insuficientes. Execute o programa como administrador.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

def atualizar_lista_sites_bloqueados():
    sistema = platform.system()

    if sistema == "Windows":
        caminho_hosts = r"C:\Windows\System32\drivers\etc\hosts"
    elif sistema == "Linux" or sistema == "Darwin": 
        caminho_hosts = "/etc/hosts"
    else:
        messagebox.showerror("Erro", "Sistema não suportado.")
        return

    try:
        with open(caminho_hosts, "r") as hosts_file:
            linhas = hosts_file.readlines()

        lista_sites_bloqueados.delete(0, tk.END)
        for i in range(len(linhas) - 1):
            if linhas[i].strip() == "# Bloqueado pelo programa":
                url = linhas[i + 1].split()[1]  
                lista_sites_bloqueados.insert(tk.END, url)

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao atualizar a lista de sites: {str(e)}")


def criar_interface():
    root = tk.Tk()
    root.title("Bloqueador de sites")

    label = tk.Label(root, text="Digite o URL do site:",font="arial",fg="black")
    label.pack(pady=10)

    global entry
    entry = tk.Entry(root, width=40)
    entry.pack(pady=10)

    botao_bloquear = tk.Button(root, text="Bloquear Site", command=bloquear_site,fg="white",bg="black",font="arial")
    botao_bloquear.pack(pady=10)

    global lista_sites_bloqueados
    lista_sites_bloqueados = tk.Listbox(root, height=10, width=40, selectmode=tk.SINGLE)
    lista_sites_bloqueados.pack(pady=10)

    botao_desbloquear = tk.Button(root, text="Desbloquear Site", command=desbloquear_site,fg="white",bg="black",font="arial")
    botao_desbloquear.pack(pady=10)

    atualizar_lista_sites_bloqueados()

    root.mainloop()


# Iniciar a aplicação
if __name__ == "__main__":
    criar_interface()
