import dearpygui.dearpygui as dpg

dpg.create_context()

# --- PALETA DE COLORES ---
COLOR_FONDO = (2, 48, 71, 255)       # #023047
COLOR_DISPLAY = (255, 255, 255, 255) # Blanco puro
COLOR_NUMEROS = (33, 158, 188, 255)  # #219EBC
COLOR_OPERADOR = (255, 183, 3, 255)  # #FFB703
COLOR_ACCION = (251, 133, 0, 255)    # #FB8500
COLOR_TEXTO_OSCURO = (2, 48, 71, 255)
COLOR_TEXTO_BLANCO = (255, 255, 255, 255)

expresion = [""]

def presionar_boton(sender, app_data, user_data):
    texto = user_data
    if texto == "C":
        expresion[0] = ""
    elif texto == "=":
        try:
            resultado = eval(expresion[0])
            if isinstance(resultado, float) and resultado.is_integer():
                resultado = int(resultado)
            expresion[0] = str(resultado)
        except Exception:
            expresion[0] = "Error"
    else:
        if expresion[0] == "Error":
            expresion[0] = ""
        expresion[0] += texto

    dpg.set_value("pantalla_display", expresion[0])

# --- CONSTRUCCIÓN DE LA INTERFAZ ---
with dpg.window(tag="VentanaPrincipal", no_title_bar=True, no_resize=True, no_move=True):
    
    # Fila superior: Display + Botón de Información (?)
    with dpg.group(horizontal=True):
        dpg.add_input_text(
            tag="pantalla_display",
            readonly=True,
            width=238,
            multiline=False
        )
        
        # Botón '?' de información
        btn_info = dpg.add_button(label="?", width=36, height=52, tag="btn_info_popup")
        
        with dpg.popup(btn_info, mousebutton=dpg.mvMouseButton_Left):
            dpg.add_text(" Información", color=COLOR_OPERADOR)
            dpg.add_separator()
            dpg.add_text("Librería: Dear PyGui")
            dpg.add_text("Autor: Jaquelin Cielo V.")

    # Reducimos el espacio entre el display y la botonera
    dpg.add_spacer(height=3)

    # Distribución de botones
    botones_grid = [
        ["C", "(", ")", "/"],
        ["7", "8", "9", "*"],
        ["4", "5", "6", "-"],
        ["1", "2", "3", "+"],
        ["0", ".", "="]
    ]

    for fila in botones_grid:
        with dpg.group(horizontal=True):
            for item in fila:
                ancho = 136 if item == "0" else 65
                tag_btn = f"btn_{item}"
                if item in ["(", ")"]:
                    tag_btn = f"btn_par_{item}"

                dpg.add_button(
                    label=item,
                    width=ancho,
                    height=48,
                    callback=presionar_boton,
                    user_data=item,
                    tag=tag_btn
                )

# --- CONFIGURACIÓN DE ESTILOS Y TEMAS ---
with dpg.theme() as tema_global:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, COLOR_FONDO)
        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 15, 15)
        dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 8, 6) # Espaciado vertical más compacto
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 6)

# Estilo para el Display (más alto y centrado)
with dpg.theme() as tema_display:
    with dpg.theme_component(dpg.mvInputText):
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, COLOR_DISPLAY)
        dpg.add_theme_color(dpg.mvThemeCol_Text, COLOR_TEXTO_OSCURO)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 6)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 15)  # Mayor relleno vertical para más altura

# Estilo para el botón '?'
with dpg.theme() as tema_btn_info:
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button, COLOR_OPERADOR)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (255, 200, 50, 255))
        dpg.add_theme_color(dpg.mvThemeCol_Text, COLOR_TEXTO_OSCURO)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 6)

dpg.bind_item_theme("pantalla_display", tema_display)
dpg.bind_item_theme("btn_info_popup", tema_btn_info)

# Colores para la botonera
for fila in botones_grid:
    for item in fila:
        tag_btn = f"btn_{item}"
        if item in ["(", ")"]:
            tag_btn = f"btn_par_{item}"

        with dpg.theme() as tema_btn:
            with dpg.theme_component(dpg.mvButton):
                if item in ["C", "="]:
                    color = COLOR_ACCION
                    texto_color = COLOR_TEXTO_BLANCO
                elif item in ["(", ")", "/", "*", "-", "+"]:
                    color = COLOR_OPERADOR
                    texto_color = COLOR_TEXTO_OSCURO
                else:
                    color = COLOR_NUMEROS
                    texto_color = COLOR_TEXTO_BLANCO

                dpg.add_theme_color(dpg.mvThemeCol_Button, color)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (min(255, color[0]+20), min(255, color[1]+20), min(255, color[2]+20), 255))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (max(0, color[0]-20), max(0, color[1]-20), max(0, color[2]-20), 255))
                dpg.add_theme_color(dpg.mvThemeCol_Text, texto_color)
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 6)

        dpg.bind_item_theme(tag_btn, tema_btn)

dpg.bind_theme(tema_global)

# --- CONFIGURACIÓN DE VENTANA Y VIEWPORT ---
ANCHO_VENTANA = 325
ALTO_VENTANA = 415

dpg.create_viewport(
    title="Calculadora - Dear PyGui",
    width=ANCHO_VENTANA,
    height=ALTO_VENTANA,
    min_width=ANCHO_VENTANA,
    max_width=ANCHO_VENTANA,
    min_height=ALTO_VENTANA,
    max_height=ALTO_VENTANA,
    resizable=False
)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("VentanaPrincipal", True)
dpg.start_dearpygui()
dpg.destroy_context()