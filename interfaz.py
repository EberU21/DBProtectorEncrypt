import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from sympy import randprime, mod_inverse
from conexionDB import create_connection, fetch_table_data, fetch_table_names, fetch_table_columns, actualizar_datosBD
from codigoRSA import encriptar, desencriptar, obtenerClaves, display_encrypted_data, split_encrypted_data, encrypt_string, decrypt_string, convertir_cadena, convert_ascii_to_decimal

class InterfazEncriptacion:
    def __init__(self, master):
        self.master = master
        self.nombre_usuario = ""
        self.modo_usuario = False
        master.title("Interfaz de Encriptación")
        master.configure(bg='#2c3e50')  # Fondo azul oscuro
        
         # Menú de opciones
        self.menu = tk.Menu(master)
        master.config(menu=self.menu)
        
        self.opciones_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Opciones", menu=self.opciones_menu)
        self.opciones_menu.add_command(label="Salir modo por usuario", command=self.salir_modo_usuario)
        self.opciones_menu.add_command(label="Modo por Usuario", command=self.cambiar_modo_usuario)
        
        self.formatted_data=None
        self.col=None

        self.clave_privada = tk.StringVar()
        self.clave_publica = tk.StringVar()
        self.valor_n = tk.StringVar()

        self.frame_botones = tk.Frame(master, bg='#2c3e50')
        self.frame_botones.pack(pady=10)

        button_style = {'bg': '#34495e', 'fg': 'white', 'activebackground': '#16a085', 'relief': 'flat', 'font': ('Helvetica', 10, 'bold')}
        label_style = {'bg': '#2c3e50', 'fg': 'white', 'font': ('Helvetica', 10)}
        entry_style = {'bg': '#ecf0f1', 'font': ('Helvetica', 10)}

        self.btn_conectar = tk.Button(self.frame_botones, text="Conectar a la Base de Datos", command=self.conectar_base_datos, **button_style)
        self.btn_conectar.grid(row=0, column=0, padx=5)

        self.btn_agregar = tk.Button(self.frame_botones, text="Agregar Dato", command=self.agregar_dato, **button_style)
        self.btn_agregar.grid(row=0, column=1, padx=5)


        self.btn_encriptar = tk.Button(self.frame_botones, text="Encriptar Dato", command=self.encriptar_dato, **button_style)
        self.btn_encriptar.grid(row=0, column=3, padx=5)

        self.btn_desencriptar = tk.Button(self.frame_botones, text="Desencriptar Dato", command=self.desencriptar_dato, **button_style)
        self.btn_desencriptar.grid(row=0, column=4, padx=5)

        self.frame_selector = tk.Frame(master, bg='#2c3e50')
        self.frame_selector.pack(pady=10)

        tk.Label(self.frame_selector, text="Seleccione la tabla:", **label_style).grid(row=0, column=0, sticky=tk.W)
        self.tabla_seleccionada = tk.StringVar()
        self.combobox_tabla = ttk.Combobox(self.frame_selector, textvariable=self.tabla_seleccionada, state='readonly')
        self.combobox_tabla.grid(row=0, column=1)

        self.btn_mostrar_tabla = tk.Button(self.frame_selector, text="Mostrar Datos de la Tabla", command=self.mostrar_datos_tabla, **button_style)
        self.btn_mostrar_tabla.grid(row=0, column=2, padx=5)

        self.frame_claves = tk.Frame(master, bg='#2c3e50')
        self.frame_claves.pack(pady=10)

        tk.Label(self.frame_claves, text="Clave Privada:", **label_style).grid(row=0, column=0, sticky=tk.W)
        tk.Entry(self.frame_claves, textvariable=self.clave_privada, **entry_style).grid(row=0, column=1)
        tk.Button(self.frame_claves, text="Cargar desde archivo", command=self.cargar_clave_privada, **button_style).grid(row=0, column=2, padx=5)

        tk.Label(self.frame_claves, text="Clave Pública:", **label_style).grid(row=1, column=0, sticky=tk.W)
        tk.Entry(self.frame_claves, textvariable=self.clave_publica, **entry_style).grid(row=1, column=1)
        tk.Button(self.frame_claves, text="Cargar desde archivo", command=self.cargar_clave_publica, **button_style).grid(row=1, column=2, padx=5)

        tk.Label(self.frame_claves, text="Valor de n:", **label_style).grid(row=2, column=0, sticky=tk.W)
        tk.Entry(self.frame_claves, textvariable=self.valor_n, **entry_style).grid(row=2, column=1)

        self.frame_tabla = tk.Frame(master, bg='#2c3e50')
        self.frame_tabla.pack(pady=10)

        style = ttk.Style()
        style.configure("Treeview", background='#ecf0f1', foreground='black', rowheight=25, fieldbackground='#ecf0f1', font=('Helvetica', 10))
        style.configure("Treeview.Heading", background='#34495e', foreground='blue', font=('Helvetica', 10, 'bold'))

        self.tree = ttk.Treeview(self.frame_tabla, show='headings')
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<Button-1>", self.on_tree_click)

        self.frame_encriptar = tk.Frame(master, bg='#2c3e50')
        self.frame_encriptar.pack(pady=10)

        tk.Label(self.frame_encriptar, text="Datos a encriptar/desencriptar:", **label_style).pack()
        self.text_encriptar = tk.Text(self.frame_encriptar, height=5, width=50, bg='#ecf0f1', font=('Helvetica', 10))
        self.text_encriptar.pack()
        self.label = None
    
    def conectar_base_datos(self):
        try:
            connection = create_connection()
            messagebox.showinfo("Conexión Exitosa", "Se ha establecido la conexión con la base de datos.")
           
            tablas = fetch_table_names(connection)
            self.combobox_tabla['values'] = tablas
        except Exception as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos: {e}")

    def mostrar_datos_tabla(self):
        tabla = self.tabla_seleccionada.get()
        
        self.limpiar_treeview()
        try:
            connection = create_connection()
            
            columns = fetch_table_columns(connection, tabla)
            self.tree["columns"] = columns
            for col in columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, anchor=tk.W)

            
            data = fetch_table_data(connection, tabla)
            if data:
                for row in data:
                    self.tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron recuperar los datos de la tabla: {e}")

    def limpiar_treeview(self):
        # Limpiar datos previos en el treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def encriptar_dato(self):
        try:
            dato = self.label.cget("text")
            clave_publica_value = self.clave_publica.get()
            n_value = self.valor_n.get()

            
            if not clave_publica_value or not n_value:
                raise ValueError("Por favor, introduce las claves públicas y el valor de n.")

            
            clave_publica_value = int(clave_publica_value)
            n_value = int(n_value)

            encriptado = encrypt_string(dato, clave_publica_value, n_value)
            
            chunks = split_encrypted_data(encriptado)
            self.formatted_data = display_encrypted_data(chunks)
            
            self.text_encriptar.insert(tk.END, f"Dato encriptado: {self.formatted_data}\n")
            
            messagebox.showinfo("Dato Encriptado", f"El dato ha sido encriptado y mostrado en el Textbox.")
        except ValueError as ve:
            messagebox.showerror("Error", ve)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo encriptar el dato: {e}")

    
    def desencriptar_dato(self):
        dato = self.label.cget("text")
        clave_privada_value = int(self.clave_privada.get())
        n_value = int(self.valor_n.get())
        encriptado_decimal = convert_ascii_to_decimal(dato)
        encriptado_original = convertir_cadena(encriptado_decimal)
        desencriptado = decrypt_string(encriptado_original, clave_privada_value, n_value)
        self.text_encriptar.insert(tk.END, f"Dato desencriptado: {desencriptado}\n")
        
        tabla=str(self.tabla_seleccionada.get())
        nombre = str(self.label.cget("text"))
        encriptado = str(desencriptado)
        col = str(self.col)
        
        if self.modo_usuario:
            usuario_actual = self.nombre_usuario
            actualizar_datosBD(tabla, nombre, encriptado, col)
            self.mostrar_datos_usuario(usuario_actual)  
        else:
            # Estamos en modo general, agregamos el dato como de costumbre
            actualizar_datosBD(tabla, nombre, encriptado, col)
            self.mostrar_datos_tabla()  # Mostrar los datos actualizados en la tabla general
        
        

    def cargar_clave_privada(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                self.clave_privada.set(file.read())

    def cargar_clave_publica(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                # Buscar la clave pública y n en el archivo
                for line in lines:
                    parts = line.strip().split(',')
                    if len(parts) == 2:
                        self.clave_publica.set(parts[0])
                        self.valor_n.set(parts[1])

    def agregar_dato(self):
        tabla = str(self.tabla_seleccionada.get())
        nombre = str(self.label.cget("text"))
        encriptado = str(self.formatted_data)
        col = str(self.col)
        
        if self.modo_usuario:
            usuario_actual = self.nombre_usuario
            actualizar_datosBD(tabla, nombre, encriptado, col)
            self.mostrar_datos_usuario(usuario_actual)  
        else:
            # Estamos en modo general, agregamos el dato como de costumbre
            actualizar_datosBD(tabla, nombre, encriptado, col)
            self.mostrar_datos_tabla()  # Mostrar los datos actualizados en la tabla general


    def generar_claves(self):
        dato = 10000
        clave_privada, clave_publica, n = obtenerClaves(dato)
        with open('claveprivada.txt', 'w') as f:
            f.write(f"{clave_privada}")
        with open('clavepublica.txt', 'w') as f:
            f.write(f"{clave_publica},{n}")
        messagebox.showinfo("Claves Generadas", "Claves privada y pública generadas y guardadas en archivos .txt")


    def on_tree_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            item = self.tree.identify_row(event.y)
            self.col = self.tree.identify_column(event.x)

            col_index = int(self.col.replace('#', '')) - 1
            self.col = self.tree["columns"][col_index]

            value = self.tree.set(item, self.col)
    
            x, y, width, height = self.tree.bbox(item, self.col)
    
            self.show_cell_value(item, self.col, value, x, y, width, height)
        
            col = self.col
        
            self.tree.column(col, anchor='w')


    
    def show_cell_value(self, item, col, value, x, y, width, height):
        if self.label:
            self.label.destroy()
            
        self.label = tk.Label(self.tree, text=value, borderwidth=0, relief="flat", bg="#2c3e50", fg="white")
        self.label.place(x=x, y=y, width=width, height=height)
    
    def salir_modo_usuario(self):
        self.modo_usuario = False
        self.mostrar_datos_tabla()  
        self.clave_privada.set("")  
        self.clave_publica.set("")  
        self.valor_n.set("")  

        
    def cambiar_modo_usuario(self):
            self.modo_usuario = True
            ventana_usuario = tk.Toplevel(self.master)
            ventana_usuario.title("Modo de Usuario")
            ventana_usuario.configure(bg='#2c3e50')  
            

            def aceptar():
                self.nombre_usuario = entry_usuario.get().strip()  
                if self.nombre_usuario:
                    self.mostrar_datos_usuario(self.nombre_usuario)  
                    ventana_usuario.destroy()  
                else:
                    messagebox.showerror("Error", "Por favor ingresa un nombre de usuario válido.")

            
            label_usuario = tk.Label(ventana_usuario, text="Nombre de Usuario:", bg='#2c3e50', fg='white', font=('Helvetica', 10))
            label_usuario.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
            entry_usuario = tk.Entry(ventana_usuario, bg='#ecf0f1', font=('Helvetica', 10))
            entry_usuario.grid(row=0, column=1, padx=10, pady=10)
            btn_aceptar = tk.Button(ventana_usuario, text="Aceptar", command=aceptar, bg='#16a085', fg='white', font=('Helvetica', 10, 'bold'))
            btn_aceptar.grid(row=1, column=0, columnspan=2, pady=10)
        
    def mostrar_datos_usuario(self, nombre_usuario):
        tabla=str(self.tabla_seleccionada.get())
        try:
            connection = create_connection()
            id_usuario = self.obtener_id_usuario(connection, nombre_usuario)
            
            columns = fetch_table_columns(connection, tabla)
            self.tree["columns"] = columns
            for col in columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, anchor=tk.W)

            data = self.fetch_table_data_by_user(connection, tabla, id_usuario)

            self.limpiar_treeview()

            
            for row in data:
                self.tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron recuperar los datos de la tabla: {e}")

    def obtener_id_usuario(self,connection, nombre_usuario):
        cursor = connection.cursor()
        cursor.execute("SELECT idUsuario FROM usuario WHERE nombre = %s", (nombre_usuario,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            raise ValueError("Usuario no encontrado")

    def fetch_table_data_by_user(self,connection, tabla, id_usuario):
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {tabla} WHERE idUsuario = %s", (id_usuario,))
        return cursor.fetchall()


if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazEncriptacion(root)
    root.mainloop()
