import streamlit as st
import random
import os
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage

# Configuración de página
st.set_page_config(page_title="📐 Matemáticas — Triángulos", layout="wide")

# ============== GENERADOR AUTOMÁTICO DE ESQUEMAS ==============

def generar_esquema_grafico(tipo, datos):
    """
    Genera automáticamente un esquema vectorial usando Matplotlib 
    y retorna un buffer en memoria (BytesIO) listo para Streamlit o ReportLab.
    """
    fig, ax = plt.subplots(figsize=(4, 2.8), dpi=150)
    ax.set_aspect('equal')
    ax.axis('off')

    if tipo == "triangulo_rectangulo":
        base = datos.get("base", 4)
        altura = datos.get("altura", 3)
        lbl_base = datos.get("lbl_base", f"{base}")
        lbl_altura = datos.get("lbl_altura", f"{altura}")
        lbl_hip = datos.get("lbl_hip", "")
        lbl_angulo = datos.get("lbl_angulo", "")

        # Puntos del triángulo
        x = [0, base, 0, 0]
        y = [0, 0, altura, 0]
        ax.plot(x, y, color='#1F4E79', lw=2.5)
        ax.fill(x, y, color='#EBF5FB', alpha=0.6)

        # Símbolo de ángulo recto (90°)
        sq_size = min(base, altura) * 0.1
        ax.plot([0, sq_size, sq_size], [sq_size, sq_size, 0], color='#1F4E79', lw=1.2)

        # Etiquetas
        ax.text(base/2, -altura*0.1, lbl_base, ha='center', va='top', fontsize=10, fontweight='bold', color='#2E86AB')
        ax.text(-base*0.08, altura/2, lbl_altura, ha='right', va='center', rotation=90, fontsize=10, fontweight='bold', color='#2E86AB')
        if lbl_hip:
            ax.text(base/2 + base*0.05, altura/2 + altura*0.05, lbl_hip, ha='left', va='bottom', fontsize=10, fontweight='bold', color='#D9534F')
        if lbl_angulo:
            ax.text(base*0.25, altura*0.08, lbl_angulo, ha='left', va='bottom', fontsize=9, color='#D9534F')

    elif tipo == "elevacion":
        distancia = datos.get("distancia", 10)
        altura = datos.get("altura", 8)
        lbl_ang = datos.get("lbl_ang", "α")

        x = [0, distancia, 0, 0]
        y = [0, 0, altura, 0]
        ax.plot(x, y, color='#1F4E79', lw=2)
        ax.fill(x, y, color='#EBF5FB', alpha=0.5)

        # Línea de suelo
        ax.plot([-distancia*0.1, distancia*1.1], [0, 0], 'k--', lw=1)

        # Arco de ángulo
        arc_x = np.linspace(0, distancia*0.2, 20)
        arc_y = np.tan(np.arctan(altura/distancia)) * arc_x
        ax.plot(arc_x, arc_y, color='#D9534F', lw=1.5)

        ax.text(distancia/2, -altura*0.1, f"Distancia = {distancia} m", ha='center', fontsize=9)
        ax.text(-distancia*0.05, altura/2, f"h = {altura} m", ha='right', va='center', rotation=90, fontsize=9)
        ax.text(distancia*0.22, altura*0.05, lbl_ang, color='#D9534F', fontweight='bold', fontsize=10)

    elif tipo == "depresion":
        altura = datos.get("altura", 10)
        distancia = datos.get("distancia", 12)
        lbl_ang = datos.get("lbl_ang", "β")

        # Triángulo
        ax.plot([0, distancia, distancia, 0], [altura, 0, altura, altura], color='#1F4E79', lw=2)
        ax.fill([0, distancia, distancia], [altura, 0, altura], color='#FDEDEC', alpha=0.5)

        # Línea horizontal de visión (arriba)
        ax.plot([-distancia*0.1, distancia*1.1], [altura, altura], 'r--', lw=1.2, label='Línea horizontal')

        ax.text(distancia/2, altura + altura*0.08, f"Ángulo de depresión ({lbl_ang})", ha='center', color='#D9534F', fontsize=9)
        ax.text(distancia + distancia*0.05, altura/2, f"Altura = {altura} m", ha='left', va='center', rotation=270, fontsize=9)
        ax.text(distancia/2, -altura*0.1, "x (distancia al suelo)", ha='center', fontsize=9)

    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=150)
    plt.close(fig)
    buffer.seek(0)
    return buffer


# ============== BANCOS DE PREGUNTAS (Con Gráficos Automáticos) ==============

