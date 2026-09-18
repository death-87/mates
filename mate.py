import streamlit as st
import random
import os  # Importamos os para verificar la existencia de la imagen
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

# Configuración de página (Debe ir primero)
st.set_page_config(page_title="📐 Matemáticas — Triángulos", layout="wide")


# ============== BANCOS DE PREGUNTAS (Sin cambios) ==============

banco_area_perimetro = [
    {"pregunta": "Un triángulo tiene base 12 cm y altura 8 cm. Calcula su área.", "respuesta": "48 cm²", "explicacion": "Área = (12 × 8) ÷ 2 = 48 cm²"},
    {"pregunta": "Un triángulo equilátero tiene lado de 10 cm. Calcula su perímetro.", "respuesta": "30 cm", "explicacion": "Perímetro = 3 × 10 = 30 cm"},
    {"pregunta": "Un triángulo rectángulo tiene catetos de 6 cm y 8 cm, y su hipotenusa mide 10 cm. Calcula su perímetro.", "respuesta": "24 cm", "explicacion": "6 + 8 + 10 = 24 cm"},
    {"pregunta": "Un triángulo tiene base 15 m y altura 6 m. Calcula su área.", "respuesta": "45 m²", "explicacion": "(15 × 6) ÷ 2 = 45 m²"},
    {"pregunta": "Un triángulo tiene lados de 7 cm, 9 cm y 12 cm. Calcula su perímetro.", "respuesta": "28 cm", "explicacion": "7 + 9 + 12 = 28 cm"},
    {"pregunta": "Un triángulo isósceles tiene lados iguales de 5 cm y la base mide 6 cm. Calcula su perímetro.", "respuesta": "16 cm", "explicacion": "5 + 5 + 6 = 16 cm"},
    {"pregunta": "Calcula la altura de un triángulo cuya base mide 14 cm y su área es 49 cm².", "respuesta": "7 cm", "explicacion": "49 = (14 × h)/2 → h = 7 cm"},
    {"pregunta": "Un triángulo tiene base 12 cm y altura igual a la mitad de la base. Calcula su área.", "respuesta": "36 cm²", "explicacion": "Altura = 6 cm → Área = (12 × 6) ÷ 2 = 36 cm²"}
]

banco_angulos = [
    {"pregunta": "Dos ángulos de un triángulo miden 40° y 65°. ¿Cuánto mide el tercer ángulo?", "respuesta": "75°", "explicacion": "180° − 105° = 75°"},
    {"pregunta": "En un triángulo rectángulo, un ángulo agudo mide 32°. ¿Cuánto mide el otro ángulo agudo?", "respuesta": "58°", "explicacion": "90° − 32° = 58°"},
    {"pregunta": "Un triángulo es equilátero. ¿Cuánto mide cada uno de sus ángulos?", "respuesta": "60°", "explicacion": "180° ÷ 3 = 60°"},
    {"pregunta": "Un triángulo tiene un ángulo de 110°, y los otros dos ángulos son iguales. ¿Cuánto mide cada uno?", "respuesta": "35°", "explicacion": "70° ÷ 2 = 35°"},
    {"pregunta": "Si un triángulo tiene dos ángulos de 55° cada uno, ¿de qué tipo es y cuánto mide el tercer ángulo?", "respuesta": "Isósceles, 70°", "explicacion": "180° − 110° = 70°, tiene dos ángulos iguales."},
    {"pregunta": "Los tres ángulos de un triángulo son proporcionales a 1, 2 y 3. ¿Cuánto mide cada ángulo?", "respuesta": "30°, 60° y 90°", "explicacion": "x + 2x + 3x = 180° → x = 30°"},
    {"pregunta": "Un ángulo exterior de un triángulo mide 125°, y uno de los ángulos interiores opuestos mide 48°. ¿Cuánto mide el otro?", "respuesta": "77°", "explicacion": "125° − 48° = 77°"},
    {"pregunta": "En un triángulo, el ángulo mayor es el doble que el mediano y el triple que el menor. ¿Cuánto mide cada uno?", "respuesta": "30°, 60°, 90°", "explicacion": "30 + 60 + 90 = 180° ✅"}
]

