import mysql.connector
import getpass
from cryptography.fernet import Fernet
import sys

def create_maskey():
    with open("keygen.key","wb") as f:
        key = Fernet.generate_key()
        f.write(key)
    with open("keygen.key","rb") as f:
        a = f.read()
    master_k1 = getpass.getpass(prompt="Enter MasterKey: ")
    while not master_k1:
        print("Empty Master Key!!")    
        master_k1 = getpass.getpass(prompt="Enter MasterKey: ")

    master_k2 = getpass.getpass(prompt="Enter Again: ")
    while master_k1 != master_k2:
        print("Key Did Not match!!")
        master_k2 = getpass.getpass(prompt="Enter Again: ")
    print("Key Saved")
    master_k1 = Fernet(a).encrypt(master_k1.encode())
    return master_k1
   
h = input("Enter Hostname: ")
u = input("Enter Database Username: ")
p = getpass.getpass(prompt="Enter Database Password: ")
try:
    my_conn_obj = mysql.connector.connect(
        host = h,
        user = u,
        passwd = p)
    curs = my_conn_obj.cursor(buffered=True)
except:
    print("\nIncorrect Credentials\n")
    sys.exit(0)
curs.execute("show databases")
l = []
for i in curs:
    l.append(i[0])

if "password_manager" in l:
    curs.execute("use password_manager")
    print("Database already exists !!")
else:
    curs.execute("create database password_manager")
    curs.execute("use password_manager")
    curs.execute("create table pass_tab(Site varchar(50),User varchar(30),Email varchar(30),Password varchar(100))")
    master_k = create_maskey()
    curs.execute("insert into pass_tab(Site,User,Password) values(%s,%s,%s)",("SYSTEM","MASTER",master_k))
    my_conn_obj.commit()

def add_pass():
    site = input("Site/App: ")
    user = input("User_Name: ")
    email = input("Email: ")
    password = input("Password: ")
    with open("keygen.key","rb") as f:
        a = f.read()
    password = Fernet(a).encrypt(password.encode())
    curs.execute("insert into pass_tab(Site,User,Email,Password) values(%s,%s,%s,%s)",(site,user,email,password))
    my_conn_obj.commit()
    print("Password Saved!!")

def load_pass():
    site = input("Enter Site: ")
    user = input("Enetr User: ")
    curs.execute("select password from pass_tab where site=%s and user=%s",(site,user))
    rc = curs.rowcount
    if rc==1:
        p = curs.fetchone()
        p = p[0]
        with open("keygen.key","rb") as f:
            a = f.read()
        p = Fernet(a).decrypt(p.encode())
        p = p.decode()
        print("Password for {} of user {}: ".format(site,user),p)
    else:
        print("No such user or site")


def main():
    master = False
    print("Welcome To this AmaZing password manager")
    print("""
--------------------------------------------------------------------
        1. Add a Password
        2. Load a Password
        3. Quit
--------------------------------------------------------------------   
    """)

    mk = getpass.getpass(prompt="Enter Master Key: ")
    with open("keygen.key","rb") as f:
        a = f.read()
    curs.execute("select password from pass_tab where site=%s and user=%s",("SYSTEM","MASTER"))

    p = curs.fetchone()
    p = p[0]
    p = Fernet(a).decrypt(p.encode())
    p = p.decode()
    while p!=mk:
        mk = getpass.getpass(prompt="Wrong Master key, Enter Again: ")
    master = True
    if master:
        print("WELCOME\n")
        while True:
            
                action = int(input("Enter Option: "))
                if action==3:
                    print("Bye")
                    my_conn_obj.close()
                    sys.exit(0)
                elif action==2:
                    load_pass()
                elif action==1:
                    add_pass()
                else:
                    print("Invalid Input")
            # except:
            #     print("Invalid Input")


if __name__ == "__main__":
    main()




