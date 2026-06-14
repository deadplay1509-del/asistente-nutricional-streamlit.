import streamlit as st
import reportlab
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import io

# ==========================================
# 📊 FUNCIONADORES Y LÓGICA DE DETRÁS
# ==========================================

def generar_pdf_semanal(plan_semanal, peso_usuario):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=40, bottomMargin=40)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=20, leading=24, textColor=colors.HexColor('#1f77b4'), spaceAfter=15, alignment=1)
    day_style = ParagraphStyle('DayStyle', fontName='Helvetica-Bold', fontSize=12, leading=14, textColor=colors.HexColor('#2c3e50'))
    text_style = ParagraphStyle('TextStyle', fontName='Helvetica', fontSize=9.5, leading=14)
    
    story.append(Paragraph("📅 Plan de Alimentación Semanal Personalizado", title_style))
    story.append(Spacer(1, 10))
    
    data = [[
        Paragraph("<b>Día</b>", ParagraphStyle('H1', fontName='Helvetica-Bold', fontSize=11, textColor=colors.white)), 
        Paragraph("<b>Menú Planificado e Ingredientes</b>", ParagraphStyle('H2', fontName='Helvetica-Bold', fontSize=11, textColor=colors.white))
    ]]
    
    dias_ordenados = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    for dia in dias_ordenados:
        comidas = plan_semanal.get(dia, [])
        if not comidas:
            contenido_dia = "<i>Sin planificar para este día todavía.</i>"
        else:
            detalles_comidas = []
            for c in comidas:
                detalles_comidas.append(f"<b>• {c['nombre']}:</b> {c['detalles']} <font color='#2ecc71'><b>({c['calorias']} kcal)</b></font>")
            contenido_dia = "<br/><br/>".join(detalles_comidas)
            
        data.append([
            Paragraph(f"<b>{dia}</b>", day_style),
            Paragraph(contenido_dia, text_style)
        ])
        
    tabla = Table(data, colWidths=[70, 480])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (1,0), colors.HexColor('#1f77b4')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#bdc3c7')),
        ('BACKGROUND', (0,1), (0,-1), colors.HexColor('#f8f9fa'))
    ]))
    story.append(tabla)
    
    story.append(Spacer(1, 25))
    litros_agua = round((peso_usuario * 35) / 1000, 2)
    gramos_creatina = round(peso_usuario * 0.1, 1)
    
    section_title_style = ParagraphStyle('SecTitle', fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=colors.HexColor('#2c3e50'), spaceAfter=8)
    story.append(Paragraph("💧 Notas de Hidratación y Rendimiento Semanal", section_title_style))
    
    info_style = ParagraphStyle('InfoStyle', fontName='Helvetica', fontSize=10, leading=15)
    texto_rendimiento = (
        f"• <b>Meta de Hidratación Diaria:</b> Consumir un mínimo de <b>{litros_agua} Litros de agua</b> al día distribuidos de manera uniforme.<br/>"
        f"• <b>Suplementación Inteligente (Creatina Monohidratada):</b> Tu dosis diaria exacta es de <b>{gramos_creatina}g</b>. Se debe tomar todos los días (entrenes o no)."
    )
    story.append(Paragraph(texto_rendimiento, info_style))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# ==========================================
# ⚡ CONFIGURACIÓN DE LA INTERFAZ
# ==========================================

st.set_page_config(page_title="MacroFit & Nutrient Planner", page_icon="💪", layout="wide")

if 'plan_semanal' not in st.session_state:
    st.session_state.plan_semanal = {d: [] for d in ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]}