banco_area_perimetro = [
    {
        "pregunta": "Un triángulo tiene base 12 cm y altura 8 cm. Calcula su área.", 
        "respuesta": "48 cm²", 
        "explicacion": "Área = (12 × 8) ÷ 2 = 48 cm²",
        "esquema": {"tipo": "triangulo_rectangulo", "datos": {"base": 12, "altura": 8, "lbl_base": "b = 12 cm", "lbl_altura": "h = 8 cm"}}
    },
    {"pregunta": "Un triángulo equilátero tiene lado de 10 cm. Calcula su perímetro.", "respuesta": "30 cm", "explicacion": "Perímetro = 3 × 10 = 30 cm"},
    {"pregunta": "Un triángulo rectángulo tiene catetos de 6 cm y 8 cm, y su hipotenusa mide 10 cm. Calcula su perímetro.", "respuesta": "24 cm", "explicacion": "6 + 8 + 10 = 24 cm"},
    {"pregunta": "Un triángulo tiene base 15 m y altura 6 m. Calcula su área.", "respuesta": "45 m²", "explicacion": "(15 × 6) ÷ 2 = 45 m²"}
]

banco_angulos = [
    {"pregunta": "Dos ángulos de un triángulo miden 40° y 65°. ¿Cuánto mide el tercer ángulo?", "respuesta": "75°", "explicacion": "180° − 105° = 75°"},
    {"pregunta": "En un triángulo rectángulo, un ángulo agudo mide 32°. ¿Cuánto mide el otro ángulo agudo?", "respuesta": "58°", "explicacion": "90° − 32° = 58°"}
]

banco_pitagoras = [
    {
        "pregunta": "Los catetos de un triángulo rectángulo miden 3 cm y 4 cm. ¿Cuánto mide la hipotenusa (c)?", 
        "respuesta": "5 cm", 
        "explicacion": "3² + 4² = 9 + 16 = 25 → √25 = 5 cm",
        "esquema": {"tipo": "triangulo_rectangulo", "datos": {"base": 4, "altura": 3, "lbl_base": "4 cm", "lbl_altura": "3 cm", "lbl_hip": "c = ?"}}
    },
    {
        "pregunta": "Un cateto mide 12 cm y la hipotenusa 13 cm. ¿Cuánto mide el otro cateto (a)?", 
        "respuesta": "5 cm", 
        "explicacion": "13² − 12² = 169 − 144 = 25 → √25 = 5 cm",
        "esquema": {"tipo": "triangulo_rectangulo", "datos": {"base": 12, "altura": 5, "lbl_base": "12 cm", "lbl_altura": "a = ?", "lbl_hip": "13 cm"}}
    }
]

banco_cosenos = [
    {"pregunta": "Lados 5 cm y 7 cm con ángulo de 60° entre ellos. Tercer lado = ?", "respuesta": "√39 cm", "explicacion": "c² = 25 + 49 − 35 = 39 → √39 cm"}
]

banco_trigonometria = [
    {
        "categoria": "📐 Ángulo de elevación", 
        "pregunta": "Desde el suelo, a 12 m de la base de un árbol, se observa su cima con un ángulo de elevación de 45°. ¿Cuál es la altura del árbol?", 
        "respuesta": "12 m", 
        "explicacion": "tan(45°) = h/12 → h = 12 m",
        "esquema": {"tipo": "elevacion", "datos": {"distancia": 12, "altura": 12, "lbl_ang": "45°"}}
    },
    {
        "categoria": "📉 Ángulo de depresión", 
        "pregunta": "Desde un faro de 30 m de altura, se observa un barco con un ángulo de depresión de 45°. ¿A qué distancia horizontal está el barco?", 
        "respuesta": "30 m", 
        "explicacion": "Ángulo depresión = ángulo elevación → tan(45°) = 30/d → d = 30 m",
        "esquema": {"tipo": "depresion", "datos": {"distancia": 30, "altura": 30, "lbl_ang": "45°"}}
    }
]

banco_guia_2medio = [
    {
        "categoria": "Triángulos Notables (30°-60°)",
        "pregunta": "En un triángulo rectángulo de 30°-60°, la hipotenusa mide 16 mm. ¿Cuánto miden sus catetos?",
        "respuesta": "Cateto menor = 8 mm, Cateto mayor = 8√3 mm",
        "explicacion": "Hipotenusa = 2k = 16 mm → k = 8 mm. Catetos: 8 mm y 8√3 mm.",
        "esquema": {"tipo": "triangulo_rectangulo", "datos": {"base": 13.8, "altura": 8, "lbl_base": "8√3 mm", "lbl_altura": "8 mm", "lbl_hip": "16 mm", "lbl_angulo": "30°"}}
    },
    {
        "categoria": "Ángulo de Depresión — La Torre",
        "pregunta": "El ángulo de depresión desde lo alto de una torre de 34 m a un punto K en el suelo es de 80°. Calcula la distancia x de K a la base.",
        "respuesta": "≈ 6 metros",
        "explicacion": "tan(10°) = x / 34 → x = 34 · tan(10°) ≈ 6 m.",
        "esquema": {"tipo": "depresion", "datos": {"distancia": 6, "altura": 34, "lbl_ang": "80°"}}
    }
]

