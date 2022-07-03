import sqlite3
from tkinter import *
from tkinter import messagebox

root = Tk()
root.title('ATM SIMULATOR')
root.geometry('450x400')


TRIES = 0

#create db
conn = sqlite3.connect('Bank_Accounts.db')
#create cursor
c = conn.cursor()

#create table in db

# c.execute('''CREATE TABLE Accounts(
#                Name text,
#                Pin integer,
#                Balance Float
#               )
#          ''')

def query_all():
    conn = sqlite3.connect('Bank_Accounts.db')
    #create cursor
    c = conn.cursor()

    c.execute('SELECT *, oid FROM Accounts')
    records = c.fetchall()

    #commit changes
    conn.commit()
    #close connection
    conn.close()
    return records

def delete(oid):
    #create db or conect to one
    conn = sqlite3.connect('Bank_Accounts.db')
    #create cursor
    c = conn.cursor()

    c.execute('DELETE from Accounts')# WHERE oid= '+ int(oid))

    #commit changes
    conn.commit()
    #close connection
    conn.close()


def create_acct_win():
    global createwin
    global name
    global pin
    global balance

    createwin = Tk()
    createwin.title('Create Account')
    createwin.geometry('400x300')

    name_lb = Label(createwin, text='Enter Name: ')
    name_lb.grid(row=0, column=0, pady=(10, 0))

    pin_lb = Label(createwin, text='Enter Pin: ')
    pin_lb.grid(row=1, column=0)

    balance_lb = Label(createwin, text='Deposit: ')
    balance_lb.grid(row=2, column=0)

    name = Entry(createwin, width= 30)
    name.grid(row=0, column=1, padx=20, pady=(10, 0))

    pin = Entry(createwin, width= 30)
    pin.grid(row=1, column=1)

    balance = Entry(createwin, width= 30)
    balance.grid(row=2, column=1)

    acct_create = Button(createwin, text='Create Now', command=create_acct)
    acct_create.grid(row=3, column=0, columnspan=2, padx=10, pady=(15,0), ipadx=146)

def create_acct():
    
    conn = sqlite3.connect('Bank_Accounts.db')
    c = conn.cursor()
    c.execute('INSERT INTO Accounts VALUES(:Name, :Pin, :Balance)',
    {
        'Name': name.get(),
        'Pin': pin.get(),
        'Balance': float(balance.get())
    }
    )
    accounts = query_all()
    createwin.destroy()
    messagebox.showinfo('information', f'Account created Successfully! \n Account Number is: {accounts[-1][-1] + 1}')

    #commit changes
    conn.commit()
    #close connection
    conn.close()

    print('Account Created Succesfully')

def login_win():
    global loginwin
    global enter_pin
    global a_num
    
    loginwin = Tk()
    loginwin.title('Login Account')
    loginwin.geometry('400x200')

    card_lb = Label(loginwin, text='Card Received !')
    card_lb.grid(row=0, column=0)

    num_lb = Label(loginwin, text='Account No: ')
    num_lb.grid(row=1, column=0)
    a_num = Entry(loginwin, width= 30)
    a_num.grid(row=1, column=1, padx=20, pady=(10, 0))

    pin_lb = Label(loginwin, text='Enter Pin: ')
    pin_lb.grid(row=2, column=0)
    enter_pin = Entry(loginwin, width= 30)
    enter_pin.grid(row=2, column=1, padx=20, pady=(10, 0))

    login_acct = Button(loginwin, text='Login', command=login)
    login_acct.grid(row=3, column=0, columnspan=2, padx=10, pady=(15,0), ipadx=146)

def login():
    global TRIES 
    global account

    conn = sqlite3.connect('Bank_Accounts.db')
    c = conn.cursor()
    
    acct_num = a_num.get()
    c.execute('SELECT *, oid from Accounts WHERE oid='+acct_num)
    account = c.fetchall()

    while TRIES < 3:
        pin_value = int(enter_pin.get())
        if pin_value in account[0]:
            messagebox.showinfo('information', f'Pin Correct \n Welcome {account[0][0]}')
            main_win()
            break
        else:
            messagebox.showerror('error', f'Pin Incorrect \n {3-TRIES} more trie(s)')
            TRIES = TRIES + 1
            loginwin.destroy()
            login_win()
    if TRIES >= 3:
        messagebox.showerror('error', f'Tries Limit Reached !!')
        loginwin.destroy()

def main_win():
    global mainwin
    global check_bal
    global withdraw
    global deposit
    global transfer
    global pin_value

    mainwin = Tk()
    mainwin.title('Welcome')
    mainwin.geometry('400x400')

    conn = sqlite3.connect('Bank_Accounts.db')
    c = conn.cursor()

    pin_value = enter_pin.get()

    c.execute('SELECT *, oid FROM Accounts WHERE pin = '+ pin_value)
    records = c.fetchall()

    check_bal = Button(mainwin, text='Check Balance', command=check_balance)
    check_bal.grid(row=1, column=0, columnspan=2, padx=10, pady=(15,0), ipadx=146)
    
    withdraw = Button(mainwin, text='Withdraw', command=withdrawal_win)
    withdraw.grid(row=2, column=0, columnspan=2, padx=10, pady=(15,0), ipadx=146)
    
    deposit = Button(mainwin, text='Deposit', command=deposit_win)
    deposit.grid(row=3, column=0, columnspan=2, padx=10, pady=(15,0), ipadx=146)
    
    transfer = Button(mainwin, text='Transfer', command=Transfer)
    transfer.grid(row=4, column=0, columnspan=2, padx=10, pady=(15,0), ipadx=146)

    loginwin.destroy()

