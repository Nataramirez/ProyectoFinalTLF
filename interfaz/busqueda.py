# =============================================================================
# ventana_busqueda.py
# Interfaz gráfica para búsqueda de patrones en textos
# Usa tkinter — sin librerías externas adicionales
# =============================================================================

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from patrones import PATRONES, buscar_con_patron, buscar_todos

# =============================================================================
# PALETA DE COLORES Y ESTILOS
# =============================================================================
COLOR_FONDO         = "#1E1E2E"   # fondo principal oscuro
COLOR_PANEL         = "#2A2A3E"   # paneles secundarios
COLOR_BORDE         = "#3A3A5C"   # bordes y separadores
COLOR_ACENTO        = "#7C6AF7"   # morado principal
COLOR_ACENTO_HOVER  = "#9B8FF9"   # morado claro hover
COLOR_TEXTO         = "#CDD6F4"   # texto principal claro
COLOR_TEXTO_SUAVE   = "#6E6E9A"   # texto secundario
COLOR_EXITO         = "#A6E3A1"   # verde para resultados
COLOR_ERROR         = "#F38BA8"   # rojo para errores
COLOR_ADVERTENCIA   = "#FAB387"   # naranja para advertencias
COLOR_RESALTADO     = "#F9E2AF"   # amarillo para resaltar coincidencias

FONT_TITULO   = ("Georgia", 18, "bold")
FONT_SUBTITULO= ("Georgia", 11, "italic")
FONT_NORMAL   = ("Courier New", 10)
FONT_BOLD     = ("Courier New", 10, "bold")
FONT_BOTON    = ("Courier New", 10, "bold")
FONT_PEQUEÑO  = ("Courier New", 9)


# =============================================================================
# CLASE PRINCIPAL DE LA VENTANA DE BÚSQUEDA
# =============================================================================

