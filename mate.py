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
st.set_page_config(page_title="📐 Matemáticas — Triángulos y Trigonometría", layout="wide")


# ==============================================================================
# ============== DIBUJANTES DE ELEMENTOS AMIGABLES (MATPLOTLIB) =================
# ==============================================================================

def dibujar_nino(ax, x, y, escala=1.0):
    """ Dibuja un niño/persona amigable en la posición (x, y) """
    r_cabeza = 0.15 * escala
    
    # Cabeza
    cabeza = patches.Circle((x, y + 0.7 * escala), r_cabeza, facecolor='#FFD1DC', edgecolor='#2B2B2B', lw=1.5, zorder=5)
    ax.add_patch(cabeza)
    # Ojos
    ax.plot([x - 0.05 * escala, x + 0.05 * escala], [y + 0.72 * escala, y + 0.72 * escala], 'o', color='#2B2B2B', ms=3*escala, zorder=6)
    # Sonrisa
    arc = patches.Arc((x, y + 0.68 * escala), 0.12 * escala, 0.08 * escala, angle=0, theta1=200, theta2=340, color='#D9534F', lw=1.5, zorder=6)
    ax.add_patch(arc)
    # Cuerpo / Polera
    cuerpo = patches.Polygon([[x - 0.12 * escala, y + 0.25 * escala], [x + 0.12 * escala, y + 0.25 * escala], [x + 0.08 * escala, y + 0.55 * escala], [x - 0.08 * escala, y + 0.55 * escala]], facecolor='#4A90E2', edgecolor='#2B2B2B', lw=1.5, zorder=4)
    ax.add_patch(cuerpo)
    # Piernas
    ax.plot([x - 0.06 * escala, x - 0.06 * escala], [y, y + 0.25 * escala], color='#2B2B2B', lw=2.5, zorder=3)
    ax.plot([x + 0.06 * escala, x + 0.06 * escala], [y, y + 0.25 * escala], color='#2B2B2B', lw=2.5, zorder=3)
    # Zapatos
    ax.plot([x - 0.09 * escala, x - 0.03 * escala], [y, y], color='#8B5A2B', lw=3, zorder=4)
    ax.plot([x + 0.03 * escala, x + 0.09 * escala], [y, y], color='#8B5A2B', lw=3, zorder=4)

def dibujar_arbol(ax, x, y, altura=4.0, ancho=2.0):
    """ Dibuja un árbol amigable (tronco + copa frondosa) """
    w_tronco = ancho * 0.2
    h_tronco = altura * 0.4
    
    # Tronco
    tronco = patches.Rectangle((x - w_tronco/2, y), w_tronco, h_tronco, facecolor='#8B5A2B', edgecolor='#4A2E12', lw=1.5, zorder=3)
    ax.add_patch(tronco)
    
    # Copa (círculos verdes superpuestos)
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
    """ Dibuja un faro/torre estilizada """
    torre = patches.Polygon([[x - ancho/2, y], [x + ancho/2, y], [x + ancho*0.3, y + altura], [x - ancho*0.3, y + altura]], facecolor='#E74C3C', edgecolor='#922B21', lw=1.5, zorder=3)
    ax.add_patch(torre)
    for h_frac in [0.25, 0.5, 0.75]:
        franja = patches.Rectangle((x - ancho*0.4, y + altura*h_frac), ancho*0.8, altura*0.1, facecolor='#FFFFFF', edgecolor='none', zorder=4)
        ax.add_patch(franja)
    copula = patches.Circle((x, y + altura + 0.3), 0.4, facecolor='#F1C40F', edgecolor='#B7950B', lw=1.5, zorder=5)
    ax.add_patch(copula)

def dibujar_resbalin(ax, x, y, largo=4.0, altura=2.5):
    """ Dibuja un resbalín """
    ax.plot([x, x], [y, y + altura], color='#7F8C8D', lw=4, zorder=3)
    ax.plot([x, x + largo], [y + altura, y], color='#E67E22', lw=5, zorder=4)
    ax.plot([x + largo, x + largo], [y, y + 0.3], color='#7F8C8D', lw=3, zorder=3)


