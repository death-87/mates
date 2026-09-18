import streamlit as st
import random
import math

st.set_page_config(page_title="Ejercicios de Matemáticas — Triángulos", layout="wide")
st.title("📐 Ejercicios de Triángulos y Trigonometría")

# ============== FUNCIONES AUXILIARES ==============
def generar_triangulo_rectangulo():
    """Genera un triángulo rectángulo con lados enteros"""
    cateto1 = random.randint(3, 12)
    cateto2 = random.randint(3, 12)
    hipotenusa = round(math.hypot(cateto1, cateto2), 2)
    angulo_alto = round(math.degrees(math.atan(cateto2 / cateto1)), 2)
    return cateto1, cateto2, hipotenusa, angulo_alto

def generar_triangulo_cualquiera():
    """Genera un triángulo cualquiera válido"""
    while True:
        a = random.randint(5, 15)
        b = random.randint(5, 15)
        c = random.randint(abs(a-b)+1, a+b-1)
        if a + b > c and a + c > b and b + c > a:
            break
    s = (a + b + c) / 2
    area = round(math.sqrt(s * (s-a) * (s-b) * (s-c)), 2)
    return a, b, c, area

# ============== MENU PRINCIPAL ==============
menu = st.sidebar.radio("Selecciona el tipo de ejercicio", [
    "📏 Área y Perímetro — Triángulo Rectángulo",
    "📐 Ángulos del Triángulo Rectángulo",
    "🔺 Razones Trigonométricas",
    "📐 Triángulo Cualquiera — Ley de Cosenos"
])

