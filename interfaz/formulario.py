# =============================================================================
# ventana_formulario.py
# Interfaz de formulario con validación en tiempo real de cada campo
# Usa tkinter — sin librerías externas adicionales
# =============================================================================

import tkinter as tk
from datetime import date
from tkinter import scrolledtext, messagebox
from patrones import validar_con_patron
from motor_regex import es_letra, es_digito, es_mayuscula

# =============================================================================
# PALETA DE COLORES (coherente con ventana_busqueda.py)
# =============================================================================
COLOR_FONDO         = "#1E1E2E"
COLOR_PANEL         = "#2A2A3E"
COLOR_BORDE         = "#3A3A5C"
COLOR_ACENTO        = "#7C6AF7"
COLOR_ACENTO_HOVER  = "#9B8FF9"
COLOR_TEXTO         = "#CDD6F4"
COLOR_TEXTO_SUAVE   = "#6E6E9A"
COLOR_EXITO         = "#A6E3A1"
COLOR_ERROR         = "#F38BA8"
COLOR_ADVERTENCIA   = "#FAB387"
COLOR_CAMPO_OK      = "#1E3A2E"   # fondo verde oscuro cuando es válido
COLOR_CAMPO_MAL     = "#3A1E2E"   # fondo rojo oscuro cuando es inválido
COLOR_CAMPO_NEUTRO  = "#252535"   # fondo neutro sin validar

FONT_TITULO    = ("Georgia", 18, "bold")
FONT_SUBTITULO = ("Georgia", 11, "italic")
FONT_NORMAL    = ("Courier New", 10)
FONT_BOLD      = ("Courier New", 10, "bold")
FONT_BOTON     = ("Courier New", 10, "bold")
FONT_PEQUEÑO   = ("Courier New", 9)
FONT_ICONO     = ("Courier New", 13, "bold")


# =============================================================================
# VALIDADORES ADICIONALES (específicos del formulario)
# Estos no están en motor_regex porque son reglas de negocio del formulario
# =============================================================================

def validar_contrasena(cadena):
    """
    Contraseña segura:
      - Mínimo 8 caracteres
      - Al menos 1 letra mayúscula
      - Al menos 1 letra minúscula
      - Al menos 1 dígito
      - Al menos 1 carácter especial: @#$%^&*!_-
    Retorna (bool, str) → (es_válida, mensaje_de_error)
    """
    especiales = set('@#$%^&*!_-')
    if len(cadena) < 8:
        return False, "Mínimo 8 caracteres"

    tiene_may  = any(es_mayuscula(c) for c in cadena)
    tiene_min  = any('a' <= c <= 'z' for c in cadena)
    tiene_dig  = any(es_digito(c) for c in cadena)
    tiene_esp  = any(c in especiales for c in cadena)

    if not tiene_may:
        return False, "Falta al menos una mayúscula"
    if not tiene_min:
        return False, "Falta al menos una minúscula"
    if not tiene_dig:
        return False, "Falta al menos un número"
    if not tiene_esp:
        return False, "Falta un carácter especial (@#$%^&*!_-)"
    return True, "Contraseña segura ✔"


def validar_nombre_usuario(cadena):
    """
    Nombre de usuario:
      - Entre 4 y 20 caracteres
      - Solo letras, dígitos y guión bajo
      - Debe empezar con letra
      - No puede terminar en _ ni tener __ consecutivos
    Retorna (bool, str)
    """
    if len(cadena) < 4:
        return False, "Mínimo 4 caracteres"
    if len(cadena) > 20:
        return False, "Máximo 20 caracteres"
    if not es_letra(cadena[0]):
        return False, "Debe empezar con una letra"
    if cadena[-1] == '_':
        return False, "No puede terminar con _"
    if '__' in cadena:
        return False, "No puede tener __ consecutivos"
    for c in cadena:
        if not (es_digito(c) or es_letra(c) or c == '_'):
            return False, f"Carácter no permitido: '{c}'"
    return True, "Usuario válido ✔"


