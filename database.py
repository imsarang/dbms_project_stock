import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
    host="localhost", user="root", password="",
    database="stock_market_management"
)
c = mydb.cursor()

def userEmail():
    c.execute("select * from login where login_id = (select max(login_id) from login)")
    data = c.fetchall()
    df = pd.DataFrame(data,columns=['login_id','email','password'])
    email = df.iloc[0]['email']
    return email

login = userEmail()

# create table statements
def create_table():
    c.execute("create table if not exists Company(company_id INT not null auto_increment,company_name VARCHAR(200),manager_id INT,stock_id INT,no_of_stocks INT,PRIMARY KEY(company_id))")
    c.execute("create table if not exists Stock(stock_id INT not null auto_increment,owner_id INT,sold_by_id INT,buying_price INT,selling_price INT,net_profit INT,company_name varchar(200),no_of_stock int,PRIMARY KEY(stock_id))")
    c.execute("create table if not exists User(user_id INT not null auto_increment,name varchar(200),email varchar(200) unique,password varchar(200),age int,works_in varchar(200),gender varchar(200),PRIMARY KEY(user_id))")
    c.execute("create table if not exists Manager(user_id INT not null auto_increment,name varchar(200),email varchar(200) unique,password varchar(200),age int,works_in varchar(200),gender varchar(200),PRIMARY KEY(user_id))")
    c.execute("create table if not exists BankDetails(account_number int not null auto_increment,balance int,email varchar(200),bank_name varchar(200),PRIMARY KEY(account_number))")
    c.execute("create table if not exists Invoice(invoice_id int not null auto_increment,price int,user_id int,stock_id int,no_of_stocks int,action varchar(200),PRIMARY KEY(invoice_id))")
    c.execute("create table if not exists Login(login_id int not null auto_increment,email varchar(200) not null,password varchar(200) not null ,PRIMARY KEY(login_id))")

# auth
def add_login_db(email,password):
    c.execute('INSERT INTO login(email,password) VALUES (%s,%s)',
    (email,password))
    mydb.commit()

def deleteLoginRecord(email):
    c.execute('DELETE FROM login')
    mydb.commit()

def add_user_account(name,email,password,works_in,gender,age,balance,bank_name):
    c.execute('INSERT INTO user(name,email,password,age,works_in,gender) VALUES (%s,%s,%s,%s,%s,%s)',
                  (name,email,password,age,works_in,gender))
    c.execute('insert into bankDetails(balance,email,bank_name) values(%s,%s,%s)',
    (balance,email,bank_name))
    mydb.commit()

def add_company(name,no_of_stocks,price):
    # print(login)
    user_df = getUserInfo(login)
    user_id = int(user_df.iloc[0]['user_id'])
    c.execute('INSERT INTO stock(owner_id,buying_price,selling_price,company_name) VALUES (%s,%s,%s,%s)',
    (user_id,price,int(price)+10,name))
    mydb.commit()
    stock_id = getStockId()
    # c.execute('INSERT INTO manager()')
    c.execute('call assign_net_profit({})'.format(stock_id))
    c.execute('INSERT INTO company(company_name,manager_id,stock_id,no_of_stocks) VALUES (%s,%s,%s,%s)',
    (name,user_id,stock_id,no_of_stocks))
    # mydb.commit()
    # id = getCompanyByName(name)[0][0]
    # c.execute('update stock set company_name = {} where stock_id = (select max(stock_id) from stock)'.format(name))
    mydb.commit()


# all get functions

def getUserInfo(email):
    c.execute('SELECT * FROM user where email="{}"'.format(email))
    result = c.fetchall()
    df = pd.DataFrame(result,columns=['user_id','name','email','password','age','works_in','gender'])
    return df

def getUserInfoId(user_id):
    c.execute('select * from user where user_id = {}'.format(user_id))
    user_data = c.fetchall()
    return user_data

def getStockId():
    c.execute('SELECT stock_id from stock where stock_id = (select max(stock_id) from stock)')
    result = c.fetchall()
    df = pd.DataFrame(result,columns=['stock_id'])
    return int(df.iloc[0]['stock_id'])

def getCompanyDetails(user_id):
    c.execute('SELECT * from company where manager_id = "{}"'.format(user_id))
    company_data = c.fetchall()
    # df = pd.DataFrame(company_data)
    return company_data