banco_alternativas = [
    {"pregunta": "¿Cuál es el área de un triángulo con base 10 cm y altura 6 cm?", "opciones": ["A) 16 cm²", "B) 30 cm²", "C) 60 cm²", "D) 120 cm²"], "respuesta_correcta": "B", "explicacion": "Área = (10 × 6) ÷ 2 = 30 cm²"},
    {"pregunta": "¿Cuánto mide el tercer ángulo de un triángulo si los otros dos miden 50° y 60°?", "opciones": ["A) 70°", "B) 80°", "C) 90°", "D) 110°"], "respuesta_correcta": "A", "explicacion": "180° − 50° − 60° = 70°"}
]


# ============== ESTILOS Y GENERACIÓN PDF ==============

def crear_estilos():
    estilos = getSampleStyleSheet()
    return {
        'titulo': ParagraphStyle('Titulo', parent=estilos['Title'], fontSize=18, spaceAfter=14, textColor=colors.HexColor('#1F4E79'), bold=True),
        'subtitulo': ParagraphStyle('Subtitulo', parent=estilos['Heading2'], fontSize=12, spaceAfter=10, textColor=colors.HexColor('#2E86AB')),
        'normal': ParagraphStyle('Normal', parent=estilos['Normal'], fontSize=11, spaceAfter=6, leading=14),
        'pregunta': ParagraphStyle('Pregunta', parent=estilos['Normal'], fontSize=11, spaceAfter=6, leading=14, bold=True),
        'respuesta': ParagraphStyle('Respuesta', parent=estilos['Normal'], fontSize=11, spaceAfter=4, textColor=colors.HexColor('#28A745')),
        'explicacion': ParagraphStyle('Explicacion', parent=estilos['Normal'], fontSize=10, spaceAfter=8, textColor=colors.HexColor('#6C757D'), leftIndent=12)
    }

def generar_pdf_desarrollo(preguntas, titulo, fecha, con_respuestas=False):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=2*cm, bottomMargin=2*cm, leftMargin=2*cm, rightMargin=2*cm)
    estilos = crear_estilos()
    elementos = []
    
    elementos.append(Paragraph(titulo, estilos['titulo']))
    elementos.append(Paragraph(f"Fecha: {fecha}", estilos['subtitulo']))
    
    if not con_respuestas:
        datos = [["Nombre: ___________________________________________", "Curso: _______________"]]
        tabla_datos = Table(datos, colWidths=[13*cm, 5*cm])
        tabla_datos.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 1, colors.HexColor('#CCCCCC')), ('PADDING', (0,0), (-1,-1), 6)]))
        elementos.append(tabla_datos)
        elementos.append(Spacer(1, 0.4*cm))
        elementos.append(Paragraph("Instrucciones: Resuelve cada ejercicio en el espacio indicado.", estilos['normal']))
    else:
        elementos.append(Paragraph("SOLUCIONARIO — Respuestas y Explicaciones", estilos['subtitulo']))
    
    elementos.append(Spacer(1, 0.4*cm))
    
    for i, p in enumerate(preguntas, 1):
        elementos.append(Paragraph(f"<b>{i}.</b> {p['pregunta']}", estilos['pregunta']))
        
        # INSERTAR ESQUEMA SI EL EJERCICIO TIENE UNO
        if "esquema" in p:
            buf_img = generar_esquema_grafico(p["esquema"]["tipo"], p["esquema"]["datos"])
            img_rl = RLImage(buf_img, width=7*cm, height=4.9*cm)
            elementos.append(img_rl)
            elementos.append(Spacer(1, 0.2*cm))

        if con_respuestas:
            elementos.append(Paragraph(f"✅ <b>Respuesta:</b> {p['respuesta']}", estilos['respuesta']))
            elementos.append(Paragraph(f"💡 {p['explicacion']}", estilos['explicacion']))
        else:
            elementos.append(Spacer(1, 1.2*cm))
            linea_resp = Table([[""]], colWidths=[16*cm], rowHeights=[1])
            linea_resp.setStyle(TableStyle([('LINE', (0,0), (-1,-1), 1, colors.HexColor('#CCCCCC'))]))
            elementos.append(linea_resp)
            
        elementos.append(Spacer(1, 0.4*cm))
    
    doc.build(elementos)
    buffer.seek(0)
    return buffer


