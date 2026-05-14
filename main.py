# =============================================================================
# main.py
# Punto de entrada de la aplicación.
# Une la ventana de búsqueda y el formulario en una interfaz con pestañas.
# =============================================================================

import tkinter as tk
from tkinter import ttk

from interfaz.busqueda import VentanaBusqueda
from interfaz.formulario import VentanaFormulario
from interfaz.pruebas import VentanaPruebas

# =============================================================================
# PALETA DE COLORES (coherente con el resto del proyecto)
# =============================================================================
COLOR_FONDO       = "#1E1E2E"
COLOR_PANEL       = "#2A2A3E"
COLOR_BORDE       = "#3A3A5C"
COLOR_ACENTO      = "#7C6AF7"
COLOR_TEXTO       = "#CDD6F4"
COLOR_TEXTO_SUAVE = "#6E6E9A"
COLOR_EXITO       = "#A6E3A1"

FONT_TITULO  = ("Georgia", 14, "bold")
FONT_PEQUEÑO = ("Courier New", 9)


# =============================================================================
# CLASE PRINCIPAL DE LA APLICACIÓN
# =============================================================================

class Aplicacion(tk.Tk):
    """
    Ventana principal de la aplicación.
    Contiene un Notebook (pestañas) con:
      - Pestaña 1: Búsqueda de patrones en textos
      - Pestaña 2: Formulario con validación en tiempo real
    """

    def __init__(self):
        super().__init__()
        self._configurar_ventana()
        self._aplicar_estilos()
        self._construir_interfaz()

    # -------------------------------------------------------------------------
    # CONFIGURACIÓN INICIAL
    # -------------------------------------------------------------------------

    def _configurar_ventana(self):
        """Propiedades de la ventana principal."""
        self.title("Buscador y Validador de Patrones")
        self.geometry("1080x720")
        self.minsize(860, 600)
        self.configure(bg=COLOR_FONDO)

        # Icono de la barra de tareas (texto alternativo si no hay .ico)
        try:
            self.iconbitmap("icono.ico")
        except Exception:
            pass

        # Centrar la ventana en la pantalla al iniciar
        self.update_idletasks()
        ancho  = self.winfo_width()
        alto   = self.winfo_height()
        x      = (self.winfo_screenwidth()  // 2) - (ancho // 2)
        y      = (self.winfo_screenheight() // 2) - (alto  // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def _aplicar_estilos(self):
        """Aplica estilos ttk personalizados para las pestañas."""
        estilo = ttk.Style(self)

        # Usar tema base neutro
        estilo.theme_use("default")

        # Estilo del Notebook (contenedor de pestañas)
        estilo.configure(
            "App.TNotebook",
            background=COLOR_FONDO,
            borderwidth=0,
            tabmargins=[0, 0, 0, 0],
        )

        # Estilo de cada pestaña
        estilo.configure(
            "App.TNotebook.Tab",
            background=COLOR_PANEL,
            foreground=COLOR_TEXTO_SUAVE,
            font=("Courier New", 10, "bold"),
            padding=[20, 10],
            borderwidth=0,
        )

        # Pestaña activa
        estilo.map(
            "App.TNotebook.Tab",
            background=[("selected", COLOR_ACENTO),   ("active", COLOR_BORDE)],
            foreground=[("selected", "#FFFFFF"),       ("active", COLOR_TEXTO)],
            expand    =[("selected", [0, 0, 0, 2])],
        )

    # -------------------------------------------------------------------------
    # CONSTRUCCIÓN DE LA INTERFAZ
    # -------------------------------------------------------------------------

    def _construir_interfaz(self):
        """Ensambla la barra superior, el notebook y la barra inferior."""
        self._crear_barra_superior()
        self._crear_notebook()
        self._crear_barra_inferior()

    def _crear_barra_superior(self):
        """Barra de título personalizada en la parte superior."""
        barra = tk.Frame(self, bg=COLOR_PANEL, pady=12)
        barra.pack(fill="x")

        # Título e ícono
        tk.Label(
            barra,
            text="⬡  Buscador y Validador de Patrones",
            font=FONT_TITULO,
            bg=COLOR_PANEL,
            fg=COLOR_ACENTO,
            padx=20,
        ).pack(side="left")

        # Versión a la derecha
        tk.Label(
            barra,
            text="v1.0  ·  Teoría de Lenguajes Formales",
            font=FONT_PEQUEÑO,
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO_SUAVE,
            padx=20,
        ).pack(side="right")

        # Línea separadora
        tk.Frame(self, bg=COLOR_ACENTO, height=2).pack(fill="x")

    def _crear_notebook(self):
        """Crea el notebook con las dos pestañas principales."""
        self.notebook = ttk.Notebook(self, style="App.TNotebook")
        self.notebook.pack(fill="both", expand=True)

        # --- Pestaña 1: Búsqueda de patrones ---
        self.tab_busqueda = VentanaBusqueda(self.notebook)
        self.notebook.add(
            self.tab_busqueda,
            text="  🔍  Búsqueda en Textos  "
        )

        # --- Pestaña 2: Formulario ---
        self.tab_formulario = VentanaFormulario(self.notebook)
        self.notebook.add(
            self.tab_formulario,
            text="  📋  Formulario de Registro  "
        )

        # --- Pestaña 3: Casos de prueba ---
        self.tab_pruebas = VentanaPruebas(self.notebook)
        self.notebook.add(
            self.tab_pruebas,
            text="  🧪  Casos de Prueba  "
        )

        # Evento al cambiar de pestaña
        self.notebook.bind("<<NotebookTabChanged>>", self._al_cambiar_pestana)

    def _crear_barra_inferior(self):
        """Barra de estado en la parte inferior."""
        tk.Frame(self, bg=COLOR_BORDE, height=1).pack(fill="x")

        barra = tk.Frame(self, bg=COLOR_FONDO, pady=5)
        barra.pack(fill="x", padx=16)

        self.label_pestana = tk.Label(
            barra,
            text="📌  Pestaña activa: Búsqueda en Textos",
            font=FONT_PEQUEÑO,
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO_SUAVE,
            anchor="w",
        )
        self.label_pestana.pack(side="left")

        tk.Label(
            barra,
            text="Python · tkinter · sin librería re",
            font=FONT_PEQUEÑO,
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO_SUAVE,
            anchor="e",
        ).pack(side="right")

    # -------------------------------------------------------------------------
    # EVENTOS
    # -------------------------------------------------------------------------

    def _al_cambiar_pestana(self, event):
        """Actualiza la barra inferior al cambiar de pestaña."""
        indice = self.notebook.index("current")
        nombres = {
            0: "Búsqueda en Textos",
            1: "Formulario de Registro",
            2: "Casos de Prueba",
        }
        nombre = nombres.get(indice, "")
        self.label_pestana.config(
            text=f"📌  Pestaña activa: {nombre}",
            fg=COLOR_EXITO,
        )
        # Volver al color suave después de 2 segundos
        self.after(2000, lambda: self.label_pestana.config(fg=COLOR_TEXTO_SUAVE))


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================
def main():
    app = Aplicacion()
    app.mainloop()


if __name__ == "__main__":
    main()