def check_balance():
    global balwin
    balwin = Tk()
    balwin.title('Account Balance')
    balwin.geometry('400x200')

    balance = account[0][-2]
    name = Label(balwin, text=f'Hello {account[0][0]}')
    name.grid(row=0, column=0)
    
    acct_bal = Label(balwin, text=f'Account Balance: {balance}')
    acct_bal.grid(row=1, column=0)

def withdrawal_win():
    global withdrawalwin
    global w_amount
    global w_pin
    withdrawalwin = Tk()
    withdrawalwin.geometry('400x400')
    withdrawalwin.title('Withdraw')

    balance = account[0][-2]

    acct_bal = Label(withdrawalwin, text=f'Account Balance: {balance}')
    acct_bal.grid(row=0, column=0)

    amount_lb = Label(withdrawalwin, text='Enter Amount to Withdraw: ')
    amount_lb.grid(row=1, column=0)

    w_amount = Entry(withdrawalwin, width= 30)
    w_amount.grid(row=2, column=0, padx=20, pady=(10, 0))

    pin_lb = Label(withdrawalwin, text='Enter Pin: ')
    pin_lb.grid(row=3, column=0)

    w_pin = Entry(withdrawalwin, width= 30)
    w_pin.grid(row=3, column=1, padx=20, pady=(10, 0))

    w_sub = Button(withdrawalwin, text='Withdraw', command=Withdrawal)
    w_sub.grid(row=4, column=0, columnspan=2, padx=10, pady=(15,0), ipadx=146)

def Withdrawal():
    amount = int(w_amount.get())
    wd_pin = int(w_pin.get())

    if wd_pin in account[0]:
        if amount > account[0][-2]:
            withdrawalwin.destroy()
            messagebox.showerror('error', f'Insufficient Balance')
        else:
            new_bal = account[0][-2] - amount
            conn = sqlite3.connect('Bank_Accounts.db')
            c = conn.cursor()
            c.execute('''
                        UPDATE Accounts SET
                        Balance = :Balance
                        WHERE oid = :oid
                    ''',
                    {
                            'Balance': new_bal,
                            'oid': account[0][-1]
                    })

            conn.commit()
            conn.close()
            withdrawalwin.destroy()
            messagebox.showinfo('information', f'Transaction Successful')

    else:
         withdrawalwin.destroy()
         messagebox.showerror('error', f'Pin Incorrect')

def deposit_win():
    global depositwin
    global d_amount
    global d_pin
    depositwin = Tk()
    depositwin.geometry('400x400')
    depositwin.title('Deposit')

    balance = account[0][-2]

    acct_bal = Label(depositwin, text=f'Account Balance: {balance}')
    acct_bal.grid(row=0, column=0)

    amount_lb = Label(depositwin, text='Enter Amount to Deposit: ')
    amount_lb.grid(row=1, column=0)

    d_amount = Entry(depositwin, width= 30)
    d_amount.grid(row=2, column=0, padx=20, pady=(10, 0))

    pin_lb = Label(depositwin, text='Enter Pin: ')
    pin_lb.grid(row=3, column=0)

    d_pin = Entry(depositwin, width= 30)
    d_pin.grid(row=3, column=1, padx=20, pady=(10, 0))

    d_sub = Button(depositwin, text='Deposit', command=Deposit)
    d_sub.grid(row=4, column=0, columnspan=2, padx=10, pady=(15,0), ipadx=146)



def Deposit():
    amount = int(d_amount.get())
    dp_pin = int(d_pin.get())

    if dp_pin in account[0]:
            new_bal = account[0][-2] + amount
            conn = sqlite3.connect('Bank_Accounts.db')
            c = conn.cursor()
            c.execute('''
                        UPDATE Accounts SET
                        Balance = :Balance
                        WHERE oid = :oid
                    ''',
                    {
                            'Balance': new_bal,
                            'oid': account[0][-1]
                    })

            conn.commit()
            conn.close()
            depositwin.destroy()
            messagebox.showinfo('information', f'Transaction Successful')

    else:
         depositwin.destroy()
         messagebox.showerror('error', f'Pin Incorrect')







def Transfer(pin, amount, account_number):
    conn = sqlite3.connect('Bank_Accounts.db')
    c = conn.cursor()

    c.execute('SELECT * FROM Accounts where oid = ' + account_number)
    record = c.fetchall()
    ben_pin = str(record[0][1])

    Withdrawal(pin, amount)
    Deposit(ben_pin, amount)

    #commit changes
    conn.commit()
    #close connection
    conn.close()

print(query_all())

f_name_lb = Label(root, text='Hidden Leaf Bank 🗽')
f_name_lb.grid(row=0, column=0, pady=(10, 0))

create_acct_btn = Button(root, text='Create Account', command=create_acct_win)
create_acct_btn.grid(row=0, column=0, columnspan=2, padx=10, pady=5, ipadx=139)

login_btn = Button(root, text='Input Card (Account No.)', command=login_win)
login_btn.grid(row=1, column=0, columnspan=2, padx=10, pady=5, ipadx=139)
#commit changes
conn.commit()
#close connection
conn.close()
mainloop()