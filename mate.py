import streamlit as st
import random
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from datetime import datetime
from io import BytesIO

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage

# Configuración de página
st.set_page_config(page_title="📐 2° Medio — Razones Trigonométricas", layout="wide")


# ==============================================================================
# ============== DIBUJANTES DE ELEMENTOS AMIGABLES (MATPLOTLIB) =================
# ==============================================================================

def dibujar_nino(ax, x, y, escala=1.0):
    """ Dibuja un niño/persona amigable en la posición (x, y) """
    r_cabeza = 0.15 * escala
    cabeza = patches.Circle((x, y + 0.7 * escala), r_cabeza, facecolor='#FFD1DC', edgecolor='#2B2B2B', lw=1.5, zorder=5)
    ax.add_patch(cabeza)
    ax.plot([x - 0.05 * escala, x + 0.05 * escala], [y + 0.72 * escala, y + 0.72 * escala], 'o', color='#2B2B2B', ms=3*escala, zorder=6)
    arc = patches.Arc((x, y + 0.68 * escala), 0.12 * escala, 0.08 * escala, angle=0, theta1=200, theta2=340, color='#D9534F', lw=1.5, zorder=6)
    ax.add_patch(arc)
    cuerpo = patches.Polygon([[x - 0.12 * escala, y + 0.25 * escala], [x + 0.12 * escala, y + 0.25 * escala], [x + 0.08 * escala, y + 0.55 * escala], [x - 0.08 * escala, y + 0.55 * escala]], facecolor='#4A90E2', edgecolor='#2B2B2B', lw=1.5, zorder=4)
    ax.add_patch(cuerpo)
    ax.plot([x - 0.06 * escala, x - 0.06 * escala], [y, y + 0.25 * escala], color='#2B2B2B', lw=2.5, zorder=3)
    ax.plot([x + 0.06 * escala, x + 0.06 * escala], [y, y + 0.25 * escala], color='#2B2B2B', lw=2.5, zorder=3)
    ax.plot([x - 0.09 * escala, x - 0.03 * escala], [y, y], color='#8B5A2B', lw=3, zorder=4)
    ax.plot([x + 0.03 * escala, x + 0.09 * escala], [y, y], color='#8B5A2B', lw=3, zorder=4)

def dibujar_arbol(ax, x, y, altura=4.0, ancho=2.0):
    """ Dibuja una araucaria / árbol estilizado """
    w_tronco = ancho * 0.2
    h_tronco = altura * 0.4
    tronco = patches.Rectangle((x - w_tronco/2, y), w_tronco, h_tronco, facecolor='#8B5A2B', edgecolor='#4A2E12', lw=1.5, zorder=3)
    ax.add_patch(tronco)
    r_copa = ancho * 0.4
    y_copa = y + h_tronco
    c1 = patches.Circle((x, y_copa + r_copa*0.8), r_copa*1.1, facecolor='#2ECC71', edgecolor='#27AE60', lw=1.5, zorder=4)
    c2 = patches.Circle((x - r_copa*0.5, y_copa + r_copa*0.4), r_copa*0.8, facecolor='#27AE60', edgecolor='#1E8449', lw=1.5, zorder=4)
    c3 = patches.Circle((x + r_copa*0.5, y_copa + r_copa*0.4), r_copa*0.8, facecolor='#27AE60', edgecolor='#1E8449', lw=1.5, zorder=4)
    ax.add_patch(c1)
    ax.add_patch(c2)
    ax.add_patch(c3)

def dibujar_avion(ax, x, y, escala=1.0):
    """ Dibuja un avión amigable """
    fuselaje = patches.Ellipse((x, y), 2.2*escala, 0.6*escala, facecolor='#ECF0F1', edgecolor='#2C3E50', lw=1.5, zorder=5)
    ax.add_patch(fuselaje)
    ala = patches.Polygon([[x - 0.2*escala, y], [x + 0.3*escala, y + 0.7*escala], [x - 0.3*escala, y + 0.7*escala]], facecolor='#3498DB', edgecolor='#2C3E50', lw=1.5, zorder=6)
    ax.add_patch(ala)
    cola = patches.Polygon([[x - 0.8*escala, y + 0.1*escala], [x - 1.1*escala, y + 0.5*escala], [x - 0.6*escala, y + 0.1*escala]], facecolor='#E74C3C', edgecolor='#2C3E50', lw=1.5, zorder=4)
    ax.add_patch(cola)
    for dx in [-0.3, 0.0, 0.3]:
        win = patches.Circle((x + dx*escala, y + 0.05*escala), 0.08*escala, facecolor='#34495E', zorder=7)
        ax.add_patch(win)

