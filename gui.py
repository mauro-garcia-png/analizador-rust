# ============================================================
#  Interfaz gráfica del analizador de Rust (Tkinter)
#  Proyecto de Lenguajes de Programación
#
#  Uso:  py gui.py
# ============================================================
import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import lexer as rust_lexer
import parser as rust_parser
import semantic as rust_semantic

CARPETA_ALGORITMOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'algoritmos')

# Nombre mostrado -> usuario de GitHub (se usa en el nombre del log)
INTEGRANTES = {
    'Misael Moreira': 'mijo5002',
    'Mauro García': 'mauro-garcia-png',
    'Walter Murillo': 'waledos1',
}

FASES = {
    'lexico': 'léxico',
    'sintactico': 'sintáctico',
    'semantico': 'semántico',
}

FUENTE_CODIGO = ('Consolas', 11)
FUENTE_UI = ('Segoe UI', 10)
AZUL = '#1f5fa8'
AZUL_HOVER = '#174a85'
ROJO = '#c62828'
VERDE = '#2e7d32'
FONDO = '#f4f5f7'
BORDE = '#d0d4d9'


class EditorConLineas(tk.Frame):
    """Área de texto con números de línea sincronizados."""

    def __init__(self, master):
        super().__init__(master, bg='white', highlightthickness=1, highlightbackground=BORDE)
        self.lineas = tk.Text(self, width=4, padx=6, takefocus=0, bd=0, bg=FONDO, fg='#999',
                              font=FUENTE_CODIGO, state='disabled', wrap='none', cursor='arrow')
        self.texto = tk.Text(self, wrap='none', undo=True, bd=0, padx=8, pady=4,
                             font=FUENTE_CODIGO, insertbackground='#222')
        self.scroll_y = ttk.Scrollbar(self, orient='vertical', command=self._desplazar)
        self.scroll_x = ttk.Scrollbar(self, orient='horizontal', command=self.texto.xview)
        self.texto.configure(yscrollcommand=self._al_desplazar_texto,
                             xscrollcommand=self.scroll_x.set)
        self.lineas.configure(pady=4)

        self.lineas.grid(row=0, column=0, sticky='ns')
        self.texto.grid(row=0, column=1, sticky='nsew')
        self.scroll_y.grid(row=0, column=2, sticky='ns')
        self.scroll_x.grid(row=1, column=1, sticky='ew')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.texto.tag_configure('linea_error', background='#fde2e2')
        self.texto.bind('<<Modified>>', self._al_modificar)
        self.texto.bind('<Tab>', self._tabulacion)
        self.lineas.bind('<MouseWheel>', lambda e: self.texto.event_generate('<MouseWheel>', delta=e.delta))
        self.actualizar_lineas()

    def _desplazar(self, *args):
        self.texto.yview(*args)
        self.lineas.yview(*args)

    def _al_desplazar_texto(self, inicio, fin):
        self.scroll_y.set(inicio, fin)
        self.lineas.yview_moveto(inicio)

    def _al_modificar(self, _evento):
        if self.texto.edit_modified():
            self.actualizar_lineas()
            self.texto.edit_modified(False)

    def _tabulacion(self, _evento):
        self.texto.insert('insert', '    ')
        return 'break'

    def actualizar_lineas(self):
        total = int(self.texto.index('end-1c').split('.')[0])
        self.lineas.configure(state='normal', width=max(3, len(str(total))) + 1)
        self.lineas.delete('1.0', 'end')
        self.lineas.insert('1.0', '\n'.join(str(i) for i in range(1, total + 1)))
        self.lineas.configure(state='disabled')
        self.lineas.yview_moveto(self.texto.yview()[0])

    def obtener(self):
        return self.texto.get('1.0', 'end-1c')

    def establecer(self, contenido):
        self.texto.delete('1.0', 'end')
        self.texto.insert('1.0', contenido)
        self.texto.edit_reset()

    def marcar_lineas(self, numeros):
        self.texto.tag_remove('linea_error', '1.0', 'end')
        for n in numeros:
            self.texto.tag_add('linea_error', f'{n}.0', f'{n}.0 lineend +1c')
        if numeros:
            self.texto.see(f'{min(numeros)}.0')


