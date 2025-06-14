import tkinter as tk
from tkinter import messagebox, scrolledtext
import ctypes
import customtkinter
import os
import tempfile
import subprocess

ctypes.windll.shcore.SetProcessDpiAwareness(1)

escuro = False
cores = {
    "claro": {
        "bg": "#f0f0f0",
        "fg": "#000000",
        "menu_bg": "#d9ead3",
        "menu_fg": "#000000",
        "botao_bg": "#08500A",
        "botao_fg": "#ffffff",
        "caixa_bg": "#ffffff",
        "caixa_fg": "#000000"
    },
    "escuro": {
        "bg": "#2e2e2e",
        "fg": "#ffffff",
        "menu_bg": "#444444",
        "menu_fg": "#ffffff",
        "botao_bg": "#EC0C0C",
        "botao_fg": "#ffffff",
        "caixa_bg": "#1e1e1e",
        "caixa_fg": "#ffffff"
    }
}

arquivos = {
    "Análise": "C:/Users/marce/Downloads/Escola/listaExercicio_APS.txt",
    "Redes": "C:/Users/marce/Downloads/Escola/listaExercicio_Redes.txt",
    "Java": "C:/Users/marce/Downloads/Escola/listaExercicio_Java.txt",
    "C#": "C:/Users/marce/Downloads/Escola/listaExercicio_CSharp.txt",
    "ORM": "C:/Users/marce/Downloads/Escola/listaExercicio_APS2.txt",
    "Micro": "C:/Users/marce/Downloads/Escola/listaMicro.txt",
}

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")

janela = customtkinter.CTk()
janela.title("Visualizador de Arquivos Pré-definidos")
janela.geometry("700x500")
janela.minsize(600, 400)

top_frame = customtkinter.CTkFrame(janela)
top_frame.pack(pady=10, padx=10, fill='x')

label = customtkinter.CTkLabel(top_frame, text="Escolha um arquivo:", font=('Consolas', 14, 'bold'))
label.pack(side='left')

opcao_var = tk.StringVar(value="Selecione")


menu = customtkinter.CTkOptionMenu(top_frame, values=list(arquivos.keys()), variable=opcao_var,
                                   command=lambda v: carregar_arquivo(v))
menu.pack(side='left', padx=10)

button_tema = customtkinter.CTkButton(top_frame, text='Claro / Escuro', command=lambda: alternar_tema(),
                                      font=('Consolas', 11, 'bold'), cursor="hand2", corner_radius=10)
button_tema.pack(side='right')

button_recarregar = customtkinter.CTkButton(top_frame, text='Recarregar', command=lambda: carregar_arquivo(opcao_var.get()),
                                            font=('Consolas', 11, 'bold'), cursor="hand2", corner_radius=10)
button_recarregar.pack(side='right', padx=10)

button_imprimir = customtkinter.CTkButton(top_frame, text='Imprimir', command= lambda: imprimir_arquivo(),
                                          font=('Consolas', 11, 'bold'), cursor="hand2", corner_radius=10)
button_imprimir.pack(side='right', padx=10)

arquivo_atual_label = customtkinter.CTkLabel(janela, text="", font=('Consolas', 11, 'italic'))
arquivo_atual_label.pack(pady=5)

caixa_texto = scrolledtext.ScrolledText(janela, wrap=tk.WORD, font=('Consolas', 12), state='disabled')
caixa_texto.pack(expand=True, fill='both', padx=15, pady=10)


def aplicar_tema():
    global escuro
    tema = "escuro" if escuro else "claro"
    c = cores[tema]
    janela.config(bg=c["bg"])
    top_frame.configure(fg_color=c["bg"])
    label.configure(fg_color=c["bg"], text_color=c["fg"])
    button_tema.configure(fg_color=c["botao_bg"], text_color=c["botao_fg"], hover_color="#440A0A" if "escuro" else "#4CAF50")
    button_recarregar.configure(fg_color=c["botao_bg"], text_color=c["botao_fg"], hover_color="#440A0A" if "escuro" else "#4CAF50")
    button_imprimir.configure(fg_color=c["botao_bg"], text_color=c["botao_fg"], hover_color="#440A0A"if "escuro" else "#4CAF50")
    arquivo_atual_label.configure(fg_color=c["bg"], text_color=c["fg"])

    menu.configure(fg_color=c["menu_bg"], button_color=c["menu_bg"], text_color=c["menu_fg"],
                   dropdown_fg_color=c["menu_bg"], dropdown_text_color=c["menu_fg"],
                   dropdown_hover_color=c["botao_bg"])

    caixa_texto.config(bg=c["caixa_bg"], fg=c["caixa_fg"], insertbackground=c["caixa_fg"])


def alternar_tema():
    global escuro
    escuro = not escuro
    aplicar_tema()


def carregar_arquivo(nome_arquivo):
    if nome_arquivo not in arquivos:
        messagebox.showwarning("Aviso", "Selecione um arquivo válido.")
        return

    caminho = arquivos[nome_arquivo]
    try:
        with open(caminho, 'r', encoding='utf-8') as arquivo:
            conteudo = arquivo.read()
            caixa_texto.config(state='normal')
            caixa_texto.delete(1.0, tk.END)
            caixa_texto.insert(tk.END, conteudo)
            caixa_texto.config(state='disabled')
            arquivo_atual_label.configure(text=f"Arquivo aberto: {nome_arquivo}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao abrir o arquivo '{caminho}':\n{e}")


def imprimir_arquivo():
    nome_arquivo = opcao_var.get()
    if nome_arquivo not in arquivos:
        messagebox.showwarning("Aviso", "Selecione um arquivo válido para imprimir.")
        return

    caminho = arquivos[nome_arquivo]
    try:
        with open(caminho, 'r', encoding='utf-8') as arquivo:
            conteudo = arquivo.read()

        # Cria arquivo temporário para impressão
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode='w', encoding='utf-8') as temp_file:
            temp_file.write(conteudo)
            temp_path = temp_file.name

        if os.name == 'nt':
           
            subprocess.Popen(['notepad.exe', '/p', temp_path])
            messagebox.showinfo("Impressão", f"Arquivo '{nome_arquivo}' enviado para impressão.")
        else:
            subprocess.run(['lp', temp_path])
            messagebox.showinfo("Impressão", f"Arquivo '{nome_arquivo}' enviado para impressão.")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao imprimir o arquivo:\n{e}")
    finally:
        try:
            os.remove(temp_path)
        except Exception:
            pass


aplicar_tema()

janela.mainloop()
    