def dibujar_torre(ax, x, y, altura=5.0, ancho=1.5):
    """ Dibuja una torre/faro """
    torre = patches.Polygon([[x - ancho/2, y], [x + ancho/2, y], [x + ancho*0.3, y + altura], [x - ancho*0.3, y + altura]], facecolor='#E74C3C', edgecolor='#922B21', lw=1.5, zorder=3)
    ax.add_patch(torre)
    for h_frac in [0.25, 0.5, 0.75]:
        franja = patches.Rectangle((x - ancho*0.4, y + altura*h_frac), ancho*0.8, altura*0.1, facecolor='#FFFFFF', edgecolor='none', zorder=4)
        ax.add_patch(franja)
    copula = patches.Circle((x, y + altura + 0.3), 0.4, facecolor='#F1C40F', edgecolor='#B7950B', lw=1.5, zorder=5)
    ax.add_patch(copula)

def dibujar_resbalin(ax, x, y, largo=4.0, altura=2.5):
    """ Dibuja un resbalín de parque """
    ax.plot([x, x], [y, y + altura], color='#7F8C8D', lw=4, zorder=3)
    ax.plot([x, x + largo], [y + altura, y], color='#E67E22', lw=5, zorder=4)
    ax.plot([x + largo, x + largo], [y, y + 0.3], color='#7F8C8D', lw=3, zorder=3)


# ==============================================================================
# ============== GENERADOR DE ESQUEMAS GRÁFICOS ===============================
# ==============================================================================

def generar_esquema_amigable(tipo, datos):
    fig, ax = plt.subplots(figsize=(5.5, 3.8), dpi=150)
    ax.set_aspect('equal')
    ax.axis('off')

    if tipo == "arbol_elevacion":
        distancia = datos.get("distancia", 21)
        h_arbol = datos.get("h_arbol", 38)
        ang = datos.get("ang", 60)
        
        ax.plot([-2, distancia + 4], [0, 0], color='#27AE60', lw=3, zorder=2)
        ax.fill_between([-2, distancia + 4], -0.5, 0, color='#D5F5E3', zorder=1)
        
        dibujar_nino(ax, 0, 0, escala=1.8)
        dibujar_arbol(ax, distancia, 0, altura=h_arbol, ancho=3.0)
        
        h_ojo = 1.6
        ax.plot([0, distancia], [h_ojo, h_ojo], color='#7F8C8D', linestyle='--', lw=1.5, zorder=5)
        ax.plot([0, distancia], [h_ojo, h_arbol], color='#E74C3C', linestyle='-', lw=2.5, zorder=6)
        ax.plot([distancia, distancia], [h_ojo, h_arbol], color='#2980B9', linestyle=':', lw=2, zorder=5)

        r_arc = min(distancia, h_arbol) * 0.25
        arc = patches.Arc((0, h_ojo), r_arc*2, r_arc*2, angle=0, theta1=0, theta2=ang, color='#E74C3C', lw=2, zorder=7)
        ax.add_patch(arc)
        
        ax.text(r_arc + 0.5, h_ojo + 0.3, f"{ang}°", color='#E74C3C', fontweight='bold', fontsize=11)
        ax.text(distancia/2, -0.8, f"Distancia = {distancia} m", ha='center', fontweight='bold', color='#2C3E50', fontsize=10)
        ax.text(distancia + 0.8, h_arbol/2, f"H = {h_arbol} m", va='center', rotation=270, fontweight='bold', color='#2980B9', fontsize=10)

    elif tipo == "avion_depresion":
        distancia = datos.get("distancia", 15)
        altura = datos.get("altura", 8)
        ang = datos.get("ang", 25)
        
        ax.plot([-2, distancia + 4], [0, 0], color='#7F8C8D', lw=4, zorder=2)
        ax.text(0, -0.8, "📍 Pista de Aterrizaje", ha='center', fontweight='bold', color='#2C3E50', fontsize=10)
        
        dibujar_avion(ax, distancia, altura, escala=1.2)
        
        ax.plot([distancia - 6, distancia + 2], [altura, altura], color='#E74C3C', linestyle='--', lw=1.5, zorder=5)
        ax.plot([0, distancia], [0, altura], color='#2980B9', lw=2.5, zorder=6)
        ax.plot([distancia, distancia], [0, altura], color='#7F8C8D', linestyle=':', lw=1.5, zorder=4)
        
        arc = patches.Arc((distancia, altura), 3.0, 3.0, angle=0, theta1=180, theta2=180+ang, color='#E74C3C', lw=2, zorder=7)
        ax.add_patch(arc)
        
        ax.text(distancia - 2.2, altura - 0.6, f"{ang}°", color='#E74C3C', fontweight='bold', fontsize=11)
        ax.text(distancia + 0.6, altura/2, f"Altura = {altura} m", va='center', rotation=270, fontweight='bold', color='#27AE60', fontsize=10)
        ax.text(distancia/2, altura/2 + 0.5, "x (distancia visual)", rotation=np.degrees(np.arctan(altura/distancia)), ha='center', color='#2980B9', fontweight='bold', fontsize=10)

    elif tipo == "torre_depresion":
        altura = datos.get("altura", 34)
        distancia = datos.get("distancia", 6)
        ang = datos.get("ang", 80)
        
        ax.plot([-2, distancia + 4], [0, 0], color='#27AE60', lw=3, zorder=2)
        dibujar_torre(ax, 0, 0, altura=altura, ancho=2.0)
        
        ax.plot([0, distancia + 2], [altura, altura], color='#E74C3C', linestyle='--', lw=1.5, zorder=5)
        ax.plot([0, distancia], [altura, 0], color='#2980B9', lw=2.5, zorder=6)
        
        arc = patches.Arc((0, altura), 3.0, 3.0, angle=0, theta1=360-ang, theta2=360, color='#E74C3C', lw=2, zorder=7)
        ax.add_patch(arc)
        
        ax.text(1.5, altura - 0.8, f"{ang}°", color='#E74C3C', fontweight='bold', fontsize=11)
        ax.text(-1.2, altura/2, f"Torre: {altura} m", rotation=90, va='center', fontweight='bold', color='#C0392B', fontsize=10)
        ax.text(distancia/2, -0.8, f"Distancia K = {distancia} m", ha='center', fontweight='bold', color='#2980B9', fontsize=10)

    elif tipo == "resbalin":
        largo = datos.get("largo", 4)
        ang = datos.get("ang", 30)
        
        ax.plot([-1, largo + 2], [0, 0], color='#27AE60', lw=3, zorder=2)
        h_resbalin = largo * np.sin(np.radians(ang))
        
        dibujar_resbalin(ax, 0, 0, largo=largo*np.cos(np.radians(ang)), altura=h_resbalin)
        dibujar_nino(ax, largo*np.cos(np.radians(ang)) + 0.3, 0, escala=1.3)
        
        arc = patches.Arc((largo*np.cos(np.radians(ang)), 0), 1.5, 1.5, angle=0, theta1=180-ang, theta2=180, color='#E74C3C', lw=2)
        ax.add_patch(arc)
        
        ax.text(largo*0.3, h_resbalin*0.7, f"Largo = {largo} m", rotation=-ang, ha='center', fontweight='bold', color='#E67E22', fontsize=10)
        ax.text(-0.8, h_resbalin/2, "Altura (h)", rotation=90, va='center', fontweight='bold', color='#2980B9', fontsize=10)

    else:
        base = datos.get("base", 4)
        altura = datos.get("altura", 3)
        lbl_b = datos.get("lbl_base", f"{base}")
        lbl_a = datos.get("lbl_altura", f"{altura}")
        lbl_h = datos.get("lbl_hip", "c")
        
        x = [0, base, 0, 0]
        y = [0, 0, altura, 0]
        ax.plot(x, y, color='#2C3E50', lw=3, zorder=4)
        ax.fill(x, y, color='#EBF5FB', alpha=0.7, zorder=3)
        
        sq = min(base, altura) * 0.12
        ax.plot([0, sq, sq], [sq, sq, 0], color='#E74C3C', lw=1.8, zorder=5)
        
        ax.text(base/2, -altura*0.12, lbl_b, ha='center', fontweight='bold', color='#2980B9', fontsize=11)
        ax.text(-base*0.1, altura/2, lbl_a, ha='right', va='center', rotation=90, fontweight='bold', color='#2980B9', fontsize=11)
        ax.text(base/2 + 0.2, altura/2 + 0.2, lbl_h, ha='left', va='bottom', fontweight='bold', color='#E74C3C', fontsize=11)

    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=180)
    plt.close(fig)
    buffer.seek(0)
    return buffer


