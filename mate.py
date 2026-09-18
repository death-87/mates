import streamlit as st
import random
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

st.set_page_config(page_title="📐 Matemáticas — Triángulos", layout="wide")
st.title("📐 Banco de Ejercicios — Triángulos y Trigonometría")

# ============== BANCOS DE PREGUNTAS ==============

# --- ÁREA Y PERÍMETRO ---
banco_area_perimetro = [
    {
        "pregunta": "Un triángulo tiene base 12 cm y altura 8 cm. Calcula su área.",
        "respuesta": "48 cm²",
        "explicacion": "Área = (base × altura) ÷ 2 = (12 × 8) ÷ 2 = 48 cm²"
    },
    {
        "pregunta": "Un triángulo equilátero tiene lado de 10 cm. Calcula su perímetro.",
        "respuesta": "30 cm",
        "explicacion": "Perímetro = 3 × lado = 3 × 10 = 30 cm"
    },
    {
        "pregunta": "Un triángulo rectángulo tiene catetos de 6 cm y 8 cm, y su hipotenusa mide 10 cm. Calcula su perímetro.",
        "respuesta": "24 cm",
        "explicacion": "Perímetro = 6 + 8 + 10 = 24 cm"
    },
    {
        "pregunta": "Un triángulo tiene base 15 m y altura 6 m. Calcula su área.",
        "respuesta": "45 m²",
        "explicacion": "Área = (15 × 6) ÷ 2 = 90 ÷ 2 = 45 m²"
    },
    {
        "pregunta": "Un triángulo tiene lados de 7 cm, 9 cm y 12 cm. Calcula su perímetro.",
        "respuesta": "28 cm",
        "explicacion": "Perímetro = 7 + 9 + 12 = 28 cm"
    },
    {
        "pregunta": "Un triángulo isósceles tiene lados iguales de 5 cm y la base mide 6 cm. Calcula su perímetro.",
        "respuesta": "16 cm",
        "explicacion": "Perímetro = 5 + 5 + 6 = 16 cm"
    },
    {
        "pregunta": "Calcula la altura de un triángulo cuya base mide 14 cm y su área es 49 cm².",
        "respuesta": "7 cm",
        "explicacion": "Área = (base × altura)/2 → 49 = (14 × h)/2 → 49 = 7h → h = 7 cm"
    },
    {
        "pregunta": "Un triángulo tiene base 12 cm y altura igual a la mitad de la base. Calcula su área.",
        "respuesta": "36 cm²",
        "explicacion": "Altura = 12 ÷ 2 = 6 cm → Área = (12 × 6) ÷ 2 = 36 cm²"
    }
]

# --- ÁNGULOS DEL TRIÁNGULO ---
banco_angulos = [
    {
        "pregunta": "Dos ángulos de un triángulo miden 40° y 65°. ¿Cuánto mide el tercer ángulo?",
        "respuesta": "75°",
        "explicacion": "La suma de los ángulos es 180° → 180° − (40° + 65°) = 75°"
    },
    {
        "pregunta": "En un triángulo rectángulo, un ángulo agudo mide 32°. ¿Cuánto mide el otro ángulo agudo?",
        "respuesta": "58°",
        "explicacion": "90° − 32° = 58°"
    },
    {
        "pregunta": "Un triángulo es equilátero. ¿Cuánto mide cada uno de sus ángulos?",
        "respuesta": "60°",
        "explicacion": "180° ÷ 3 = 60°"
    },
    {
        "pregunta": "Un triángulo tiene un ángulo de 110°, y los otros dos ángulos son iguales. ¿Cuánto mide cada uno?",
        "respuesta": "35°",
        "explicacion": "180° − 110° = 70° → 70° ÷ 2 = 35°"
    },
    {
        "pregunta": "Si un triángulo tiene dos ángulos de 55° cada uno, ¿de qué tipo de triángulo se trata y cuánto mide el tercer ángulo?",
        "respuesta": "Isósceles, 70°",
        "explicacion": "180° − 55° − 55° = 70°. Tiene dos ángulos iguales, por lo tanto es isósceles."
    },
    {
        "pregunta": "Los tres ángulos de un triángulo son proporcionales a 1, 2 y 3. ¿Cuánto mide cada ángulo?",
        "respuesta": "30°, 60° y 90°",
        "explicacion": "x + 2x + 3x = 180° → 6x = 180° → x = 30° → 30°, 60°, 90°"
    },
    {
        "pregunta": "Un ángulo exterior de un triángulo mide 125°, y uno de los ángulos interiores opuestos mide 48°. ¿Cuánto mide el otro ángulo interior opuesto?",
        "respuesta": "77°",
        "explicacion": "Ángulo exterior = suma de los dos interiores opuestos → 125° − 48° = 77°"
    },
    {
        "pregunta": "En un triángulo, el ángulo mayor mide el doble que el mediano y el triple que el menor. ¿Cuánto mide cada ángulo?",
        "respuesta": "30°, 60°, 90°",
        "explicacion": "30° + 60° + 90° = 180°. El mayor es el triple del menor y el doble del mediano."
    }
]

