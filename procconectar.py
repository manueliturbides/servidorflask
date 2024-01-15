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

       return(mydb)
    except mysql.connector.Error as err:
      return("Error")


