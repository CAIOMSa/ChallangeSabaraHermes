import tensorflow as tf
import numpy as np
import json
import os
from tensorflow.keras.preprocessing.image import load_img, img_to_array # type: ignore
from tensorflow.keras.applications import MobileNetV2 # type: ignore
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D # type: ignore
from tensorflow.keras.models import Model # type: ignore

TAMANHO_IMAGEM = (224, 224)
PASTA_IMAGENS = "banco_de_imagens"


if not os.path.exists(PASTA_IMAGENS):
    os.makedirs(PASTA_IMAGENS)

def salvar_imagem(imagem, nome_arquivo):
    """
    Salva a imagem na pasta banco_de_imagens.
    """
    caminho_arquivo = os.path.join(PASTA_IMAGENS, nome_arquivo)
    with open(caminho_arquivo, "wb") as buffer:
        buffer.write(imagem.file.read())
    return caminho_arquivo

def prever_imagem(nome_arquivo):
    """
    Usa o modelo treinado para classificar uma imagem.
    """
    caminho_imagem = os.path.join(PASTA_IMAGENS, nome_arquivo)

    if not os.path.exists(caminho_imagem):
        return {"erro": "Imagem não encontrada"}

    # Carregar modelo e classes
    model = tf.keras.models.load_model('modelo_classificador.h5')
    with open('class_indices.json', 'r') as f:
        classes = json.load(f)

    img = load_img(caminho_imagem, target_size=TAMANHO_IMAGEM)
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predicao = model.predict(img_array)[0]
    resultados = {classes[i]: float(predicao[i]) for i in range(len(classes)) if predicao[i] > 0.5}

    return resultados