class VentanaBusqueda(tk.Frame):
    """
    Frame que contiene toda la interfaz de búsqueda de patrones en texto.
    Puede usarse como ventana independiente o como pestaña dentro de un notebook.
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, bg=COLOR_FONDO, **kwargs)
        self.patron_seleccionado = tk.StringVar(value="todos")
        self._construir_interfaz()

    # -------------------------------------------------------------------------
    # CONSTRUCCIÓN DE LA INTERFAZ
    # -------------------------------------------------------------------------

    def _construir_interfaz(self):
        """Ensambla todos los componentes de la ventana."""
        self._crear_encabezado()
        self._crear_area_principal()
        self._crear_barra_estado()

    def _crear_encabezado(self):
        """Encabezado con título y descripción."""
        frame = tk.Frame(self, bg=COLOR_FONDO, pady=16)
        frame.pack(fill="x", padx=24)

        tk.Label(
            frame,
            text="🔍  Buscador de Patrones",
            font=FONT_TITULO,
            bg=COLOR_FONDO,
            fg=COLOR_ACENTO,
        ).pack(anchor="w")

        tk.Label(
            frame,
            text="Pega o escribe un texto y detecta patrones automáticamente",
            font=FONT_SUBTITULO,
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO_SUAVE,
        ).pack(anchor="w")

        # Línea separadora
        tk.Frame(self, bg=COLOR_BORDE, height=1).pack(fill="x", padx=24)

    def _crear_area_principal(self):
        """Área principal dividida en panel izquierdo (entrada) y derecho (resultados)."""
        contenedor = tk.Frame(self, bg=COLOR_FONDO)
        contenedor.pack(fill="both", expand=True, padx=24, pady=16)

        contenedor.columnconfigure(0, weight=3)
        contenedor.columnconfigure(1, weight=2)
        contenedor.rowconfigure(0, weight=1)

        self._crear_panel_entrada(contenedor)
        self._crear_panel_resultados(contenedor)

    def _crear_panel_entrada(self, parent):
        """Panel izquierdo: área de texto + controles."""
        frame = tk.Frame(parent, bg=COLOR_PANEL, bd=0, relief="flat")
        frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # --- Título del panel ---
        tk.Label(
            frame,
            text="TEXTO DE ENTRADA",
            font=FONT_BOLD,
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO_SUAVE,
            pady=10,
            padx=14,
            anchor="w",
        ).pack(fill="x")

        tk.Frame(frame, bg=COLOR_BORDE, height=1).pack(fill="x")

        # --- Área de texto ---
        self.area_texto = scrolledtext.ScrolledText(
            frame,
            font=FONT_NORMAL,
            bg="#252535",
            fg=COLOR_TEXTO,
            insertbackground=COLOR_ACENTO,
            selectbackground=COLOR_ACENTO,
            selectforeground="#FFFFFF",
            relief="flat",
            padx=12,
            pady=12,
            wrap="word",
            height=18,
        )
        self.area_texto.pack(fill="both", expand=True, padx=2, pady=2)

        # Texto de ayuda inicial
        self.area_texto.insert("1.0",
            "Pega aquí el texto que deseas analizar...\n\n"
            "Ejemplo:\n"
            "  Escríbeme a correo@ejemplo.com o llama al 3001234567\n"
            "  Visita https://www.pagina.com el día 06/05/2026\n"
            "  Cédula: 1098765432 · Placa: ABC-123"
        )
        self.area_texto.config(fg=COLOR_TEXTO_SUAVE)
        self.area_texto.bind("<FocusIn>", self._limpiar_placeholder)

        # --- Selector de patrón ---
        frame_selector = tk.Frame(frame, bg=COLOR_PANEL, pady=10, padx=12)
        frame_selector.pack(fill="x")

        tk.Label(
            frame_selector,
            text="Buscar:",
            font=FONT_BOLD,
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
        ).pack(side="left")

        opciones = [("Todos los patrones", "todos")] + [
            (p["nombre"], p["id"]) for p in PATRONES
        ]

        for texto_opcion, valor in opciones:
            tk.Radiobutton(
                frame_selector,
                text=texto_opcion,
                variable=self.patron_seleccionado,
                value=valor,
                font=FONT_PEQUEÑO,
                bg=COLOR_PANEL,
                fg=COLOR_TEXTO,
                selectcolor=COLOR_ACENTO,
                activebackground=COLOR_PANEL,
                activeforeground=COLOR_ACENTO_HOVER,
                cursor="hand2",
            ).pack(side="left", padx=6)

        # --- Botones de acción ---
        frame_botones = tk.Frame(frame, bg=COLOR_PANEL, pady=10, padx=12)
        frame_botones.pack(fill="x")

        self._boton(frame_botones, "▶  Buscar patrones", self._ejecutar_busqueda,
                    COLOR_ACENTO, "#FFFFFF").pack(side="left", padx=(0, 8))

        self._boton(frame_botones, "📂  Cargar archivo .txt", self._cargar_archivo,
                    COLOR_PANEL, COLOR_TEXTO, borde=COLOR_BORDE).pack(side="left", padx=(0, 8))

        self._boton(frame_botones, "🗑  Limpiar", self._limpiar_todo,
                    COLOR_PANEL, COLOR_ERROR, borde=COLOR_ERROR).pack(side="left")

    def _crear_panel_resultados(self, parent):
        """Panel derecho: lista de resultados por categoría."""
        frame = tk.Frame(parent, bg=COLOR_PANEL, bd=0)
        frame.grid(row=0, column=1, sticky="nsew")

        tk.Label(
            frame,
            text="RESULTADOS",
            font=FONT_BOLD,
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO_SUAVE,
            pady=10,
            padx=14,
            anchor="w",
        ).pack(fill="x")

        tk.Frame(frame, bg=COLOR_BORDE, height=1).pack(fill="x")

        # Área scrollable de resultados
        self.area_resultados = scrolledtext.ScrolledText(
            frame,
            font=FONT_NORMAL,
            bg="#252535",
            fg=COLOR_TEXTO,
            relief="flat",
            padx=12,
            pady=12,
            wrap="word",
            state="disabled",
            height=22,
        )
        self.area_resultados.pack(fill="both", expand=True, padx=2, pady=2)

        # Configurar etiquetas de color para el texto de resultados
        self.area_resultados.tag_config("titulo",    foreground=COLOR_ACENTO,      font=FONT_BOLD)
        self.area_resultados.tag_config("exito",     foreground=COLOR_EXITO,       font=FONT_NORMAL)
        self.area_resultados.tag_config("vacio",     foreground=COLOR_TEXTO_SUAVE, font=FONT_PEQUEÑO)
        self.area_resultados.tag_config("resumen",   foreground=COLOR_ADVERTENCIA, font=FONT_BOLD)
        self.area_resultados.tag_config("separador", foreground=COLOR_BORDE,       font=FONT_PEQUEÑO)

        # --- Contador de resultados ---
        self.label_conteo = tk.Label(
            frame,
            text="Sin búsquedas aún",
            font=FONT_PEQUEÑO,
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO_SUAVE,
            pady=8,
            padx=12,
            anchor="w",
        )
        self.label_conteo.pack(fill="x")

    def _crear_barra_estado(self):
        """Barra inferior con estado actual."""
        tk.Frame(self, bg=COLOR_BORDE, height=1).pack(fill="x")
        frame = tk.Frame(self, bg=COLOR_FONDO, pady=6)
        frame.pack(fill="x", padx=24)

        self.label_estado = tk.Label(
            frame,
            text="⬤  Listo",
            font=FONT_PEQUEÑO,
            bg=COLOR_FONDO,
            fg=COLOR_EXITO,
            anchor="w",
        )
        self.label_estado.pack(side="left")

    # -------------------------------------------------------------------------
    # LÓGICA DE BÚSQUEDA
    # -------------------------------------------------------------------------

    def _ejecutar_busqueda(self):
        """Obtiene el texto, ejecuta la búsqueda y muestra los resultados."""
        texto = self.area_texto.get("1.0", "end-1c").strip()

        if not texto or texto.startswith("Pega aquí"):
            messagebox.showwarning("Sin texto", "Por favor ingresa o carga un texto para analizar.")
            return

        self._actualizar_estado("⬤  Buscando...", COLOR_ADVERTENCIA)
        self.update_idletasks()

        patron_id = self.patron_seleccionado.get()

        # Ejecutar búsqueda según selección
        if patron_id == "todos":
            resultados = buscar_todos(texto)
        else:
            encontrados = buscar_con_patron(patron_id, texto)
            resultados = {patron_id: encontrados}

        self._mostrar_resultados(resultados, texto)
        self._resaltar_en_texto(resultados)
        self._actualizar_estado("⬤  Búsqueda completada", COLOR_EXITO)

    def _mostrar_resultados(self, resultados, texto_original):
        """Escribe los resultados en el panel derecho con formato y colores."""
        self.area_resultados.config(state="normal")
        self.area_resultados.delete("1.0", "end")

        total = 0

        for categoria, encontrados in resultados.items():
            # Buscar nombre legible de la categoría
            nombre_cat = categoria.upper()
            for p in PATRONES:
                if p["id"] == categoria:
                    nombre_cat = p["nombre"].upper()
                    break

            self.area_resultados.insert("end", f"\n▌ {nombre_cat}\n", "titulo")
            self.area_resultados.insert("end", "─" * 32 + "\n", "separador")

            if encontrados:
                for item in encontrados:
                    self.area_resultados.insert("end", f"  ✔  {item}\n", "exito")
                    total += 1
            else:
                self.area_resultados.insert("end", "  (ninguno encontrado)\n", "vacio")

        self.area_resultados.insert("end", f"\n{'─'*32}\n", "separador")
        self.area_resultados.insert("end", f"  Total encontrado: {total} coincidencia(s)\n", "resumen")

        self.area_resultados.config(state="disabled")
        self.label_conteo.config(
            text=f"{total} coincidencia(s) encontrada(s)",
            fg=COLOR_EXITO if total > 0 else COLOR_TEXTO_SUAVE
        )

    def _resaltar_en_texto(self, resultados):
        """Resalta visualmente las coincidencias dentro del área de texto."""
        # Quitar resaltados previos
        self.area_texto.tag_remove("resaltado", "1.0", "end")
        self.area_texto.tag_config("resaltado", background=COLOR_RESALTADO, foreground="#1E1E2E")

        texto = self.area_texto.get("1.0", "end-1c")

        for _, encontrados in resultados.items():
            for item in encontrados:
                inicio = 0
                while True:
                    pos = texto.find(item, inicio)
                    if pos == -1:
                        break
                    # Convertir posición absoluta a índice tkinter (línea.columna)
                    linea = texto[:pos].count('\n') + 1
                    col   = pos - texto[:pos].rfind('\n') - 1
                    idx_inicio = f"{linea}.{col}"
                    idx_fin    = f"{linea}.{col + len(item)}"
                    self.area_texto.tag_add("resaltado", idx_inicio, idx_fin)
                    inicio = pos + 1

    # -------------------------------------------------------------------------
    # ACCIONES AUXILIARES
    # -------------------------------------------------------------------------

    def _cargar_archivo(self):
        """Abre un diálogo para cargar un archivo .txt en el área de texto."""
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo de texto",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if ruta:
            try:
                with open(ruta, "r", encoding="utf-8") as f:
                    contenido = f.read()
                self.area_texto.config(fg=COLOR_TEXTO)
                self.area_texto.delete("1.0", "end")
                self.area_texto.insert("1.0", contenido)
                self._actualizar_estado(f"⬤  Archivo cargado: {ruta.split('/')[-1]}", COLOR_EXITO)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{e}")

    def _limpiar_todo(self):
        """Limpia el área de texto y los resultados."""
        self.area_texto.config(fg=COLOR_TEXTO_SUAVE)
        self.area_texto.delete("1.0", "end")
        self.area_texto.insert("1.0",
            "Pega aquí el texto que deseas analizar...\n\n"
            "Ejemplo:\n"
            "  Escríbeme a correo@ejemplo.com o llama al 3001234567\n"
            "  Visita https://www.pagina.com el día 06/05/2026\n"
            "  Cédula: 1098765432 · Placa: ABC-123"
        )
        self.area_resultados.config(state="normal")
        self.area_resultados.delete("1.0", "end")
        self.area_resultados.config(state="disabled")
        self.label_conteo.config(text="Sin búsquedas aún", fg=COLOR_TEXTO_SUAVE)
        self._actualizar_estado("⬤  Listo", COLOR_EXITO)

    def _limpiar_placeholder(self, event):
        """Limpia el texto de ayuda cuando el usuario hace clic en el área."""
        contenido = self.area_texto.get("1.0", "end-1c")
        if contenido.startswith("Pega aquí"):
            self.area_texto.delete("1.0", "end")
            self.area_texto.config(fg=COLOR_TEXTO)

    def _actualizar_estado(self, mensaje, color):
        """Actualiza el mensaje de la barra de estado."""
        self.label_estado.config(text=mensaje, fg=color)

    # -------------------------------------------------------------------------
    # UTILIDAD: crear botón estilizado
    # -------------------------------------------------------------------------

    def _boton(self, parent, texto, comando, bg, fg, borde=None):
        """Crea y retorna un botón con el estilo del proyecto."""
        btn = tk.Button(
            parent,
            text=texto,
            command=comando,
            font=FONT_BOTON,
            bg=bg,
            fg=fg,
            relief="flat",
            padx=14,
            pady=6,
            cursor="hand2",
            activebackground=COLOR_ACENTO_HOVER,
            activeforeground="#FFFFFF",
            bd=1 if borde else 0,
            highlightbackground=borde or bg,
            highlightthickness=1 if borde else 0,
        )
        btn.bind("<Enter>", lambda e: btn.config(bg=COLOR_ACENTO_HOVER if bg == COLOR_ACENTO else COLOR_BORDE))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        return btn


# =============================================================================
# EJECUCIÓN INDEPENDIENTE
# =============================================================================

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Buscador de Patrones")
    root.geometry("1000x680")
    root.configure(bg=COLOR_FONDO)
    root.resizable(True, True)

    app = VentanaBusqueda(root)
    app.pack(fill="both", expand=True)

    root.mainloop()