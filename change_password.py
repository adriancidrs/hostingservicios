import os
import sys
var1=(sys.argv[1])
var2=(sys.argv[2])
var3=(sys.argv[3])

#MySQL
import MySQLdb
bd = MySQLdb.connect(host="localhost", user="root", passwd="root", db="ftpusers")
bd2 = MySQLdb.connect(host="localhost", user="root", passwd="root", db="mysql")
cursor = bd.cursor()
cursor2 = bd2.cursor()
consulta = "select userid from users where userid='%s';" % (var2)
cursor.execute(consulta)
resultado = cursor.fetchone()
if resultado == None:
    print "El usuario %s no exite" % (var2)
else:
    if "-sql" == sys.argv[1]:
        print "La nueva contraseña para MySQL del usuario %s es %s" % (var2,var3)
        consulta2 = "update user set password=PASSWORD('%s') where user='%s';" % (var3,var2)
        cursor2.execute(consulta2)
        basereload = "FLUSH PRIVILEGES;"
        cursor2.execute(basereload)
        bd2.commit()
    elif "-ftp" == sys.argv[1]:
        print "La nueva contraseña para Proftpd del usuario %s es %s" % (var2,var3)
        consulta3 = "update users set passwd=PASSWORD('%s') where userid='%s';" % (var3,var2)
        cursor.execute(var3)
        basereload = "FLUSH PRIVILEGES;"
        cursor.execute(basereload)
        bd.commit()
