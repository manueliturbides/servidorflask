def conectServerDatabase():
    import mysql.connector
    
    try:
              #crear base de datos
       mydb = mysql.connector.connect(host="127.0.0.1",user="root",password="00100267590")

       return(mydb)
    except Exception as e:
      print(e +" error")
      return("Error")

def conectUserDatabase(nombre):    
    import mysql.connector
    
    try:
       #crear base de datos
       mydb = mysql.connector.connect(host="127.0.0.1",user="root",password="00100267590")
       mycursor = mydb.cursor()
       mycursor.execute("create database if not exists "+nombre)
       
       mydb=mysql.connector.connect(host="127.0.0.1",user="root",password="00100267590",port = 3306,database=nombre)
       mycursor = mydb.cursor(dictionary=True)
 
       mycursor.execute("Create table if not exists Company(nombre varchar(255),direccion varchar(255),logo MEDIUMBLOB,telefono varchar(255),pais varchar(255));")
       mycursor.execute("CREATE TABLE IF NOT EXISTS Users (id varchar(255) NOT NULL PRIMARY KEY,parent varchar(255),nombre varchar(255),apellido varchar(255),email varchar(255),password varchar(255),permissions varchar(255));")
       mycursor.execute("CREATE TABLE IF NOT EXISTS Facturas (id INT NOT NULL AUTO_INCREMENT primary key,plan varchar(255),total int,promocode varchar(255),suscriptionid varchar(255),fecha date);")


     
       mycursor.execute("create table if not exists solicit(id MEDIUMINT NOT NULL AUTO_INCREMENT,nosolic int(4),cedula varchar(15),\
       nombres varchar(100),apellidos varchar(100),provincia varchar(45),direccion varchar(100),telefono varchar(45),sector varchar(45),nacionalidad varchar(45),nombrepila varchar(45),\
       email varchar(45),comentario varchar(450),financiamiento float,plazo int,formapago varchar(45),interes float,mora float,\
       cedulafiador varchar(15),nombrefiador varchar(100),telefonofiador varchar(15),tipofinanciamiento varchar(15),valorcuotas float,deudatotal float,aprobado varchar(1),\
       aprobadopor varchar(25),edad varchar(10),sexo varchar(45),direccionfiador varchar(100),celular varchar(45),\
       ecivil varchar(15),dependientes varchar(15),user varchar(100),fecha_crea date, fecha_mod date, PRIMARY KEY(id))")
 
       mycursor.execute("create table if not exists amort(id mediumint not null auto_increment,noprest int,nosolic int,cedula varchar(15),nocuota int,\
                        fecha date,cuota float,capital float,interes float,balance float, status varchar(1),vpagcap float,vpagint float,\
                        descuento float,pagadodescuento varchar(1),pcuotas int,vpagmora float,user varchar(45),fecha_crea date,fecha_mod date,primary key(id))")
 
       mycursor.execute("create table if not exists prestamo(noprest mediumint not null auto_increment,nosolic int,fecha date,periodos int,\
                        cedula varchar(45),nombres varchar(45),apellidos varchar(45),solicitado float,plazo int,interes float,mora float,status varchar(1),vpagint float,vpagcap float,vpagmora float,pcuotas int,fcancel date,fultpago date,\
                        norecibo int,montoult float,user varchar(45),fecha_crea date,fecha_mod date,PRIMARY KEY(noprest))")
       
       mycursor.execute("create table if not exists pagosres(norecibo MEDIUMINT NOT NULL AUTO_INCREMENT,noprest int,nosolic int,cedula varchar(15),\
         nocuota int,cuota float,mora float,fecha date,vpagint float,vpagmora float,vpagcap float,descinte float,fecha1 date,\
         descmora float,sucursal varchar(15),user varchar(100),fecha_crea date, fecha_mod date,timestamp datetime, \
         tipodepago varchar(45),aprobacion varchar(45), numerotarjeta varchar(45),PRIMARY KEY(norecibo))")
 
       mycursor.execute("create table if not exists pagos(norecibo MEDIUMINT NOT NULL AUTO_INCREMENT,noprest int,nosolic int,cedula varchar(15),\
         nocuota int,cuota float,mora float,fecha date,vpagint float,vpagmora float,vpagcap float,descinte float,fecha1 date,\
         descmora float,sucursal varchar(15),user varchar(100),fecha_crea date, \
         balance float,fecha_mod date,timestamp datetime,PRIMARY KEY(norecibo))")
       
       return(mydb)
    except Exception as e:
      print(e)
      return(e)


def conectUserDatabaseVendedor(nombre):    
    import mysql.connector
    
    try:
              #crear base de datos
       mydb = mysql.connector.connect(host="127.0.0.1",user="root",password="00100267590")
       mycursor = mydb.cursor()
       mycursor.execute("create database if not exists "+nombre)
       

       mydb=mysql.connector.connect(host="127.0.0.1",user="root",password="00100267590",port = 3306,database=nombre)
       mycursor = mydb.cursor(dictionary=True)
       
       mycursor.execute("Create table if not exists Clientes(id varchar(255) PRIMARY KEY,email varchar(255),producto varchar(255),fecha date);")
       mycursor.execute("CREATE TABLE IF NOT EXISTS User (id varchar(255),Nombre varchar(255),email varchar(255),password varchar(255),promcode varchar(255),paypal varchar(255));")
       mycursor.execute("CREATE TABLE IF NOT EXISTS Facturas (id INT NOT NULL AUTO_INCREMENT primary key,fecha date,numSuscrip int,retired varchar(255));")
       return(mydb)
    except Exception as e:
      print(e +" error")
      return("Error")


