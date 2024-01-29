def conect():

    
    import mysql.connector
    
    try:
              #crear base de datos
       mydb = mysql.connector.connect(host="127.0.0.1",user="root",password="manueliturbides00100267590")
       mycursor = mydb.cursor()
       mycursor.execute("create database if not exists finanzas1")
       

       mydb=mysql.connector.connect(host="127.0.0.1",user="root",password="manueliturbides00100267590",port = 3306,database="finanzas1")
       return(mydb)
    except mysql.connector.Error as err:
      return("Error")


