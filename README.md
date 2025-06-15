# 🧾 Verificador de Validade de Produtos com OCR

Este projeto realiza a verificação de datas de validade em rótulos de produtos por meio de OCR (Reconhecimento Óptico de Caracteres). É possível processar imagens de uma pasta, identificar a data de validade e gerar um relatório em PDF.

## 🧠 Técnicas Aplicadas
- Pré-processamento de Imagem:

Conversão para tons de cinza e limiarização (binarização) para melhorar a acurácia do OCR.

- OCR com Tesseract:

Extração de texto das imagens.

- Regex:

Busca de padrões no formato de data dd/mm/yyyy ou dd-mm-yyyy.

- Validação:

Comparação com a data atual para indicar se o produto está vencido.

## 📌 Observações
O OCR pode falhar se a imagem estiver borrada ou com contraste ruim.

A precisão melhora com imagens bem iluminadas e bem recortadas.

## 📦 Funcionalidades

- Seleção de uma pasta com imagens de rótulos.
- Extração automática das datas das imagens usando OCR (Tesseract).
- Verificação da validade (vencido ou não).
- Geração de um relatório PDF com os resultados.
- Barra de progresso durante o processamento.

## 🛠️ Tecnologias Utilizadas e Requisitos
- Python 3.10+
- Tesseract OCR
- OpenCV
- Regex
- FPDF
- Tkinter (GUI)

## 📥 Instalação
1. Clone o repositório:
   ```bash
   git clone https://github.com/seuusuario/repositorio.git
   cd repositorio

2. Instale as dependências necessárias
   ```bash
   $ pip install easyocr
   $ pip install reportlab
   $ pip install ttkbootstrap

3. Instale o Tesseract OCR
   Baixe e instale: https://github.com/UB-Mannheim/tesseract/wiki

## ▶️ Executar
   1. $ python app.py;
   2. Escolha a pasta contendo as imagens de rótulos;
   3. Aguarde enquanto o programa processa os arquivos (a barra de progresso será exibida);
   4. O resultado irá aparecer em sua tela (Você pode gerar um relatório a partir desse resultado).