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
	os.system("pwgen -c |cat > contra")
	contrasena=open("contra","r")
	cont=contrasena.read()
	contrasena