# ==============================================================================
# ============== BANCOS DE PREGUNTAS ===========================================
# ==============================================================================

banco_sec1_definiciones = [
    {
        "categoria": "1. Definición de Razones Trigonométricas",
        "pregunta": "En un triángulo rectángulo con catetos a = 8 cm, b = 15 cm e hipotenusa c = 17 cm, halla sen(β), cos(β) y tan(β) para el ángulo β (opuesto al cateto b = 15 cm).",
        "respuesta": "sen(β) = 15/17, cos(β) = 8/17, tan(β) = 15/8",
        "explicacion": "sen(β) = Cateto Opuesto / Hipotenusa = 15/17. cos(β) = Cateto Adyacente / Hipotenusa = 8/17. tan(β) = Cateto Opuesto / Cateto Adyacente = 15/8.",
        "esquema": {"tipo": "triangulo", "datos": {"base": 8, "altura": 15, "lbl_base": "a = 8 cm", "lbl_altura": "b = 15 cm", "lbl_hip": "c = 17 cm"}}
    },
    {
        "categoria": "1. Definición de Razones Trigonométricas",
        "pregunta": "¿Cuáles son las 6 razones trigonométricas principales y cómo se definen para un ángulo agudo en un triángulo rectángulo?",
        "respuesta": "sen=CO/HIP, cos=CA/HIP, tan=CO/CA, ctg=CA/CO, sec=HIP/CA, csc=HIP/CO",
        "explicacion": "Estas 6 razones dependen exclusivamente de la medida de los ángulos y no del tamaño del triángulo."
    }
]

