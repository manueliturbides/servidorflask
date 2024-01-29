import procedimiento
import globales
import mysql.connector

x = 0
if x == 0:
#try:
  #def database():
    conectado = procedimiento.conectmotor()
    print(conectado)
    if conectado == "Error":
       #crear base de datos
       try:
          mydb = mysql.connector.connect(host=globales.db1_host,user=globales.db1_user,password=globales.db1_user_password)
          mycursor = mydb.cursor()
          mycursor.execute("create database if not exists prestamo1")
          
          conectado = "OK"
          conectado = procedimiento.conectmotor()
          
          
       except Exception as e: 
          print(e)
          conectado == "Error"

    if conectado != "Error":
       mycursor = conectado.cursor()

       mycursor.execute("create table if not exists sucursal(sucursal INT(11),descripcion varchar(50),creado char(50),modificado char(50),fechamod date)")

       mycursor.execute("create table if not exists producto(id MEDIUMINT NOT NULL AUTO_INCREMENT,fecha date, marca varchar(25),modelo varchar(25),\
       colore varchar(15),chasis varchar(25),costo float,precio float,mprecio float,condicion varchar(25),\
       estado varchar(45),ubicacion int(2),localizacion varchar(100),noprest int(4),nombres varchar(50),apellidos varchar(50),fincauto date,\
       matestado varchar(50),matfecha date,matnombre varchar(50),matrecibido varchar(25),inventario varchar(5),user varchar(100),fecha_crea date, fecha_mod date,sucursal varchar(15),usuario varchar(45),PRIMARY KEY(id))")
       
       mycursor.execute("create table if not exists reingre(id MEDIUMINT NOT NULL AUTO_INCREMENT,fecha date, marca varchar(25),modelo varchar(25),\
       colore varchar(15),chasis varchar(25),costo float,precio float,mprecio float,codicion varchar(1),\
       estado varchar(1),ubicacion int(2),user varchar(100),fecha_crea date,sucursal varchar(15), fecha_mod date,usuario varchar(15),PRIMARY KEY(id))")
       
       mycursor.execute("create table if not exists prestamo(id MEDIUMINT NOT NULL AUTO_INCREMENT,noprest int(4),nosolic int(8),fecha date,periodos varchar(25),\
       nombres varchar(50),apellidos varchar(50),cantsol float,plazo int(4),interes float,fecha1 date,\
       tipoprest varchar(25),garantia varchar(15),status varchar(1),vpagint float,vpagcap float,vpagmora float,pcuotas int(4),\
       cedula varchar(15),fcancel date,fultpago date,norecibo int(8),montoult float,chasis varchar(25),chance varchar(100),\
       llamada float,user varchar(100),fecha_crea date, sucursal varchar(15), fecha_mod date,timestamp datetime,usuario varchar(45),PRIMARY KEY(id))")
      
       mycursor.execute("create table if not exists amort(id MEDIUMINT NOT NULL AUTO_INCREMENT,noprest int(10),\
       nosolic int(10),cedula varchar(15),nocuota int(10),debitocap float,capital float,bcecap float,debitoint float,\
       interes float,bceint float,descinte float,bceconj float,mora float,moraori float,fecha date,vpagcuota float,\
       vpagmora float,vpagcap float,vpagint float, codcar varchar(10),status varchar(2),tprestamo int(1),sucursal varchar(15),user varchar(100),fecha_crea date, fecha_mod date,usuario varchar(45),PRIMARY KEY(id))")

       mycursor.execute("create table if not exists factmot(secuencia MEDIUMINT NOT NULL AUTO_INCREMENT,fecha date,nombres varchar(45),\
       apellidos varchar(45),cedula varchar(15),marca varchar(15),modelo varchar(15),colore varchar(15),chasis varchar(20),\
       precio float,inicial float,financia float,interes float,cuotas int(4),vcuotas float,deudadat float,sucursal varchar(15),noprest int(10),ncf varchar(15),user varchar(100),fecha_crea date, fecha_mod date, PRIMARY KEY(secuencia))")
 
       mycursor.execute("create table if not exists solicit(id MEDIUMINT NOT NULL AUTO_INCREMENT,nosolic int(4),noprest int(8),\
       fecha date,apellidos varchar(45),nombres varchar(45),direccion varchar(100),urb varchar(45),telefono varchar(15),celular varchar(45),email varchar(45),\
       apodo varchar(45),comentario varchar(1000),depend int(4),dirpadres varchar(100),edad int(4),cedula varchar(15),ecivil varchar(45),\
       cantsol float,razon varchar(100),plazo int(3),fechaini date,empresa varchar(45),dirtrab varchar(100),teltrab varchar(100),\
       tiempotrab int(4),fiador varchar(100),fiadordir varchar(100),urbfiad varchar(100),fiadortel varchar(15),edadfiad int(3),fiadorced varchar(15),\
       chasis varchar(45),status char(1),sucursal varchar(15),user varchar(100),fecha_crea date, fecha_mod date, PRIMARY KEY(id))")
 
       mycursor.execute("create table if not exists inicial(id MEDIUMINT NOT NULL AUTO_INCREMENT,fecha date,nombres varchar(45), \
       apellidos varchar(45),cedula varchar(15),chasis varchar(20),valor float,sucursal varchar(15),user varchar(100),fecha_crea date, fecha_mod date,PRIMARY KEY(id))")
 
       mycursor.execute("create table if not exists previnc(id MEDIUMINT NOT NULL AUTO_INCREMENT,fecha date,nuprest int,nombres varchar(45),\
         apellidos varchar(45),cedula varchar(15),estado varchar(1),incautador varchar(45),cedincaut varchar(15),\
         chasis varchar(45),valor float,sucursal varchar(15),user varchar(100),fecha_crea date, fecha_mod date,PRIMARY KEY(id))")
 
       mycursor.execute("create table if not exists pagosres(norecibo MEDIUMINT NOT NULL AUTO_INCREMENT,noprest int,nosolic int,cedula varchar(15),\
         nocuota int,cuota float,mora float,fecha date,vpagint float,vpagmora float,vpagcap float,descinte float,fecha1 date,\
         descmora float,sucursal varchar(15),user varchar(100),fecha_crea date, fecha_mod date,timestamp datetime, PRIMARY KEY(norecibo))")
 
       mycursor.execute("create table if not exists pagos(norecibo MEDIUMINT NOT NULL,noprest int,nosolic int,cedula varchar(15),\
         nocuota int,cuota float,mora float,fecha date,vpagint float,vpagmora float,vpagcap float,descinte float,fecha1 date,\
         descmora float,sucursal varchar(15),user varchar(100),fecha_crea date, fecha_mod date,timestamp datetime)")
 
       mycursor.execute("create table if not exists pagoscanc(norecibo MEDIUMINT NOT NULL,noprest int,nosolic int,cedula varchar(15),\
         nocuota int,cuota float,mora float,fecha date,vpagint float,vpagmora float,vpagcap float,descinte float,fecha1 date,\
         descmora float,sucursal varchar(15),user varchar(100),fecha_crea date, fecha_mod date,timestamp datetime)")
 
       mycursor.execute("create table if not exists excedente(id MEDIUMINT NOT NULL AUTO_INCREMENT,noprest int,fecha date,valor float,\
        sucursal varchar(15),user varchar(100),fecha_crea date, fecha_mod date, PRIMARY KEY(id))")
 
       mycursor.execute("create table if not exists increg(id MEDIUMINT NOT NULL AUTO_INCREMENT,fecha date,nuprest int,incsec int,\
         nombres varchar(45),apellidos varchar(45),cedula varchar(15),valor float,fechacobro date,estado varchar(1),incautador varchar(45),\
         sucursal varchar(15),cedulaincaut varchar(15),chasis varchar(45),fincauto date,user varchar(100),fecha_crea date, fecha_mod date, tipoincauto varchar(15),razon varchar(200),\
         PRIMARY KEY(id))")

       mycursor.execute("create table if not exists llamadas(id MEDIUMINT NOT NULL AUTO_INCREMENT,fecha date,noprest int,\
       sucursal varchar(15), nombres varchar(100), apellidos varchar(100),razoncanc varchar(200),cedula varchar(15),valor float,razon varchar(250),user varchar(100),fecha_crea date, fecha_mod date,PRIMARY KEY(id))")

       mycursor.execute("create table if not exists pagollam(id MEDIUMINT NOT NULL AUTO_INCREMENT,fecha date,noprest int,valor float,estado varchar(1),\
       sucursal varchar(15), user varchar(100),fecha_crea date, fecha_mod date, PRIMARY KEY(id))")

       mycursor.execute("create table if not exists maestinc(id MEDIUMINT NOT NULL AUTO_INCREMENT,fecha date,cedula varchar(15),nombres varchar(45),\
       sucursal varchar(15), user varchar(100),fecha_crea date, fecha_mod date,PRIMARY KEY(id))")
       
       mycursor.execute("create table if not exists pagomatri(id MEDIUMINT NOT NULL AUTO_INCREMENT,noprest int,fecha date,nombres varchar(100),\
        apellidos varchar(100),cedula varchar(15),marca varchar(15),modelo varchar(15),\
       sucursal varchar(15), colore varchar(15),chasis varchar(100),valor float,ncf varchar(100),user varchar(100),fecha_crea date, fecha_mod date,PRIMARY KEY(id))")
 
       mycursor.execute("create table if not exists traspaso(id MEDIUMINT NOT NULL AUTO_INCREMENT,noprest int,fecha date,\
        nombres varchar(100),apellidos varchar(100),cedula varchar(15),marca varchar(15),modelo varchar(15),colore varchar(15),\
        sucursal varchar(15),chasis varchar(45), valor float, tnombres varchar(100),tapellidos varchar(100),tcedula varchar(15), \
        user varchar(100),fecha_crea date, fecha_mod date,PRIMARY KEY(id))")


       mycursor.execute("create table if not exists sucursal(id MEDIUMINT NOT NULL AUTO_INCREMENT,sucursal int,descripcion varchar(100),\
       sucursal varchar(15),creado varchar(50),modificado varchar(50), fecha_mod date, PRIMARY KEY(id))")

       mycursor.execute("create table if not exists expedienteunico(id MEDIUMINT NOT NULL AUTO_INCREMENT,cedula varchar(20) not null unique, PRIMARY KEY(id))")

       mycursor.execute("create table if not exists gastos(id MEDIUMINT NOT NULL AUTO_INCREMENT,fecha date,tipogastos varchar(100),\
                         referencia varchar(200),descripcion varchar(255),valor float,sucursal varchar(15),user varchar(100),fecha_crea date, fecha_mod date,PRIMARY KEY(id))")

       
       mycursor.execute("create index noprestamort on amort(noprest) ")
       mycursor.execute("create index noprestprest on prestamo(noprest) ")
       mycursor.execute("create index chasisidx on producto(chasis)")
 
       conectado.commit()
       conectado.close()
       

       #except Exception as e:
       
       #   print(e)

       #mycursor.close()
       #procedimiento.mensaje("OK","Listo").exec()
#except Exception as e:
#       print(str(e))  