# ==============================================================================
# ============== GENERADOR DE ESQUEMAS GRÁFICOS ===============================
# ==============================================================================

def generar_esquema_amigable(tipo, datos):
    """
    Genera el esquema gráfico contextualizado y lo retorna como BytesIO (PNG).
    """
    fig, ax = plt.subplots(figsize=(5.5, 3.8), dpi=150)
    ax.set_aspect('equal')
    ax.axis('off')

    if tipo == "arbol_elevacion":
        distancia = datos.get("distancia", 12)
        h_arbol = datos.get("h_arbol", 12)
        ang = datos.get("ang", 45)
        
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
        ax.text(distancia + 0.8, h_arbol/2, f"Altura = {h_arbol} m", va='center', rotation=270, fontweight='bold', color='#2980B9', fontsize=10)

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

    elif tipo == "faro_depresion":
        altura = datos.get("altura", 10)
        distancia = datos.get("distancia", 12)
        ang = datos.get("ang", 45)
        
        ax.plot([-2, distancia + 4], [0, 0], color='#2980B9', lw=4, zorder=2)
        ax.fill_between([-2, distancia + 4], -0.8, 0, color='#AED6F1', zorder=1)
        
        dibujar_torre(ax, 0, 0, altura=altura, ancho=2.0)
        
        ax.plot([distancia - 0.8, distancia + 0.8, distancia + 0.5, distancia - 0.5], [0.3, 0.3, 0, 0], color='#8B5A2B', zorder=4)
        ax.fill([distancia - 0.8, distancia + 0.8, distancia + 0.5, distancia - 0.5], [0.3, 0.3, 0, 0], color='#D35400', zorder=4)
        
        ax.plot([0, distancia + 3], [altura + 0.3, altura + 0.3], color='#E74C3C', linestyle='--', lw=1.5, zorder=5)
        ax.plot([0, distancia], [altura + 0.3, 0.3], color='#2980B9', lw=2.5, zorder=6)
        
        arc = patches.Arc((0, altura + 0.3), 3.0, 3.0, angle=0, theta1=360-ang, theta2=360, color='#E74C3C', lw=2, zorder=7)
        ax.add_patch(arc)
        
        ax.text(1.8, altura - 0.4, f"{ang}°", color='#E74C3C', fontweight='bold', fontsize=11)
        ax.text(-1.2, altura/2, f"Faro: {altura} m", rotation=90, va='center', fontweight='bold', color='#C0392B', fontsize=10)
        ax.text(distancia/2, -0.6, f"Distancia = {distancia} m", ha='center', fontweight='bold', color='#2980B9', fontsize=10)

    elif tipo == "resbalin":
        largo = datos.get("largo", 4)
        ang = datos.get("ang", 30)
        
        ax.plot([-1, largo + 2], [0, 0], color='#27AE60', lw=3, zorder=2)
        h_resbalin = largo * np.sin(np.radians(ang))
        
        dibujar_resbalin(ax, 0, 0, largo=largo*np.cos(np.radians(ang)), altura=h_resbalin)
        dibujar_nino(ax, largo*np.cos(np.radians(ang)) + 0.3, 0, escala=1.3)
        
        arc = patches.Arc((largo*np.cos(np.radians(ang)), 0), 1.5, 1.5, angle=0, theta1=180-ang, theta2=180, color='#E74C3C', lw=2)
        ax.add_patch(arc)
        
        ax.text(largo*0.3, h_resbalin*0.7, f"Resbalín = {largo} m", rotation=-ang, ha='center', fontweight='bold', color='#E67E22', fontsize=10)
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