# ============== INTERFAZ INTERACTIVA Y NAVEGACIÓN ==============

def inicializar_sesion(clave, valor_inicial):
    if clave not in st.session_state:
        st.session_state[clave] = valor_inicial

def mostrar_banco(titulo, banco, clave_sesion):
    if titulo:
        st.header(titulo)
    inicializar_sesion(f"{clave_sesion}_indice", random.randint(0, len(banco)-1))
    inicializar_sesion(f"{clave_sesion}_ver", False)
    
    idx = st.session_state[f"{clave_sesion}_indice"]
    preg = banco[idx]
    
    if "categoria" in preg:
        st.subheader(f"{preg['categoria']}")
    
    st.info(f"📝 {preg['pregunta']}")
    
    # MOSTRAR ESQUEMA EN PANTALLA SI EXISTE
    if "esquema" in preg:
        buf_img = generar_esquema_grafico(preg["esquema"]["tipo"], preg["esquema"]["datos"])
        st.image(buf_img, caption="Esquema del problema", width=350)

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

with st.sidebar:
    st.title("Dashboard 📊")
    ruta_imagen = "IMG_7157.jpeg"
    if os.path.exists(ruta_imagen):
        st.image(ruta_imagen, use_container_width=True)
    
    st.divider()
    opcion_menu = st.radio(
        "Navegación",
        ["🏠 Inicio", "📏 Área y Perímetro", "📐 Teorema de Pitágoras", "🔺 Razones Trigonométricas", "📘 Guía 2° Medio", "📄 Generar Prueba Desarrollo"],
        label_visibility="collapsed"
    )

st.title("📐 Banco de Ejercicios — Triángulos y Trigonometría")

if opcion_menu == "🏠 Inicio":
    st.subheader("¡Bienvenido!")
    st.markdown("Practica ejercicios interactivos con esquemas automáticos o genera pruebas completas en PDF.")

elif opcion_menu == "📏 Área y Perímetro":
    mostrar_banco("📏 Área y Perímetro", banco_area_perimetro, "area")

elif opcion_menu == "📐 Teorema de Pitágoras":
    mostrar_banco("📐 Teorema de Pitágoras", banco_pitagoras, "pitagoras")

elif opcion_menu == "🔺 Razones Trigonométricas":
    mostrar_banco("🔺 Razones Trigonométricas", banco_trigonometria, "trigo")

elif opcion_menu == "📘 Guía 2° Medio":
    mostrar_banco("📘 Guía 2° Medio — Razones Trigonométricas", banco_guia_2medio, "g2m")

elif opcion_menu == "📄 Generar Prueba Desarrollo":
    st.header("📄 Generar Prueba de Desarrollo con Esquemas")
    
    temas_seleccion = st.multiselect("Selecciona temas:", ["Área y Perímetro", "Teorema de Pitágoras", "Razones Trigonométricas", "Guía 2° Medio"], default=["Teorema de Pitágoras", "Guía 2° Medio"])
    nombre_prueba = st.text_input("Nombre de la prueba:", value="Evaluación de Matemáticas — Trigonometría")
    
    mapeo = {"Área y Perímetro": banco_area_perimetro, "Teorema de Pitágoras": banco_pitagoras, "Razones Trigonométricas": banco_trigonometria, "Guía 2° Medio": banco_guia_2medio}
    
    if st.button("📄 Generar Archivos PDF", type="primary"):
        prueba_preguntas = []
        for t in temas_seleccion:
            for item in mapeo[t]:
                cp = item.copy()
                cp['_tema'] = t
                prueba_preguntas.append(cp)
        
        fecha_hoy = datetime.now().strftime("%d/%m/%Y")
        pdf_p = generar_pdf_desarrollo(prueba_preguntas, nombre_prueba, fecha_hoy, False)
        pdf_s = generar_pdf_desarrollo(prueba_preguntas, nombre_prueba, fecha_hoy, True)
        
        st.success(f"✅ Se generaron {len(prueba_preguntas)} ejercicios con sus esquemas gráficos.")
        c1, c2 = st.columns(2)
        c1.download_button("📥 Descargar PRUEBA (.pdf)", pdf_p, file_name="Prueba.pdf", mime="application/pdf")
        c2.download_button("📥 Descargar SOLUCIONARIO (.pdf)", pdf_s, file_name="Solucionario.pdf", mime="application/pdf")

st.divider()
st.caption("💡 Banco de ejercicios v1.2 — Gráficos automáticos con Matplotlib")