banco_sec2_pitagoras = [
    {
        "categoria": "2. Teorema de Pitágoras",
        "pregunta": "En un triángulo rectángulo ABC, los catetos miden a = 4 cm y b = 3 cm. Calcula la hipotenusa c y las razones sen(α) y cos(α) para el ángulo α en el vértice A.",
        "respuesta": "c = 5 cm, sen(α) = 4/5, cos(α) = 3/5",
        "explicacion": "c = √(3² + 4²) = √25 = 5 cm. Para α: cateto opuesto = 4, cateto adyacente = 3.",
        "esquema": {"tipo": "triangulo", "datos": {"base": 3, "altura": 4, "lbl_base": "b = 3 cm", "lbl_altura": "a = 4 cm", "lbl_hip": "c = 5 cm"}}
    },
    {
        "categoria": "2. Teorema de Pitágoras",
        "pregunta": "Un triángulo rectángulo tiene cateto adyacente = 40 y cateto opuesto = 9. Determina su hipotenusa c y sen(β).",
        "respuesta": "c = 41, sen(β) = 9/41",
        "explicacion": "c = √(40² + 9²) = √(1600 + 81) = √1681 = 41. sen(β) = 9/41.",
        "esquema": {"tipo": "triangulo", "datos": {"base": 40, "altura": 9, "lbl_base": "40", "lbl_altura": "9", "lbl_hip": "c = 41"}}
    }
]

banco_sec3_identidades = [
    {
        "categoria": "3. Identidades y Relaciones Trigonométricas",
        "pregunta": "Demuestra cómo calcular tan(α), cot(α), sec(α) y csc(α) si solo conoces los valores de sen(α) y cos(α).",
        "respuesta": "tan(α)=sen(α)/cos(α), cot(α)=cos(α)/sen(α), sec(α)=1/cos(α), csc(α)=1/sen(α)",
        "explicacion": "Cualquier razón trigonométrica se puede derivar directamente si se conocen únicamente seno y coseno del mismo ángulo."
    },
    {
        "categoria": "3. Identidades y Relaciones Trigonométricas",
        "pregunta": "Si sen(α) = 3/5 y cos(α) = 4/5, calcula el valor exacto de tan(α) y sec(α).",
        "respuesta": "tan(α) = 3/4, sec(α) = 5/4",
        "explicacion": "tan(α) = (3/5)/(4/5) = 3/4. sec(α) = 1/(4/5) = 5/4."
    }
]

banco_sec4_operaciones = [
    {
        "categoria": "4. Ángulos Conocidos y Operaciones",
        "pregunta": "Calcula el valor exacto de la expresión: sen(30°) + sen(60°).",
        "respuesta": "(1 + √3)/2",
        "explicacion": "sen(30°) = 1/2, sen(60°) = √3/2. Suma = 1/2 + √3/2 = (1 + √3)/2."
    },
    {
        "categoria": "4. Ángulos Conocidos y Operaciones",
        "pregunta": "Reduce la siguiente expresión trigonométrica: B = tan²(30°) − sec²(30°).",
        "respuesta": "-1",
        "explicacion": "tan(30°) = 1/√3 → tan² = 1/3. sec(30°) = 2/√3 → sec² = 4/3. B = 1/3 − 4/3 = −1."
    },
    {
        "categoria": "4. Ángulos Conocidos y Operaciones",
        "pregunta": "Calcula el valor numérico de: [tan(60°) + 3·cos(30°)] ÷ [sen(45°)]²",
        "respuesta": "5√3",
        "explicacion": "tan(60°)=√3, cos(30°)=√3/2 → Num = 5√3/2. sen(45°)=√2/2 → Den = 1/2. Res = (5√3/2)/(1/2) = 5√3."
    }
]

banco_sec5_notables = [
    {
        "categoria": "5. Ángulos Notables (37°-53°)",
        "pregunta": "En un triángulo notable de 37°-53° (lados 3k:4k:5k), la hipotenusa mide 15 cm. Calcula la longitud de sus catetos.",
        "respuesta": "Cateto menor = 9 cm, Cateto mayor = 12 cm",
        "explicacion": "Hipotenusa = 5k = 15 → k = 3. Cateto opuesto a 37° = 3k = 9 cm. Cateto opuesto a 53° = 4k = 12 cm.",
        "esquema": {"tipo": "triangulo", "datos": {"base": 12, "altura": 9, "lbl_base": "12 cm", "lbl_altura": "9 cm", "lbl_hip": "15 cm"}}
    },
    {
        "categoria": "5. Ángulos Notables (30°-60°)",
        "pregunta": "En un triángulo rectángulo de 30°-60°, la hipotenusa mide 16 mm. ¿Cuánto miden sus catetos?",
        "respuesta": "Cateto menor (30°) = 8 mm, Cateto mayor (60°) = 8√3 mm",
        "explicacion": "Hipotenusa = 2k = 16 mm → k = 8 mm. Cateto menor = 8 mm, cateto mayor = 8√3 mm.",
        "esquema": {"tipo": "triangulo", "datos": {"base": 13.8, "altura": 8, "lbl_base": "8√3 mm", "lbl_altura": "8 mm", "lbl_hip": "16 mm"}}
    },
    {
        "categoria": "5. Ángulos Notables (45°-45°)",
        "pregunta": "En un triángulo rectángulo isósceles con ángulos de 45°, la hipotenusa mide 7√2 cm. Encuentra la longitud de sus catetos x.",
        "respuesta": "x = 7 cm",
        "explicacion": "Hipotenusa = k√2 = 7√2 cm → k = 7 cm. Ambos catetos miden 7 cm.",
        "esquema": {"tipo": "triangulo", "datos": {"base": 7, "altura": 7, "lbl_base": "7 cm", "lbl_altura": "7 cm", "lbl_hip": "7√2 cm"}}
    }
]

