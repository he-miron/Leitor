import streamlit as st
from reportlab.lib.pagesizes import A6 # Etiquetas Shopee costumam ser A6
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128
from reportlab.graphics.shapes import Drawing, renderPDF
import qrcode
import os

def gerar_pdf_shopee(dados):
    filename = f"etiqueta_{dados['pedido']}.pdf"
    c = canvas.Canvas(filename, pagesize=A6)
    width, height = A6

    # --- Borda da Etiqueta ---
    c.rect(2*mm, 2*mm, width-4*mm, height-4*mm)

    # --- Cabeçalho FSA MARKET ---
    c.setFont("Helvetica-Bold", 16)
    c.drawString(10*mm, height - 15*mm, "FSA MARKET")
    c.setFont("Helvetica", 10)
    c.drawString(10*mm, height - 20*mm, "Logística E-commerce")

    # --- QR Code (Simulando Rastreio Shopee) ---
    qr = qrcode.make(f"https://fsamarket.com/track/{dados['pedido']}")
    qr.save("temp_qr.png")
    c.drawImage("temp_qr.png", width - 35*mm, height - 35*mm, width=30*mm, height=30*mm)

    # --- Informações do Destinatário ---
    c.setFont("Helvetica-Bold", 11)
    c.drawString(10*mm, height - 45*mm, "DESTINATÁRIO:")
    c.setFont("Helvetica", 10)
    c.drawString(10*mm, height - 50*mm, dados['nome'])
    c.drawString(10*mm, height - 55*mm, f"{dados['rua']}, {dados['num']}")
    c.drawString(10*mm, height - 60*mm, f"CEP: {dados['cep']} - {dados['cidade']}/{dados['uf']}")

    # --- Código de Barras do Pedido ---
    barcode = code128.Code128(dados['pedido'], barHeight=15*mm, barWidth=1.5)
    d = Drawing(width, 20*mm)
    d.add(barcode)
    renderPDF.draw(d, c, 10*mm, 25*mm)
    c.drawCentredString(width/2, 20*mm, dados['pedido'])

    c.showPage()
    c.save()
    return filename

# --- Interface Streamlit ---
st.title("📦 FSA MARKET - Gerador de Etiquetas")
st.subheader("Padrão Shopee / Logística")

with st.form("dados_etiqueta"):
    col1, col2 = st.columns(2)
    with col1:
        pedido = st.text_input("Número do Pedido", value="FSA-123456789")
        nome = st.text_input("Nome do Cliente")
        cep = st.text_input("CEP")
    with col2:
        rua = st.text_input("Endereço")
        num = st.text_input("Número")
        cidade_uf = st.text_input("Cidade/UF", value="Formosa/GO")
    
    submit = st.form_submit_button("Gerar Etiqueta")

if submit:
    dados = {
        "pedido": pedido, "nome": nome, "cep": cep,
        "rua": rua, "num": num, "cidade": cidade_uf.split('/')[0], "uf": cidade_uf.split('/')[-1]
    }
    pdf_path = gerar_pdf_shopee(dados)
    
    with open(pdf_path, "rb") as f:
        st.download_button("📩 Baixar Etiqueta PDF", f, file_name=pdf_path)
