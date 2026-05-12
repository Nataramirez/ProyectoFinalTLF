import tkinter as tk
from tkinter import scrolledtext
from patrones import PATRONES

COLOR_FONDO        = "#1E1E2E"
COLOR_PANEL        = "#2A2A3E"
COLOR_BORDE        = "#3A3A5C"
COLOR_ACENTO       = "#7C6AF7"
COLOR_ACENTO_HOVER = "#9B8FF9"
COLOR_TEXTO        = "#CDD6F4"
COLOR_TEXTO_SUAVE  = "#6E6E9A"
COLOR_EXITO        = "#A6E3A1"
COLOR_ERROR        = "#F38BA8"
COLOR_ADVERTENCIA  = "#FAB387"

FONT_TITULO    = ("Georgia", 18, "bold")
FONT_SUBTITULO = ("Georgia", 11, "italic")
FONT_NORMAL    = ("Courier New", 10)
FONT_BOLD      = ("Courier New", 10, "bold")
FONT_BOTON     = ("Courier New", 10, "bold")
FONT_PEQUEÑO   = ("Courier New", 9)


class VentanaPruebas(tk.Frame):
    """
    Pestaña que ejecuta y muestra los casos de prueba de todos los patrones.
    Muestra ejemplos válidos e inválidos con resultado OK o FALLO en colores.
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, bg=COLOR_FONDO, **kwargs)
        self._construir_interfaz()
        self._ejecutar_pruebas()

    def _construir_interfaz(self):
        self._crear_encabezado()
        self._crear_area_resultados()
        self._crear_barra_estado()

    def _crear_encabezado(self):
        frame = tk.Frame(self, bg=COLOR_FONDO, pady=16)
        frame.pack(fill="x", padx=24)

        tk.Label(
            frame,
            text="🧪  Casos de Prueba",
            font=FONT_TITULO,
            bg=COLOR_FONDO,
            fg=COLOR_ACENTO,
        ).pack(anchor="w")

        tk.Label(
            frame,
            text="Verificación automática de todos los patrones con ejemplos válidos e inválidos",
            font=FONT_SUBTITULO,
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO_SUAVE,
        ).pack(anchor="w")

        tk.Frame(self, bg=COLOR_BORDE, height=1).pack(fill="x", padx=24)

        frame_btn = tk.Frame(self, bg=COLOR_FONDO, pady=10)
        frame_btn.pack(fill="x", padx=24)

        btn = tk.Button(
            frame_btn,
            text="▶  Re-ejecutar pruebas",
            command=self._ejecutar_pruebas,
            font=FONT_BOTON,
            bg=COLOR_ACENTO,
            fg="#FFFFFF",
            relief="flat",
            padx=14,
            pady=6,
            cursor="hand2",
            activebackground=COLOR_ACENTO_HOVER,
            activeforeground="#FFFFFF",
        )
        btn.bind("<Enter>", lambda e: btn.config(bg=COLOR_ACENTO_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=COLOR_ACENTO))
        btn.pack(side="left")

    def _crear_area_resultados(self):
        frame = tk.Frame(self, bg=COLOR_PANEL)
        frame.pack(fill="both", expand=True, padx=24, pady=(0, 8))

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

        self.area = scrolledtext.ScrolledText(
            frame,
            font=FONT_NORMAL,
            bg="#252535",
            fg=COLOR_TEXTO,
            relief="flat",
            padx=14,
            pady=12,
            wrap="word",
            state="disabled",
        )
        self.area.pack(fill="both", expand=True, padx=2, pady=2)

        self.area.tag_config("titulo",    foreground=COLOR_ACENTO,     font=FONT_BOLD)
        self.area.tag_config("subtitulo", foreground=COLOR_TEXTO_SUAVE, font=FONT_PEQUEÑO)
        self.area.tag_config("ok",        foreground=COLOR_EXITO,       font=FONT_NORMAL)
        self.area.tag_config("fallo",     foreground=COLOR_ERROR,        font=FONT_NORMAL)
        self.area.tag_config("resumen",   foreground=COLOR_ADVERTENCIA,  font=FONT_BOLD)
        self.area.tag_config("separador", foreground=COLOR_BORDE,        font=FONT_PEQUEÑO)

    def _crear_barra_estado(self):
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

        self.label_score = tk.Label(
            frame,
            text="",
            font=FONT_BOLD,
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO_SUAVE,
            anchor="e",
        )
        self.label_score.pack(side="right")

    def _ejecutar_pruebas(self):
        self.area.config(state="normal")
        self.area.delete("1.0", "end")

        total = 0
        exitosos = 0

        for patron in PATRONES:
            self.area.insert("end", f"\n▌ {patron['nombre'].upper()}\n", "titulo")
            self.area.insert("end", f"   Formato esperado: {patron['formato']}\n", "subtitulo")
            self.area.insert("end", "─" * 52 + "\n", "separador")

            for ejemplo in patron["ejemplos_ok"]:
                total += 1
                resultado = patron["validar"](ejemplo)
                if resultado:
                    exitosos += 1
                    self.area.insert("end", f"   ✅ OK     [esperado: VÁLIDO  ] → {ejemplo}\n", "ok")
                else:
                    self.area.insert("end", f"   ❌ FALLO  [esperado: VÁLIDO  ] → {ejemplo}\n", "fallo")

            for ejemplo in patron["ejemplos_mal"]:
                total += 1
                resultado = patron["validar"](ejemplo)
                if not resultado:
                    exitosos += 1
                    self.area.insert("end", f"   ✅ OK     [esperado: INVÁLIDO] → {ejemplo}\n", "ok")
                else:
                    self.area.insert("end", f"   ❌ FALLO  [esperado: INVÁLIDO] → {ejemplo}\n", "fallo")

        porcentaje = (exitosos / total * 100) if total > 0 else 0
        self.area.insert("end", f"\n{'─'*52}\n", "separador")
        self.area.insert(
            "end",
            f"   RESULTADO FINAL: {exitosos}/{total} casos correctos  —  {porcentaje:.1f}%\n",
            "resumen",
        )
        self.area.config(state="disabled")

        color = (
            COLOR_EXITO if porcentaje == 100
            else COLOR_ADVERTENCIA if porcentaje >= 80
            else COLOR_ERROR
        )
        self.label_score.config(text=f"{exitosos}/{total}  ({porcentaje:.1f}%)", fg=color)
        self.label_estado.config(
            text=f"⬤  {total} casos ejecutados",
            fg=COLOR_EXITO,
        )
