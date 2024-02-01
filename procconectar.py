
def conectUserDatabase(nombre):    
    import mysql.connector
    
    try:
       #crear base de datos
       mydb = mysql.connector.connect(host="127.0.0.1",user="root",password="00100267590")
       mycursor = mydb.cursor()
       mycursor.execute("create database if not exists "+nombre)
       
       mydb=mysql.connector.connect(host="127.0.0.1",user="root",password="00100267590",port = 3306,database=nombre)
       mycursor = mydb.cursor(dictionary=True)
       sqlCompany = "Create table if not exists Company(nombre varchar(255),direccion varchar(255),logo BLOB,telefono varchar(255));"
       sqlUsers = "CREATE TABLE IF NOT EXISTS Users (id varchar(255) NOT NULL PRIMARY KEY,parent varchar(255),nombre varchar(255),apellido varchar(255),email varchar(255),password varchar(255),permissions varchar(255));"
       mycursor.execute(sqlUsers)
       mycursor.execute(sqlCompany)

       mycursor.execute("create table if not exists solicit(id MEDIUMINT NOT NULL AUTO_INCREMENT,nosolic int(4),noprest int(8),\
       fecha date,apellidos varchar(45),nombres varchar(45),direccion varchar(100),urb varchar(45),telefono varchar(15),celular varchar(45),email varchar(45),\
       apodo varchar(45),comentario varchar(1000),depend int(4),dirpadres varchar(100),edad int(4),cedula varchar(15),ecivil varchar(45),\
       cantsol float,razon varchar(100),plazo int(3),fechaini date,empresa varchar(45),dirtrab varchar(100),teltrab varchar(100),\
       tiempotrab int(4),fiador varchar(100),fiadordir varchar(100),urbfiad varchar(100),fiadortel varchar(15),edadfiad int(3),fiadorced varchar(15),\
       chasis varchar(45),status char(1),sucursal varchar(15),user varchar(100),fecha_crea date, fecha_mod date, PRIMARY KEY(id))")
 

       return(mydb)
    except mysql.connector.Error as err:
      return("Error")