banco_sec6_calculadora = [
    {
        "categoria": "6. Cálculo de Lados (Uso de Calculadora)",
        "pregunta": "En un triángulo rectángulo, la hipotenusa mide 11 cm y un ángulo agudo mide 42°. Calcula la longitud del cateto adyacente x.",
        "respuesta": "x ≈ 8.2 cm",
        "explicacion": "cos(42°) = x / 11 → x = 11 · cos(42°) ≈ 11 · 0.7431 ≈ 8.17 cm ≈ 8.2 cm.",
        "esquema": {"tipo": "triangulo", "datos": {"base": 8.2, "altura": 7.4, "lbl_base": "x ≈ 8.2 cm", "lbl_altura": "y ≈ 7.4 cm", "lbl_hip": "11 cm"}}
    },
    {
        "categoria": "6. Cálculo de Ángulos (Inversas)",
        "pregunta": "En un triángulo rectángulo, el cateto opuesto a un ángulo z mide 32 pulgadas y la hipotenusa mide 74 pulgadas. Encuentra la medida del ángulo z.",
        "respuesta": "z ≈ 25.6° (o 26°)",
        "explicacion": "sen(z) = 32 / 74 → z = sen⁻¹(32/74) ≈ sen⁻¹(0.4324) ≈ 25.6° ≈ 26°.",
        "esquema": {"tipo": "triangulo", "datos": {"base": 66.7, "altura": 32, "lbl_base": "CA", "lbl_altura": "32 pulg", "lbl_hip": "74 pulg"}}
    }
]

banco_sec7_aplicaciones = [
    {
        "categoria": "7. Ángulos de Depresión — La Torre",
        "pregunta": "La medida del ángulo de depresión desde lo alto de una torre de 34 m de altura hasta un punto K en el suelo es de 80°. Calcula la distancia del punto K a la base de la torre.",
        "respuesta": "≈ 6 metros",
        "explicacion": "El ángulo interior superior mide 90° − 80° = 10°. tan(10°) = x / 34 → x = 34 · tan(10°) ≈ 6 m.",
        "esquema": {"tipo": "torre_depresion", "datos": {"distancia": 6, "altura": 34, "ang": 80}}
    },
    {
        "categoria": "7. Ángulos de Elevación — La Araucaria",
        "pregunta": "Antonia observa la copa de una araucaria con un ángulo de elevación de 60° respecto del nivel de sus ojos. Ella mide 1,60 m de estatura y está a 21 m de la base. ¿Cuál es la altura total H de la araucaria?",
        "respuesta": "≈ 38 metros",
        "explicacion": "Altura sobre nivel de ojos = 21 · tan(60°) = 21√3 ≈ 36,37 m. Altura total = 36,37 + 1,60 ≈ 38 m.",
        "esquema": {"tipo": "arbol_elevacion", "datos": {"distancia": 21, "h_arbol": 38, "ang": 60}}
    },
    {
        "categoria": "7. Ángulos de Depresión — El Avión",
        "pregunta": "Un avión vuela a 1 700 m de altura cuando comienza su descenso a la pista con un ángulo de depresión de 25°. ¿A qué distancia visual (x) se encuentra de la pista?",
        "respuesta": "≈ 4 022,7 metros",
        "explicacion": "sen(25°) = 1700 / x → x = 1700 / sen(25°) ≈ 1700 / 0,4226 ≈ 4022,7 m.",
        "esquema": {"tipo": "avion_depresion", "datos": {"distancia": 4022, "altura": 1700, "ang": 25}}
    },
    {
        "categoria": "7. Ángulos de Elevación — El Resbalín",
        "pregunta": "Ángela sube a un resbalín que tiene una inclinación de 30° respecto al suelo y 4 metros de longitud. ¿Cuál es la altura máxima h que alcanza?",
        "respuesta": "2 metros",
        "explicacion": "sen(30°) = h / 4 → 1/2 = h / 4 → h = 2 m.",
        "esquema": {"tipo": "resbalin", "datos": {"largo": 4, "ang": 30}}
    }
]