def getStockDetails(stock_id):
    c.execute('SELECT * from stock where stock_id = "{}"'.format(stock_id))
    stock_data = c.fetchall()
    return stock_data

def getCompanyOwner(email):
    c.execute('select * from user where email = "{}"'.format(email))
    user_data = c.fetchall()
    return user_data

def getEmployees(company_name):
    c.execute('select * from  user where works_in =  {}'.format(company_name))
    employee_data  =  c.fetchall()
    return employee_data

def getManagerData(company_name):
    c.execute('select * from user where user_id = (select manager_id from company where company_name  = "{}")'.format(company_name))
    manager_data=c.fetchall()
    return manager_data

def getWorksIn(email):
    c.execute('select * from company where company_name = (select works_in from user where email = "{}")'.format(email))
    company_data = c.fetchall()
    return company_data[0][1]

def forNewOwner(company_id):
    c.execute('select user_id,name from user where user_id not in (select manager_id from company where company_id = {})'.format(company_id))
    user_id = c.fetchall()
    return user_id

def getCompany(stock_id):
    c.execute('select * from company where stock_id = "{}"'.format(stock_id))
    company_data = c.fetchall()
    return company_data

def getStock(owner_id):
    c.execute('select * from stock where owner_id != {}'.format(owner_id))
    stock_data = c.fetchall()
    return stock_data

def getCompanies(user_id):
    c.execute('select * from company where manager_id != {}'.format(user_id)) 
    company_data = c.fetchall()
    return company_data

def getCompaniesOwned(user_id):
    c.execute('select * from company where manager_id = {}'.format(user_id))
    data = c.fetchall()
    return data

def getBankDetails(email):
    c.execute('select * from bankDetails where email = "{}"'.format(email))
    data = c.fetchall()
    return data

def getCurrentStock(id):
    c.execute('select * from stock where stock_id = (select max(stock_id) from stock where owner_id = {})'.format(id))
    data = c.fetchall()
    return data

def currentStockByName(name):
    c.execute('select * from stock where company_name="{}"'.format(name))
    data = c.fetchall()
    return data

def currentCompanyName(id):
    c.execute('select * from company where company_id={}'.format(id))
    data = c.fetchall()
    return data

def stockCompanyOwned(user_id):
    c.execute('select *,sum(no_of_stock) from stock where owner_id={} group by company_name;'.format(user_id))
    data = c.fetchall()
    return data

def companyByName(name):
    c.execute('select * from company where company_name= "{}"'.format(name))
    data = c.fetchall()
    return data

def getPieChart():
    c.execute('select sum(no_of_stocks),company_name from company group by company_name')
    data=c.fetchall()
    return data
    
# update statements
def updateUser(name,password,works_in,age,email):  
    c.execute('UPDATE user SET name=%s,password=%s,works_in=%s,age=%s WHERE email=%s',
    (name,password,works_in,age,email))
    mydb.commit()
    

def updateCompany(name,buying_price,email,company_id,stock_id,old_name):
    c.execute('UPDATE company SET company_name=%s where company_id=%s',(name,company_id))
    c.execute('UPDATE stock SET buying_price=%s where stock_id=%s',(buying_price,stock_id))
    c.execute('UPDATE user SET works_in = %s where works_in = %s',(name,old_name))
    mydb.commit()

def updateStockCompanies(company_id,stock_id,user_id,old_num,new_num,balance,purchase):
    c.execute('select * from stock where owner_id = {}'.format(user_id))
    stock_data = c.fetchall()
    user_data = getUserInfoId(user_id)
    owners = forNewOwner(company_id)
    new_owner_id = owners[0][0]
    # print(old_num)
    # print(new_num)
    c.execute('update company set no_of_stocks=%s where company_id = %s',(old_num-new_num,company_id))
    # c.execute('update stock set owner_id = %s where manager_id = %s',(new_owner_id,user_id))
    
    company_name =  currentCompanyName(company_id)[0][1]
    stock_data = currentStockByName(company_name)
    c.execute('insert into stock(owner_id,buying_price,selling_price,net_profit,company_name,no_of_stock) values (%s,%s,%s,%s,%s,%s)',
    (int(user_id),int(stock_data[0][4]),int(stock_data[0][4]+10),10,company_name,new_num)
    )
    mydb.commit()
    print(purchase)
    c.execute('update bankDetails set balance = %s where email=%s',(int(balance-purchase),str(user_data[0][2])))
    c.execute('insert into invoice(price,user_id,stock_id,no_of_stocks,action) values (%s,%s,%s,%s,%s)',(int(purchase),int(user_id),stock_id,new_num,"Buy"))
    mydb.commit()