banco_pitagoras = [
    {"pregunta": "Los catetos de un triángulo rectángulo miden 3 cm y 4 cm. ¿Cuánto mide la hipotenusa?", "respuesta": "5 cm", "explicacion": "3² + 4² = 9 + 16 = 25 → √25 = 5 cm"},
    {"pregunta": "Un cateto mide 12 cm y la hipotenusa 13 cm. ¿Cuánto mide el otro cateto?", "respuesta": "5 cm", "explicacion": "13² − 12² = 169 − 144 = 25 → √25 = 5 cm"},
    {"pregunta": "Los catetos miden 5 cm y 7 cm. Calcula la hipotenusa.", "respuesta": "√74 cm", "explicacion": "5² + 7² = 25 + 49 = 74 → √74 cm"},
    {"pregunta": "Una escalera de 10 m apoya en una pared. Su base está a 6 m de la pared. ¿Qué altura alcanza?", "respuesta": "8 m", "explicacion": "h² + 6² = 10² → h = 8 m"},
    {"pregunta": "Hipotenusa = 18 cm, un cateto = 9 cm. ¿Cuánto mide el otro cateto?", "respuesta": "9√3 cm", "explicacion": "18² − 9² = 243 → √243 = 9√3 cm"},
    {"pregunta": "Catetos 8 cm y 15 cm. Calcula el perímetro.", "respuesta": "40 cm", "explicacion": "Hipotenusa = 17 cm → 8 + 15 + 17 = 40 cm"},
    {"pregunta": "¿Es rectángulo un triángulo de lados 6, 8 y 10 cm?", "respuesta": "Sí", "explicacion": "6² + 8² = 36 + 64 = 100 = 10² ✅"},
    {"pregunta": "Calcula la diagonal de un rectángulo de 12 cm × 5 cm.", "respuesta": "13 cm", "explicacion": "d² = 12² + 5² = 169 → d = 13 cm"}
]

banco_cosenos = [
    {"pregunta": "Lados 5 cm y 7 cm con ángulo de 60° entre ellos. Tercer lado = ?", "respuesta": "√39 cm", "explicacion": "c² = 25 + 49 − 35 = 39 → √39 cm"},
    {"pregunta": "Lados 8, 10 y 12 cm. Ángulo opuesto al de 10 cm = ?", "respuesta": "≈ 55.77°", "explicacion": "cos(B) = 9/16 → B ≈ 55.77°"},
    {"pregunta": "Lados 6 m y 9 m con ángulo de 45° entre ellos. Tercer lado = ?", "respuesta": "√(117 − 54√2) m", "explicacion": "c² = 36 + 81 − 54√2"},
    {"pregunta": "Lados 10, 10 y 12 cm. Área = ?", "respuesta": "48 cm²", "explicacion": "Área = (10 × 10 × sen(C))/2 = 48 cm²"},
    {"pregunta": "Lados 8 cm y 6 cm con ángulo de 120° entre ellos. Tercer lado = ?", "respuesta": "√148 cm", "explicacion": "c² = 64 + 36 + 48 = 148 → √148 cm"},
    {"pregunta": "Lados 7, 9 y 12 cm. Ángulo entre los lados de 7 y 9 cm = ?", "respuesta": "≈ 96.38°", "explicacion": "cos(C) = -1/9 → C ≈ 96.38°"},
    {"pregunta": "Lados 8 cm y 5 cm con ángulo de 60°. Diagonal mayor del paralelogramo = ?", "respuesta": "√129 cm", "explicacion": "d² = 64 + 25 + 40 = 129 → √129 cm"},
    {"pregunta": "Lados 13, 14 y 15 cm. Ángulo mayor = ?", "respuesta": "≈ 67.38°", "explicacion": "cos(C) = 5/13 → C ≈ 67.38°"}
]

