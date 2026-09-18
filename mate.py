import streamlit as st
import random

st.set_page_config(page_title="Razones Trigonométricas — Ejercicios", layout="wide")
st.title("🔺 Razones Trigonométricas — Ángulos Notables")
st.subheader("30° · 45° · 60° · Elevación · Depresión")

# ============== BANCO DE PREGUNTAS ==============
banco_preguntas = [
    # === VALORES BÁSICOS ===
    {
        "categoria": "Valores básicos",
        "pregunta": "Calcula sen(30°)",
        "respuesta": "1/2",
        "explicacion": "sen(30°) = 1/2."
    },
    {
        "categoria": "Valores básicos",
        "pregunta": "Calcula cos(30°)",
        "respuesta": "√3/2",
        "explicacion": "cos(30°) = √3/2."
    },
    {
        "categoria": "Valores básicos",
        "pregunta": "Calcula sen(45°)",
        "respuesta": "√2/2",
        "explicacion": "sen(45°) = √2/2."
    },
    {
        "categoria": "Valores básicos",
        "pregunta": "Calcula cos(45°)",
        "respuesta": "√2/2",
        "explicacion": "cos(45°) = √2/2."
    },
    {
        "categoria": "Valores básicos",
        "pregunta": "Calcula sen(60°)",
        "respuesta": "√3/2",
        "explicacion": "sen(60°) = √3/2."
    },
    {
        "categoria": "Valores básicos",
        "pregunta": "Calcula cos(60°)",
        "respuesta": "1/2",
        "explicacion": "cos(60°) = 1/2."
    },
    {
        "categoria": "Valores básicos",
        "pregunta": "Calcula tan(30°)",
        "respuesta": "√3/3",
        "explicacion": "tan(30°) = sen(30°)/cos(30°) = (1/2) ÷ (√3/2) = √3/3"
    },
    {
        "categoria": "Valores básicos",
        "pregunta": "Calcula tan(45°)",
        "respuesta": "1",
        "explicacion": "tan(45°) = 1."
    },
    {
        "categoria": "Valores básicos",
        "pregunta": "Calcula tan(60°)",
        "respuesta": "√3",
        "explicacion": "tan(60°) = sen(60°)/cos(60°) = √3"
    },
    
    # === COMBINACIONES ===
    {
        "categoria": "Combinaciones",
        "pregunta": "Calcula 2·sen(30°) + 3·cos(60°)",
        "respuesta": "5/2",
        "explicacion": "= 2·(1/2) + 3·(1/2) = 1 + 3/2 = 5/2"
    },
    {
        "categoria": "Combinaciones",
        "pregunta": "sen²(45°) + cos²(45°) = ?",
        "respuesta": "1",
        "explicacion": "= (√2/2)² + (√2/2)² = 2/4 + 2/4 = 1. ¡Identidad fundamental!"
    },
    {
        "categoria": "Combinaciones",
        "pregunta": "Calcula tan(60°) · cos(30°)",
        "respuesta": "3/2",
        "explicacion": "= √3 · (√3/2) = 3/2"
    },
    
    # === ÁNGULO DE ELEVACIÓN ===
    {
        "categoria": "📐 Ángulo de elevación",
        "pregunta": "Desde el suelo, se observa la cima de un árbol con un ángulo de elevación de 45°. Si estás a 12 metros de su base, ¿cuál es la altura del árbol?",
        "respuesta": "12 m",
        "explicacion": "tan(45°) = altura / distancia → 1 = h / 12 → h = 12 m"
    },
    {
        "categoria": "📐 Ángulo de elevación",
        "pregunta": "Una escalera apoya en una pared formando un ángulo de 60° con el suelo. Si la base está a 4 m de la pared, ¿qué altura alcanza en la pared?",
        "respuesta": "4√3 m",
        "explicacion": "tan(60°) = altura / 4 → √3 = h / 4 → h = 4√3 m"
    },
    {
        "categoria": "📐 Ángulo de elevación",
        "pregunta": "Se observa la parte superior de una torre con ángulo de elevación de 30°. Si la torre mide 10 m de alto, ¿a qué distancia está el observador de su base?",
        "respuesta": "10√3 m",
        "explicacion": "tan(30°) = 10 / d → √3/3 = 10 / d → d = 10 ÷ (√3/3) = 10√3 m"
    },
    {
        "categoria": "📐 Ángulo de elevación",
        "pregunta": "Un poste vertical proyecta una sombra de 8 m cuando el sol tiene un ángulo de elevación de 60°. ¿Cuál es la altura del poste?",
        "respuesta": "8√3 m",
        "explicacion": "tan(60°) = h / 8 → √3 = h / 8 → h = 8√3 m"
    },
    {
        "categoria": "📐 Ángulo de elevación",
        "pregunta": "Desde el suelo se ve la cima de un edificio con ángulo de 30°. El edificio mide 15 m de alto. ¿Cuál es la distancia horizontal al edificio?",
        "respuesta": "15√3 m",
        "explicacion": "tan(30°) = 15 / d → d = 15 / tan(30°) = 15 ÷ (√3/3) = 15√3 m"
    },
    {
        "categoria": "📐 Ángulo de elevación",
        "pregunta": "Una rampa forma un ángulo de 30° con el suelo y llega a una altura de 6 m. ¿Qué longitud tiene la rampa?",
        "respuesta": "12 m",
        "explicacion": "sen(30°) = 6 / rampa → 1/2 = 6 / rampa → rampa = 6 × 2 = 12 m"
    },
    
    # === ÁNGULO DE DEPRESIÓN ===
    {
        "categoria": "📉 Ángulo de depresión",
        "pregunta": "Desde lo alto de un faro de 30 m de altura, se observa un barco con un ángulo de depresión de 45°. ¿A qué distancia está el barco desde la base del faro?",
        "respuesta": "30 m",
        "explicacion": "El ángulo de depresión = ángulo de elevación en el barco → tan(45°) = 30 / d → 1 = 30 / d → d = 30 m"
    },
    {
        "categoria": "📉 Ángulo de depresión",
        "pregunta": "Desde un edificio de 18 m de alto, se observa un auto con ángulo de depresión de 60°. ¿Qué distancia horizontal hay entre el edificio y el auto?",
        "respuesta": "6√3 m",
        "explicacion": "tan(60°) = 18 / d → √3 = 18 / d → d = 18/√3 = 6√3 m"
    },
    {
        "categoria": "📉 Ángulo de depresión",
        "pregunta": "Un observador está en una torre de 20 m de altura y ve un árbol con ángulo de depresión de 30°. La distancia horizontal entre la torre y el árbol es de x metros. ¿Cuánto vale x?",
        "respuesta": "20√3 m",
        "explicacion": "tan(30°) = 20 / x → x = 20 / tan(30°) = 20 ÷ (√3/3) = 20√3 m"
    },
    {
        "categoria": "📉 Ángulo de depresión",
        "pregunta": "Desde un globo aerostático a una altura de 500 m, se observa una aldea con un ángulo de depresión de 30°. ¿Cuál es la distancia en línea recta entre el globo y la aldea?",
        "respuesta": "1000 m",
        "explicacion": "sen(30°) = 500 / hipotenusa → 1/2 = 500 / d → d = 500 × 2 = 1000 m"
    },
    {
        "categoria": "📉 Ángulo de depresión",
        "pregunta": "Desde la cima de una montaña de 450 m de altura, el ángulo de depresión hacia un pueblo en el valle mide 45°. ¿Qué distancia horizontal separa la montaña del pueblo?",
        "respuesta": "450 m",
        "explicacion": "tan(45°) = 450 / d → 1 = 450 / d → d = 450 m"
    },
    {
        "categoria": "📉 Ángulo de depresión",
        "pregunta": "Desde un helicóptero a 80 m de altura, se observa el techo de una casa con ángulo de depresión de 60°. ¿Cuál es la distancia horizontal entre el helicóptero y la casa?",
        "respuesta": "(80√3)/3 m",
        "explicacion": "tan(60°) = 80 / d → √3 = 80 / d → d = 80/√3 = (80√3)/3 m"
    }
]

