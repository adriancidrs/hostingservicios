import os
import sys
import MySQLdb


var1=(sys.argv[1])
#MySQL
bd = MySQLdb.connect(host="localhost", user="root", passwd="root", db="ftpusers")
cursor = bd.cursor()
consul = "select userid from users where domain='%s';" % (var1)
cursor.execute(consul)
resultado = cursor.fetchone()
if resultado == None:
        print "El dominio %s no existe" % (var1)
else:
        borrarbase="drop database %s" % (resultado)
        cursor.execute(borrarbase)
        permi="revoke all on *.* from my%s@localhost;" % (resultado)
        cursor.execute(permi)
        borrausua="drop user my%s@localhost" % (resultado)
        cursor.execute(borrausua)
#PROFTPD
        borracolum="delete from users where domain='%s';" % (var1)
        cursor.execute(borracolum)
        basereload = "FLUSH PRIVILEGES;"
        cursor.execute(basereload)
        bd.commit()
#Directorios
        os.system("rm -r /var/www/%s" % resultado)
        os.system("a2dissite %s" % resultado)
        os.system("rm -r /etc/apache2/sites-available/%s" % resultado)
        os.system("service apache2 reload")
        os.system("rm -r /var/cache/bind/db.%s" % var1)
        os.system("sed '/zone " + '"%s"'% var1 + "/,/};/d' /etc/bind/named.conf.local > tmp")
        os.system("mv tmp /etc/bind/named.conf.local")
        bd.close()