banco_trigonometria = [
    {"categoria": "Valores básicos", "pregunta": "¿Cuál es el valor de sen(30°)?", "respuesta": "1/2", "explicacion": "Valor del ángulo notable."},
    {"categoria": "Valores básicos", "pregunta": "¿Cuál es el valor de cos(30°)?", "respuesta": "√3/2", "explicacion": "Valor del ángulo notable."},
    {"categoria": "Valores básicos", "pregunta": "¿Cuál es el valor de sen(45°)?", "respuesta": "√2/2", "explicacion": "Valor del ángulo notable."},
    {"categoria": "Valores básicos", "pregunta": "¿Cuál es el valor de cos(45°)?", "respuesta": "√2/2", "explicacion": "Valor del ángulo notable."},
    {"categoria": "Valores básicos", "pregunta": "¿Cuál es el valor de sen(60°)?", "respuesta": "√3/2", "explicacion": "Valor del ángulo notable."},
    {"categoria": "Valores básicos", "pregunta": "¿Cuál es el valor de cos(60°)?", "respuesta": "1/2", "explicacion": "Valor del ángulo notable."},
    {"categoria": "Valores básicos", "pregunta": "¿Cuál es el valor de tan(30°)?", "respuesta": "√3/3", "explicacion": "sen(30°)/cos(30°)"},
    {"categoria": "Valores básicos", "pregunta": "¿Cuál es el valor de tan(45°)?", "respuesta": "1", "explicacion": "Valor del ángulo notable."},
    {"categoria": "Valores básicos", "pregunta": "¿Cuál es el valor de tan(60°)?", "respuesta": "√3", "explicacion": "Valor del ángulo notable."},
    {"categoria": "Combinaciones", "pregunta": "Calcula: 2·sen(30°) + 3·cos(60°)", "respuesta": "5/2", "explicacion": "2·(1/2) + 3·(1/2) = 5/2"},
    {"categoria": "Combinaciones", "pregunta": "Calcula: sen²(45°) + cos²(45°)", "respuesta": "1", "explicacion": "Identidad fundamental de la trigonometría."},
    {"categoria": "Combinaciones", "pregunta": "Calcula: tan(60°) × cos(30°)", "respuesta": "3/2", "explicacion": "√3 × (√3/2) = 3/2"},
    {"categoria": "📐 Ángulo de elevación", "pregunta": "Desde el suelo, a 12 m de la base de un árbol, se observa su cima con un ángulo de elevación de 45°. ¿Cuál es la altura del árbol?", "respuesta": "12 m", "explicacion": "tan(45°) = h/12 → h = 12 m"},
    {"categoria": "📐 Ángulo de elevación", "pregunta": "Una escalera forma un ángulo de 60° con el suelo y su base está a 4 m de la pared. ¿Qué altura alcanza en la pared?", "respuesta": "4√3 m", "explicacion": "tan(60°) = h/4 → h = 4√3 m"},
    {"categoria": "📐 Ángulo de elevación", "pregunta": "Desde el suelo se observa la cima de una torre de 10 m de altura con un ángulo de 30°. ¿A qué distancia está el observador de la base?", "respuesta": "10√3 m", "explicacion": "tan(30°) = 10/d → d = 10√3 m"},
    {"categoria": "📉 Ángulo de depresión", "pregunta": "Desde un faro de 30 m de altura, se observa un barco con un ángulo de depresión de 45°. ¿A qué distancia está el barco?", "respuesta": "30 m", "explicacion": "Ángulo depresión = ángulo elevación → tan(45°) = 30/d → d = 30 m"},
    {"categoria": "📉 Ángulo de depresión", "pregunta": "Desde la cima de un edificio de 18 m, se observa un punto en el suelo con ángulo de depresión de 60°. ¿Cuál es la distancia horizontal?", "respuesta": "6√3 m", "explicacion": "tan(60°) = 18/d → d = 6√3 m"},
    {"categoria": "📉 Ángulo de depresión", "pregunta": "Un globo aerostático está a 500 m de altura. Se observa un pueblo con ángulo de depresión de 30°. ¿Cuál es la distancia en línea recta al pueblo?", "respuesta": "1000 m", "explicacion": "sen(30°) = 500/d → d = 1000 m"}
]