# ==============================================================================
# ============== REPORTLAB PDF GENERATOR (SOLO PREGUNTAS) =======================
# ==============================================================================

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
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=1.8*cm, bottomMargin=1.8*cm, leftMargin=1.8*cm, rightMargin=1.8*cm)
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
        elementos.append(Paragraph("Instrucciones: Resuelve cada ejercicio en el espacio indicado utilizando los esquemas de apoyo.", estilos['normal']))
    else:
        elementos.append(Paragraph("SOLUCIONARIO — Respuestas y Explicaciones Paso a Paso", estilos['subtitulo']))
    
    elementos.append(Spacer(1, 0.4*cm))
    
    for i, p in enumerate(preguntas, 1):
        elementos.append(Paragraph(f"<b>{i}.</b> {p['pregunta']}", estilos['pregunta']))
        
        if "esquema" in p:
            buf_img = generar_esquema_amigable(p["esquema"]["tipo"], p["esquema"]["datos"])
            img_rl = RLImage(buf_img, width=8.5*cm, height=5.8*cm)
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


# ==============================================================================
# ============== FUNCIONES AUXILIARES DE INTERFAZ STREAMLIT ====================
# ==============================================================================

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
    
    st.info(f"📝 **Ejercicio Interactivo:** {preg['pregunta']}")
    
    if "esquema" in preg:
        buf_img = generar_esquema_amigable(preg["esquema"]["tipo"], preg["esquema"]["datos"])
        st.image(buf_img, caption="Esquema ilustrado del ejercicio", width=420)

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


# ==============================================================================
# ============== INTERFAZ PRINCIPAL Y NAVEGACIÓN DEDICADA =======================
# ==============================================================================

with st.sidebar:
    st.title("Dashboard 📊")
    ruta_imagen = "IMG_7157.jpeg"
    if os.path.exists(ruta_imagen):
        st.image(ruta_imagen, use_container_width=True, caption="Panel de Control")
    
    st.divider()
    st.subheader("Secciones del PPT (En orden):")
    opcion_menu = st.radio(
        "Navegación",
        [
            "🏠 Inicio",
            "1. Definición de Razones Trigonométricas",
            "2. Teorema de Pitágoras",
            "3. Identidades y Relaciones Trigonométricas",
            "4. Ángulos Conocidos y Operaciones",
            "5. Ángulos Notables (30°-60°, 45°-45°, 37°-53°)",
            "6. Cálculo de Lados y Ángulos (Calculadora)",
            "7. Ángulos de Elevación y Depresión (Aplicaciones)",
            "📄 Generar Prueba Desarrollo"
        ],
        label_visibility="collapsed"
    )

st.title("📐 2° Medio — Razones Trigonométricas")

# --- SECCIÓN 0: INICIO ---
if opcion_menu == "🏠 Inicio":
    st.subheader("¡Bienvenido al Módulo Interactivo de Trigonometría!")
    st.markdown("""
    Esta plataforma organiza el contenido del curso en **7 clases explicativas e interactivas**:
    
    1. **Definición de Razones Trigonométricas:** Mnemotecnia SOH-CAH-TOA y definiciones básicas.
    2. **Teorema de Pitágoras:** Relación entre catetos e hipotenusa.
    3. **Identidades y Relaciones:** Derivación de tangente, secante y cosecante.
    4. **Ángulos Conocidos y Operaciones:** Tabla oficial de valores numéricos.
    5. **Ángulos Notables:** Proporciones geométricas en triángulos especiales (30°-60°, 45°-45°, 37°-53°).
    6. **Cálculo con Calculadora:** Encontrar lados desconocidos y ángulos con funciones inversas ($\sin^{-1}, \cos^{-1}, \tan^{-1}$).
    7. **Ángulos de Elevación y Depresión:** Aplicaciones prácticas ilustradas.
    """)

# --- SECCIÓN 1 ---
elif opcion_menu == "1. Definición de Razones Trigonométricas":
    with st.expander("📚 CLASE EXPLICATIVA: Definición de Razones Trigonométricas", expanded=True):
        st.markdown("""
        Las **razones trigonométricas** son relaciones cociente entre las longitudes de dos lados de un triángulo rectángulo respecto a uno de sus ángulos agudos ($\alpha$).

        * **Seno ($\text{sen } \alpha$):** $\\frac{\\text{Cateto Opuesto}}{\\text{Hipotenusa}}$
        * **Coseno ($\text{cos } \alpha$):** $\\frac{\\text{Cateto Adyacente}}{\\text{Hipotenusa}}$
        * **Tangente ($\text{tan } \alpha$):** $\\frac{\\text{Cateto Opuesto}}{\\text{Cateto Adyacente}}$

        💡 **Mnemotecnia Famosa:** **SOH - CAH - TOA**
        * **SOH:** **S**en = **O**puesto / **H**ipotenusa
        * **CAH:** **C**os = **A**dyacente / **H**ipotenusa
        * **TOA:** **T**an = **O**puesto / **A**dyacente
        """)
    st.divider()
    mostrar_banco("Ejercicios Prácticos", banco_sec1_definiciones, "sec1")

