import cv2 as cv  # Importa a biblioteca OpenCV para processamento de imagens e vídeos
import time  # Importa a biblioteca time para funções relacionadas ao tempo
import os  # Importa a biblioteca os para manipulação de arquivos e diretórios
from FancyDrawn import FancyDrawn  # Importa a classe FancyDrawn do módulo FancyDrawn
from tkinter import messagebox
from datetime import datetime  # Importa a classe datetime do módulo datetime
import face_recognition as fr  # Importa a biblioteca face_recognition para reconhecimento facial

initialInvasionLimitTime = 10  # Tempo limite inicial para invasão em segundos
initialSafeLimitTime = 5  # Tempo limite inicial de segurança em segundos
cronometroDeRoubo = None  # Variável para armazenar o cronômetro de roubo
cronometroSeguranca = None  # Variável para armazenar o cronômetro de segurança

# CORES
corVermelha = (0, 0, 255)  # Define a cor vermelha em BGR
corVerde = (0, 255, 0)  # Define a cor verde em BGR

# TEXTOS NAS IMAGENS
textFont = cv.FONT_HERSHEY_SIMPLEX  # Fonte do texto nas imagens
fontScale = 1  # Escala da fonte
textColor = (255, 255, 255)  # Cor do texto em BGR (branco)
textThickness = 2  # Espessura do texto