banco_alternativas = [
    {"pregunta": "¿Cuál es el área de un triángulo con base 10 cm y altura 6 cm?", "opciones": ["A) 16 cm²", "B) 30 cm²", "C) 60 cm²", "D) 120 cm²"], "respuesta_correcta": "B", "explicacion": "Área = (base × altura) ÷ 2 = (10 × 6) ÷ 2 = 30 cm²"},
    {"pregunta": "¿Cuánto mide el tercer ángulo de un triángulo si los otros dos miden 50° y 60°?", "opciones": ["A) 70°", "B) 80°", "C) 90°", "D) 110°"], "respuesta_correcta": "A", "explicacion": "180° − 50° − 60° = 70°"},
    {"pregunta": "En un triángulo rectángulo, los catetos miden 6 cm y 8 cm. ¿Cuánto mide la hipotenusa?", "opciones": ["A) 10 cm", "B) 12 cm", "C) 14 cm", "D) 100 cm"], "respuesta_correcta": "A", "explicacion": "c² = 6² + 8² = 36 + 64 = 100 → c = 10 cm"},
    {"pregunta": "¿Qué valor tiene sen(30°)?", "opciones": ["A) 0", "B) 1/2", "C) √2/2", "D) √3/2"], "respuesta_correcta": "B", "explicacion": "sen(30°) = 1/2"},
    {"pregunta": "Un triángulo con todos sus lados iguales se llama:", "opciones": ["A) Isósceles", "B) Escaleno", "C) Equilátero", "D) Rectángulo"], "respuesta_correcta": "C", "explicacion": "Equilátero = todos sus lados tienen la misma longitud"},
    {"pregunta": "¿Cuánto mide cada ángulo de un triángulo equilátero?", "opciones": ["A) 30°", "B) 45°", "C) 60°", "D) 90°"], "respuesta_correcta": "C", "explicacion": "180° ÷ 3 = 60°"},
    {"pregunta": "¿Cuál es el perímetro de un triángulo con lados de 5 cm, 7 cm y 9 cm?", "opciones": ["A) 21 cm", "B) 23 cm", "C) 112 cm", "D) 11.5 cm"], "respuesta_correcta": "B", "explicacion": "Perímetro = 5 + 7 + 9 = 23 cm"},
    {"pregunta": "¿Qué valor tiene cos(60°)?", "opciones": ["A) 1/2", "B) √2/2", "C) √3/2", "D) 1"], "respuesta_correcta": "A", "explicacion": "cos(60°) = 1/2"},
    {"pregunta": "Si un triángulo tiene un ángulo de 90°, se llama:", "opciones": ["A) Acutángulo", "B) Obtusángulo", "C) Rectángulo", "D) Equilátero"], "respuesta_correcta": "C", "explicacion": "Triángulo rectángulo = tiene un ángulo de 90°"},
    {"pregunta": "Dos ángulos de un triángulo miden 35° y 55°. ¿Qué tipo de triángulo es?", "opciones": ["A) Acutángulo", "B) Rectángulo", "C) Obtusángulo", "D) Equilátero"], "respuesta_correcta": "B", "explicacion": "El tercer ángulo mide 90°, por lo tanto es rectángulo"},
    {"pregunta": "¿Cuál de las siguientes opciones representa correctamente el Teorema de Pitágoras?", "opciones": ["A) a + b = c", "B) a² + b² = c²", "C) a² − b² = c²", "D) a × b = c²"], "respuesta_correcta": "B", "explicacion": "En un triángulo rectángulo: a² + b² = c², donde c es la hipotenusa"},
    {"pregunta": "¿Qué valor tiene tan(45°)?", "opciones": ["A) 0", "B) 1/2", "C) 1", "D) √3"], "respuesta_correcta": "C", "explicacion": "tan(45°) = 1"},
    {"pregunta": "Un triángulo tiene dos ángulos iguales. ¿Qué tipo es?", "opciones": ["A) Equilátero", "B) Isósceles", "C) Escaleno", "D) Rectángulo"], "respuesta_correcta": "B", "explicacion": "Isósceles = tiene dos ángulos y dos lados iguales"},
    {"pregunta": "La suma de los tres ángulos de cualquier triángulo siempre es:", "opciones": ["A) 90°", "B) 180°", "C) 270°", "D) 360°"], "respuesta_correcta": "B", "explicacion": "Propiedad fundamental: la suma es siempre 180°"},
    {"pregunta": "Desde el suelo, a 10 m de la base de un árbol, se observa su cima con un ángulo de 45°. ¿Cuál es su altura?", "opciones": ["A) 5 m", "B) 10 m", "C) 15 m", "D) 20 m"], "respuesta_correcta": "B", "explicacion": "tan(45°) = h/10 → 1 = h/10 → h = 10 m"},
    {"pregunta": "Un triángulo tiene ángulos de 100°, 50° y 30°. ¿De qué tipo es?", "opciones": ["A) Rectángulo", "B) Acutángulo", "C) Obtusángulo", "D) Equilátero"], "respuesta_correcta": "C", "explicacion": "Tiene un ángulo mayor a 90°, por lo tanto es obtusángulo"},
    {"pregunta": "¿Qué fórmula permite calcular el área de un triángulo?", "opciones": ["A) base × altura", "B) (base + altura)/2", "C) (base × altura)/2", "D) perímetro/2"], "respuesta_correcta": "C", "explicacion": "Área = (base × altura) ÷ 2"},
    {"pregunta": "Si la hipotenusa mide 13 cm y un cateto mide 5 cm, ¿cuánto mide el otro cateto?", "opciones": ["A) 8 cm", "B) 10 cm", "C) 12 cm", "D) 18 cm"], "respuesta_correcta": "C", "explicacion": "b² = 13² − 5² = 169 − 25 = 144 → b = 12 cm"},
    {"pregunta": "¿Qué valor tiene sen(60°)?", "opciones": ["A) 1/2", "B) √2/2", "C) √3/2", "D) 1"], "respuesta_correcta": "C", "explicacion": "sen(60°) = √3/2"},
    {"pregunta": "Un triángulo con lados de 3 cm, 4 cm y 5 cm es:", "opciones": ["A) Equilátero", "B) Isósceles", "C) Rectángulo", "D) Obtusángulo"], "respuesta_correcta": "C", "explicacion": "3² + 4² = 5² → cumple el teorema de Pitágoras ✅"}
]

