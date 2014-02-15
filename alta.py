import sys
import os
import MySQLdb

nombre=raw_input("Introduzca el nombre de usuario:")
dominio=raw_input("Introduzca la direccion del dominio:")

#Conexion a la base de datos
bd = MySQLdb.connect(host="localhost", user="root", passwd="root", db="ftpusers")

#Comprobacion de usuario o dominio repetido
cursor = bd.cursor()
cursor.execute("select userid,domain from users where userid='%s' or domain='%s';" % (nombre,dominio))
data = cursor.fetchone()
if data != None:
        print "El usuario o dominio estan utilizados"
        quit()
else:
#Creacion de carpetas del usuario/dominio
        os.system("mkdir -p /var/www/%s" % nombre)
        os.system("chgrp -R ftpusers /var/www/%s" % nombre)
        os.system("chmod -R 775 /var/www/%s" % nombre)
#Creacion del index.html
        os.system("echo \<html\>\<head\>\<title\>Bienvenido\</title\>\<body\>\<center\>\<h1\>La pagina %s se encuentra en construccion\</h1\>\</center\>\</body\>\</html\> > /var/www/%s/index.html" % (dominio,nombre))
#Creacion del virtualhost
        host=open("ficheros/plantillavirtualhost","r")
        modif=host.read()
        host.close()
        modif=modif.replace("@nom@","%s" % nombre)
        modif=modif.replace("@domain@","%s" % dominio)
        host=open("/etc/apache2/sites-available/%s" % nombre,"w")
        host.write(modif)
        host.close
        os.system("a2ensite %s" % nombre)
        os.system("service apache2 reload")

#FTP
        os.system("pwgen -c > contra")
        contra=open("contra","r")
        leccontra=contra.read()
        contra.close()
        print "La contrasena generada para el usuario ftp es: %s" % leccontra
        uid=open("uid","r")
        uid2=uid.read()
        uid.close()
        uid2=int(uid2)
#variable uid2 con el uid nuevo
        uid2=uid2+1
        uid=open("uid","w")
        uid2=str(uid2)
        uid.write(uid2)
        uid.close()
        insert="insert into users values ('%s', PASSWORD('%s'),'%s','%s',''/var/www/%s','%s','/bin/false')" % (nombre,leccontra,uid2,500,nombre,dominio)

#MySQL
        os.system("pwgen -c > contra")
        contra=open("contra","r")
        leccontra=contra.read()
        contra.close()
        print "La contrasena generada para el usuario mysql es: %s" % leccontra
        varbase="create database %s" % nombre
        cursor.execute(varbase)
        varusu="grant all privileges on %s.* to my%s@localhost identified by '%s'" % (nombre,nombre,leccontra)
        cursor.execute(varusu)
#DNS
        fdns=open("fichero/plantilladnsd","r")
        fdns2=open("fichero/plantilladns","r")
        var=fdns.read()
        var2=fdns2.read()
        fdns.close()
        fdns2.close()
        var2=var2.replace("@dom@","%s" % dominio)
        fdns2=open("/etc/bind/named.conf.local","a")
        fdns2.write(var2)
        fdns2.close()
        var=var.replace("@dom@","%s" % dominio)
        fdns=open("/var/cache/bind/bd.%s" % (dominio),"w")
        fdns.write(var)
        fdns.close()
        os.system("service bind9 restart")

#Cierre de conexion de base de datos
        bd.close()