class AplicacionAnalizador(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title('Analizador de Rust — Léxico · Sintáctico · Semántico')
        self.geometry('1150x720')
        self.minsize(900, 560)
        self.configure(bg=FONDO)
        self.archivo_actual = None

        estilo = ttk.Style(self)
        estilo.configure('Treeview', font=('Segoe UI', 9), rowheight=22)
        estilo.configure('Treeview.Heading', font=('Segoe UI', 9, 'bold'))

        # La barra de estado se empaqueta antes que los paneles para que no quede oculta
        self._crear_barra_herramientas()
        self._crear_barra_estado()
        self._crear_paneles()

        self.bind('<Control-o>', lambda e: self.abrir_archivo())
        self.bind('<F5>', lambda e: self.ejecutar('lexico'))
        self.bind('<F6>', lambda e: self.ejecutar('sintactico'))
        self.bind('<F7>', lambda e: self.ejecutar('semantico'))

    # ------------------------------------------------------------
    # Construcción de la ventana
    # ------------------------------------------------------------
    def _boton(self, padre, texto, comando, principal=False):
        fondo, frente, activo = (AZUL, 'white', AZUL_HOVER) if principal else ('#f8f9fa', '#222', '#e2e6ea')
        boton = tk.Button(padre, text=texto, command=comando, font=FUENTE_UI, bg=fondo, fg=frente,
                          activebackground=activo, activeforeground=frente, relief='flat',
                          bd=0, padx=14, pady=5, cursor='hand2',
                          highlightthickness=1, highlightbackground=BORDE)
        boton.bind('<Enter>', lambda e: boton.configure(bg=activo))
        boton.bind('<Leave>', lambda e: boton.configure(bg=fondo))
        return boton

    def _crear_barra_herramientas(self):
        barra = tk.Frame(self, bg='white', highlightthickness=1, highlightbackground=BORDE)
        barra.pack(fill='x')

        self._boton(barra, 'Abrir archivo', self.abrir_archivo).pack(side='left', padx=(12, 4), pady=10)
        self._boton(barra, 'Limpiar', self.limpiar).pack(side='left', padx=4)
        tk.Frame(barra, width=1, height=26, bg=BORDE).pack(side='left', padx=10)
        self._boton(barra, 'Léxico (F5)', lambda: self.ejecutar('lexico'), True).pack(side='left', padx=4)
        self._boton(barra, 'Sintáctico (F6)', lambda: self.ejecutar('sintactico'), True).pack(side='left', padx=4)
        self._boton(barra, 'Semántico (F7)', lambda: self.ejecutar('semantico'), True).pack(side='left', padx=4)

        self.integrante = tk.StringVar(value=next(iter(INTEGRANTES)))
        selector = ttk.Combobox(barra, textvariable=self.integrante, values=list(INTEGRANTES),
                                state='readonly', width=18, font=FUENTE_UI)
        selector.pack(side='right', padx=(4, 12))
        tk.Label(barra, text='Integrante:', bg='white', font=FUENTE_UI).pack(side='right')

    def _panel(self, padre, titulo):
        marco = tk.Frame(padre, bg='white', highlightthickness=1, highlightbackground=BORDE)
        encabezado = tk.Label(marco, text=titulo, anchor='w', bg='#eef1f4', font=('Segoe UI', 9, 'bold'),
                              padx=10, pady=5)
        encabezado.pack(fill='x')
        return marco, encabezado

    def _crear_paneles(self):
        contenedor = tk.PanedWindow(self, orient='vertical', bg=FONDO, sashwidth=6, bd=0)
        contenedor.pack(fill='both', expand=True, padx=12, pady=(10, 0))

        superior = tk.PanedWindow(contenedor, orient='horizontal', bg=FONDO, sashwidth=6, bd=0)

        # Editor de código
        marco_editor, self.titulo_editor = self._panel(superior, 'Código fuente')
        self.editor = EditorConLineas(marco_editor)
        self.editor.configure(highlightthickness=0)
        self.editor.pack(fill='both', expand=True)
        superior.add(marco_editor, minsize=380, stretch='always')

        # Tabla de tokens
        marco_tokens, self.titulo_tokens = self._panel(superior, 'Tokens reconocidos')
        cuerpo = tk.Frame(marco_tokens, bg='white')
        cuerpo.pack(fill='both', expand=True)
        self.tabla = ttk.Treeview(cuerpo, columns=('linea', 'token', 'lexema'), show='headings')
        for columna, texto, ancho in (('linea', 'Línea', 60), ('token', 'Token', 130), ('lexema', 'Lexema', 200)):
            self.tabla.heading(columna, text=texto, anchor='w')
            self.tabla.column(columna, width=ancho, anchor='w', stretch=(columna == 'lexema'))
        scroll_tabla = ttk.Scrollbar(cuerpo, orient='vertical', command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll_tabla.set)
        self.tabla.pack(side='left', fill='both', expand=True)
        scroll_tabla.pack(side='right', fill='y')
        superior.add(marco_tokens, minsize=300, stretch='always')

        contenedor.add(superior, minsize=250, stretch='always')

        # Consola de resultados
        marco_consola, _ = self._panel(contenedor, 'Resultados')
        cuerpo_consola = tk.Frame(marco_consola, bg='white')
        cuerpo_consola.pack(fill='both', expand=True)
        self.consola = tk.Text(cuerpo_consola, height=8, bd=0, padx=10, pady=6,
                               font=('Consolas', 10), state='disabled', wrap='word')
        scroll_consola = ttk.Scrollbar(cuerpo_consola, orient='vertical', command=self.consola.yview)
        self.consola.configure(yscrollcommand=scroll_consola.set)
        self.consola.pack(side='left', fill='both', expand=True)
        scroll_consola.pack(side='right', fill='y')
        self.consola.tag_configure('error', foreground=ROJO)
        self.consola.tag_configure('exito', foreground=VERDE)
        self.consola.tag_configure('info', foreground='#555')
        contenedor.add(marco_consola, minsize=120)

    def _crear_barra_estado(self):
        barra = tk.Frame(self, bg='#dde3ea')
        barra.pack(fill='x', side='bottom', pady=(10, 0))
        self.estado = tk.Label(barra, text='Listo. Escriba código Rust o abra un archivo .rs.',
                               bg='#dde3ea', anchor='w', font=('Segoe UI', 9), padx=12, pady=4)
        self.estado.pack(side='left')
        self.estado_log = tk.Label(barra, text='', bg='#dde3ea', anchor='e', font=('Segoe UI', 9), padx=12)
        self.estado_log.pack(side='right')

    # ------------------------------------------------------------
    # Acciones
    # ------------------------------------------------------------
    def abrir_archivo(self):
        ruta = filedialog.askopenfilename(
            title='Abrir archivo Rust', initialdir=CARPETA_ALGORITMOS,
            filetypes=[('Archivos Rust', '*.rs'), ('Todos los archivos', '*.*')])
        if not ruta:
            return
        with open(ruta, encoding='utf-8') as f:
            self.editor.establecer(f.read())
        self.archivo_actual = ruta
        self.titulo_editor.configure(text=f'Código fuente — {os.path.basename(ruta)}')
        self._limpiar_resultados()
        self.estado.configure(text=f'Archivo cargado: {os.path.basename(ruta)}')

    def limpiar(self):
        self.editor.establecer('')
        self.archivo_actual = None
        self.titulo_editor.configure(text='Código fuente')
        self._limpiar_resultados()
        self.estado.configure(text='Listo. Escriba código Rust o abra un archivo .rs.')

    def _limpiar_resultados(self):
        self.tabla.delete(*self.tabla.get_children())
        self.titulo_tokens.configure(text='Tokens reconocidos')
        self.consola.configure(state='normal')
        self.consola.delete('1.0', 'end')
        self.consola.configure(state='disabled')
        self.editor.marcar_lineas([])
        self.estado_log.configure(text='')

    def _escribir(self, texto, etiqueta=None):
        self.consola.configure(state='normal')
        self.consola.insert('end', texto + '\n', etiqueta)
        self.consola.configure(state='disabled')
        self.consola.see('end')

    def _mostrar_tokens(self, tokens):
        self.tabla.delete(*self.tabla.get_children())
        for tok in tokens:
            self.tabla.insert('', 'end', values=(tok.lineno, tok.type, tok.value))
        self.titulo_tokens.configure(text=f'Tokens reconocidos ({len(tokens)})')

    def ejecutar(self, fase):
        codigo = self.editor.obtener()
        if not codigo.strip():
            messagebox.showwarning('Sin código', 'Escriba código Rust o abra un archivo .rs antes de analizar.')
            return

        usuario = INTEGRANTES[self.integrante.get()]
        archivo = os.path.basename(self.archivo_actual) if self.archivo_actual else 'código escrito en el editor'
        nombre_fase = FASES[fase]
        self._limpiar_resultados()

        try:
            tokens, errores_lexicos = rust_lexer.analizar(codigo)
            self._mostrar_tokens(tokens)
            if fase == 'lexico':
                errores = errores_lexicos
                ruta_log = rust_lexer.generar_log(archivo, usuario, tokens, errores)
            elif fase == 'sintactico':
                _, errores = rust_parser.analizar(codigo)
                ruta_log = rust_parser.generar_log(archivo, usuario, errores)
            else:
                errores = rust_semantic.analizar(codigo)
                ruta_log = rust_semantic.generar_log(archivo, usuario, errores)
        except Exception as exc:  # el análisis no debe cerrar la ventana
            self._escribir(f'✖ Error interno durante el análisis {nombre_fase}: {exc}', 'error')
            self.estado.configure(text=f'Análisis {nombre_fase} interrumpido')
            return

        self._escribir(f'Análisis {nombre_fase} — {archivo} — {self.integrante.get()}', 'info')
        for e in errores:
            self._escribir(f'✖ {e}', 'error')
        if errores:
            self._escribir(f'Se encontraron {len(errores)} errores.', 'error')
        elif fase == 'lexico':
            self._escribir(f'✔ Análisis léxico exitoso: {len(tokens)} tokens reconocidos.', 'exito')
        else:
            self._escribir(f'✔ Análisis {nombre_fase} exitoso.', 'exito')

        self.consola.see('1.0')

        lineas = sorted({int(n) for e in errores for n in re.findall(r'línea (\d+)', e)})
        self.editor.marcar_lineas(lineas)

        cantidad = f'{len(errores)} error' + ('' if len(errores) == 1 else 'es')
        self.estado.configure(text=f'Análisis {nombre_fase} finalizado · {cantidad}')
        self.estado_log.configure(text=f'Log guardado: {os.path.basename(ruta_log)}')


if __name__ == '__main__':
    AplicacionAnalizador().mainloop()