# ============== ESTILOS PDF PROFESIONAL (Sin cambios) ==============
def crear_estilos():
    estilos = getSampleStyleSheet()
    estilo_titulo = ParagraphStyle(
        'Titulo', parent=estilos['Title'], fontSize=18, spaceAfter=16,
        textColor=colors.HexColor('#1F4E79'), alignment=1, bold=True
    )
    estilo_subtitulo = ParagraphStyle(
        'Subtitulo', parent=estilos['Heading2'], fontSize=12, spaceAfter=10,
        textColor=colors.HexColor('#2E86AB'), alignment=1
    )
    estilo_normal = ParagraphStyle(
        'Normal', parent=estilos['Normal'], fontSize=11, spaceAfter=8, leading=14
    )
    estilo_pregunta = ParagraphStyle(
        'Pregunta', parent=estilos['Normal'], fontSize=11, spaceAfter=6, leading=14, bold=True
    )
    estilo_respuesta = ParagraphStyle(
        'Respuesta', parent=estilos['Normal'], fontSize=11, spaceAfter=6,
        textColor=colors.HexColor('#28A745'), leading=14
    )
    estilo_explicacion = ParagraphStyle(
        'Explicacion', parent=estilos['Normal'], fontSize=10, spaceAfter=10,
        textColor=colors.HexColor('#6C757D'), leading=13, leftIndent=15
    )
    return {
        'titulo': estilo_titulo, 'subtitulo': estilo_subtitulo, 'normal': estilo_normal,
        'pregunta': estilo_pregunta, 'respuesta': estilo_respuesta, 'explicacion': estilo_explicacion
    }

# ============== GENERAR PDF DE ALTERNATIVAS (Sin cambios) ==============
def generar_pdf_alternativas(preguntas, titulo, fecha, con_respuestas=False):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=2*cm, bottomMargin=2*cm,
                          leftMargin=2*cm, rightMargin=2*cm)
    estilos = crear_estilos()
    elementos = []
    
    # Encabezado
    elementos.append(Paragraph(titulo, estilos['titulo']))
    elementos.append(Paragraph(f"Fecha: {fecha}", estilos['subtitulo']))
    if not con_respuestas:
        datos = [["Nombre: ___________________________________________", "Curso: _______________"]]
        tabla_datos = Table(datos, colWidths=[13*cm, 5*cm])
        tabla_datos.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8F9FA'))
        ]))
        elementos.append(tabla_datos)
        elementos.append(Spacer(1, 0.5*cm))
        elementos.append(Paragraph("Instrucciones: Selecciona la alternativa correcta para cada pregunta.", estilos['normal']))
    else:
        elementos.append(Paragraph("SOLUCIONARIO — Respuestas y explicaciones", estilos['subtitulo']))
    elementos.append(Spacer(1, 0.5*cm))
    
    # Línea separadora
    linea = Table([[""]], colWidths=[17*cm], rowHeights=[1])
    linea.setStyle(TableStyle([('LINE', (0, 0), (-1, -1), 1, colors.HexColor('#1F4E79'))]))
    elementos.append(linea)
    elementos.append(Spacer(1, 0.5*cm))
    
    # Preguntas
    for i, p in enumerate(preguntas, 1):
        elementos.append(Paragraph(f"<b>{i}.</b> {p['pregunta']}", estilos['pregunta']))
        for opcion in p['opciones']:
            elementos.append(Paragraph(f"&nbsp;&nbsp;{opcion}", estilos['normal']))
        if con_respuestas:
            elementos.append(Paragraph(f"✅ <b>Respuesta correcta:</b> {p['respuesta_correcta']}", estilos['respuesta']))
            elementos.append(Paragraph(f"💡 {p['explicacion']}", estilos['explicacion']))
        elementos.append(Spacer(1, 0.3*cm))
    
    doc.build(elementos)
    buffer.seek(0)
    return buffer