banco_area_perimetro = [
    {
        "pregunta": "Un triángulo tiene base 12 cm y altura 8 cm. Calcula su área.", 
        "respuesta": "48 cm²", 
        "explicacion": "Área = (12 × 8) ÷ 2 = 48 cm²",
        "esquema": {"tipo": "triangulo", "datos": {"base": 12, "altura": 8, "lbl_base": "b = 12 cm", "lbl_altura": "h = 8 cm", "lbl_hip": ""}}
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
        "esquema": {"tipo": "triangulo", "datos": {"base": 4, "altura": 3, "lbl_base": "4 cm", "lbl_altura": "3 cm", "lbl_hip": "c = ?"}}
    },
    {
        "pregunta": "Un cateto mide 12 cm y la hipotenusa 13 cm. ¿Cuánto mide el otro cateto (a)?", 
        "respuesta": "5 cm", 
        "explicacion": "13² − 12² = 169 − 144 = 25 → √25 = 5 cm",
        "esquema": {"tipo": "triangulo", "datos": {"base": 12, "altura": 5, "lbl_base": "12 cm", "lbl_altura": "a = ?", "lbl_hip": "13 cm"}}
    }
]

banco_cosenos = [
    {"pregunta": "Lados 5 cm y 7 cm con ángulo de 60° entre ellos. Tercer lado = ?", "respuesta": "√39 cm", "explicacion": "c² = 25 + 49 − 35 = 39 → √39 cm"}
]

banco_trigonometria = [
    {
        "categoria": "📐 Ángulo de elevación — El Árbol", 
        "pregunta": "Desde el suelo, a 12 m de la base de un árbol, un niño observa su cima con un ángulo de elevación de 45°. ¿Cuál es la altura del árbol?", 
        "respuesta": "12 m", 
        "explicacion": "tan(45°) = h/12 → h = 12 m",
        "esquema": {"tipo": "arbol_elevacion", "datos": {"distancia": 12, "h_arbol": 12, "ang": 45}}
    },
    {
        "categoria": "📉 Ángulo de depresión — El Faro", 
        "pregunta": "Desde un faro de 30 m de altura, se observa un barco con un ángulo de depresión de 45°. ¿A qué distancia horizontal está el barco?", 
        "respuesta": "30 m", 
        "explicacion": "tan(45°) = 30/d → d = 30 m",
        "esquema": {"tipo": "faro_depresion", "datos": {"distancia": 30, "altura": 30, "ang": 45}}
    }
]

banco_guia_2medio = [
    {
        "categoria": "📐 Árbol y Araucaria (Elevación)",
        "pregunta": "Antonia observa el punto más alto de una araucaria con un ángulo de elevación de 60° respecto del nivel de sus ojos. Ella mide 1,60 m de estatura y la distancia a la base es de 21 m. ¿Cuál es la altura total de la araucaria?",
        "respuesta": "≈ 38 metros",
        "explicacion": "Altura desde ojos = 21 · tan(60°) = 21√3 ≈ 36,37 m. Altura total = 36,37 + 1,60 ≈ 38 m.",
        "esquema": {"tipo": "arbol_elevacion", "datos": {"distancia": 21, "h_arbol": 38, "ang": 60}}
    },
    {
        "categoria": "✈️ Avión en Descenso (Depresión)",
        "pregunta": "Un avión vuela a 1 700 m de altura y comienza su descenso a la pista con un ángulo de depresión de 25°. ¿A qué distancia visual (x) se encuentra de la pista?",
        "respuesta": "≈ 4 022,7 metros",
        "explicacion": "sen(25°) = 1700 / x → x = 1700 / sen(25°) ≈ 4022,7 m.",
        "esquema": {"tipo": "avion_depresion", "datos": {"distancia": 4022, "altura": 1700, "ang": 25}}
    },
    {
        "categoria": "🛝 El Resbalín del Parque",
        "pregunta": "Ángela sube a un resbalín que tiene una inclinación de 30° respecto al suelo y 4 metros de longitud. ¿Cuál es la altura máxima que alcanza?",
        "respuesta": "2 metros",
        "explicacion": "sen(30°) = h / 4 → 1/2 = h / 4 → h = 2 m.",
        "esquema": {"tipo": "resbalin", "datos": {"largo": 4, "ang": 30}}
    }
]