# ============== EJERCICIO 1: ÁREA Y PERÍMETRO ==============
if menu == "📏 Área y Perímetro — Triángulo Rectángulo":
    st.header("📏 Área y Perímetro — Triángulo Rectángulo")
    
    if "ej1" not in st.session_state:
        st.session_state.ej1 = generar_triangulo_rectangulo()
    
    c1, c2, hip, ang = st.session_state.ej1
    
    st.info(f"""
    📐 Tienes un triángulo rectángulo con:
    - Cateto adyacente = **{c1} cm**
    - Cateto opuesto = **{c2} cm**
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        area_usuario = st.number_input("Calcula el ÁREA (cm²)", min_value=0.0, step=0.1)
    with col2:
        peri_usuario = st.number_input("Calcula el PERÍMETRO (cm)", min_value=0.0, step=0.1)
    
    area_correcta = (c1 * c2) / 2
    peri_correcto = c1 + c2 + hip
    
    if st.button("✅ Verificar Respuesta"):
        errores = []
        if abs(area_usuario - area_correcta) < 0.01:
            st.success(f"✅ ¡Área correcta! El área es {area_correcta} cm²")
        else:
            st.error(f"❌ Área incorrecta — Pista: Área = ({c1} × {c2}) ÷ 2 = {area_correcta} cm²")
        
        if abs(peri_usuario - peri_correcto) < 0.01:
            st.success(f"✅ ¡Perímetro correcto! Es {peri_correcto} cm")
        else:
            st.error(f"❌ Perímetro incorrecto — Pista: suma de todos los lados = {c1} + {c2} + {hip} = {peri_correcto} cm")
    
    if st.button("🔄 Nuevo Ejercicio"):
        st.session_state.ej1 = generar_triangulo_rectangulo()
        st.rerun()

# ============== EJERCICIO 2: ÁNGULOS ==============
elif menu == "Ángulos del Triángulo Rectángulo":
    st.header("📐 Ángulos del Triángulo Rectángulo")
    
    if "ej2" not in st.session_state:
        st.session_state.ej2 = generar_triangulo_rectangulo()
    
    c1, c2, hip, ang = st.session_state.ej2
    
    st.info(f"""
    📐 En este triángulo rectángulo:
    - Cateto horizontal = **{c1} cm**
    - Cateto vertical = **{c2} cm**
    - Hipotenusa = **{hip} cm**
       """)
    
    ang1 = st.number_input("¿Cuánto mide el ángulo en el vértice inferior izquierdo? (°)", min_value=0.0, max_value=90.0, step=0.5)
    ang2 = st.number_input("¿Cuánto mide el ángulo en el vértice superior? (°)", min_value=0.0, max_value=90.0, step=0.5)
    
    ang_vert = ang
    ang_sup = 90 - ang
    
    if st.button("✅ Verificar Ángulos"):
        if abs(ang1 - ang_vert) < 1 or abs(ang1 - ang_sup) < 1:
            st.success(f"✅ ¡Correcto! Ángulos: {ang_vert:.1f}° y {ang_sup:.1f}°")
            st.info("💡 Recuerda: Los 3 ángulos suman 180°, así que 90° + ángulo1 + ángulo2 = 180°")
        else:
            st.error(f"❌ Revisa el cálculo — Los ángulos son aproximadamente {ang_vert:.1f}° y {ang_sup:.1f}°")
    
    if st.button("🔄 Nuevo Triángulo"):
        st.session_state.ej2 = generar_triangulo_rectangulo()
        st.rerun()

# ============== EJERCICIO 3: RAZONES TRIGONOMÉTRICAS ==============
elif menu == "🔺 Razones Trigonométricas":
    st.header("🔺 Razones Trigonométricas")
    
    if "ej3" not in st.session_state:
        st.session_state.ej3 = generar_triangulo_rectangulo()
    
    c1, c2, hip, ang = st.session_state.ej3
    
    st.latex(r"""
    \sin(\theta) = \frac{\text{opuesto}}{\text{hipotenusa}} \quad
    \cos(\theta) = \frac{\text{adyacente}}{\text{hipotenusa}} \quad
    \tan(\theta) = \frac{\text{opuesto}}{\text{adyacente}}
    """)
    
    st.info(f"""
    📐 Ángulo θ = **{ang:.1f}°**
    - Cateto opuesto = **{c2} cm**
    - Cateto adyacente = **{c1} cm**
    - Hipotenusa = **{hip} cm**
    """)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        seno_u = st.number_input("sen(θ) =", min_value=0.0, max_value=1.0, step=0.01)
    with col2:
        coseno_u = st.number_input("cos(θ) =", min_value=0.0, max_value=1.0, step=0.01)
    with col3:
        tangente_u = st.number_input("tan(θ) =", min_value=0.0, step=0.01)
    
    seno_c = round(c2 / hip, 4)
    cos_c = round(c1 / hip, 4)
    tan_c = round(c2 / c1, 4)
    
    if st.button("✅ Comprobar Razones"):
        st.write(f"""
        | Razón | Tu respuesta | Valor correcto |
        |-------|-------------|----------------|
        | sen(θ) | {seno_u} | **{seno_c}** |
        | cos(θ) | {coseno_u} | **{cos_c}** |
        | tan(θ) | {tangente_u} | **{tan_c}** |
        """)
        st.info(f"""
        💡 Cálculos:
        - sen({ang:.1f}°) = {c2} ÷ {hip} = {seno_c}
        - cos({ang:.1f}°) = {c1} ÷ {hip} = {cos_c}
        - tan({ang:.1f}°) = {c2} ÷ {c1} = {tan_c}
        """)
    
    if st.button("🔄 Nuevo Ángulo"):
        st.session_state.ej3 = generar_triangulo_rectangulo()
        st.rerun()

# ============== EJERCICIO 4: LEY DE COSENOS ==============
elif menu == "📐 Triángulo Cualquiera — Ley de Cosenos":
    st.header("📐 Triángulo Cualquiera — Ley de Cosenos")
    
    if "ej4" not in st.session_state:
        st.session_state.ej4 = generar_triangulo_cualquiera()
    
    a, b, c, area = st.session_state.ej4
    
    st.info(f"""
    🔺 En un triángulo con:
    - Lado a = **{a} cm**
    - Lado b = **{b} cm**
    - Lado c = **{c} cm**
    """)
    
    st.latex(r"c^2 = a^2 + b^2 - 2ab \cdot \cos(C)")
    
    angulo_c = st.number_input("Calcula el ángulo opuesto al lado c (en grados)", min_value=0.0, max_value=180.0, step=1.0)
    area_u = st.number_input("Calcula el área del triángulo (usando fórmula de Herón)", min_value=0.0, step=0.1)
    
    ang_c_correcto = math.degrees(math.acos((a**2 + b**2 - c**2) / (2*a*b)))
    
    if st.button("✅ Verificar"):
        if abs(angulo_c - ang_c_correcto) < 1:
            st.success(f"✅ ¡Ángulo correcto! = {ang_c_correcto:.1f}°")
        else:
            st.error(f"❌ Ángulo — El correcto es aproximadamente {ang_c_correcto:.1f}°")
        
        if abs(area_u - area) < 0.5:
            st.success(f"✅ ¡Área correcta! = {area} cm²")
        else:
            st.error(f"❌ Área — Pista: semiperímetro s = {(a+b+c)/2} → Área = √s(s-a)(s-b)(s-c) = {area} cm²")
    
    if st.button("🔄 Nuevo Triángulo"):
        st.session_state.ej4 = generar_triangulo_cualquiera()
        st.rerun()

# ============== PIE DE PÁGINA ==============
st.divider()
st.markdown("💡 **Consejo**: Usa la calculadora de tu celular para resolver cada ejercicio. ¡Buena suerte! 🧠✨")