import mysql.connector as cn

db=cn.connect(host='localhost',port='3306',user='root',password='Leo@20027112',
                database='bank',auth_plugin='mysql_native_password')

cu=db.cursor()

class Banksys:

    def __init__(self):
        query='''create table if not exists customers_data(account_number bigint unsigned auto_increment primary key,
        name varchar(30) not null,age int not null,gender varchar(7) not null,balance bigint default 0,password varchar(100) not null)'''
        cu.execute(query)

    def closeBank(self):
        query='''drop table customers_data'''
        try:
            cu.execute(query)
        except Exception as ec:
            print(ec)


    def newAccount(self):

        name=input("\nEnter your name:- ")
        age=int(input("\nEnter your Age:- "))
        if age<18:
            print("\nYour Age is Less than 18  year,you can't open bank account")
            return
        amt=input("\nEnter opening balance:- ")
        gender=input("\nEnter your Gender Male/Female:- ")
        password=input('\nEnter a password for login :- ')
        query="insert into customers_data(name,age,gender,balance,password) values('{}',{},'{}',{},'{}')".format(name,age,gender,amt,password)
        cu.execute(query)
        db.commit()
        query='''select count(account_number) from customers_data'''
        cu.execute(query)
        c=cu.fetchone()
        print('''\nSuccessfully created Account with Account Number:- {}'''.format(c[0]))

    def getData(self):
        id=input("\nEnter Account Number:- ")
        psd=input('\nEnter your Account Password:- ')

        if self.checkPassword(id,psd)==False:
            print("\nyou Entered WRONG PASSWORD or WRONG ACCOUNT NUMBER\n")
            return

        query='''select name,age,gender,balance from customers_data where account_number={}'''.format(id)
        cu.execute(query)
        x=cu.fetchone()
        if self.checkId(x):
            print('''\nName:- {}\nAge:- {}\nGender:- {}\nBalance:- {}'''.format(x[0],x[1],x[2],x[3]))
        else:
            print('\nInvalid Account Number\n')

    def deposit(self):

        id=input("\nEnter the Account Number:- ")
        psd=input('\nEnter your Account Password:- ')

        if self.checkPassword(id,psd)==False:
            print("\nyou Entered WRONG PASSWORD or WRONG ACCOUNT NUMBER\n")
            return

        amount=int(input("\nEnter The Amount in multiples of 100 :- "))
        if amount<=0 or amount%100!=0:
            print("\nAmount should be greater than 100 in multiples of 100")
            return
        
        query='''update customers_data set balance=balance+{} where account_number={}'''.format(amount,id)
        cu.execute(query)
        db.commit()

        query='''select balance from customers_data where account_number={}'''.format(id)
        cu.execute(query)
        x=cu.fetchone()
        print('\nUpdated Balance is :- {} '.format(x[0]))


    def withDraw(self):

        id=input('\nEnter the Account number:- ')
        psd=input('\nEnter your account password:- ')

        if self.checkPassword(id,psd)==False:
            print("\nyou Entered WRONG PASSWORD or WRONG ACCOUNT NUMBER\n")
            return

        query='''select balance from customers_data where account_number={}'''.format(id)
        cu.execute(query)
        x=cu.fetchone()
        act_bal=x[0]

        amount=int(input('\nEnter the Amount to withdraw in multiples of 100 :- '))
        if amount>act_bal:
            print("\nLow Balance in your account than entered amount\nBalance is {}".format(act_bal))
            return

        if amount%100!=0:
           print("\nAmount should be in multiples of 100")
           return
        
        query='''update customers_data set balance=balance-{}'''.format(amount)
        cu.execute(query)
        db.commit()
        print("\nMoney withdrawn successfully\nAvailable Balance is:- {}".format(act_bal-amount))


    def checkPassword(self,id,psd):
        query='''select password from customers_data where account_number={}'''.format(id)
        cu.execute(query)
        act_psd=cu.fetchone()
        if act_psd==None:
            return False
        if psd==act_psd[0]:
            return True
        return False
        

    def checkId(self,x):
        if x==[]:
            return False
        return True




obj=Banksys()

while True:

    print('\nChoose the below options to proceed\n\n1.New Account Opening.\n2.Get Info\n3.Deposit\n4.Withdraw\n5.Exit')

    op=int(input('\nEnter your choose:- '))

    if(op==1):
        obj.newAccount()
    elif(op==2):
        obj.getData()
    elif(op==3):
        obj.deposit()
    elif(op==4):
        obj.withDraw()
    elif(op==5):
        break