# --- SECCIÓN 2 ---
elif opcion_menu == "2. Teorema de Pitágoras":
    with st.expander("📚 CLASE EXPLICATIVA: Teorema de Pitágoras", expanded=True):
        st.markdown("""
        En todo triángulo rectángulo, el cuadrado de la hipotenusa ($c$) es igual a la suma de los cuadrados de los catetos ($a$ y $b$):

        $$\large c^2 = a^2 + b^2$$

        * **Para hallar la Hipotenusa:** $c = \\sqrt{a^2 + b^2}$
        * **Para hallar un Cateto:** $a = \\sqrt{c^2 - b^2}$ o $b = \\sqrt{c^2 - a^2}$
        """)
    st.divider()
    mostrar_banco("Ejercicios Prácticos", banco_sec2_pitagoras, "sec2")

# --- SECCIÓN 3 ---
elif opcion_menu == "3. Identidades y Relaciones Trigonométricas":
    with st.expander("📚 CLASE EXPLICATIVA: Identidades y Relaciones Trigonométricas", expanded=True):
        st.markdown("""
        Las 6 razones trigonométricas están directamente ligadas entre sí. Si conoces $\text{sen}(\\alpha)$ y $\text{cos}(\\alpha)$, puedes obtener todas las demás:

        * **Tangente:** $\\tan(\\alpha) = \\frac{\\text{sen}(\\alpha)}{\\text{cos}(\\alpha)}$
        * **Cotangente:** $\\cot(\\alpha) = \\frac{\\text{cos}(\\alpha)}{\\text{sen}(\\alpha)} = \\frac{1}{\\tan(\\alpha)}$
        * **Secante:** $\\sec(\\alpha) = \\frac{1}{\\text{cos}(\\alpha)}$
        * **Cosecante:** $\\csc(\\alpha) = \\frac{1}{\\text{sen}(\\alpha)}$
        """)
    st.divider()
    mostrar_banco("Ejercicios Prácticos", banco_sec3_identidades, "sec3")

# --- SECCIÓN 4 ---
elif opcion_menu == "4. Ángulos Conocidos y Operaciones":
    with st.expander("📚 CLASE EXPLICATIVA: Tabla de Ángulos Conocidos", expanded=True):
        st.markdown("""
        A continuación se presentan los valores numéricos exactos para los ángulos más utilizados en las evaluaciones:

| Ángulo α | sen(α) | cos(α) | tan(α) | cot(α) | sec(α) | csc(α) |
|---|---|---|---|---|---|---|
| **0°** | 0 | 1 | 0 | ∞ | 1 | ∞ |
| **30°** | 1/2 | √3/2 | √3/3 | √3 | 2/√3 | 2 |
| **45°** | √2/2 | √2/2 | 1 | 1 | √2 | √2 |
| **60°** | √3/2 | 1/2 | √3 | √3/3 | 2 | 2/√3 |
| **90°** | 1 | 0 | ∞ | 0 | ∞ | 1 |
| **180°** | 0 | -1 | 0 | ∞ | -1 | ∞ |
| **270°** | -1 | 0 | ∞ | 0 | ∞ | -1 |
| **360°** | 0 | 1 | 0 | ∞ | 1 | ∞ |
""")
    st.divider()
    mostrar_banco("Ejercicios Prácticos", banco_sec4_operaciones, "sec4")

# --- SECCIÓN 5 ---
elif opcion_menu == "5. Ángulos Notables (30°-60°, 45°-45°, 37°-53°)":
    with st.expander("📚 CLASE EXPLICATIVA: Triángulos Notables y Proporciones", expanded=True):
        st.markdown("""
        Existen tres triángulos rectángulos notables cuyas proporciones entre lados son constantes:

        1. **Triángulo 30° - 60°:** Proporción de lados $\\rightarrow k : k\\sqrt{3} : 2k$ (Hipotenusa $= 2k$, opuesto a 30° $= k$).
        2. **Triángulo 45° - 45°:** Proporción de lados $\\rightarrow k : k : k\\sqrt{2}$ (Catetos iguales).
        3. **Triángulo 37° - 53°:** Proporción aproximada $\\rightarrow 3k : 4k : 5k$ (Catetos 3k y 4k, Hipotenusa 5k).
        """)
    st.divider()
    mostrar_banco("Ejercicios Prácticos", banco_sec5_notables, "sec5")

# --- SECCIÓN 6 ---
elif opcion_menu == "6. Cálculo de Lados y Ángulos (Calculadora)":
    with st.expander("📚 CLASE EXPLICATIVA: Uso de Calculadora y Funciones Inversas", expanded=True):
        st.markdown("""
        * **Para encontrar un lado desconocido:** Se despeja la incógnita de la razón trigonométrica conveniente.
          $$\\text{Ejemplo: } \\text{cos}(42°) = \\frac{x}{11} \\implies x = 11 \\cdot \\text{cos}(42°)$$
        
        * **Para encontrar un ángulo desconocido:** Se aplica la función trigonométrica inversa (SHIFT / $\text{sin}^{-1}, \text{cos}^{-1}, \text{tan}^{-1}$).
          $$\\text{Ejemplo: } \\text{sen}(\\theta) = \\frac{32}{74} \\implies \\theta = \\text{sen}^{-1}\\left(\\frac{32}{74}\\right) \\approx 25,6°$$
        """)
    st.divider()
    mostrar_banco("Ejercicios Prácticos", banco_sec6_calculadora, "sec6")