def updateSellStock(name,user_id,old_num,new_num,balance,purchase,company_stocks,price,company_id,stock_id):
    
    email = getUserInfoId(user_id)[0][2]

    if(old_num<=new_num):
        c.execute('delete from stock where owner_id={} and company_name="{}" and no_of_stock={}'.format(user_id,name,old_num))
        c.execute('update bankDetails set balance={} where email="{}"'.format((new_num * price)+balance,email))
        #c.execute('update company set no_of_stock={} where company_name={}'.format(,name))
       
    else:
        c.execute('update stock set no_of_stock={} where owner_id={} and company_name="{}" and no_of_stock={}'.format(old_num-new_num,user_id,name,old_num))
        c.execute('update bankDetails set balance={} where email="{}"'.format(purchase+balance,email))
    c.execute('update company set no_of_stocks={} where company_name="{}" and company_id={}'.format(company_stocks+new_num,name,company_id))
    c.execute('insert into invoice(price,user_id,stock_id,no_of_stocks,action) values (%s,%s,%s,%s,%s)',(int(purchase),int(user_id),stock_id,new_num,"Sell"))

    mydb.commit()
    

# delete statements
def deleteUser(email):
    user_data = getCompanyOwner(email)   
    works_in_data = getWorksIn(email) 
    print(works_in_data)
    manager_data =  getManagerData(works_in_data)
    manager_id  = manager_data[0][0]
    user_id = user_data[0][0]
    owner_email = user_data[0][2]
    c.execute('delete from user where user_id = {}'.format(user_id))
    mydb.commit()

def deleteCompany(name):
    c.execute('delete from company where company_name="{}"'.format(name))
    c.execute('delete from stock where company_name="{}"'.format(name))
    mydb.commit()



# joins
def getAllStocksOwned(user_id):
    c.execute('select * from user right outer join stock on user.user_id = stock.owner_id where user_id = {}'.format(user_id))
    join_data = c.fetchall()
    return join_data

def employeeCompany(works_in):
    c.execute('select * from company left outer join user on company.company_name=user.works_in where works_in = "{}"'.format(works_in))
    join_data = c.fetchall()
    return join_data

def allUsersCompany():
    c.execute('select * from user left outer join company on company.company_name=user.works_in')
    join_data = c.fetchall()
    return join_data

def getStocksOwnedByUser(email):
    c.execute('select * from user left outer join stock on stock.owner_id = user.user_id where email="{}"'.format(email))
    join_data = c.fetchall()
    return join_data

# aggregate functions:

def getNumberOfEmployees():
    c.execute('select works_in,count(user_id) as no_of_emp from user group by works_in')
    data= c.fetchall()
    return data

def getCompanyWithMaxStockValue():
    c.execute('select * from company where stock_id = (select stock_id from stock where buying_price = (select  max(buying_price) from  stock))')
    company_data = c.fetchall()
    return company_data

def getCompanyWithMaxNoOfStocks():
    c.execute('select * from company where no_of_stocks = (select max(no_of_stocks) from company)')
    data = c.fetchall()
    return data

def getCompanyWithMinStocks():
    c.execute('select * from company where no_of_stocks = (select min(no_of_stocks) from company)')
    data = c.fetchall()
    return data

def totalNoOfStocksInMarket(email):
    c.execute('select sum(no_of_stocks) from company')
    data = c.fetchall()
    return data[0][0]


# SET OPERATIONS
def union():
    c.execute('select user_id from user union (select manager_id from company)')
    data = c.fetchall()
    return data

def intersect():
    c.execute('select user_id from user intersect (select manager_id from company)')
    data =  c.fetchall()
    return data

def setExcept():
    c.execute('select user_id from user except select manager_id from company')
    data= c.fetchall()
    return data

def union_all():
    c.execute('select company_name,manager_id from company where manager_id in (select user_id from user union all select manager_id from company)')
    data = c.fetchall()
    return data

#function
def checkToOwn(email):
    user_df = getUserInfo(email)
    user_id = user_df.iloc[0]['user_id']
    c.execute('select user_id,check_no_company(user_id) from user where user_id = {}'.format(user_id))
    data = c.fetchall()
    return data

#sql query input
def query_1(x):
    c.execute(x)
    data = c.fetchall()
    return data