# 🎉 ==========================================
# 👑 BARRA LATERAL (SIDEBAR) & BOTÓN PREMIUM
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3406/3406041.png", width=80) # Icono de usuario/fitness genérico
    st.markdown("### ⚙️ Panel de Cuenta")
    st.write("Versión Actual: **Free Plan**")
    st.markdown("---")
    
    # Caja Premium llamativa
    st.markdown(
        """
        <div style="background-color:#fff3cd; padding:15px; border-radius:10px; border-left: 5px solid #ffc107; margin-bottom:15px;">
            <h4 style="color:#856404; margin:0;">👑 Pásate a Premium</h4>
            <p style="color:#856404; font-size:13px; margin:5px 0 0 0;">
                Desbloquea recetas ilimitadas, escáner de códigos de barras, IA de seguimiento y soporte 1-a-1 con nutricionistas.
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Botón interactivo Premium
    if st.button("🚀 Desbloquear Versión Premium", use_container_width=True, type="primary"):
        st.balloons()
        st.toast("🛒 ¡Abriendo pasarela de pago segura...!", icon="💳")
        st.info("💡 *Nota de simulación: Aquí integrarías la API de Stripe, PayPal o Cashea para procesar la suscripción.*")

st.title("💪 Asistente Nutricional Inteligente")
st.write("Calcula requerimientos con desglose de macros, diseña platos a la medida y exporta tu PDF semanal.")

tab1, tab2, tab3 = st.tabs(["📊 1. Tus Datos y Requerimientos", "🍳 2. Constructor de Platos e Ingredientes", "📅 3. Tu Agenda Semanal y PDF"])

# ---- PESTAÑA 1: DATOS Y DESGLOSE ----
with tab1:
    st.header("Introduce los datos del usuario")
    col1, col2, col3 = st.columns(3)
    with col1:
        user_weight = st.number_input("Peso corporal (kg)", min_value=40.0, max_value=200.0, value=75.0, step=0.1)
        age = st.number_input("Edad", min_value=15, max_value=80, value=25)
    with col2:
        height = st.number_input("Estatura (cm)", min_value=120, max_value=230, value=175)
        gender = st.selectbox("Género", ["Hombre", "Mujer"])
    with col3:
        activity = st.selectbox("Nivel de Actividad", ["Sedentario", "Ligero (1-3 días)", "Moderado (3-5 días)", "Intenso", "Extremo"])
    
    goal = st.radio("Objetivo Nutricional", ["Volumen (Ganar masa muscular)", "Definición (Perder grasa)", "Mantenimiento"])
    
    tmb = (13.4 * user_weight) + (4.8 * height) - (5.7 * age) + (88.36 if gender == "Hombre" else 447.59)
    act_factors = {"Sedentario": 1.2, "Ligero (1-3 días)": 1.375, "Moderado (3-5 días)": 1.55, "Intenso": 1.725, "Extremo": 1.9}
    gasto_total = tmb * act_factors[activity]
    
    if "Volumen" in goal:
        calorias_objetivo = int(gasto_total + 400)
        p_g = 2.0  
        g_g = 1.0  
    elif "Definición" in goal:
        calorias_objetivo = int(gasto_total - 500)
        p_g = 2.3  
        g_g = 0.8  
    else:
        calorias_objetivo = int(gasto_total)
        p_g = 1.8
        g_g = 1.0

    gramos_proteina = int(user_weight * p_g)
    gramos_grasa = int(user_weight * g_g)
    calorias_restantes = calorias_objetivo - ((gramos_proteina * 4) + (gramos_grasa * 9))
    gramos_carbohidratos = int(max(0, calorias_restantes / 4))
    
    st.markdown("---")
    st.subheader("🎯 Tus Requerimientos Diarios Estimados")
    
    c_meta1, c_meta2, c_meta3 = st.columns(3)
    c_meta1.metric(label="🔥 Calorías Meta Diarias", value=f"{calorias_objetivo} kcal")
    c_meta2.metric(label="💧 Agua Mínima", value=f"{round((user_weight * 35) / 1000, 2)} L/día")
    c_meta3.metric(label="💪 Creatina Recomendada", value=f"{round(user_weight * 0.1, 1)} g/día")
    
    st.markdown("#### ⚖️ Distribución Diaria de Macronutrientes")
    col_mac1, col_mac2, col_mac3 = st.columns(3)
    col_mac1.info(f"🍗 **Proteínas:** {gramos_proteina}g al día ({gramos_proteina * 4} kcal)")
    col_mac2.success(f"🌾 **Carbohidratos:** {gramos_carbohidratos}g al día ({gramos_carbohidratos * 4} kcal)")
    col_mac3.warning(f"🥑 **Grasas Saludables:** {gramos_grasa}g al día ({gramos_grasa * 9} kcal)")

# ---- PESTAÑA 2: CONSTRUCTOR CON ALERTAS Y SELECCIÓN MÚLTIPLE ----
with tab2:
    st.header("🔨 Diseñador de Comidas Inteligente")
    
    db_proteinas = {
        "Pollo (Muslo / Pechuga)": {"p": 22.0, "c": 0.0, "g": 3.0, "cal": 115},
        "Carne de Res Magra": {"p": 21.0, "c": 0.0, "g": 6.0, "cal": 140},
        "Sardina en lata": {"p": 20.0, "c": 0.0, "g": 10.0, "cal": 170},
        "Huevo entero (Por Unidad)": {"p": 6.0, "c": 0.0, "g": 5.0, "cal": 70},
        "Queso Blanco Duro / Llanero": {"p": 22.0, "c": 2.0, "g": 24.0, "cal": 310},
        "Requesón / Ricotta": {"p": 12.0, "c": 3.0, "g": 8.0, "cal": 132},
        "Cuajada / Queso Fresco": {"p": 14.0, "c": 2.5, "g": 16.0, "cal": 210},
        "Atún en lata": {"p": 24.0, "c": 0.0, "g": 1.0, "cal": 110},
        "Hígado de Res": {"p": 20.0, "c": 4.0, "g": 4.0, "cal": 132}
    }
    db_granos = {
        "Ninguno": {"p": 0.0, "c": 0.0, "g": 0.0, "cal": 0},
        "Caraotas Negras (Cocidas)": {"p": 9.0, "c": 20.0, "g": 0.5, "cal": 120},
        "Lentejas (Cocidas)": {"p": 9.0, "c": 20.0, "g": 0.4, "cal": 116},
        "Arvejas / Guisantes (Cocidos)": {"p": 8.5, "c": 20.0, "g": 0.4, "cal": 118},
        "Garbanzos (Cocidos)": {"p": 9.0, "c": 27.0, "g": 2.6, "cal": 164}
    }
    db_carbohidratos = {
        "Ninguno": {"p": 0.0, "c": 0.0, "g": 0.0, "cal": 0},
        "Yuca Sancochada": {"p": 1.2, "c": 38.0, "g": 0.3, "cal": 160},
        "Plátano Sancochado": {"p": 1.3, "c": 32.0, "g": 0.4, "cal": 140},
        "Arroz Blanco cocido": {"p": 2.7, "c": 28.0, "g": 0.3, "cal": 130},
        "Pasta de Trigo cocida": {"p": 5.0, "c": 30.0, "g": 0.5, "cal": 150},
        "Papa hervida": {"p": 2.0, "c": 20.0, "g": 0.1, "cal": 87},
        "Avena en hojuelas": {"p": 13.0, "c": 68.0, "g": 7.0, "cal": 390},
        "Arepa Pequeña (1 Ud - aprox 30g harina seca)": {"p": 1.5, "c": 23.0, "g": 0.3, "cal": 100},
        "Arepa Mediana (1 Ud - aprox 50g harina seca)": {"p": 2.5, "c": 38.0, "g": 0.5, "cal": 165},
        "Arepa Grande (1 Ud - aprox 80g harina seca)": {"p": 4.0, "c": 60.0, "g": 0.8, "cal": 260}
    }
    db_vegetales = {
        "Ninguno": {"p": 0.0, "c": 0.0, "g": 0.0, "cal": 0},
        "Ensalada Rallada (Repollo y Zanahoria)": {"p": 1.0, "c": 6.0, "g": 0.2, "cal": 30},
        "Ensalada de Tomate y Cebolla": {"p": 0.8, "c": 5.0, "g": 0.1, "cal": 24},
        "Ensalada Verde (Lechuga y Pepino)": {"p": 0.6, "c": 3.0, "g": 0.1, "cal": 15},
        "Vegetales al Vapor (Zanahoria, Brócoli, Vainitas)": {"p": 1.5, "c": 7.0, "g": 0.2, "cal": 35}
    }
    db_grasas = {
        "Ninguno": {"p": 0.0, "c": 0.0, "g": 0.0, "cal": 0},
        "Maní Tostado natural": {"p": 26.0, "c": 16.0, "g": 49.0, "cal": 570},
        "Aguacate": {"p": 2.0, "c": 9.0, "g": 15.0, "cal": 160},
        "Aceite de Oliva / Vegetal (ml)": {"p": 0.0, "c": 0.0, "g": 100.0, "cal": 884},
        "Suero de Leche Criollo (ml)": {"p": 1.0, "c": 4.0, "g": 12.0, "cal": 130}
    }

    dia_destino = st.selectbox("¿Para qué día de la semana es esta preparación?", ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"])
    tipo_registro = st.radio("¿Qué tipo de comida deseas armar?", ["🍽️ Plato de Comida Completo", "🥤 Batido de Proteínas Personalizado"])
    
    if tipo_registro == "🍽️ Plato de Comida Completo":
        nombre_comida = st.selectbox("Asignar como:", ["Desayuno", "Almuerzo", "Cena"])
        
        cal_sugeridas_comida = int(calorias_objetivo * 0.28 if "Desayuno" in nombre_comida or "Cena" in nombre_comida else calorias_objetivo * 0.34)
        p_sugerida_comida = int(gramos_proteina / 3.5)
        c_sugerida_comida = int(gramos_carbohidratos / 3.5)
        g_sugerida_comida = int(gramos_grasa / 3.5)
        
        st.markdown(f"💡 **Objetivo Sugerido para tu {nombre_comida}:** `{cal_sugeridas_comida} kcal` | 🍗 P: `{p_sugerida_comida}g` | 🌾 C: `{c_sugerida_comida}g` | 🥑 G: `{g_sugerida_comida}g` ")
        st.write("---")

        col_p1, col_p2 = st.columns(2)
        
        t_p, t_c, t_g, t_cal = 0.0, 0.0, 0.0, 0.0
        detalles_lista = []

        with col_p1:
            st.markdown("##### 🍗 Proteínas (Puedes elegir varias)")
            prots_seleccionadas = st.multiselect("Selecciona tus fuentes de proteína:", list(db_proteinas.keys()), default=["Huevo entero (Por Unidad)"])
            
            for p_choice in prots_seleccionadas:
                is_unit = "Por Unidad" in p_choice
                label_slider = f"Cantidad de [{p_choice}] ({'unidades' if is_unit else 'gramos'}):"
                p_amount = st.slider(label_slider, 0, 500, 2 if is_unit else 100, key=f"slider_{p_choice}")
                
                factor = p_amount if is_unit else p_amount / 100.0
                
                t_p += db_proteinas[p_choice]["p"] * factor
                t_c += db_proteinas[p_choice]["c"] * factor
                t_g += db_proteinas[p_choice]["g"] * factor
                t_cal += db_proteinas[p_choice]["cal"] * factor
                
                # 🆕 PUNTO 1: Limpieza estética del nombre comercial eliminando aclaraciones entre paréntesis
                nombre_limpio_p = p_choice.split(" (")[0]
                detalles_lista.append(f"{p_amount}{'uds' if is_unit else 'g'} de {nombre_limpio_p}")

            st.write("") 
            grano_choice = st.selectbox("2. Elige el Tipo de Grano / Legumbre", list(db_granos.keys()))
            grano_amount = st.slider("Cantidad de Granos (g)", 0, 500, 0)
            
            veg_choice = st.selectbox("3. Elige el Tipo de Ensalada / Vegetal", list(db_vegetales.keys()))
            veg_amount = st.slider("Cantidad de Ensalada (g)", 0, 300, 0)
            
        with col_p2:
            st.markdown("##### 🌾 Acompañantes y Grasas")
            carb_choice = st.selectbox("4. Elige el Carbohidrato acompañante", list(db_carbohidratos.keys()))
            
            is_arepa = "Arepa" in carb_choice
            if is_arepa:
                carb_amount = st.slider("Cantidad de Arepas (Unidades):", 0, 5, 1, step=1)
                f_c = float(carb_amount)
                detalles_lista.append(f"{carb_amount} ud(s) de {carb_choice.split(' (')[0]}")
            else:
                carb_amount = st.slider("Cantidad Carbohidrato (g)", 0, 500, 100)
                f_c = carb_amount / 100.0
                if carb_choice != "Ninguno" and carb_amount > 0: 
                    detalles_lista.append(f"{carb_amount}g de {carb_choice.split(' (')[0]}")
            
            gras_choice = st.selectbox("5. Elige la Grasa Saludable (o aderezo)", list(db_grasas.keys()))
            gras_amount = st.slider("Cantidad Grasa (g/ml)", 0, 200, 0)
            
        f_g = grano_amount / 100.0
        f_v = veg_amount / 100.0
        f_gr = gras_amount / 100.0
        
        t_p += (db_granos[grano_choice]["p"] * f_g) + (db_vegetales[veg_choice]["p"] * f_v) + (db_carbohidratos[carb_choice]["p"] * f_c) + (db_grasas[gras_choice]["p"] * f_gr)
        t_c += (db_granos[grano_choice]["c"] * f_g) + (db_vegetales[veg_choice]["c"] * f_v) + (db_carbohidratos[carb_choice]["c"] * f_c) + (db_grasas[gras_choice]["c"] * f_gr)
        t_g += (db_granos[grano_choice]["g"] * f_g) + (db_vegetales[veg_choice]["g"] * f_v) + (db_carbohidratos[carb_choice]["g"] * f_c) + (db_grasas[gras_choice]["g"] * f_gr)
        t_cal += (db_granos[grano_choice]["cal"] * f_g) + (db_vegetales[veg_choice]["cal"] * f_v) + (db_carbohidratos[carb_choice]["cal"] * f_c) + (db_grasas[gras_choice]["cal"] * f_gr)
        
        if grano_choice != "Ninguno" and grano_amount > 0: detalles_lista.append(f"{grano_amount}g de {grano_choice.split(' (')[0]}")
        if veg_choice != "Ninguno" and veg_amount > 0: detalles_lista.append(f"{veg_amount}g de {veg_choice.split(' (')[0]}")
        if gras_choice != "Ninguno" and gras_amount > 0: detalles_lista.append(f"{gras_amount}g/ml de {gras_choice.split(' (')[0]}")
        detalles_texto = " | ".join(detalles_lista)

    else:
        nombre_comida = "Batido / Merienda"
        cal_sugeridas_comida = int(calorias_objetivo * 0.15) 
        st.markdown(f"💡 **Objetivo Sugerido para tu Batido/Merienda:** `{cal_sugeridas_comida} kcal`")
        st.write("---")
        
        db_bases_batido = {
            "Agua": {"p": 0.0, "c": 0.0, "g": 0.0, "cal": 0},
            "Leche Líquida Completa (ml)": {"p": 3.2, "c": 4.8, "g": 3.3, "cal": 62},
            "Leche en Polvo (g)": {"p": 26.0, "c": 38.0, "g": 26.0, "cal": 490}
        }
        db_proteina_batido = {
            "Ninguno": {"p": 0.0, "c": 0.0, "g": 0.0, "cal": 0},
            "Requesón / Ricotta": {"p": 12.0, "c": 3.0, "g": 8.0, "cal": 132},
            "Claras de Huevo (Por Unidad - Sancochadas)": {"p": 3.6, "c": 0.2, "g": 0.0, "cal": 17},
            "Whey Protein (1 Scoop / Suero de Leche)": {"p": 25.0, "c": 2.0, "g": 1.5, "cal": 120}
        }
        db_energia_batido = {
            "Ninguno": {"p": 0.0, "c": 0.0, "g": 0.0, "cal": 0},
            "Avena en hojuelas": {"p": 13.0, "c": 68.0, "g": 7.0, "cal": 390},
            "Cambur / Plátano maduro (Por cada 100g)": {"p": 1.1, "c": 22.0, "g": 0.3, "cal": 89},
            "Maní Tostado (g)": {"p": 26.0, "c": 16.0, "g": 49.0, "cal": 570}
        }
        
        col_b1, col_b2, col_b3 = st.columns(3)
        with col_b1:
            base_b = st.selectbox("Líquido Base", list(db_bases_batido.keys()))
            cant_base = st.slider("Cantidad Base (ml o g)", 0, 500, 250)
        with col_b2:
            prot_b = st.selectbox("Proteína para licuar", list(db_proteina_batido.keys()))
            cant_prot = st.slider("Cantidad Proteína batido", 0, 300, 60 if "Requesón" in prot_b else 1)
        with col_b3:
            ener_b = st.selectbox("Carbohidrato / Extra energético", list(db_energia_batido.keys()))
            cant_ener = st.slider("Cantidad Extra (g)", 0, 200, 50)
            
        f_base = cant_base / 100.0
        f_p_b = cant_prot if "Por Unidad" in prot_b else (1.0 if "Scoop" in prot_b and cant_prot > 0 else cant_prot / 100.0)
        f_e_b = cant_ener / 100.0
        
        t_p = (db_bases_batido[base_b]["p"] * f_base) + (db_proteina_batido[prot_b]["p"] * f_p_b) + (db_energia_batido[ener_b]["p"] * f_e_b)
        t_c = (db_bases_batido[base_b]["c"] * f_base) + (db_proteina_batido[prot_b]["c"] * f_p_b) + (db_energia_batido[ener_b]["c"] * f_e_b)
        t_g = (db_bases_batido[base_b]["g"] * f_base) + (db_proteina_batido[prot_b]["g"] * f_p_b) + (db_energia_batido[ener_b]["g"] * f_e_b)
        t_cal = (db_bases_batido[base_b]["cal"] * f_base) + (db_proteina_batido[prot_b]["cal"] * f_p_b) + (db_energia_batido[ener_b]["cal"] * f_e_b)
        
        detalles_texto = f"{cant_base}ml de {base_b.split(' (')[0]} + {cant_prot}{'uds' if 'Unidad' in prot_b else 'g'} de {prot_b.split(' (')[0]} + {cant_ener}g de {ener_b.split(' (')[0]}"

    st.markdown("#### 🍽️ Aporte Actual de la Preparación:")
    
    c_plat1, c_plat2, c_plat3, c_plat4 = st.columns(4)
    c_plat1.metric(label="🔥 Calorías", value=f"{int(t_cal)} / {cal_sugeridas_comida} kcal")
    c_plat2.write(f"🍗 **Proteína:** {round(t_p, 1)}g")
    c_plat3.write(f"🌾 **Carbohidratos:** {round(t_c, 1)}g")
    c_plat4.write(f"🥑 **Grasas:** {round(t_g, 1)}g")

    if t_cal > cal_sugeridas_comida + 70:
        st.error(f"⚠️ **¡ALERTA DE EXCESO!:** Esta comida suma `{int(t_cal)} kcal`, superando el objetivo sugerido de `{cal_sugeridas_comida} kcal`.")
    elif t_cal < cal_sugeridas_comida - 100 and t_cal > 0:
        st.warning(f"ℹ️ **Bajo el objetivo:** Esta preparación está significativamente por debajo de tu meta para esta comida.")
    else:
        if t_cal > 0: st.success("✅ **¡Perfecto!** La comida está en el rango calórico ideal para tu objetivo.")

    if st.button("💾 Guardar esta preparación en la Agenda Semanal", use_container_width=True):
        # 🆕 PUNTO 2: Ahora guardamos no solo las calorías, sino la estructura completa de macronutrientes para el análisis diario
        nueva_comida = {
            "nombre": nombre_comida,
            "detalles": detalles_texto,
            "calorias": int(t_cal),
            "p": round(t_p, 1),
            "c": round(t_c, 1),
            "g": round(t_g, 1)
        }
        st.session_state.plan_semanal[dia_destino].append(nueva_comida)
        st.success(f"✅ ¡{nombre_comida} agregado exitosamente al {dia_destino}!")

# ---- PESTAÑA 3: AGENDA ----
with tab3:
    st.header("📅 Agenda de Alimentación Semanal")
    
    for dia, comidas in st.session_state.plan_semanal.items():
        with st.expander(f"📅 {dia}"):
            if not comidas:
                st.write("*Sin planificar para este día todavía.*")
            else:
                # Inicializamos acumuladores diarios para el reporte avanzado
                total_cal_dia = 0
                total_p_dia = 0.0
                total_c_dia = 0.0
                total_g_dia = 0.0
                
                for c in comidas:
                    st.write(f"**{c['nombre']}:** {c['detalles']} — `{c['calorias']} kcal`")
                    total_cal_dia += c['calorias']
                    # Sumamos los macros guardados (usamos .get() por compatibilidad si había registros viejos)
                    total_p_dia += c.get("p", 0.0)
                    total_c_dia += c.get("c", 0.0)
                    total_g_dia += c.get("g", 0.0)
                
                st.write("---")
                # 🆕 Interfaz Profesional: Desglose en tiempo real del cumplimiento de macros del día completo
                col_m1, col_m2, col_m3, col_m4 = st.columns(4)
                col_m1.markdown(f"**🔥 Energía:** `{total_cal_dia} / {calorias_objetivo} kcal`")
                col_m2.markdown(f"🍗 **Proteína:** `{round(total_p_dia, 1)} / {gramos_proteina}g`")
                col_m3.markdown(f"🌾 **Carbos:** `{round(total_c_dia, 1)} / {gramos_carbohidratos}g`")
                col_m4.markdown(f"🥑 **Grasas:** `{round(total_g_dia, 1)} / {gramos_grasa}g`")
                
                if total_cal_dia > calorias_objetivo + 100:
                    st.error(f"🚨 **{dia} excede el total diario de energía permitido.**")
                elif total_cal_dia > 0 and total_cal_dia >= calorias_objetivo - 100:
                    st.success(f"🎯 ¡Objetivos nutricionales del {dia} completados a nivel profesional!")
                
    st.markdown("---")
    st.subheader("🖨️ Exportación Oficial")
    
    if st.button("🗑️ Vaciar Agenda Semanal (Reiniciar todo)"):
        st.session_state.plan_semanal = {d: [] for d in ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]}
        st.rerun()
        
    pdf_semana = generar_pdf_semanal(st.session_state.plan_semanal, user_weight)
    
    st.download_button(
        label="📥 Descargar plan_nutricional_semanal.pdf (PDF Profesional)",
        data=pdf_semana,
        file_name="plan_nutricional_semanal.pdf",
        mime="application/pdf",
        use_container_width=True
    )