class Camera():
    def __init__(self):
        self.__facesCodificadasConhecidas = []  # Lista de codificações faciais conhecidas
        self.__nomeDasFacesConhecidas = []  # Lista de nomes conhecidos
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Diretório base
        fotos_dir = os.path.join(base_dir, "fotos")  # Diretório das fotos
        try:
            for filename in os.listdir(fotos_dir):  # Percorre os arquivos no diretório de fotos
                if filename.endswith(".jpg") or filename.endswith(".png"):  # Verifica a extensão do arquivo
                    img_path = os.path.join(fotos_dir, filename)  # Caminho da imagem
                    try:
                        img = fr.load_image_file(img_path)  # Carrega a imagem
                        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)  # Converte a imagem para RGB
                        facesCodificadas = fr.face_encodings(img)  # Codifica a face na imagem
                        if facesCodificadas:  # Se houver codificação
                            self.__facesCodificadasConhecidas.append(facesCodificadas[0])  # Adiciona a codificação à lista
                            self.__nomeDasFacesConhecidas.append(os.path.splitext(filename)[0])  # Adiciona o nome à lista
                    except Exception as e:
                        print(f"Erro ao processar a imagem {img_path}: {e}")
        except Exception as e:
            print(f"Erro ao acessar a pasta 'fotos': {e}")
            messagebox.showerror("FACE CAR - Erro", f"Erro ao acessar a pasta 'fotos': {e}")  # Exibe uma mensagem de erro
    def reconhecer(self):
        global corVerde, corVermelha  # Declara variáveis globais usadas para cronômetros e cores
        
        camera = cv.VideoCapture(0, cv.CAP_DSHOW)  # Inicializa a captura de vídeo da câmera padrão
        
        # Time variables
        tempoFinal = 0  # Variável para armazenar o tempo final de captura de frame
        tempoInicial = 0  # Variável para armazenar o tempo inicial de captura de frame
        
        while camera.isOpened():  # Loop que continua enquanto a câmera estiver aberta
            _, frame = camera.read()  # Lê um frame da câmera
            rgb_frame = frame[:, :, ::-1]  # Converte o frame de BGR para RGB
            # Find all the faces and face encodings in the current frame
            facesDetectadas = fr.face_locations(rgb_frame)  # Detecta a localização das faces no frame
            facesCodificadas = fr.face_encodings(rgb_frame, facesDetectadas)  # Obtém as codificações das faces detectadas
            # Show FPS
            tempoFinal = time.time()  # Obtém o tempo final para cálculo de FPS
            fps = int(1 / (tempoFinal - tempoInicial))  # Calcula o FPS como o inverso do tempo entre frames
            tempoInicial = tempoFinal  # Atualiza o tempo inicial para o próximo frame
            # Adiciona a informação de FPS ao frame
            cv.putText(frame, f"FPS: {(fps)}", (5, 70), textFont, fontScale, textColor, 3)  # Coloca o texto de FPS no frame
            for (top, right, bottom, left), face_encoding in zip(facesDetectadas, facesCodificadas):  # Itera sobre as faces detectadas e suas codificações
                # See if the face in the frame matches the known face(s)
                matches = fr.compare_faces(self.__facesCodificadasConhecidas, face_encoding)  # Compara a face detectada com as faces conhecidas
                if not matches:  # Se não houver correspondência com faces conhecidas
                    name = "Desconhecido"  # Define o nome como "Desconhecido"
                    confianca = 0.0  # Define a confiança como 0.0
                else:
                    # Use the known face with the smallest distance to the new face
                    face_distances = fr.face_distance(self.__facesCodificadasConhecidas, face_encoding)  # Calcula a distância das faces conhecidas para a face detectada
                    best_match_index = face_distances.argmin()  # Obtém o índice da melhor correspondência (menor distância)
                    if best_match_index < len(matches) and matches[best_match_index]:  # Verifica se a melhor correspondência é válida
                        name = self.__nomeDasFacesConhecidas[best_match_index]  # Obtém o nome da melhor correspondência
                        confianca = (1 - face_distances[best_match_index]) * 100  # Calcula a confiança como um percentual
                        # Formata o texto com o nome e confiança
                        texto = f"{name} - {round(confianca, 2)}%"
                        (texto_largura, texto_altura), _ = cv.getTextSize(texto, textFont, fontScale, textThickness)  # Obtém a largura e altura do texto
                        # Desenha o fundo do retângulo para o texto
                        cv.rectangle(frame, (left, top - texto_altura - 10), (left + texto_largura, top), (0,0,0), -1)
                        # Adiciona o texto ao frame
                        cv.putText(frame, texto, (left, top - 10), textFont, fontScale, textColor, textThickness, cv.LINE_AA)
                        fancydrawn = FancyDrawn(frame, corVerde)  # Cria um objeto FancyDrawn com cor verde
                        bbox = (left, top, right - left, bottom - top)  # Define a caixa delimitadora
                        frame = fancydrawn.draw(bbox)  # Desenha a caixa delimitadora no frame
                    else:
                        name = "Desconhecido"  # Define o nome como "Desconhecido"
                        confianca = 0.0  # Define a confiança como 0.0
                        # Formata o texto com o nome e confiança
                        texto = f"{name} - {round(confianca, 2)}%"
                        (texto_largura, texto_altura), _ = cv.getTextSize(texto, textFont, fontScale, textThickness)  # Obtém a largura e altura do texto
                        # Desenha o fundo do retângulo para o texto
                        cv.rectangle(frame, (left, top - texto_altura - 10), (left + texto_largura, top), (0,0,0), -1)
                        # Adiciona o texto ao frame
                        cv.putText(frame, texto, (left, top - 10), textFont, fontScale, textColor, textThickness, cv.LINE_AA)
                        # Desenha uma caixa ao redor da face usando FancyDrawn
                        fancydrawn = FancyDrawn(frame, corVermelha)  # Cria um objeto FancyDrawn com cor vermelha
                        bbox = (left, top, right - left, bottom - top)  # Define a caixa delimitadora
                        frame = fancydrawn.draw(bbox)  # Desenha a caixa delimitadora no frame
            key = cv.waitKey(1)  # ESC = 27
            if key == 27:  # Se apertou o ESC
                break
            cv.imshow("Camera", frame)
        cv.destroyAllWindows()

if __name__ == "__main__":
    cadastrarFace=Camera()
    cadastrarFace.reconhecer()