banco_alternativas = [
    {"pregunta": "¿Cuál es el área de un triángulo con base 10 cm y altura 6 cm?", "opciones": ["A) 16 cm²", "B) 30 cm²", "C) 60 cm²", "D) 120 cm²"], "respuesta_correcta": "B", "explicacion": "Área = (10 × 6) ÷ 2 = 30 cm²"},
    {"pregunta": "¿Cuánto mide el tercer ángulo de un triángulo si los otros dos miden 50° y 60°?", "opciones": ["A) 70°", "B) 80°", "C) 90°", "D) 110°"], "respuesta_correcta": "A", "explicacion": "180° − 50° − 60° = 70°"}
]


# ==============================================================================
# ============== REPORTLAB PDF GENERATOR ========================================
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
# ============== INTERFAZ STREAMLIT ============================================
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
    
    if "categoria" in preg:
        st.subheader(f"{preg['categoria']}")
    
    st.info(f"📝 {preg['pregunta']}")
    
    if "esquema" in preg:
        buf_img = generar_esquema_amigable(preg["esquema"]["tipo"], preg["esquema"]["datos"])
        st.image(buf_img, caption="Esquema amigable del ejercicio", width=420)

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
        st.image(ruta_imagen, use_container_width=True, caption="Panel de Control")
    
    st.divider()
    opcion_menu = st.radio(
        "Navegación",
        ["🏠 Inicio", "📏 Área y Perímetro", "📐 Teorema de Pitágoras", "🔺 Razones Trigonométricas", "📘 Guía 2° Medio", "📄 Generar Prueba Desarrollo"],
        label_visibility="collapsed"
    )

st.title("📐 Banco de Ejercicios — Triángulos y Trigonometría")

if opcion_menu == "🏠 Inicio":
    st.subheader("¡Bienvenido!")
    st.markdown("""
    Esta aplicación incluye **esquemas amigables e ilustrados** (niños, árboles, aviones, faros, resbalines) dibujados automáticamente para facilitar la comprensión de la trigonometría.
    
    * **Práctica Interactiva:** Navega por los temas para ver los esquemas dinámicos.
    * **Generación de Evaluaciones:** Genera PDFs con ilustraciones y solucionarios listos para imprimir.
    """)

elif opcion_menu == "📏 Área y Perímetro":
    mostrar_banco("📏 Área y Perímetro", banco_area_perimetro, "area")

elif opcion_menu == "📐 Teorema de Pitágoras":
    mostrar_banco("📐 Teorema de Pitágoras", banco_pitagoras, "pitagoras")

elif opcion_menu == "🔺 Razones Trigonométricas":
    mostrar_banco("🔺 Razones Trigonométricas", banco_trigonometria, "trigo")

elif opcion_menu == "📘 Guía 2° Medio":
    mostrar_banco("📘 Guía 2° Medio — Razones Trigonométricas", banco_guia_2medio, "g2m")

elif opcion_menu == "📄 Generar Prueba Desarrollo":
    st.header("📄 Generar Prueba de Desarrollo con Ilustraciones")
    
    temas_seleccion = st.multiselect("Selecciona temas a incluir:", ["Área y Perímetro", "Teorema de Pitágoras", "Razones Trigonométricas", "Guía 2° Medio"], default=["Teorema de Pitágoras", "Guía 2° Medio"])
    nombre_prueba = st.text_input("Nombre de la prueba:", value="Evaluación de Matemáticas — Trigonometría y Triángulos")
    
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
        
        st.success(f"✅ ¡Se generaron {len(prueba_preguntas)} ejercicios con sus esquemas e ilustraciones!")
        c1, c2 = st.columns(2)
        c1.download_button("📥 Descargar PRUEBA (.pdf)", pdf_p, file_name="Prueba_Ilustrada.pdf", mime="application/pdf")
        c2.download_button("📥 Descargar SOLUCIONARIO (.pdf)", pdf_s, file_name="Solucionario_Ilustrado.pdf", mime="application/pdf")

st.divider()
st.caption("💡 Banco de ejercicios v2.0 — Ilustraciones vectoriales amigables")