# --- TEOREMA DE PITÁGORAS ---
banco_pitagoras = [
    {
        "pregunta": "Los catetos de un triángulo rectángulo miden 3 cm y 4 cm. ¿Cuánto mide la hipotenusa?",
        "respuesta": "5 cm",
        "explicacion": "c² = a² + b² → c² = 3² + 4² = 9 + 16 = 25 → c = 5 cm"
    },
    {
        "pregunta": "Un cateto mide 12 cm y la hipotenusa 13 cm. ¿Cuánto mide el otro cateto?",
        "respuesta": "5 cm",
        "explicacion": "b² = c² − a² → b² = 13² − 12² = 169 − 144 = 25 → b = 5 cm"
    },
    {
        "pregunta": "Los catetos miden 5 cm y 7 cm. Calcula la longitud de la hipotenusa.",
        "respuesta": "√74 cm",
        "explicacion": "c² = 5² + 7² = 25 + 49 = 74 → c = √74 cm"
    },
    {
        "pregunta": "Una escalera de 10 m de longitud apoya contra una pared. La base está a 6 m de la pared. ¿Qué altura alcanza en la pared?",
        "respuesta": "8 m",
        "explicacion": "h² + 6² = 10² → h² + 36 = 100 → h² = 64 → h = 8 m"
    },
    {
        "pregunta": "La hipotenusa de un triángulo rectángulo mide 18 cm y un cateto mide 9 cm. ¿Cuánto mide el otro cateto?",
        "respuesta": "9√3 cm",
        "explicacion": "b² = 18² − 9² = 324 − 81 = 243 → b = √243 = 9√3 cm"
    },
    {
        "pregunta": "Calcula el perímetro de un triángulo rectángulo cuyos catetos miden 8 cm y 15 cm.",
        "respuesta": "40 cm",
        "explicacion": "Hipotenusa: √(8² + 15²) = √289 = 17 cm → Perímetro = 8 + 15 + 17 = 40 cm"
    },
    {
        "pregunta": "¿Es un triángulo rectángulo si sus lados miden 6 cm, 8 cm y 10 cm?",
        "respuesta": "Sí, es rectángulo",
        "explicacion": "6² + 8² = 36 + 64 = 100 = 10² → Cumple el teorema de Pitágoras ✅"
    },
    {
        "pregunta": "Calcula la diagonal de un rectángulo de 12 cm de largo y 5 cm de ancho.",
        "respuesta": "13 cm",
        "explicacion": "d² = 12² + 5² = 144 + 25 = 169 → d = 13 cm"
    }
]

