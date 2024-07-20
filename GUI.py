import tkinter as tk
from tkinter import *
import os
from tkinter import filedialog
from Camera import Camera
from TirarFoto import TirarFoto
from tkinter import messagebox
import shutil
from ReconhecimentoFacial import ReconhecimentoFacial

DIR=os.path.dirname(os.path.abspath(__file__))#Diretório do arquivo que está sendo executado

def salvar_imagem():# Função para salvar imagem
    nome_usuario = inputName.get()    # Obtém o nome do usuário a partir do campo de entrada
    if nome_usuario == "":# Verifica se o nome do usuário está vazio
        messagebox.showerror("Erro", "O nome do usuário está vazio. Digite o nome do usuário!")# Exibe uma mensagem de erro se o nome estiver vazio
        return
    arquivo_imagem = filedialog.askopenfilename(# Abre uma caixa de diálogo para selecionar uma imagem
        title="Selecione uma imagem", # Título da janela de seleção de arquivos
        filetypes=[("Arquivos de Imagem", "*.jpg;*.png;*.jpeg")] # Tipos de arquivos permitidos
    )
    if not arquivo_imagem:# Verifica se nenhum arquivo foi selecionado
        messagebox.showinfo("Info", "Nenhuma imagem selecionada.")# Exibe uma mensagem informando que nenhuma imagem foi selecionada
        return
    pasta_fotos = os.path.join(DIR, 'fotos')# Define o caminho para a pasta fotos
    if not os.path.exists(pasta_fotos):# Cria a pasta fotos se não existir
        os.makedirs(pasta_fotos)
    # Define o caminho para salvar a nova imagem
    nome_imagem = f"{nome_usuario}.jpg"  # Usa .jpg como extensão padrão
    caminho_novo = os.path.join(pasta_fotos, nome_imagem)
    try:
        shutil.copy(arquivo_imagem, caminho_novo)# Copia a imagem selecionada para o novo caminho
        messagebox.showinfo("Sucesso", f"Imagem salva como {nome_imagem} na pasta 'fotos'.")# Exibe uma mensagem de sucesso informando onde a imagem foi salva
        inputName.delete(0, tk.END)# Limpa o campo de entrada
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível salvar a imagem: {e}")# Exibe uma mensagem de erro se ocorrer algum problema ao salvar a imagem
def runCamera():# Função para executar a câmera
    cadastrarFace = Camera()# Cria uma instância da classe Camera
    cadastrarFace.reconhecer()# Chama o método reconhecer da instância cadastrarFace para iniciar o reconhecimento facial

def tirarFotos():
    nomeUsuario=inputName.get()
    if nomeUsuario == "":# Verifica se o nome do usuário está vazio
        messagebox.showerror("Erro", "O nome do usuário está vazio. Digite o nome do usuário!")# Exibe uma mensagem de erro se o nome estiver vazio
        return
    tirarfotos=TirarFoto(DIR, nomeUsuario)
    tirarfotos.tirarFoto()

def open_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        reconhecimento=ReconhecimentoFacial(file_path)
        reconhecimento.reconhecer()

janela = tk.Tk()
img = PhotoImage(file=os.path.join(os.path.dirname(__file__), 'icon', 'icon.png'))
janela.iconphoto(False, img)
janela.title("Reconhecimento facial")
janela.geometry("400x250")
janela.configure(bg="#6a0dad")  # Cor de fundo roxo

labelTitle = tk.Label(janela, text="Reconhecimento Facial", font=("calibri", 30), bg="#6a0dad", fg="white")
labelTitle.pack(side=tk.TOP)

labelName = tk.Label(janela, text="Digite o nome da usuário: ", font=("calibri", 12), bg="#6a0dad", fg="white")
labelName.pack(side=tk.TOP)

inputName = tk.Entry(janela, width=40)
inputName.pack(side=tk.TOP)

buttonRegister = tk.Button(janela, text="Cadastrar nova face", width=20, command=tirarFotos, bg="#9370DB", fg="white")
buttonRegister.pack(side=tk.TOP)

buttons_frame = tk.Frame(janela, bg="#6a0dad")
buttons_frame.pack(side=tk.TOP)

button_camera = tk.Button(buttons_frame, text="Abrir Câmera", width=30, command=runCamera, bg="#9370DB", fg="white")
button_camera.pack(pady=10)

button_reconhecimento = tk.Button(buttons_frame, text="Reconhecer em Imagem", width=30, command=open_image, bg="#9370DB", fg="white")
button_reconhecimento.pack(pady=10)

training_label = tk.Label(janela, text="", font=("calibri", 12), bg="#483D8B")

janela.mainloop()