# --- SECCIÓN 7 ---
elif opcion_menu == "7. Ángulos de Elevación y Depresión (Aplicaciones)":
    with st.expander("📚 CLASE EXPLICATIVA: Ángulos de Elevación y Depresión", expanded=True):
        st.markdown("""
        * **Línea de Visión / Visual:** La línea recta imaginaria que une los ojos del observador con el objeto.
        * **Línea Horizontal:** Línea paralela al suelo que pasa por los ojos del observador.
        * **Ángulo de Elevación:** Ángulo formado entre la línea horizontal y la línea visual **hacia arriba**.
        * **Ángulo de Depresión:** Ángulo formado entre la línea horizontal y la línea visual **hacia abajo**.
        """)
    st.divider()
    mostrar_banco("Ejercicios Prácticos", banco_sec7_aplicaciones, "sec7")

# --- SECCIÓN GENERAR PRUEBAS EN PDF ---
elif opcion_menu == "📄 Generar Prueba Desarrollo":
    st.header("📄 Generar Prueba de Desarrollo (Solo Evaluaciones)")
    st.info("Nota: Las clases explicativas de la pantalla interactiva no se incluirán en el PDF generado. El PDF contendrá únicamente el formato de examen oficial con preguntas y esquemas de desarrollo.")
    
    mapeo_secciones = {
        "1. Definición de Razones": banco_sec1_definiciones,
        "2. Teorema de Pitágoras": banco_sec2_pitagoras,
        "3. Identidades Trigonométricas": banco_sec3_identidades,
        "4. Ángulos Conocidos": banco_sec4_operaciones,
        "5. Ángulos Notables": banco_sec5_notables,
        "6. Cálculo con Calculadora": banco_sec6_calculadora,
        "7. Elevación y Depresión": banco_sec7_aplicaciones
    }
    
    temas_seleccion = st.multiselect(
        "Selecciona las secciones a incluir en la prueba:",
        list(mapeo_secciones.keys()),
        default=["2. Teorema de Pitágoras", "5. Ángulos Notables", "7. Elevación y Depresión"]
    )
    
    nombre_prueba = st.text_input("Nombre de la evaluación:", value="Evaluación de Matemáticas 2° Medio — Razones Trigonométricas")
    
    if st.button("📄 Generar Pruebas en PDF", type="primary"):
        prueba_preguntas = []
        for t in temas_seleccion:
            for item in mapeo_secciones[t]:
                cp = item.copy()
                cp['_tema'] = t
                prueba_preguntas.append(cp)
        
        fecha_hoy = datetime.now().strftime("%d/%m/%Y")
        pdf_p = generar_pdf_desarrollo(prueba_preguntas, nombre_prueba, fecha_hoy, False)
        pdf_s = generar_pdf_desarrollo(prueba_preguntas, nombre_prueba, fecha_hoy, True)
        
        st.success(f"✅ ¡Se generaron {len(prueba_preguntas)} ejercicios ordenados con sus ilustraciones en PDF!")
        c1, c2 = st.columns(2)
        c1.download_button("📥 Descargar PRUEBA (.pdf)", pdf_p, file_name="Prueba_Trigonometria.pdf", mime="application/pdf")
        c2.download_button("📥 Descargar SOLUCIONARIO (.pdf)", pdf_s, file_name="Solucionario_Trigonometria.pdf", mime="application/pdf")

st.divider()
st.caption("💡 Banco de ejercicios 2° Medio — Basado en el programa oficial PPT")


---

### Resumen de cambios:
1. **Clases explicativas agregadas:** Se incorporó un bloque descriptivo `st.expander("📚 CLASE EXPLICATIVA: ...")` en cada una de las 7 secciones del menú de Streamlit con las definiciones teóricas, gráficos y fórmulas del PPT.
2. **Generación de PDF preservada:** La función `generar_pdf_desarrollo()` continúa utilizando únicamente los bancos de preguntas (`banco_sec1_definiciones`, etc.), asegurando que el PDF generado contenga exclusivamente la evaluación limpia para los estudiantes y su solucionario.Sí, es totalmente posible estructurar el contenido para que incluya explicaciones o guías teóricas que no aparezcan al exportar o generar el PDF final.

Dependiendo de las herramientas o del entorno de trabajo que estés utilizando para redactar tu documento, existen diferentes métodos para lograrlo:

---

### Opción 1: Uso de Bloques Ocultos / Comentarios
Si redactas en formatos como **Markdown**, **HTML** o compiladores basados en texto (como **LaTeX**), puedes envolver la enseñanza en bloques de comentarios o condicionales.

* **Markdown / HTML:**
  ```html
  <!-- 
  [CLASE EXPLICATIVA / NOTA PARA EL DOCENTE]
  Aquí va el resumen conceptual o la enseñanza antes de las preguntas.
  -->