# --- LEY DE COSENOS ---
banco_cosenos = [
    {
        "pregunta": "En un triángulo, dos lados miden 5 cm y 7 cm, y el ángulo entre ellos es de 60°. Calcula el tercer lado.",
        "respuesta": "√39 cm",
        "explicacion": "c² = a² + b² − 2ab·cos(C) → c² = 25 + 49 − 35 = 39 → c = √39 cm"
    },
    {
        "pregunta": "Un triángulo tiene lados de 8 cm, 10 cm y 12 cm. Calcula el ángulo opuesto al lado de 10 cm.",
        "respuesta": "≈ 55.77°",
        "explicacion": "10² = 8² + 12² − 2·8·12·cos(B) → cos(B) = 9/16 → B ≈ 55.77°"
    },
    {
        "pregunta": "Dos lados de un triángulo miden 6 m y 9 m, formando un ángulo de 45° entre ellos. Calcula el tercer lado.",
        "respuesta": "√(117 − 54√2) m",
        "explicacion": "c² = 36 + 81 − 108·(√2/2) = 117 − 54√2 → c = √(117 − 54√2) m"
    },
    {
        "pregunta": "Un triángulo tiene lados de 10 cm, 10 cm y 12 cm. Calcula su área usando la ley de cosenos.",
        "respuesta": "48 cm²",
        "explicacion": "cos(C) = 0.28 → sen(C) = 0.96 → Área = (10·10·0.96)/2 = 48 cm² ✅"
    },
    {
        "pregunta": "En un triángulo, el lado a = 8 cm, el lado b = 6 cm y el ángulo C = 120°. Calcula el lado c.",
        "respuesta": "√148 cm",
        "explicacion": "c² = 64 + 36 − 96·(-1/2) = 100 + 48 = 148 → c = √148 cm"
    },
    {
        "pregunta": "Un triángulo tiene lados a = 7 cm, b = 9 cm y c = 12 cm. Calcula el ángulo entre los lados a y b.",
        "respuesta": "≈ 96.38°",
        "explicacion": "144 = 49 + 81 − 126·cos(C) → cos(C) = -1/9 → C ≈ 96.38°"
    },
    {
        "pregunta": "Un paralelogramo tiene lados de 8 cm y 5 cm, y uno de sus ángulos interiores mide 60°. Calcula la longitud de su diagonal mayor.",
        "respuesta": "√129 cm",
        "explicacion": "d² = 64 + 25 − 80·(-1/2) = 89 + 40 = 129 → d = √129 cm"
    },
    {
        "pregunta": "Calcula el ángulo mayor de un triángulo con lados de 13 cm, 14 cm y 15 cm.",
        "respuesta": "≈ 67.38°",
        "explicacion": "15² = 13² + 14² − 2·13·14·cos(C) → cos(C) = 5/13 → C ≈ 67.38° ✅"
    }
]

# --- RAZONES TRIGONOMÉTRICAS + ELEVACIÓN/DEPRESIÓN ---
banco_trigonometria = [
    {"categoria": "Valores básicos", "pregunta": "Calcula sen(30°)", "respuesta": "1/2", "explicacion": "sen(30°) = 1/2."},
    {"categoria": "Valores básicos", "pregunta": "Calcula cos(30°)", "respuesta": "√3/2", "explicacion": "cos(30°) = √3/2."},
    {"categoria": "Valores básicos", "pregunta": "Calcula sen(45°)", "respuesta": "√2/2", "explicacion": "sen(45°) = √2/2."},
    {"categoria": "Valores básicos", "pregunta": "Calcula cos(45°)", "respuesta": "√2/2", "explicacion": "cos(45°) = √2/2."},
    {"categoria": "Valores básicos", "pregunta": "Calcula sen(60°)", "respuesta": "√3/2", "explicacion": "sen(60°) = √3/2."},
    {"categoria": "Valores básicos", "pregunta": "Calcula cos(60°)", "respuesta": "1/2", "explicacion": "cos(60°) = 1/2."},
    {"categoria": "Valores básicos", "pregunta": "Calcula tan(30°)", "respuesta": "√3/3", "explicacion": "tan(30°) = sen(30°)/cos(30°) = √3/3."},
    {"categoria": "Valores básicos", "pregunta": "Calcula tan(45°)", "respuesta": "1", "explicacion": "tan(45°) = 1."},
    {"categoria": "Valores básicos", "pregunta": "Calcula tan(60°)", "respuesta": "√3", "explicacion": "tan(60°) = √3."},
    {"categoria": "Combinaciones", "pregunta": "2·sen(30°) + 3·cos(60°) = ?", "respuesta": "5/2", "explicacion": "= 2·(1/2) + 3·(1/2) = 1 + 3/2 = 5/2"},
    {"categoria": "Combinaciones", "pregunta": "sen²(45°) + cos²(45°) = ?", "respuesta": "1", "explicacion": "= (√2/2)² + (√2/2)² = 1/2 + 1/2 = 1."},
    {"categoria": "Combinaciones", "pregunta": "tan(60°) · cos(30°) = ?", "respuesta": "3/2", "explicacion": "= √3 · (√3/2) = 3/2"},
    {"categoria": "📐 Ángulo de elevación", "pregunta": "Desde el suelo, se observa la cima de un árbol con un ángulo de elevación de 45°. Si estás a 12 m de su base, ¿cuál es la altura del árbol?", "respuesta": "12 m", "explicacion": "tan(45°) = h/12 → 1 = h/12 → h = 12 m"},
    {"categoria": "📐 Ángulo de elevación", "pregunta": "Una escalera apoya en una pared formando 60° con el suelo. La base está a 4 m de la pared. ¿Qué altura alcanza?", "respuesta": "4√3 m", "explicacion": "tan(60°) = h/4 → √3 = h/4 → h = 4√3 m"},
    {"categoria": "📐 Ángulo de elevación", "pregunta": "Se observa la cima de una torre con ángulo de elevación de 30°. La torre mide 10 m de alto. ¿A qué distancia está el observador?", "respuesta": "10√3 m", "explicacion": "tan(30°) = 10/d → d = 10 ÷ (√3/3) = 10√3 m"},
    {"categoria": "📉 Ángulo de depresión", "pregunta": "Desde un faro de 30 m de altura, se observa un barco con ángulo de depresión de 45°. ¿A qué distancia está el barco?", "respuesta": "30 m", "explicacion": "Ángulo de depresión = ángulo de elevación → tan(45°) = 30/d → d = 30 m"},
    {"categoria": "📉 Ángulo de depresión", "pregunta": "Desde un edificio de 18 m de alto, se observa un auto con ángulo de depresión de 60°. ¿Qué distancia horizontal hay?", "respuesta": "6√3 m", "explicacion": "tan(60°) = 18/d → √3 = 18/d → d = 6√3 m"},
    {"categoria": "📉 Ángulo de depresión", "pregunta": "Desde un globo a 500 m de altura, se observa una aldea con ángulo de depresión de 30°. ¿Distancia en línea recta al globo?", "respuesta": "1000 m", "explicacion": "sen(30°) = 500/d → 1/2 = 500/d → d = 1000 m"}
]