# ============== INICIALIZAR SESIÓN ==============
if "indice_actual" not in st.session_state:
    st.session_state.indice_actual = random.randint(0, len(banco_preguntas)-1)
if "mostrar_respuesta" not in st.session_state:
    st.session_state.mostrar_respuesta = False

# ============== SELECCIONAR PREGUNTA ==============
indice = st.session_state.indice_actual
pregunta_actual = banco_preguntas[indice]

# ============== TABLA DE REFERENCIA ==============
with st.expander("📋 Ver tabla de valores — Ángulos notables"):
    st.markdown("""
| Ángulo θ | sen(θ) | cos(θ) | tan(θ) |
|----------|--------|--------|--------|
| **30°**  | 1/2    | √3/2   | √3/3   |
| **45°**  | √2/2   | √2/2   | 1      |
| **60°**  | √3/2   | 1/2    | √3     |

> 💡 **Ángulo de elevación**: desde el suelo hacia arriba  
> 💡 **Ángulo de depresión**: desde arriba hacia abajo — es igual al ángulo de elevación desde el objeto hacia el observador
""")

st.divider()

# ============== PREGUNTA ==============
st.subheader(f"{pregunta_actual['categoria']}")
st.info(f"📝 {pregunta_actual['pregunta']}")

st.divider()

# ============== BOTONES ==============
col1, col2 = st.columns(2)

with col1:
    if st.button("👁️ Ver Respuesta y Explicación", type="primary", use_container_width=True):
        st.session_state.mostrar_respuesta = True
    
    if st.session_state.mostrar_respuesta:
        st.success(f"✅ **Respuesta:** {pregunta_actual['respuesta']}")
        st.info(f"💡 **Explicación:** {pregunta_actual['explicacion']}")

with col2:
    if st.button("🔄 Nueva Pregunta", use_container_width=True):
        st.session_state.indice_actual = random.randint(0, len(banco_preguntas)-1)
        st.session_state.mostrar_respuesta = False
        st.rerun()

st.divider()
st.caption(f"Pregunta {indice + 1} de {len(banco_preguntas)} | {pregunta_actual['categoria']}")