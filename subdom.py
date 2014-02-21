import sys
import os
import MySQLdb

nombre=(sys.argv[1])
subdominio=(sys.argv[2])

#Conexion a la base de datos
bd = MySQLdb.connect(host="localhost", user="root", passwd="root", db="ftpusers")

#Comprobacion de usuario
cursor = bd.cursor()
cursor.execute("select domain from users where userid='%s';" % (nombre))
data = cursor.fetchone()
if data == None:
        print "El usuario no existe"
        quit()
else:

#Creacion de carpetas del usuario/dominio
        os.system("mkdir -p /var/www/%s/subdominio/%s/" % (nombre,subdominio))
        os.system("chgrp -R ftpusers /var/www/%s/" % nombre)
        os.system("chmod -R 775 /var/www/%s/" % nombre)
#Creacion del virtualhost
        host=open("ficheros/plantillavirtualhostsub","r")
        modif=host.read()
        host.close()
        modif=modif.replace("@nom@","%s" % nombre)
        modif=modif.replace("@domain@","%s" % data)
        modif=modif.replace("@sub@","%s" % subdominio)
        host=open("/etc/apache2/sites-available/%s" % subdominio,"w")
        host.write(modif)
        host.close
        os.system("a2ensite %s" % subdominio)
        os.system("service apache2 reload")
#Se cierra la conexion a la base de datos
        bd.commit()
        bd.close()
#Se anade linea al dns
        fdns=open("/var/cache/bind/db.%s" % data,"a")
        fdns.write("%s          CNAME   hosting" % subdominio)
        fdns.close()
        os.system("service bind9 reload")


