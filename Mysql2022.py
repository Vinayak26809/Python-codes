import mysql.connector

md = mysql.connector.connect(host="localhost", user="root", password="1234", database="mydb")
personal = md.cursor()

personal.execute("select * from personal");

dataPersonal=personal.fetchall();

if(personal.rowcount!=0):
    
    for row in dataPersonal:
        print(row);
        print("Emp Code:",row[2]);
else:
    print("No record found");
    


# print(md)
