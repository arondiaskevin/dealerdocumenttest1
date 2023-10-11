from flask import Flask, render_template, request
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)

# Função para editar o PDF
def editar_pdf(input_pdf, output_pdf, lista_de_textos):
    # Lendo o PDF de entrada
    reader = PdfReader(input_pdf)

    # Criando um objeto para escrever o novo PDF
    writer = PdfWriter()

    # Iterando sobre cada página do PDF de entrada
    for i, pagina in enumerate(reader.pages):
        # Obtendo a lista de textos e posições específicas para a página atual
        textos_e_posicoes = lista_de_textos[i]

        # Iterando sobre cada texto e posição
        for texto, posicao_x, posicao_y in textos_e_posicoes:
            # Criando um buffer de bytes para adicionar o texto ao PDF
            packet = io.BytesIO()
            # Criando um objeto de desenho (canvas)
            c = canvas.Canvas(packet)
            # Adicionando o texto à posição especificada
            c.drawString(posicao_x, posicao_y, texto)
            # Salvando o canvas no buffer
            c.save()
            # Movendo o cursor do buffer para o início
            packet.seek(0)
            # Lendo o conteúdo do buffer como um novo PDF
            overlay = PdfReader(packet)

            # Mesclando a página atual com o novo PDF contendo o texto
            pagina.merge_page(overlay.pages[0])

        # Adicionando a página modificada ao novo PDF
        writer.add_page(pagina)

    # Escrevendo o novo PDF no arquivo de saída
    with open(output_pdf, "wb") as arquivo_saida:
        writer.write(arquivo_saida)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gerar_pdf', methods=['POST'])
def gerar_pdf():
    # Obter os dados do formulário
    customer_name = request.form['customer_name']
    dob = request.form['dob']
    dl_number = request.form['dl_number']
    dl_state = request.form['dl_state']
    street_address = request.form['street_address']
    city = request.form['city']
    zip_code = request.form['zip_code']
    state = request.form['state']
    car_year = request.form['car_year']
    vin = request.form['vin']
    car_make = request.form['car_make']
    car_model = request.form['car_model']
    car_cylinder = request.form['car_cylinder']
    car_color = request.form['car_color']

    # Definindo os textos e posições para cada página
    textos_por_pagina = [
        [
            (dl_number, 27, 650),
            (customer_name, 27, 628),
            (dl_state, 200, 650),
            (dob, 240, 650),
            (street_address, 27, 605),
            (city, 308, 605),
            (state, 480, 605),
            (zip_code, 520, 605),
            (vin, 230, 428),
            (car_color, 230, 408),
            (car_year, 230, 450),
            (car_make, 275, 450),
            (car_model, 408, 450),
            (car_cylinder, 499, 430),
        ],
         [  # Página 2
            (car_make, 78, 645),
            (car_model, 205, 645),
            (car_year, 305, 645),
            (vin, 385, 645),
    ],
          [  # Página
            ("Texto na terceira página", 25, 650),
            ("Outro texto na terceira página", 25, 628),
    ],
        
    ]

    # Chamando a função para editar o PDF
    editar_pdf("document.pdf", "output.pdf", textos_por_pagina)

    return "PDF gerado com sucesso!"

if __name__ == '__main__':
    app.run(debug=True)
