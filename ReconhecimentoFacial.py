import cv2 as cv
import os
from tkinter import messagebox
from FancyDrawn import FancyDrawn
import face_recognition as fr

# CORES
corVermelha = (0, 0, 255)  # Define a cor vermelha em BGR
corVerde = (0, 255, 0)  # Define a cor verde em BGR

# TEXTOS NAS IMAGENS
textFont = cv.FONT_HERSHEY_SIMPLEX  # Fonte do texto nas imagens
fontScale = 1  # Escala da fonte
textColor = (255, 255, 255)  # Cor do texto em BGR (branco)
textThickness = 2  # Espessura do texto

class ReconhecimentoFacial():
    def __init__(self, image_path):
        self.__facesCodificadasConhecidas = []  # Lista de codificações faciais conhecidas
        self.__nomeDasFacesConhecidas = []  # Lista de nomes conhecidos
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Diretório base
        fotos_dir = os.path.join(base_dir, "fotos")  # Diretório das fotos
        self.__img = cv.imread(image_path)
        print(f"Carregando imagem para reconhecimento: {image_path}")

        if self.__img is None:
            print(f"Erro ao carregar a imagem: {image_path}")
            return

        try:
            for filename in os.listdir(fotos_dir):  # Percorre os arquivos no diretório de fotos
                if filename.endswith(".jpg") or filename.endswith(".png"):  # Verifica a extensão do arquivo
                    img_path = os.path.join(fotos_dir, filename)  # Caminho da imagem
                    try:
                        img = fr.load_image_file(img_path)  # Carrega a imagem
                        print(f"Imagem carregada: {img_path}")
                        facesCodificadas = fr.face_encodings(img)  # Codifica a face na imagem
                        if facesCodificadas:  # Se houver codificação
                            self.__facesCodificadasConhecidas.append(facesCodificadas[0])  # Adiciona a codificação à lista
                            self.__nomeDasFacesConhecidas.append(os.path.splitext(filename)[0])  # Adiciona o nome à lista
                            print(f"Face codificada para: {filename}")
                        else:
                            print(f"Nenhuma face encontrada em: {img_path}")
                    except Exception as e:
                        print(f"Erro ao processar a imagem {img_path}: {e}")
        except Exception as e:
            print(f"Erro ao acessar a pasta 'fotos': {e}")
            messagebox.showerror("FACE CAR - Erro", f"Erro ao acessar a pasta 'fotos': {e}")  # Exibe uma mensagem de erro

    def reconhecer(self):
        rgb_frame = cv.cvtColor(self.__img, cv.COLOR_BGR2RGB)  # Converte o frame de BGR para RGB
        facesDetectadas = fr.face_locations(rgb_frame)  # Detecta a localização das faces no frame
        facesCodificadas = fr.face_encodings(rgb_frame, facesDetectadas)  # Obtém as codificações das faces detectadas
        print(f"Faces detectadas: {facesDetectadas}")

        for (top, right, bottom, left), face_encoding in zip(facesDetectadas, facesCodificadas):  # Itera sobre as faces detectadas e suas codificações
            matches = fr.compare_faces(self.__facesCodificadasConhecidas, face_encoding)  # Compara a face detectada com as faces conhecidas
            print(f"Correspondências: {matches}")

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
                else:
                    name = "Desconhecido"  # Define o nome como "Desconhecido"
                    confianca = 0.0  # Define a confiança como 0.0

            # Formata o texto com o nome e confiança
            texto = f"{name} - {round(confianca, 2)}%"
            (texto_largura, texto_altura), _ = cv.getTextSize(texto, textFont, fontScale, textThickness)  # Obtém a largura e altura do texto
            # Desenha o fundo do retângulo para o texto
            cv.rectangle(self.__img, (left, top - texto_altura - 10), (left + texto_largura, top), (0, 0, 0), -1)
            # Adiciona o texto ao frame
            cv.putText(self.__img, texto, (left, top - 10), textFont, fontScale, textColor, textThickness, cv.LINE_AA)
            fancydrawn = FancyDrawn(self.__img, corVerde if name != "Desconhecido" else corVermelha)  # Cria um objeto FancyDrawn com cor verde ou vermelha
            bbox = (left, top, right - left, bottom - top)  # Define a caixa delimitadora
            self.__img = fancydrawn.draw(bbox)  # Desenha a caixa delimitadora no frame

        cv.imshow('Detected Face', self.__img)
        cv.waitKey(0)
        cv.destroyAllWindows()

if __name__ == "__main__":
    file_path = input("Informe o diretório da foto: ")
    if file_path:
        reconhecimento = ReconhecimentoFacial(file_path)
        reconhecimento.reconhecer()