def validar_fecha_nacimiento(cadena, hoy=None):
    """Valida formato de fecha y evita fechas de nacimiento futuras."""
    if not validar_con_patron("fecha", cadena):
        return False, "Usa el formato DD/MM/AAAA"

    dia = int(cadena[0:2])
    mes = int(cadena[3:5])
    anio = int(cadena[6:10])
    nacimiento = date(anio, mes, dia)
    hoy = hoy or date.today()

    if nacimiento > hoy:
        return False, "La fecha no puede ser futura"
    return True, "Fecha válida ✔"


def validar_confirmacion(original, confirmacion):
    """Verifica que la confirmación de contraseña coincida."""
    if confirmacion == "":
        return False, "Repite tu contraseña"
    if original != confirmacion:
        return False, "Las contraseñas no coinciden"
    return True, "Contraseñas coinciden ✔"


# =============================================================================
# CLASE PRINCIPAL DEL FORMULARIO
# =============================================================================

class VentanaFormulario(tk.Frame):
    """
    Frame con formulario interactivo y validación en tiempo real.
    Campos: nombre de usuario, correo, teléfono, cédula, fecha de nacimiento,
            contraseña y confirmación de contraseña.
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, bg=COLOR_FONDO, **kwargs)
        # Diccionario para guardar el estado de cada campo {nombre: bool}
        self.estados = {}
        self._construir_interfaz()

    # -------------------------------------------------------------------------
    # CONSTRUCCIÓN DE LA INTERFAZ
    # -------------------------------------------------------------------------

    def _construir_interfaz(self):
        self._crear_encabezado()
        self._crear_cuerpo()
        self._crear_barra_estado()

    def _crear_encabezado(self):
        frame = tk.Frame(self, bg=COLOR_FONDO, pady=16)
        frame.pack(fill="x", padx=24)

        tk.Label(
            frame,
            text="📋  Formulario de Registro",
            font=FONT_TITULO,
            bg=COLOR_FONDO,
            fg=COLOR_ACENTO,
        ).pack(anchor="w")

        tk.Label(
            frame,
            text="Cada campo se valida en tiempo real mientras escribes",
            font=FONT_SUBTITULO,
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO_SUAVE,
        ).pack(anchor="w")

        tk.Frame(self, bg=COLOR_BORDE, height=1).pack(fill="x", padx=24)

    def _crear_cuerpo(self):
        """Cuerpo principal con dos columnas de campos + log lateral."""
        contenedor = tk.Frame(self, bg=COLOR_FONDO)
        contenedor.pack(fill="both", expand=True, padx=24, pady=16)

        contenedor.columnconfigure(0, weight=2)
        contenedor.columnconfigure(1, weight=1)
        contenedor.rowconfigure(0, weight=1)

        self._crear_columna_campos(contenedor)
        self._crear_columna_log(contenedor)

    def _crear_columna_campos(self, parent):
        """Columna izquierda con todos los campos del formulario."""
        frame = tk.Frame(parent, bg=COLOR_PANEL)
        frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        tk.Label(
            frame,
            text="DATOS DE REGISTRO",
            font=FONT_BOLD,
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO_SUAVE,
            pady=10,
            padx=14,
            anchor="w",
        ).pack(fill="x")

        tk.Frame(frame, bg=COLOR_BORDE, height=1).pack(fill="x")

        # Área scrollable para los campos
        canvas = tk.Canvas(frame, bg=COLOR_PANEL, highlightthickness=0)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        self.frame_campos = tk.Frame(canvas, bg=COLOR_PANEL)

        self.frame_campos.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.frame_campos, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        canvas.bind("<Enter>", lambda e: self._activar_scroll_campos(canvas))
        canvas.bind("<Leave>", lambda e: self._desactivar_scroll_campos(canvas))
        self.frame_campos.bind("<Enter>", lambda e: self._activar_scroll_campos(canvas))
        self.frame_campos.bind("<Leave>", lambda e: self._desactivar_scroll_campos(canvas))

        # Crear cada campo
        self._agregar_campo(
            nombre="usuario",
            etiqueta="👤  Nombre de usuario",
            placeholder="ej: juan_perez_01",
            tipo="texto",
            validador=self._validar_campo_usuario,
            regla="4-20 caracteres · empieza con letra · sin _ final/doble"
        )
        self._agregar_campo(
            nombre="correo",
            etiqueta="✉️  Correo electrónico",
            placeholder="ej: usuario@dominio.com",
            tipo="texto",
            validador=self._validar_campo_correo,
            regla="formato usuario@dominio.extension"
        )
        self._agregar_campo(
            nombre="telefono",
            etiqueta="📱  Teléfono colombiano",
            placeholder="ej: 3001234567",
            tipo="texto",
            validador=self._validar_campo_telefono,
            regla="10 dígitos iniciando en 3 · o +57..."
        )
        self._agregar_campo(
            nombre="cedula",
            etiqueta="🪪  Cédula",
            placeholder="ej: 1098765432",
            tipo="texto",
            validador=self._validar_campo_cedula,
            regla="6-10 dígitos · no empieza en 0"
        )
        self._agregar_campo(
            nombre="fecha",
            etiqueta="📅  Fecha de nacimiento",
            placeholder="ej: 15/08/1995",
            tipo="texto",
            validador=self._validar_campo_fecha,
            regla="formato DD/MM/AAAA o DD-MM-AAAA"
        )
        self._agregar_campo(
            nombre="contrasena",
            etiqueta="🔒  Contraseña",
            placeholder="mínimo 8 caracteres",
            tipo="password",
            validador=self._validar_campo_contrasena,
            regla="mayús + minús + número + especial"
        )
        self._agregar_campo(
            nombre="confirmacion",
            etiqueta="🔒  Confirmar contraseña",
            placeholder="repite tu contraseña",
            tipo="password",
            validador=self._validar_campo_confirmacion,
            regla="debe coincidir con la contraseña"
        )

        # Indicador de fortaleza de contraseña
        self._crear_indicador_fortaleza()

        # Botones
        frame_botones = tk.Frame(self.frame_campos, bg=COLOR_PANEL, pady=16, padx=14)
        frame_botones.pack(fill="x")

        self._boton(frame_botones, "✅  Enviar formulario", self._enviar,
                    COLOR_ACENTO, "#FFFFFF").pack(side="left", padx=(0, 10))
        self._boton(frame_botones, "🗑  Limpiar todo", self._limpiar_formulario,
                    COLOR_PANEL, COLOR_ERROR, borde=COLOR_ERROR).pack(side="left")

    def _agregar_campo(self, nombre, etiqueta, placeholder, tipo, validador, regla):
        """
        Crea un campo completo con:
          - Etiqueta superior
          - Entry con icono de estado (✔ / ✘)
          - Mensaje de validación en tiempo real
          - Texto de ayuda con la regla
        """
        contenedor = tk.Frame(self.frame_campos, bg=COLOR_PANEL, pady=8, padx=14)
        contenedor.pack(fill="x")

        # Etiqueta del campo
        tk.Label(
            contenedor,
            text=etiqueta,
            font=FONT_BOLD,
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
            anchor="w",
        ).pack(fill="x")

        # Fila: entry + icono de estado
        fila = tk.Frame(contenedor, bg=COLOR_PANEL)
        fila.pack(fill="x", pady=(4, 0))

        entry = tk.Entry(
            fila,
            font=FONT_NORMAL,
            bg=COLOR_CAMPO_NEUTRO,
            fg=COLOR_TEXTO,
            insertbackground=COLOR_ACENTO,
            relief="flat",
            bd=0,
            highlightthickness=2,
            highlightbackground=COLOR_BORDE,
            highlightcolor=COLOR_ACENTO,
            show="●" if tipo == "password" else "",
        )
        entry.pack(side="left", fill="x", expand=True, ipady=8, ipadx=8)
        entry.insert(0, placeholder)
        entry.config(fg=COLOR_TEXTO_SUAVE)

        # Icono de estado (✔ o ✘)
        icono = tk.Label(
            fila,
            text="  ○  ",
            font=FONT_ICONO,
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO_SUAVE,
            width=3,
        )
        icono.pack(side="left", padx=(6, 0))

        # Mensaje de validación
        msg = tk.Label(
            contenedor,
            text=regla,
            font=FONT_PEQUEÑO,
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO_SUAVE,
            anchor="w",
        )
        msg.pack(fill="x", pady=(2, 0))

        # Guardar referencias
        setattr(self, f"entry_{nombre}", entry)
        setattr(self, f"icono_{nombre}", icono)
        setattr(self, f"msg_{nombre}",   msg)
        self.estados[nombre] = False

        # Eventos: limpiar placeholder al entrar, validar al escribir
        entry.bind("<FocusIn>",  lambda e, n=nombre, p=placeholder: self._focus_in(n, p))
        entry.bind("<FocusOut>", lambda e, n=nombre, p=placeholder: self._focus_out(n, p))
        entry.bind("<KeyRelease>", lambda e, n=nombre, v=validador: v(n))

    def _crear_indicador_fortaleza(self):
        """Barra visual de fortaleza de contraseña."""
        frame = tk.Frame(self.frame_campos, bg=COLOR_PANEL, padx=14, pady=4)
        frame.pack(fill="x")

        tk.Label(
            frame,
            text="Fortaleza de la contraseña:",
            font=FONT_PEQUEÑO,
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO_SUAVE,
        ).pack(side="left")

        self.label_fortaleza = tk.Label(
            frame,
            text="—",
            font=FONT_BOLD,
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO_SUAVE,
        )
        self.label_fortaleza.pack(side="left", padx=8)

    def _crear_columna_log(self, parent):
        """Columna derecha: resumen visual del estado de todos los campos."""
        frame = tk.Frame(parent, bg=COLOR_PANEL)
        frame.grid(row=0, column=1, sticky="nsew")

        tk.Label(
            frame,
            text="ESTADO DEL FORMULARIO",
            font=FONT_BOLD,
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO_SUAVE,
            pady=10,
            padx=14,
            anchor="w",
        ).pack(fill="x")

        tk.Frame(frame, bg=COLOR_BORDE, height=1).pack(fill="x")

        # Log de validación en tiempo real
        self.log = scrolledtext.ScrolledText(
            frame,
            font=FONT_PEQUEÑO,
            bg="#252535",
            fg=COLOR_TEXTO,
            relief="flat",
            padx=10,
            pady=10,
            wrap="word",
            state="disabled",
            height=20,
        )
        self.log.pack(fill="both", expand=True, padx=2, pady=2)
        self.log.tag_config("ok",      foreground=COLOR_EXITO)
        self.log.tag_config("error",   foreground=COLOR_ERROR)
        self.log.tag_config("neutro",  foreground=COLOR_TEXTO_SUAVE)
        self.log.tag_config("titulo",  foreground=COLOR_ACENTO, font=FONT_BOLD)

        # Indicador de progreso (campos completados / total)
        self.label_progreso = tk.Label(
            frame,
            text="0 / 7 campos válidos",
            font=FONT_BOLD,
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO_SUAVE,
            pady=8,
            padx=12,
            anchor="w",
        )
        self.label_progreso.pack(fill="x")

        self._actualizar_log()

    def _crear_barra_estado(self):
        tk.Frame(self, bg=COLOR_BORDE, height=1).pack(fill="x")
        frame = tk.Frame(self, bg=COLOR_FONDO, pady=6)
        frame.pack(fill="x", padx=24)

        self.label_estado = tk.Label(
            frame,
            text="⬤  Completa todos los campos para enviar",
            font=FONT_PEQUEÑO,
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO_SUAVE,
            anchor="w",
        )
        self.label_estado.pack(side="left")

    # -------------------------------------------------------------------------
    # VALIDADORES DE CADA CAMPO
    # -------------------------------------------------------------------------

    def _validar_campo_usuario(self, nombre):
        valor = self._valor(nombre)
        ok, mensaje = validar_nombre_usuario(valor) if valor else (False, "Campo requerido")
        self._actualizar_campo(nombre, ok, mensaje)

    def _validar_campo_correo(self, nombre):
        valor = self._valor(nombre)
        ok = validar_con_patron("correo", valor) if valor else False
        mensaje = "Correo válido ✔" if ok else ("Campo requerido" if not valor else "Formato inválido · usuario@dominio.ext")
        self._actualizar_campo(nombre, ok, mensaje)

    def _validar_campo_telefono(self, nombre):
        valor = self._valor(nombre)
        ok = validar_con_patron("telefono", valor) if valor else False
        mensaje = "Teléfono válido ✔" if ok else ("Campo requerido" if not valor else "Debe tener 10 dígitos e iniciar en 3")
        self._actualizar_campo(nombre, ok, mensaje)

    def _validar_campo_cedula(self, nombre):
        valor = self._valor(nombre)
        ok = validar_con_patron("cedula", valor) if valor else False
        mensaje = "Cédula válida ✔" if ok else ("Campo requerido" if not valor else "6-10 dígitos · no puede empezar en 0")
        self._actualizar_campo(nombre, ok, mensaje)

    def _validar_campo_fecha(self, nombre):
        valor = self._valor(nombre)
        ok, mensaje = validar_fecha_nacimiento(valor) if valor else (False, "Campo requerido")
        self._actualizar_campo(nombre, ok, mensaje)

    def _validar_campo_contrasena(self, nombre):
        valor = self._valor(nombre)
        ok, mensaje = validar_contrasena(valor) if valor else (False, "Campo requerido")
        self._actualizar_campo(nombre, ok, mensaje)
        self._actualizar_fortaleza(valor)
        # Revalidar confirmación si ya tiene contenido
        if self._valor("confirmacion"):
            self._validar_campo_confirmacion("confirmacion")

    def _validar_campo_confirmacion(self, nombre):
        original     = self._valor("contrasena")
        confirmacion = self._valor(nombre)
        ok, mensaje  = validar_confirmacion(original, confirmacion)
        self._actualizar_campo(nombre, ok, mensaje)

    # -------------------------------------------------------------------------
    # ACTUALIZACIÓN VISUAL DE CAMPOS
    # -------------------------------------------------------------------------

    def _actualizar_campo(self, nombre, ok, mensaje):
        """Aplica color, icono y mensaje al campo según su estado."""
        entry = getattr(self, f"entry_{nombre}")
        icono = getattr(self, f"icono_{nombre}")
        msg   = getattr(self, f"msg_{nombre}")

        if ok:
            entry.config(bg=COLOR_CAMPO_OK,  highlightbackground=COLOR_EXITO)
            icono.config(text=" ✔ ",  fg=COLOR_EXITO)
            msg.config(  text=mensaje, fg=COLOR_EXITO)
        else:
            entry.config(bg=COLOR_CAMPO_MAL, highlightbackground=COLOR_ERROR)
            icono.config(text=" ✘ ",  fg=COLOR_ERROR)
            msg.config(  text=mensaje, fg=COLOR_ERROR)

        self.estados[nombre] = ok
        self._actualizar_log()
        self._actualizar_progreso()

    def _actualizar_fortaleza(self, contrasena):
        """Calcula y muestra la fortaleza de la contraseña."""
        if not contrasena:
            self.label_fortaleza.config(text="—", fg=COLOR_TEXTO_SUAVE)
            return

        puntos = 0
        especiales = set('@#$%^&*!_-')
        if len(contrasena) >= 8:  puntos += 1
        if len(contrasena) >= 12: puntos += 1
        if any(es_mayuscula(c)          for c in contrasena): puntos += 1
        if any('a' <= c <= 'z'          for c in contrasena): puntos += 1
        if any(es_digito(c)             for c in contrasena): puntos += 1
        if any(c in especiales          for c in contrasena): puntos += 1

        niveles = [
            (1, "Muy débil",  COLOR_ERROR),
            (2, "Débil",      COLOR_ERROR),
            (3, "Regular",    COLOR_ADVERTENCIA),
            (4, "Aceptable",  COLOR_ADVERTENCIA),
            (5, "Fuerte",     COLOR_EXITO),
            (6, "Muy fuerte", COLOR_EXITO),
        ]
        for umbral, texto, color in niveles:
            if puntos <= umbral:
                self.label_fortaleza.config(text=texto, fg=color)
                break

    def _actualizar_log(self):
        """Actualiza el panel lateral con el estado de todos los campos."""
        nombres_legibles = {
            "usuario"     : "Nombre de usuario",
            "correo"      : "Correo electrónico",
            "telefono"    : "Teléfono",
            "cedula"      : "Cédula",
            "fecha"       : "Fecha de nacimiento",
            "contrasena"  : "Contraseña",
            "confirmacion": "Confirmación",
        }

        self.log.config(state="normal")
        self.log.delete("1.0", "end")
        self.log.insert("end", "Estado de validación\n", "titulo")
        self.log.insert("end", "─" * 28 + "\n", "neutro")

        for campo, nombre in nombres_legibles.items():
            estado = self.estados.get(campo, False)
            icono  = "✔" if estado else "✘"
            tag    = "ok" if estado else "error"
            self.log.insert("end", f"  {icono}  {nombre}\n", tag)

        self.log.config(state="disabled")

    def _actualizar_progreso(self):
        """Actualiza el contador de campos válidos."""
        total   = len(self.estados)
        validos = sum(1 for v in self.estados.values() if v)
        color   = COLOR_EXITO if validos == total else (
                  COLOR_ADVERTENCIA if validos > 0 else COLOR_ERROR)
        self.label_progreso.config(
            text=f"{validos} / {total} campos válidos",
            fg=color,
        )
        if validos == total:
            self.label_estado.config(
                text="⬤  Todos los campos son válidos · puedes enviar",
                fg=COLOR_EXITO,
            )
        else:
            self.label_estado.config(
                text=f"⬤  Faltan {total - validos} campo(s) por completar correctamente",
                fg=COLOR_ADVERTENCIA,
            )

    # -------------------------------------------------------------------------
    # ACCIONES
    # -------------------------------------------------------------------------

    def _enviar(self):
        """Valida todos los campos y muestra resultado del envío."""
        # Forzar validación de todos los campos antes de enviar
        for nombre in self.estados:
            validador = getattr(self, f"_validar_campo_{nombre}", None)
            if validador:
                validador(nombre)

        if all(self.estados.values()):
            messagebox.showinfo(
                "✅ Formulario enviado",
                f"¡Registro exitoso!\n\n"
                f"Usuario: {self._valor('usuario')}\n"
                f"Correo:  {self._valor('correo')}\n"
                f"Teléfono: {self._valor('telefono')}\n"
                f"Cédula:  {self._valor('cedula')}\n"
                f"Fecha:   {self._valor('fecha')}"
            )
            self.label_estado.config(
                text="⬤  Formulario enviado correctamente",
                fg=COLOR_EXITO,
            )
        else:
            faltantes = [n for n, v in self.estados.items() if not v]
            messagebox.showwarning(
                "⚠ Campos incompletos",
                f"Corrige los siguientes campos antes de enviar:\n\n" +
                "\n".join(f"  • {f}" for f in faltantes)
            )

    def _limpiar_formulario(self):
        """Restablece todos los campos a su estado inicial."""
        placeholders = {
            "usuario"     : "ej: juan_perez_01",
            "correo"      : "ej: usuario@dominio.com",
            "telefono"    : "ej: 3001234567",
            "cedula"      : "ej: 1098765432",
            "fecha"       : "ej: 15/08/1995",
            "contrasena"  : "mínimo 8 caracteres",
            "confirmacion": "repite tu contraseña",
        }
        for nombre, placeholder in placeholders.items():
            entry = getattr(self, f"entry_{nombre}")
            icono = getattr(self, f"icono_{nombre}")
            msg   = getattr(self, f"msg_{nombre}")
            entry.config(bg=COLOR_CAMPO_NEUTRO, highlightbackground=COLOR_BORDE,
                         fg=COLOR_TEXTO_SUAVE)
            entry.delete(0, "end")
            entry.insert(0, placeholder)
            icono.config(text="  ○  ", fg=COLOR_TEXTO_SUAVE)
            msg.config(  text="",      fg=COLOR_TEXTO_SUAVE)
            self.estados[nombre] = False

        self.label_fortaleza.config(text="—", fg=COLOR_TEXTO_SUAVE)
        self._actualizar_log()
        self._actualizar_progreso()
        self.label_estado.config(
            text="⬤  Completa todos los campos para enviar",
            fg=COLOR_TEXTO_SUAVE,
        )

    # -------------------------------------------------------------------------
    # UTILIDADES
    # -------------------------------------------------------------------------

    def _valor(self, nombre):
        """Retorna el valor actual del campo (sin placeholder)."""
        entry = getattr(self, f"entry_{nombre}")
        valor = entry.get().strip()
        placeholders = {
            "usuario"     : "ej: juan_perez_01",
            "correo"      : "ej: usuario@dominio.com",
            "telefono"    : "ej: 3001234567",
            "cedula"      : "ej: 1098765432",
            "fecha"       : "ej: 15/08/1995",
            "contrasena"  : "mínimo 8 caracteres",
            "confirmacion": "repite tu contraseña",
        }
        return "" if valor == placeholders.get(nombre, "") else valor

    def _focus_in(self, nombre, placeholder):
        """Limpia el placeholder cuando el campo recibe foco."""
        entry = getattr(self, f"entry_{nombre}")
        if entry.get() == placeholder:
            entry.delete(0, "end")
            entry.config(fg=COLOR_TEXTO)
            if self.estados.get(nombre) is False:
                entry.config(bg=COLOR_CAMPO_NEUTRO, highlightbackground=COLOR_ACENTO)

    def _focus_out(self, nombre, placeholder):
        """Restaura el placeholder si el campo queda vacío."""
        entry = getattr(self, f"entry_{nombre}")
        if entry.get().strip() == "":
            entry.insert(0, placeholder)
            entry.config(fg=COLOR_TEXTO_SUAVE, bg=COLOR_CAMPO_NEUTRO,
                         highlightbackground=COLOR_BORDE)

    def _activar_scroll_campos(self, canvas):
        self._canvas_scroll_activo = canvas
        canvas.bind_all("<MouseWheel>", self._scroll_campos)
        canvas.bind_all("<Button-4>", self._scroll_campos)
        canvas.bind_all("<Button-5>", self._scroll_campos)

    def _desactivar_scroll_campos(self, canvas):
        self._canvas_scroll_activo = None
        canvas.unbind_all("<MouseWheel>")
        canvas.unbind_all("<Button-4>")
        canvas.unbind_all("<Button-5>")

    def _scroll_campos(self, event):
        canvas = getattr(self, "_canvas_scroll_activo", None)
        if canvas is None:
            return
        if getattr(event, "num", None) == 4:
            desplazamiento = -1
        elif getattr(event, "num", None) == 5:
            desplazamiento = 1
        else:
            desplazamiento = int(-event.delta / 120)
        canvas.yview_scroll(desplazamiento, "units")

    def _boton(self, parent, texto, comando, bg, fg, borde=None):
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
    root.title("Formulario de Registro")
    root.geometry("1000x700")
    root.configure(bg=COLOR_FONDO)
    root.resizable(True, True)

    app = VentanaFormulario(root)
    app.pack(fill="both", expand=True)

    root.mainloop()