# ============== GENERAR PDF DE DESARROLLO (Sin cambios) ==============
def generar_pdf_desarrollo(preguntas, titulo, fecha, con_respuestas=False):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=2*cm, bottomMargin=2*cm,
                          leftMargin=2*cm, rightMargin=2*cm)
    estilos = crear_estilos()
    elementos = []
    
    elementos.append(Paragraph(titulo, estilos['titulo']))
    elementos.append(Paragraph(f"Fecha: {fecha}", estilos['subtitulo']))
    if not con_respuestas:
        datos = [["Nombre: ___________________________________________", "Curso: _______________"]]
        tabla_datos = Table(datos, colWidths=[13*cm, 5*cm])
        tabla_datos.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8F9FA'))
        ]))
        elementos.append(tabla_datos)
        elementos.append(Spacer(1, 0.5*cm))
        elementos.append(Paragraph("Instrucciones: Resuelve cada ejercicio en el espacio indicado.", estilos['normal']))
    else:
        elementos.append(Paragraph("SOLUCIONARIO — Respuestas y explicaciones", estilos['subtitulo']))
    elementos.append(Spacer(1, 0.5*cm))
    
    linea = Table([[""]], colWidths=[17*cm], rowHeights=[1])
    linea.setStyle(TableStyle([('LINE', (0, 0), (-1, -1), 1, colors.HexColor('#1F4E79'))]))
    elementos.append(linea)
    elementos.append(Spacer(1, 0.5*cm))
    
    for i, p in enumerate(preguntas, 1):
        elementos.append(Paragraph(f"<b>{i}.</b> {p['pregunta']}", estilos['pregunta']))
        if con_respuestas:
            elementos.append(Paragraph(f"✅ <b>Respuesta:</b> {p['respuesta']}", estilos['respuesta']))
            elementos.append(Paragraph(f"💡 {p['explicacion']}", estilos['explicacion']))
        else:
            elementos.append(Spacer(1, 1.5*cm))
            linea_resp = Table([[""]], colWidths=[16*cm], rowHeights=[1])
            linea_resp.setStyle(TableStyle([('LINE', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC'))]))
            elementos.append(linea_resp)
        elementos.append(Spacer(1, 0.4*cm))
    
    doc.build(elementos)
    buffer.seek(0)
    return buffer

# ============== FUNCIONES AUXILIARES (Sin cambios) ==============
def inicializar_sesion(clave, valor_inicial):
    if clave not in st.session_state:
        st.session_state[clave] = valor_inicial

def mostrar_banco(titulo, banco, clave_sesion):
    if titulo: # Solo mostrar cabecera si hay título
        st.header(titulo)
    inicializar_sesion(f"{clave_sesion}_indice", random.randint(0, len(banco)-1))
    inicializar_sesion(f"{clave_sesion}_ver", False)
    
    idx = st.session_state[f"{clave_sesion}_indice"]
    preg = banco[idx]
    
    if "categoria" in preg:
        st.subheader(f"{preg['categoria']}")
    st.info(f"📝 {preg['pregunta']}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👁️ Ver Respuesta", key=f"ver_{clave_sesion}"):
            st.session_state[f"{clave_sesion}_ver"] = True
        if st.session_state[f"{clave_sesion}_ver"]:
            st.success(f"✅ Respuesta: {preg['respuesta']}")
            st.info(f"💡 {preg['explicacion']}")
    with col2:
        if st.button("🔄 Nueva Pregunta", key=f"nueva_{clave_sesion}"):
            st.session_state[f"{clave_sesion}_indice"] = random.randint(0, len(banco)-1)
            st.session_state[f"{clave_sesion}_ver"] = False
            st.rerun()
    st.caption(f"Pregunta {idx+1} de {len(banco)}")

# =============================================================
# ============== ✅ NUEVO DASHBOARD (SIDEBAR) ✅ ==============
# =============================================================

with st.sidebar:
    st.title("Dashboard 📊")
    
    # --- INTRODUCCIÓN DE LA FOTO ---
    ruta_imagen = "IMG_7157.jpeg"
    
    # Verificamos si la imagen existe antes de intentar cargarla
    if os.path.exists(ruta_imagen):
        st.image(ruta_imagen, use_container_width=True, caption="Panel de Control")
    else:
        # Mensaje de error amigable si no encuentra la foto
        st.error(f"⚠️ No se encontró la imagen: {ruta_imagen}")
        st.info("Asegúrate de que la foto esté en la misma carpeta que este script.")
    
    st.divider()
    
    # --- INTRODUCCIÓN DE LAS OPCIONES (NAVEGACIÓN) ---
    st.subheader("Selecciona una sección:")
    opcion_menu = st.radio(
        "Navegación",
        [
            "🏠 Inicio",
            "📏 Área y Perímetro",
            "📐 Ángulos del Triángulo",
            "📐 Teorema de Pitágoras",
            "📐 Ley de Cosenos",
            "🔺 Razones Trigonométricas",
            "📝 Prueba Alternativas",
            "📄 Generar Prueba Desarrollo"
        ],
        label_visibility="collapsed" # Oculta el título del radio para que se vea más limpio
    )
    
    st.divider()
    st.caption("💡 Banco de ejercicios v1.0")

# ===============================================================
# ============== LÓGICA DE VISUALIZACIÓN PRINCIPAL ==============
# ===============================================================

# Título principal siempre visible
st.title("📐 Banco de Ejercicios — Triángulos y Trigonometría")

# Dependiendo de lo seleccionado en el Dashboard (sidebar), mostramos un contenido u otro
if opcion_menu == "🏠 Inicio":
    st.subheader("¡Bienvenido!")
    st.markdown("""
    Utiliza el menú de la izquierda (**Dashboard**) para navegar por las distintas secciones:
    
    *   **Práctica Interactiva:** Repasa ejercicios de las 5 categorías matemáticas.
    *   **Generación de Evaluaciones:** Crea pruebas en PDF (Alternativas o Desarrollo) con su respectivo solucionario listos para imprimir.
    """)
    st.info("Selecciona un tema en el menú para comenzar.")

elif opcion_menu == "📏 Área y Perímetro":
    mostrar_banco("📏 Área y Perímetro", banco_area_perimetro, "area")

elif opcion_menu == "📐 Ángulos del Triángulo":
    mostrar_banco("📐 Ángulos del Triángulo", banco_angulos, "angulos")

elif opcion_menu == "📐 Teorema de Pitágoras":
    mostrar_banco("📐 Teorema de Pitágoras", banco_pitagoras, "pitagoras")
    st.divider()
    st.info("💡 Teorema: a² + b² = c²")

elif opcion_menu == "📐 Ley de Cosenos":
    mostrar_banco("📐 Ley de Cosenos", banco_cosenos, "cosenos")
    st.divider()
    st.latex(r"c^2 = a^2 + b^2 - 2ab \cdot \cos(C)")

elif opcion_menu == "🔺 Razones Trigonométricas":
    st.header("🔺 Razones Trigonométricas — Ángulos Notables")
    with st.expander("📋 Tabla de valores", expanded=True):
        st.markdown("""
| Ángulo θ | sen(θ) | cos(θ) | tan(θ) |
|----------|--------|--------|--------|
| **30°**  | 1/2    | √3/2   | √3/3   |
| **45°**  | √2/2   | √2/2   | 1      |
| **60°**  | √3/2   | 1/2    | √3     |
""")
    st.divider()
    mostrar_banco("", banco_trigonometria, "trigo")

elif opcion_menu == "📝 Prueba Alternativas":
    st.header("📝 Generar Prueba de Alternativas")
    st.info("Selecciona la cantidad de preguntas y genera una prueba con alternativas + solucionario en PDF.")
    
    # Contenedor para organizar mejor
    with st.container(border=True):
        col_config1, col_config2 = st.columns(2)
        with col_config1:
            cant_alt = st.slider("Cantidad de preguntas:", 3, len(banco_alternativas), min(10, len(banco_alternativas)), key="cant_alt")
        with col_config2:
            nombre_alt = st.text_input("Nombre de la prueba:", value="Evaluación de Matemáticas — Triángulos", key="nombre_alt")
        
        fecha_hoy = datetime.now().strftime("%d/%m/%Y")
        btn_generar = st.button("📄 Generar Archivos PDF", type="primary", key="gen_alt")

    if btn_generar:
        with st.spinner("Generando PDFs..."):
            prueba_alt = random.sample(banco_alternativas, cant_alt)
            random.shuffle(prueba_alt)
            
            pdf_prueba = generar_pdf_alternativas(prueba_alt, nombre_alt, fecha_hoy, con_respuestas=False)
            pdf_sol = generar_pdf_alternativas(prueba_alt, nombre_alt, fecha_hoy, con_respuestas=True)
            
            st.success(f"✅ ¡Prueba generada con {len(prueba_alt)} preguntas!")
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.download_button(
                    "📥 Descargar PRUEBA (.pdf)",
                    data=pdf_prueba,
                    file_name=f"Prueba_Alternativas_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            with col_b:
                st.download_button(
                    "📥 Descargar SOLUCIONARIO (.pdf)",
                    data=pdf_sol,
                    file_name=f"Solucionario_Alternativas_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            
            st.divider()
            st.subheader("👁️ Vista previa rápida de preguntas:")
            for i, p in enumerate(prueba_alt, 1):
                st.markdown(f"**{i}.** {p['pregunta']}")
                # Mostrar solo la primera opción como demo en vista previa
                st.caption(f"Demo opciones: {p['opciones'][0]} ...")

elif opcion_menu == "📄 Generar Prueba Desarrollo":
    st.header("📄 Generar Prueba de Desarrollo")
    st.info("Selecciona los temas y genera una prueba con ejercicios de desarrollo + solucionario en PDF.")
    
    with st.container(border=True):
        temas_seleccion = st.multiselect(
            "Selecciona los temas a incluir:",
            ["Área y Perímetro", "Ángulos del Triángulo", "Teorema de Pitágoras", "Ley de Cosenos", "Razones Trigonométricas"],
            default=["Área y Perímetro", "Teorema de Pitágoras"],
            key="temas_dev"
        )
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            cant_preg = st.slider("Ejercicios por tema:", 1, 8, 4, key="cant_dev")
        with col_c2:
            nombre_prueba = st.text_input("Nombre de la prueba:", value="Evaluación de Desarrollo — Triángulos", key="nombre_dev")
        
        fecha_hoy = datetime.now().strftime("%d/%m/%Y")
        btn_generar_dev = st.button("📄 Generar Archivos PDF", type="primary", key="gen_dev")
    
    mapeo_bancos = {
        "Área y Perímetro": banco_area_perimetro,
        "Ángulos del Triángulo": banco_angulos,
        "Teorema de Pitágoras": banco_pitagoras,
        "Ley de Cosenos": banco_cosenos,
        "Razones Trigonométricas": banco_trigonometria
    }
    
    if btn_generar_dev:
        if not temas_seleccion:
            st.warning("⚠️ Selecciona al menos un tema")
        else:
            with st.spinner("Generando PDFs..."):
                prueba_preguntas = []
                for tema in temas_seleccion:
                    banco = mapeo_bancos[tema]
                    # Ajuste de seguridad por si pides más preguntas de las que existen
                    cantidad_real = min(cant_preg, len(banco))
                    seleccion = random.sample(banco, cantidad_real)
                    # Añadir info del tema a la pregunta para la vista previa
                    for sp in seleccion:
                        sp['_tema'] = tema
                    prueba_preguntas.extend(seleccion)
                
                random.shuffle(prueba_preguntas)
                
                pdf_prueba = generar_pdf_desarrollo(prueba_preguntas, nombre_prueba, fecha_hoy, con_respuestas=False)
                pdf_sol = generar_pdf_desarrollo(prueba_preguntas, nombre_prueba, fecha_hoy, con_respuestas=True)
                
                st.success(f"✅ ¡Prueba generada con {len(prueba_preguntas)} ejercicios!")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.download_button(
                        "📥 Descargar PRUEBA (.pdf)",
                        data=pdf_prueba,
                        file_name=f"Prueba_Desarrollo_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                with col_b:
                    st.download_button(
                        "📥 Descargar SOLUCIONARIO (.pdf)",
                        data=pdf_sol,
                        file_name=f"Solucionario_Desarrollo_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                
                st.divider()
                st.subheader("👁️ Vista previa rápida:")
                for i, p in enumerate(prueba_preguntas[:5], 1): # Muestra max 5 en vista previa
                    st.markdown(f"**{i}.** [{p.get('_tema', '')}] {p['pregunta']}")
                if len(prueba_preguntas) > 5:
                    st.caption(f"... y {len(prueba_preguntas)-5} ejercicios más en el PDF.")

# Pie de página final
st.divider()
st.caption("💡 Los archivos se descargan directamente en PDF con diseño profesional. ¡Buena suerte! 🧠✨")
