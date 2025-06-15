import os
import re
from datetime import datetime
import cv2
import easyocr
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox

# Inicializa o leitor do EasyOCR
reader = easyocr.Reader(['pt'])
resultados = []
resultadosPdf = []

# Função para pré-processar imagem
def preprocessar_imagem(caminho):
    imagem = cv2.imread(caminho)
    if imagem is None:
        return None
    imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    imagem = cv2.bilateralFilter(imagem, 11, 17, 17)
    _, imagem = cv2.threshold(imagem, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return imagem

# Função para extrair e interpretar data
def extrair_data(textos):
    datas_preferenciais = []
    outras_datas = []

    for texto in textos:
        conteudo = texto[1].upper()
        data_bruta = re.sub(r'[^0-9./-]', '', conteudo)
        match = re.search(r'(\d{2})[./-](\d{2})[./-](\d{2,4})', data_bruta)
        if match:
            dia, mes, ano = match.groups()
            if len(ano) == 2:
                ano = '20' + ano
            try:
                data = datetime.strptime(f"{dia}.{mes}.{ano}", "%d.%m.%Y")
                if "VAL" in conteudo:
                    datas_preferenciais.append(data)
                if "V" in conteudo:
                    datas_preferenciais.append(data)
                else:
                    outras_datas.append(data)
            except ValueError:
                continue

    if datas_preferenciais:
        return datas_preferenciais[0]
    elif outras_datas:
        return outras_datas[0]
    else:
        return None

def processar_imagens(pasta, resultado_box):
    hoje = datetime.today()
    resultados.clear()
    arquivos = [nome for nome in os.listdir(pasta) if nome.lower().endswith((".jpg", ".png", ".jpeg", ".webp"))]

    progresso["maximum"] = len(arquivos)
    progresso["value"] = 0

    for i, nome_img in enumerate(arquivos, 1):
        caminho_img = os.path.join(pasta, nome_img)
        imagem = preprocessar_imagem(caminho_img)
        if imagem is None:
            resultado = f"{nome_img}: Erro ao carregar imagem."
        else:
            textos = reader.readtext(imagem)
            data = extrair_data(textos)
            if data:
                status = "VENCIDO" if data < hoje else "DENTRO DA VALIDADE"
                resultado = f"{data.strftime('%d/%m/%Y')} - PRODUTO {status}"
                resultadoPdf = f"{nome_img} - {data.strftime('%d/%m/%Y')} - PRODUTO {status}"
            else:
                resultado = "Data não identificada."
                resultadoPdf = "Data não identificada."

        resultados.append((nome_img, resultado))
        resultadosPdf.append((nome_img, resultadoPdf))
        resultado_box.insert("", "end", values=(nome_img, resultado))
        progresso["value"] = i
        app.update_idletasks()

    progresso["value"] = 0

def gerar_pdf():
    if not resultadosPdf:
        messagebox.showwarning("Aviso", "Nenhum resultado para salvar.")
        return

    caminho = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
    if not caminho:
        return

    c = canvas.Canvas(caminho, pagesize=A4)
    width, height = A4
    y = height - 50
    c.setFont("Helvetica", 12)
    c.drawString(50, y, "Relatório de Validade de Produtos")
    y -= 30
    for _, linha in resultadosPdf:
        c.drawString(50, y, linha)
        y -= 20
        if y < 50:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 12)
    c.save()
    messagebox.showinfo("Sucesso", f"PDF salvo em:\n{caminho}")

# Escolher pasta
def escolher_pasta():
    pasta = filedialog.askdirectory()
    if pasta:
        processar_imagens(pasta, treeview)

# Criar interface com ttkbootstrap
app = ttk.Window(themename="cosmo")
app.title("Verificador de Validade de Produtos")
app.geometry("700x500")

label_titulo = ttk.Label(app, text="Validação de Datas em Rótulos", font=("Segoe UI", 16, "bold"))
label_titulo.pack(pady=10)

frame_botoes = ttk.Frame(app)
frame_botoes.pack(pady=10)

btn_escolher = ttk.Button(frame_botoes, text="Escolher Pasta", bootstyle=PRIMARY, command=escolher_pasta)
btn_escolher.pack(side=LEFT, padx=10)

btn_pdf = ttk.Button(frame_botoes, text="Gerar PDF", bootstyle=SUCCESS, command=gerar_pdf)
btn_pdf.pack(side=LEFT, padx=10)

progresso = ttk.Progressbar(app, orient="horizontal", length=500, mode="determinate")
progresso.pack(pady=5)

# Tabela com Treeview
treeview = ttk.Treeview(app, columns=("Imagem", "Resultado"), show="headings", height=15, bootstyle="info")
treeview.heading("Imagem", text="Nome da Imagem - Produto", anchor="center")
treeview.heading("Resultado", text="Resultado da Verificação", anchor="center")
treeview.column("Imagem", width=250, anchor="center")
treeview.column("Resultado", width=400, anchor="center")
treeview.pack(pady=20, fill="both", expand=True)
app.mainloop()
