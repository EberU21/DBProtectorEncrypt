import os
import tkinter as tk
from tkinter import messagebox
from interfaz import InterfazEncriptacion
from codigoRSA import obtenerClaves
from datetime import datetime

class VentanaPrincipal:
    def __init__(self, master):
        self.master = master
        master.title("Ventana Principal")
        master.geometry("300x200")
        master.configure(bg='#2c3e50')  # Fondo azul oscuro

        # Estilo para los botones
        button_style = {'bg': '#16a085', 'fg': 'white', 'activebackground': '#1abc9c', 'relief': 'flat', 'font': ('Helvetica', 10, 'bold')}

        self.btn_generar_claves_usuario = tk.Button(master, text="Generar Claves (Usuario)", command=self.generar_claves_usuario, **button_style)
        self.btn_generar_claves_usuario.pack(pady=10)

        self.btn_generar_claves_administrador = tk.Button(master, text="Generar Claves (Administrador)", command=self.generar_claves_administrador, **button_style)
        self.btn_generar_claves_administrador.pack(pady=10)

        self.btn_interfaz_encriptacion = tk.Button(master, text="Interfaz de Encriptación", command=self.abrir_interfaz_encriptacion, **button_style)
        self.btn_interfaz_encriptacion.pack(pady=10)

    def generar_claves_usuario(self):
        nombre_usuario = self.ingresar_nombre_usuario()
        if nombre_usuario:
            self.generar_claves(nombre_usuario)

    def generar_claves_administrador(self):
        if messagebox.askyesno("¿Es Administrador?", "¿Es administrador?"):
            self.generar_claves("admin")
        else:
            messagebox.showerror("Error", "Se requiere permisos de administrador para esta acción.")

    def generar_claves(self, nombre_usuario):
        try:
            # Crear la carpeta con el nombre del usuario si no existe
            carpeta_usuario = os.path.join("claves", nombre_usuario)
            if not os.path.exists(carpeta_usuario):
                os.makedirs(carpeta_usuario)

            # Generar las claves
            dato = 10000
            clave_privada, clave_publica, n = obtenerClaves(dato)

            # Generar un nombre de archivo único basado en la fecha y hora actual
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename_privada = os.path.join(carpeta_usuario, f"claveprivada_{timestamp}.txt")
            filename_publica = os.path.join(carpeta_usuario, f"clavepublica_{timestamp}.txt")

            # Guardar la clave privada en el archivo
            with open(filename_privada, 'w') as f:
                f.write(f"{clave_privada}")

            # Guardar la clave pública y n en el archivo
            with open(filename_publica, 'w') as f:
                f.write(f"{clave_publica},{n}")

            messagebox.showinfo("Claves Generadas", f"Claves privada y pública generadas y guardadas en archivos:\n{filename_privada}\n{filename_publica}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al generar las claves: {e}")

    def abrir_interfaz_encriptacion(self):
        self.master.withdraw()
        ventana_encriptacion = tk.Toplevel(self.master)
        ventana_encriptacion.title("Interfaz de Encriptación")
        ventana_encriptacion.geometry("600x400")
        ventana_encriptacion.configure(bg='#2c3e50')  # Fondo azul oscuro

        app = InterfazEncriptacion(ventana_encriptacion)

        def mostrar_ventana_principal():
            ventana_encriptacion.destroy()
            self.master.deiconify()

        app.mostrar_ventana_principal = mostrar_ventana_principal

    def ingresar_nombre_usuario(self):
        nombre_usuario = tk.simpledialog.askstring("Nombre de Usuario", "Por favor, ingrese su nombre de usuario:")
        return nombre_usuario.strip() if nombre_usuario else None

root = tk.Tk()
app = VentanaPrincipal(root)
root.mainloop()