# ============== FUNCIONES AUXILIARES ==============
def inicializar_sesion(clave, valor_inicial):
    if clave not in st.session_state:
        st.session_state[clave] = valor_inicial

def mostrar_banco(titulo, banco, clave_sesion):
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

# ============== GENERAR PDF ==============
def generar_pdf_sin_respuestas(titulo, preguntas, fecha):
    from io import BytesIO
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elementos = []
    
    # Encabezado
    elementos.append(Paragraph(titulo, styles["Title"]))
    elementos.append(Spacer(1, 12))
    elementos.append(Paragraph(f"Fecha: {fecha}", styles["Normal"]))
    elementos.append(Paragraph("Alumno: __________________________    Curso: _______________", styles["Normal"]))
    elementos.append(Spacer(1, 20))
    elementos.append(Paragraph("=" * 60, styles["Normal"]))
    elementos.append(Spacer(1, 12))
    elementos.append(Paragraph("EJERCICIOS:", styles["Heading2"]))
    elementos.append(Spacer(1, 12))
    
    # Preguntas
    for i, p in enumerate(preguntas, 1):
        texto = f"{i}. {p['pregunta']}"
        elementos.append(Paragraph(texto, styles["Normal"]))
        elementos.append(Spacer(1, 6))
        elementos.append(Paragraph("Respuesta: ___________________", styles["Normal"]))
        elementos.append(Spacer(1, 12))
        elementos.append(Paragraph("-" * 50, styles["Normal"]))
        elementos.append(Spacer(1, 12))
    
    doc.build(elementos)
    buffer.seek(0)
    return buffer

def generar_pdf_con_respuestas(titulo, preguntas, fecha):
    from io import BytesIO
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elementos = []
    
    # Encabezado
    elementos.append(Paragraph(f"{titulo} — SOLUCIONARIO", styles["Title"]))
    elementos.append(Spacer(1, 12))
    elementos.append(Paragraph(f"Fecha: {fecha}", styles["Normal"]))
    elementos.append(Spacer(1, 12))
    elementos.append(Paragraph("=" * 60, styles["Normal"]))
    elementos.append(Spacer(1, 12))
    elementos.append(Paragraph("RESPUESTAS Y EXPLICACIONES:", styles["Heading2"]))
    elementos.append(Spacer(1, 12))
    
    # Preguntas con respuestas
    for i, p in enumerate(preguntas, 1):
        texto = f"<b>{i}.</b> {p['pregunta']}"
        elementos.append(Paragraph(texto, styles["Normal"]))
        elementos.append(Spacer(1, 4))
        elementos.append(Paragraph(f"✅ <b>Respuesta:</b> {p['respuesta']}", styles["Normal"]))
        elementos.append(Paragraph(f"💡 {p['explicacion']}", styles["Normal"]))
        elementos.append(Spacer(1, 12))
        elementos.append(Paragraph("-" * 50, styles["Normal"]))
        elementos.append(Spacer(1, 12))
    
    doc.build(elementos)
    buffer.seek(0)
    return buffer

