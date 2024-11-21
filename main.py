import os
import tkinter as tk
from tkinter import filedialog, messagebox


def parse_input(input_text):
    """
    Analisa o texto de entrada e retorna um dicionário representando a estrutura de diretórios e arquivos.
    """
    estrutura = {}
    caminho_atual = []

    for linha in input_text.splitlines():
        linha = linha.strip()
        if not linha:
            continue

        # Diretório
        if linha.endswith("/"):
            nivel = linha.count("├") + linha.count("└")
            dir_name = linha.replace("├── ", "").replace("└── ", "").strip("/")
            while len(caminho_atual) > nivel:
                caminho_atual.pop()
            caminho_atual.append(dir_name)
            dir_path = "/".join(caminho_atual)
            estrutura[dir_path] = []
        else:  # Arquivo
            file_name = linha.replace("├── ", "").replace("└── ", "").split("#")[0].strip()
            dir_path = "/".join(caminho_atual)
            estrutura[dir_path].append(file_name)

    return estrutura


def criar_estrutura(estrutura, pasta_destino):
    """
    Cria a estrutura de diretórios e arquivos na pasta especificada.
    """
    for pasta, arquivos in estrutura.items():
        caminho_pasta = os.path.join(pasta_destino, pasta)
        if not os.path.exists(caminho_pasta):
            os.makedirs(caminho_pasta)

        for arquivo in arquivos:
            caminho_arquivo = os.path.join(caminho_pasta, arquivo)
            if not os.path.exists(caminho_arquivo):
                with open(caminho_arquivo, "w") as f:
                    if arquivo.endswith(".py"):
                        f.write("# Arquivo gerado automaticamente\n")
                    elif arquivo.endswith(".txt"):
                        f.write("")
                    elif arquivo.endswith(".png"):
                        f.write("")  # Placeholder para imagens


def selecionar_pasta():
    """
    Abre o seletor de pastas para o usuário escolher o diretório de destino.
    """
    pasta = filedialog.askdirectory()
    if pasta:
        pasta_entry.delete(0, tk.END)
        pasta_entry.insert(0, pasta)


def gerar_estrutura():
    """
    Gera a estrutura com base na entrada do usuário e na pasta selecionada.
    """
    input_text = estrutura_text.get("1.0", tk.END).strip()
    pasta_destino = pasta_entry.get()

    if not input_text or not pasta_destino:
        messagebox.showerror("Erro", "Insira a estrutura e selecione a pasta de destino.")
        return

    try:
        estrutura = parse_input(input_text)
        criar_estrutura(estrutura, pasta_destino)
        messagebox.showinfo("Sucesso", "Estrutura criada com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao criar estrutura: {str(e)}")


# Interface gráfica com tkinter
root = tk.Tk()
root.title("Gerador de Estrutura de Projetos")
root.geometry("600x400")

# Entrada de texto para a estrutura
estrutura_label = tk.Label(root, text="Estrutura do Projeto:")
estrutura_label.pack(pady=5)

estrutura_text = tk.Text(root, height=15, width=70)
estrutura_text.pack(pady=5)

# Campo para selecionar a pasta de destino
pasta_frame = tk.Frame(root)
pasta_frame.pack(pady=5)

pasta_label = tk.Label(pasta_frame, text="Pasta de Destino:")
pasta_label.pack(side=tk.LEFT, padx=5)

pasta_entry = tk.Entry(pasta_frame, width=50)
pasta_entry.pack(side=tk.LEFT, padx=5)

pasta_button = tk.Button(pasta_frame, text="Selecionar", command=selecionar_pasta)
pasta_button.pack(side=tk.LEFT, padx=5)

# Botão para gerar a estrutura
gerar_button = tk.Button(root, text="Gerar Estrutura", command=gerar_estrutura)
gerar_button.pack(pady=20)

# Iniciar o loop principal
root.mainloop()
