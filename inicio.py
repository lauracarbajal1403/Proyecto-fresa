import alumnos as al
import dbalumnos as dbal
import profesores as pr
import dbprofesores as dbpr
import conexion as con
import customtkinter as cust
import grupos as gr
import dbgrupos as dbgr
from tkinter import ttk, messagebox, END
cust.set_default_color_theme("blue")
class App(cust.CTk):
    def __init__(self):
        super().__init__()
        self.dbal = dbal.dbalumnos()
        self.dbpr = dbpr.dbprofesores()
        self.dbgr = dbgr.dbgrupos()
        self.geometry("500x400")
        self.pantalla_iniciosesion()
    def desbloquear_administrador(self):
        for widget in self.winfo_children():
            try:
                if isinstance(widget, (cust.CTkEntry, cust.CTkButton, cust.CTkTextbox, cust.CTkCheckBox, cust.CTkRadioButton)):
                    widget.configure(state="normal")
                elif isinstance(widget, (cust.CTkFrame, cust.CTkFrame)):
                    self.desbloquear_widgets(widget)
            except Exception as e:
                print(f"Error al desbloquear {widget}: {e}")
    def limpiar_frame(self):
        for widget in self.winfo_children():
            widget.destroy()
    def pantalla_iniciosesion(self):
        self.limpiar_frame()
        self.label = cust.CTkLabel(self, text="Inicio de sesión", font=("Courier New", 25))
        self.label.place(x = 150, y=80)
        self.usuario = cust.CTkEntry(self, placeholder_text="Usuario")
        self.usuario.place(x = 180, y=120)
        self.contrasenia = cust.CTkEntry(self, placeholder_text="Contraseña")
        self.contrasenia.place(x = 180, y=180)
        self.contrasenia.configure(show = '*')
        self.salir_button = cust.CTkButton(self, text="Salir", command=self.destroy)
        self.salir_button.place(x = 300, y=250)
        self.ingresar_button = cust.CTkButton(self, text = "Ingresar", command=self.ingresar)
        self.ingresar_button.place(x=100, y =250)
    def ingresar(self):
        global usuario_actual
        usuario = pr.profesores()
        usuario.setide(self.usuario.get())
        usuario.setpassw(self.contrasenia.get())
        dbpro = dbpr.dbprofesores()  
        userlog = dbpro.autentificar(usuario)
        if userlog:
            usuario_actual=userlog
            self.usuario_iniciado = userlog.getide()
            self.perfil_iniciado = userlog.getperfil()
            print(f"Perfil detectado: {self.perfil_iniciado}")
            messagebox.showinfo("Éxito", "Usuario correcto.")
            self.pantalla_inicio()
        else:
            print("no")
    def verificar_inicio(self):
        if self.perfil_iniciado == 'Administrador':
            self.alumnos_boton.configure(state="normal")
            self.profesores_boton.configure(state="normal")
            self.horarios_boton.configure(state="normal")
        else:
           self.alumnos_boton.configure(state="normal")
           self.profesores_boton.configure(state="normal")
    def pantalla_inicio(self):
        self.limpiar_frame()
        self.alumnos_boton = cust.CTkButton(self, text="Alumnos", state = "normal", command = self.alumnos_inicio)
        self.alumnos_boton.place(x = 200, y=100)
        self.profesores_boton = cust.CTkButton(self, text="Profesores", state = "normal", command=self.profesores_inicio)
        self.profesores_boton.place(x = 200, y=200)
        self.horarios_boton = cust.CTkButton(self, text="Grupos", state = "normal", command=self.grupos_inicio)
        self.horarios_boton.place(x = 200, y=300)
        self.cerrar_boton = cust.CTkButton(self, text = "SALIR", command = self.pantalla_iniciosesion)
        self.cerrar_boton.place(x=200, y = 350)
   


    def cargar_horario(self):
        try:
                self.con = con.conexion()
                self.conn = self.con.open()
                self.cursor = self.conn.cursor()      
                self.cursor.execute("SELECT grupo FROM grupos")
                filas = self.cursor.fetchall()
                grus = [grupos[0] for grupos in filas]
                self.grupos.configure(values=grus)
                self.horarioo.configure(values=grus)
                return filas
        except:
            print(f"Error al conectar con la base de datos")

    def desbloquear_permisos(self):
        if self.perfil_iniciado == 'Administrador':
              self.desbloquear_administrador()
        else:
            self.editar_boton.configure(state="normal")
            self.buscar_boton.configure(state="normal")

    def profesores_inicio(self):
        self.limpiar_frame()
        self.geometry("650x400")
        self.label_nombre = cust.CTkLabel(self, text = "Nombre: ")
        self.label_nombre.place(x= 100, y = 50)
        self.label_usuarioid = cust.CTkLabel(self, text="ID: ")
        self.label_usuarioid.place(x=100, y = 90)
        self.label_telefono = cust.CTkLabel(self, text = "Telefono: ")
        self.label_telefono.place(x=100, y = 130)
        self.label_password = cust.CTkLabel(self, text = "Contraseña: ")
        self.label_password.place(x= 100, y=170)
        self.perfil_label = cust.CTkLabel(self, text="Perfil: ")
        self.perfil_label.place(x=100, y = 210)
        self.perfil = cust.CTkComboBox(self, values = ["Administrador", "Profesor"])
        self.perfil.place(x= 200, y = 210)
        self.nombre = cust.CTkEntry(self, state = "disabled")
        self.nombre.place(x = 200, y =50)
        self.usuarioid = cust.CTkEntry(self, state = "normal")
        self.usuarioid.place(x=200, y =90)
        self.telefono=cust.CTkEntry(self, state = "disabled")
        self.telefono.place(x=200, y = 130)
        self.password = cust.CTkEntry(self, state = "disabled")
        self.password.place(x=200, y = 170)
        self.lbgrupo = cust.CTkLabel(self, text= "Grupo")
        self.lbgrupo.place(x=100, y = 240)
        self.grupos = cust.CTkComboBox(self)
        self.grupos.place(x=200, y = 240)
        self.cargar_horario()
        #FUNCIONES
        self.buscar_label = cust.CTkLabel(self, text="Buscar")
        self.buscar_label.place(x=100, y = 20)
        self.buscar_entrada = cust.CTkEntry(self)
        self.buscar_entrada.place(x=200, y = 20)
        self.buscar_boton = cust.CTkButton(self, text= "Buscar", width=20, command=self.buscar_profe)
        self.buscar_boton.place(x=350, y = 20)
        self.nuevo_boton = cust.CTkButton(self, text= "Nuevo", width = 20, command=self.desbloquear_permisos)
        self.nuevo_boton.place(x=50, y = 300)
        self.guardar_boton = cust.CTkButton(self, text= "Guardar", width = 20, command=self.guardar_profe)
        self.guardar_boton.place(x=120, y = 300)
        self.editar_boton = cust.CTkButton(self, text= "Editar", width = 20, command=self.modificar_profesor)
        self.editar_boton.place(x=210, y = 300)
        self.eliminar_boton = cust.CTkButton(self, text= "Eliminar", width = 20, command=self.eliminar_profesor)
        self.eliminar_boton.place(x=290, y = 300)
        self.cancelar_boton = cust.CTkButton(self, text= "Cancelar", width = 20, command=self.pantalla_inicio)
        self.cancelar_boton.place(x=390, y = 300)
        style = ttk.Style()
        style.theme_use("default")  
        style.configure("Treeview", background="#FFE4E1", fieldbackground="#FFE4E1")
        self.carrito = ttk.Treeview(self, column = ("GRUPO"), show="headings")
        self.carrito.heading("GRUPO", text="Grupo")
        self.carrito.place(x=435, y=100, width=360, height=80)
        self.agregar = cust.CTkButton(self, text = "Agregar", command = self.agregar_horario)
        self.agregar.place(x=435, y =150)
        s = self.dbpr.getid_profesor()
        self.usuarioid.delete(0, "end") 
        self.usuarioid.insert(0, str(s))
    def agregar_horario(self):
        hola = self.grupos.get()
        self.carrito.insert("", "end", values=(hola, ))
    def guardar_profe(self):
        profe = pr.profesores()
        profe.setide(int(self.usuarioid.get()))
        profe.setnombrepro(self.nombre.get())
        profe.setcontacto(self.telefono.get())
        profe.setpassw(self.password.get())
        profe.setperfil(self.perfil.get())
        for item in self.carrito.get_children():
                item_dato = self.carrito.item(item)
                articulo = item_dato['values'][0]
                prof = pr.profesores()
                prof.sethorario(articulo)
                self.dbpr.nuevo_profesor(prof)
        self.dbpr.nuevo_profesor(profe)
        messagebox.showinfo("Éxito", "Profesor guardado correctamente.")

    def buscar_profe(self):
        profe = pr.profesores()
        profe.setide(int(self.buscar_entrada.get()))
        pro=self.dbpr.buscar_profesor(profe)
        if pro is not None:
            si = pro.gethorario()
            print(si)
            self.usuarioid.delete(0, END)
            self.usuarioid.insert(0, str(pro.getide()))
            self.nombre.delete(0, END)
            self.nombre.insert(0, str(pro.getnombrepro()))
            for item in self.carrito.get_children():
                self.carrito.delete(item)
            self.carrito.insert("", "end", text=(si, ))
            self.password.delete(0, END)
            self.password.insert(0, str(pro.getpassw()))
            self.telefono.delete(0, END)
            self.telefono.insert(0, str(pro.getcontacto()))
            self.perfil.set(str(pro.getperfil()))

    def modificar_profesor(self):
        profe = pr.profesores()
        profe.setide(int(self.usuarioid.get()))
        profe.setnombrepro(self.nombre.get())
        profe.setcontacto(self.telefono.get())

        profe.setpassw(self.password.get())
        profe.setperfil(self.perfil.get())
        self.dbpr.editar_profesor(profe)
        messagebox.showinfo("Éxito", "Profesor modificado correctamente.")
    
    def eliminar_profesor(self):
        profe = pr.profesores()
        profe.setide(int(self.usuarioid.get()))
        self.usuarioid.delete(0, END)
        self.nombre.delete(0, END)
        self.password.delete(0, END)
        self.perfil.set("")
        self.telefono.delete(0, END)
        self.dbpr.eliminar_profesor(profe)
        messagebox.showinfo("Éxito", "Profesor eliminado correctamente.")
    
    def cargar_horarios(self):
        try:
                self.con = con.conexion()
                self.conn = self.con.open()
                self.cursor = self.conn.cursor()      
                self.cursor.execute("SELECT grupo FROM grupos")
                filas = self.cursor.fetchall()
                grus = [grupos[0] for grupos in filas]
                self.horarioo.configure(values=grus)
                return filas
        except:
            print(f"Error al conectar con la base de datos")
    def cargar_profesor(self):
        try:
                self.con = con.conexion()
                self.conn = self.con.open()
                self.cursor = self.conn.cursor()      
                self.cursor.execute("SELECT nombre FROM profesores")
                filas = self.cursor.fetchall()
                grus = [grupos[0] for grupos in filas]
                self.profesor.configure(values=grus)
                return filas
        except:
            print(f"Error al conectar con la base de datos")
    def alumnos_inicio(self):
            self.limpiar_frame()
            self.label_nombre = cust.CTkLabel(self, text = "Nombre: ")
            self.label_nombre.place(x= 100, y = 50)
            self.label_usuarioid = cust.CTkLabel(self, text="ID: ")
            self.label_usuarioid.place(x=100, y = 90)
            self.lbprofesor = cust.CTkLabel(self, text = "Profesor: ")
            self.lbprofesor.place(x=100, y = 130)
            self.lbmensualidad = cust.CTkLabel(self, text = "Mensualidad: ")
            self.lbmensualidad.place(x= 100, y=170)
            self.lbhorario = cust.CTkLabel(self, text = "horario")
            self.lbhorario.place(x=100, y = 240)
            self.horarioo = cust.CTkComboBox(self)
            self.horarioo.place(x=200, y = 240)
            self.cargar_horarios()
            self.nombre = cust.CTkEntry(self, state = "disabled")
            self.nombre.place(x = 200, y =50)
            self.usuarioid = cust.CTkEntry(self, state = "normal")
            self.usuarioid.place(x=200, y =90)
            self.profesor=cust.CTkComboBox(self, state = "normal")
            self.profesor.place(x=200, y = 130)
            self.cargar_profesor()
            self.mensualidad=cust.CTkEntry(self, state = "disabled")
            self.mensualidad.place(x=200, y =170)
        
            
            #FUNCIONES
            self.buscar_label = cust.CTkLabel(self, text="Buscar")
            self.buscar_label.place(x=100, y = 20)
            self.buscar_entrada = cust.CTkEntry(self)
            self.buscar_entrada.place(x=200, y = 20)
            self.buscar_boton = cust.CTkButton(self, text= "Buscar", width=20, command=self.buscar_alumno)
            self.buscar_boton.place(x=350, y = 20)
            self.nuevo_boton = cust.CTkButton(self, text= "Nuevo", width = 20, command=self.desbloquear_administrador)
            self.nuevo_boton.place(x=50, y = 300)
            self.guardar_boton = cust.CTkButton(self, text= "Guardar", width = 20, command=self.guardar_alumno)
            self.guardar_boton.place(x=120, y = 300)
            self.editar_boton = cust.CTkButton(self, text= "Editar", width = 20, command=self.modificar_alumno)
            self.editar_boton.place(x=210, y = 300)
            self.eliminar_boton = cust.CTkButton(self, text= "Eliminar", width = 20, command=self.eliminar_alumno)
            self.eliminar_boton.place(x=290, y = 300)
            self.cancelar_boton = cust.CTkButton(self, text= "Cancelar", width = 20, command=self.pantalla_inicio)
            self.cancelar_boton.place(x=390, y = 300)
            d = self.dbal.getid_alumno()
            self.usuarioid.delete(0, "end") 
            self.usuarioid.insert(0, str(d))
    
    def guardar_alumno(self):
        alumno = al.alumnos()
        alumno.setcodigo(int(self.usuarioid.get()))
        alumno.setnombre(self.nombre.get())
        alumno.setcodpro(self.profesor.get())
        alumno.setnomina(self.mensualidad.get())
        alumno.setgrupo(self.horarioo.get())
        self.dbal.nuevo_alumno(alumno)
        messagebox.showinfo("Éxito", "Alumno guardado correctamente.")

    def buscar_alumno(self):
        alumno = al.alumnos()
        alumno.setcodigo(int(self.buscar_entrada.get()))
        alum=self.dbal.buscar_alumno(alumno)
        if alum is not None:
            self.usuarioid.delete(0, END)
            self.usuarioid.insert(0, str(alum.getcodigo()))
            self.nombre.delete(0, END)
            self.nombre.insert(0, str(alum.getnombre()))
            self.profesor.set(str(alum.getcodpro()))
            self.horarioo.set(str(alum.getgrupo()))
            self.mensualidad.delete(0, END)
            self.mensualidad.insert(0, str(alum.getnomina()))
            
        

    def modificar_alumno(self):
            alumno = al.alumnos()
            alumno.setcodigo(int(self.buscar_entrada.get()))
            alumno.setnombre(self.nombre.get())
            alumno.setcodpro(self.profesor.get())
            alumno.setnomina(self.mensualidad.get())
            alumno.setgrupo(self.horarioo.get())
            self.dbal.editar_alumno(alumno)
            messagebox.showinfo("Éxito", "Alumno modificado correctamente.")
        
    def eliminar_alumno(self):
            alumno = al.alumnos()
            alumno.setcodigo(int(self.usuarioid.get()))
            self.usuarioid.delete(0, END)
            self.nombre.delete(0, END)
            self.mensualidad.delete(0, END)
            self.profesor.set("")
            self.dbal.eliminar_alumno(alumno)
            messagebox.showinfo("Éxito", "Alumno eliminado correctamente.")
    def grupos_inicio(self):
                self.limpiar_frame()
                self.label_horario = cust.CTkLabel(self, text = "Horario: ")
                self.label_horario.place(x= 100, y = 50)
                self.label_usuarioid = cust.CTkLabel(self, text="ID: ")
                self.label_usuarioid.place(x=100, y = 90)
                self.horario = cust.CTkEntry(self, state = "disabled")
                self.horario.place(x = 200, y =50)
                self.id = cust.CTkEntry(self, state = "normal")
                self.id.place(x=200, y =90)
                #FUNCIONES
                self.buscar_label = cust.CTkLabel(self, text="Buscar")
                self.buscar_label.place(x=100, y = 20)
                self.buscar_entrada = cust.CTkEntry(self)
                self.buscar_entrada.place(x=200, y = 20)
                self.buscar_boton = cust.CTkButton(self, text= "Buscar", width=20, command=self.buscar_grupo)
                self.buscar_boton.place(x=350, y = 20)
                self.nuevo_boton = cust.CTkButton(self, text= "Nuevo", width = 20, command=self.desbloquear_administrador)
                self.nuevo_boton.place(x=50, y = 300)
                self.guardar_boton = cust.CTkButton(self, text= "Guardar", width = 20, command=self.guardar_grupo)
                self.guardar_boton.place(x=120, y = 300)
                self.editar_boton = cust.CTkButton(self, text= "Editar", width = 20, command=self.modificar_grupo)
                self.editar_boton.place(x=210, y = 300)
                self.eliminar_boton = cust.CTkButton(self, text= "Eliminar", width = 20, command=self.eliminar_grupo)
                self.eliminar_boton.place(x=290, y = 300)
                self.cancelar_boton = cust.CTkButton(self, text= "Cancelar", width = 20, command=self.pantalla_inicio)
                self.cancelar_boton.place(x=390, y = 300)
                d = self.dbgr.getid_grupo()
                self.id.delete(0, "end") 
                self.id.insert(0, str(d))
    def guardar_grupo(self):
        grupo = gr.grupos()
        grupo.setid(int(self.id.get()))
        grupo.sethorario(self.horario.get())
        self.dbgr.nuevo_grupo(grupo)
        messagebox.showinfo("Éxito", "Grupo guardado correctamente.")

    def buscar_grupo(self):
        grupo = gr.grupos()
        grupo.setid(int(self.buscar_entrada.get()))
        gru=self.dbgr.buscar_grupo(grupo)
        if gru is not None:
            self.id.delete(0, END)
            self.id.insert(0, str(gru.getid()))
            self.horario.delete(0, END)
            self.horario.insert(0, str(gru.gethorario()))
        

    def modificar_grupo(self):
            grupo = gr.grupos()
            grupo.setid(int(self.buscar_entrada.get()))
            grupo.sethorario(self.horario.get(), )
            self.dbgr.editar_grupo(grupo)
            messagebox.showinfo("Éxito", "Grupo modificado correctamente.")
        
    def eliminar_grupo(self):
            grupo = gr.grupos()
            grupo.setid(int(self.id.get()))
            self.id.delete(0, END)
            self.horario.delete(0, END)
            self.dbgr.eliminar_grupo(grupo)
            messagebox.showinfo("Éxito", "Grupo eliminado correctamente.")
if __name__ == "__main__":
    app = App()
    app.mainloop()