# ============== PESTAÑAS PRINCIPALES ==============
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📏 Área y Perímetro",
    "📐 Ángulos del Triángulo",
    "📐 Teorema de Pitágoras",
    "📐 Ley de Cosenos",
    "🔺 Razones Trigonométricas",
    "📄 Generar Prueba PDF"
])

with tab1:
    mostrar_banco("📏 Área y Perímetro", banco_area_perimetro, "area")

with tab2:
    mostrar_banco("📐 Ángulos del Triángulo", banco_angulos, "angulos")

with tab3:
    mostrar_banco("📐 Teorema de Pitágoras", banco_pitagoras, "pitagoras")
    st.divider()
    st.info("💡 Teorema: En un triángulo rectángulo → a² + b² = c², donde c es la hipotenusa.")

with tab4:
    mostrar_banco("📐 Ley de Cosenos", banco_cosenos, "cosenos")
    st.divider()
    st.latex(r"c^2 = a^2 + b^2 - 2ab \cdot \cos(C)")
    st.caption("Donde C es el ángulo comprendido entre los lados a y b")

with tab5:
    st.header("🔺 Razones Trigonométricas — Ángulos Notables")
    with st.expander("📋 Tabla de valores — Ver / Ocultar"):
        st.markdown("""
| Ángulo θ | sen(θ) | cos(θ) | tan(θ) |
|----------|--------|--------|--------|
| **30°**  | 1/2    | √3/2   | √3/3   |
| **45°**  | √2/2   | √2/2   | 1      |
| **60°**  | √3/2   | 1/2    | √3     |

> 💡 **Ángulo de elevación**: desde el suelo hacia arriba  
> 💡 **Ángulo de depresión**: desde arriba hacia abajo = ángulo de elevación desde el objeto
""")
    st.divider()
    mostrar_banco("", banco_trigonometria, "trigo")

with tab6:
    st.header("📄 Generar Prueba en PDF")
    st.info("Selecciona los temas y genera una prueba lista para imprimir en formato PDF, con y sin respuestas.")
    
    temas_seleccion = st.multiselect(
        "Selecciona los temas para tu prueba:",
        ["Área y Perímetro", "Ángulos del Triángulo", "Teorema de Pitágoras", "Ley de Cosenos", "Razones Trigonométricas"]
    )
    
    cant_preg = st.slider("Cantidad de ejercicios por tema:", 2, 6, 4)
    nombre_prueba = st.text_input("Nombre de la prueba:", value="Evaluación — Triángulos y Trigonometría")
    fecha_hoy = datetime.now().strftime("%d/%m/%Y")
    
    if st.button("📄 Generar Pruebas en PDF", type="primary"):
        if not temas_seleccion:
            st.warning("⚠️ Selecciona al menos un tema")
        else:
            prueba_preguntas = []
            mapeo_bancos = {
                "Área y Perímetro": banco_area_perimetro,
                "Ángulos del Triángulo": banco_angulos,
                "Teorema de Pitágoras": banco_pitagoras,
                "Ley de Cosenos": banco_cosenos,
                "Razones Trigonométricas": banco_trigonometria
            }
            
            for tema in temas_seleccion:
                banco = mapeo_bancos[tema]
                seleccion = random.sample(banco, min(cant_preg, len(banco)))
                prueba_preguntas.extend(seleccion)
            
            random.shuffle(prueba_preguntas)
            
            # Generar PDFs
            pdf_sin = generar_pdf_sin_respuestas(nombre_prueba, prueba_preguntas, fecha_hoy)
            pdf_con = generar_pdf_con_respuestas(nombre_prueba, prueba_preguntas, fecha_hoy)
            
            st.success(f"✅ Prueba generada con {len(prueba_preguntas)} ejercicios")
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.download_button(
                    label="📥 Descargar PRUEBA (.pdf)",
                    data=pdf_sin,
                    file_name=f"Prueba_sin_respuestas_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )
            with col_b:
                st.download_button(
                    label="📥 Descargar SOLUCIONARIO (.pdf)",
                    data=pdf_con,
                    file_name=f"Solucionario_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )
            
            st.divider()
            st.subheader("👁️ Vista previa de la prueba:")
            for i, p in enumerate(prueba_preguntas, 1):
                st.markdown(f"**{i}.** {p['pregunta']}")
                st.markdown(f"*Respuesta: {p['respuesta']}*")
                st.divider()

st.divider()
st.caption("💡 Cada ejercicio se genera aleatoriamente. ¡Buena suerte estudiando! 🧠✨")