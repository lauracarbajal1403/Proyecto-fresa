import mysql.connector
import profesores as pro
import conexion as con
from tkinter import messagebox, END 
class dbprofesores:
    def nuevo_profesor(self, profe):        
        try:
            self.con = con.conexion()
            self.conn = self.con.open()
            self.cursor = self.conn.cursor()
            self.sql = "INSERT INTO profesores (idempleado, nombre, password, contacto, perfil, horario) VALUES ( %s, %s, %s, %s, %s, %s)"
            self.datos = (
                profe.getide(),
                profe.getnombrepro(), 
                profe.getpassw(),
                profe.getcontacto(),
                profe.getperfil(),
                profe.gethorario()
            )
            self.cursor.execute(self.sql, self.datos)
            self.conn.commit()
        except mysql.connector.Error as e:
            print(f"Error al guardar alumno: {e}")
        finally:
            self.conn.close()


    def buscar_profesor(self, profe):
        try:
            self.con = con.conexion()
            self.conn = self.con.open()
            self.cursor1=self.conn.cursor()
            auxi=None
            self.sql = "SELECT * FROM profesores WHERE idempleado = %s"
            self.cursor1.execute(self.sql, (profe.getide(),))
            row = self.cursor1.fetchone()
            self.conn.commit()
            self.conn.close()
            print("wow")
            if row[2] is not None:
                print("ok")
                auxi = pro.profesores()
                auxi.setide(row[0])
                auxi.setnombrepro(row[1])
                auxi.setpassw(row[2])
                auxi.setcontacto(row[3])
                auxi.setperfil(row[4])
                auxi.sethorario(row[5])
        except Exception as e:
            print(f"Error al buscar alumno: {e}")
            return None
        return auxi
    
    def editar_profesor(self, profe):
        self.con=con.conexion()
        self.conn=self.con.open()
        self.cursor1=self.conn.cursor()
        self.sql="update profesores set password=%s,perfil=%s, horario = %s where idempleado={}".format(profe.getide())
        self.datos=(profe.getpassw(),
                    profe.getperfil(),
                    profe.gethorario())
        self.cursor1.execute(self.sql, self.datos)
        self.conn.commit()
        self.conn.close()
    
    def eliminar_profesor(self, profe):
        self.con=con.conexion()
        self.conn=self.con.open()
        self.cursor1=self.conn.cursor()
        self.sql = "DELETE FROM profesores WHERE idempleado = %s"
        self.cursor1.execute(self.sql, (profe.getide(),))
        self.conn.commit()

    def getid_profesor(self):
        id=1
        self.con=con.conexion()
        self.conn=self.con.open()
        self.cursor=self.conn.cursor()
        self.sql="select max(idempleado) as id from profesores"
        self.cursor.execute(self.sql)
        row=self.cursor.fetchone()
        self.cursor.close()
        self.conn.close()
        if row[0] is None:
            return 1
        else:
            return row[0] + 1
    def autentificar(self, profe):
        try:
            self.con = con.conexion()
            self.conn=self.con.open()
            self.cursor1=self.conn.cursor()
            aux=None
            self.sql = "SELECT * FROM profesores WHERE idempleado = %s"
            self.cursor1.execute(self.sql, (profe.getide(),))
            print("ok")
            row = self.cursor1.fetchone()
            self.conn.commit()
            self.conn.close()
            if row is not None:
                print("quiza")
                if profe.getpassw()==row[2]:
                    aux=pro.profesores()
                    print("hola")
                    aux.setide(int(row[0]))
                    aux.setnombrepro(row[1])
                    aux.setpassw(row[2])
                    aux.setcontacto(row[3])
                    aux.setperfil(row[4])
                    aux.sethorario(row[5])
                    return aux
                else:
                    messagebox.showinfo("Error", "Contraseña incorrecta")
            else:
                messagebox.showinfo("Error", "Usuario no encontrado")
        except:
            print("NOOOOOO")