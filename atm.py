import sqlite3
from tkinter import *
from tkinter import messagebox

from pyparsing import col
from atm_utils import *

TRIES = 0
global root
root = Tk()
root.title('Root Win')
root.geometry('100x100')
root.configure(background="#fbfaf5")
Button(root, text='Quit', command=lambda: root.destroy()).grid(row=0, column=0)

def start_win():
    global root2
    root2 = Tk()
    root2.title('KNAB EHT')
    root2.geometry('470x400')
    root2.configure(background="#efefef")

    f_name_lb = Label(root2, text='WELCOME TO KNAB EHT!', anchor='center')
    f_name_lb.grid(row=0, column=2, pady=(10, 0), padx=5)

    lb = LabelFrame(root2, text='Available Services')
    lb.grid(row=1, column=0, columnspan=4, pady=(10, 0), padx=10)

    create_acct_btn = Button(lb, text='Create Account', command=create_acct_win)
    create_acct_btn.grid(row=2, column=0, columnspan=3, padx=10, pady=5, ipadx=139)

    login_btn = Button(lb, text='Input Card (Account No.)', command=login_win)
    login_btn.grid(row=3, column=0, columnspan=3, padx=10, pady=5, ipadx=139)

    Button(root2, text='Quit', command=lambda: root.destroy()).grid(row=5, column=3, pady=(10, 10))

def create_acct_win():
    global createwin
    createwin = Tk()
    createwin.title('KNAB EHT')
    createwin.geometry('450x350')

    fr = LabelFrame(createwin, text='Create Account')
    fr.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

    name_lb = Label(fr, text='Enter Name: ')
    name_lb.grid(row=1, column=0, pady=(10, 0))

    pin_lb = Label(fr, text='Enter Pin: ')
    pin_lb.grid(row=2, column=0)

    balance_lb = Label(fr, text='Deposit: ')
    balance_lb.grid(row=3, column=0)

    name = Entry(fr, width= 30)
    name.grid(row=1, column=1, padx=20, pady=(10, 0))

    pin = Entry(fr, width= 30)
    pin.grid(row=2, column=1)

    balance = Entry(fr, width= 30)
    balance.grid(row=3, column=1)

    acct_create = Button(fr, text='Create Now', command=lambda: create_acct(name.get(), pin.get(), balance.get()))
    acct_create.grid(row=4, column=1, padx=10, pady=(15,10), ipadx=120)

    Button(createwin, text='Quit', command=lambda: createwin.destroy()).grid(row=6, column=1, pady=15)

    root2.destroy()

def create_acct(name, pin, balance):
    conn = sqlite3.connect('Bank_Accounts.db')
    c = conn.cursor()
    c.execute('INSERT INTO Accounts VALUES(:Name, :Pin, :Balance)',
    {
        'Name': name,
        'Pin': pin,
        'Balance': float(balance)
    }
    )
    accounts = query_all()
    createwin.destroy()
    messagebox.showinfo('information', f'Account created Successfully! \n Account Number is: {accounts[-1][-1] + 1}')

    conn.commit()
    conn.close()

    print('Account Created Succesfully')

    start_win()

def login_win():
    global loginwin
    
    loginwin = Tk()
    loginwin.title('KNAB EHT')
    loginwin.geometry('350x200')

    card_lb = Label(loginwin, text='Card Received !', anchor='center')
    card_lb.grid(row=0, column=0, columnspan=2)

    num_lb = Label(loginwin, text='Account No: ')
    num_lb.grid(row=1, column=0)
    a_num = Entry(loginwin, width= 30)
    a_num.grid(row=1, column=1, padx=20, pady=(10, 0))

    pin_lb = Label(loginwin, text='Enter Pin: ')
    pin_lb.grid(row=2, column=0)
    enter_pin = Entry(loginwin, width= 30)
    enter_pin.grid(row=2, column=1, padx=20, pady=(10, 0))

    login_acct = Button(loginwin, text='Login', command=lambda: login(a_num.get(), enter_pin.get()))
    login_acct.grid(row=3, column=0, columnspan=2, padx=10, pady=(25,0), ipadx=146)

def login(acct_number, pin):
    global TRIES 
    global acct_num

    acct_num = acct_number
    conn = sqlite3.connect('Bank_Accounts.db')
    c = conn.cursor()
    
    c.execute('SELECT *, oid from Accounts WHERE oid='+acct_num)
    account = c.fetchall()

    pin_value = int(pin)
    if TRIES >= 3:
        messagebox.showerror('error', f'Tries Limit Reached !!')
        loginwin.destroy()
        return
    
    if pin_value in account[0]:
        messagebox.showinfo('information', f'Pin Correct \n Welcome {account[0][0]}')
        main_win()
        
    else:
        messagebox.showerror('error', f'Pin Incorrect \n {3-TRIES} more trie(s)')
        print(TRIES, "try: ", pin_value)
        TRIES = TRIES + 1
        loginwin.destroy()
        login_win()
    
    account = query(acct_num)
    

def main_win():
    global mainwin

    mainwin = Tk()
    mainwin.title('KNAB EHT')
    mainwin.geometry('265x300')

    fr = LabelFrame(mainwin, text='Welcome')
    fr.grid(row=0, column=0, pady=10, padx=10)

    check_bal = Button(fr, text='Balance', command=check_balance)
    check_bal.config(width=30)
    check_bal.grid(row=1, column=0, padx=10, pady=(15,0))
    
    withdraw = Button(fr, text='Withdraw', command=withdrawal_win)
    withdraw.config(width=30)
    withdraw.grid(row=2, column=0, padx=10, pady=(15,0))
    
    deposit = Button(fr, text='Deposit', command=deposit_win)
    deposit.config(width=30)
    deposit.grid(row=3, column=0, padx=10, pady=(15,0))
    
    transfer = Button(fr, text='Transfer', command=transfer_win)
    transfer.config(width=30)
    transfer.grid(row=4, column=0, padx=10, pady=(15,10))

    Button(mainwin, text='Quit', command=lambda: mainwin.destroy()).grid(row=5, column=0, pady=(15, 0))

    loginwin.destroy()
    root2.destroy

def check_balance():
    global balwin
    balwin = Tk()
    balwin.title('Account Balance')
    balwin.geometry('400x200')
    
    account = query(acct_num)
    balance = account[0][-2]

    name = Label(balwin, text=f'Hello {account[0][0]}')
    name.grid(row=0, column=0)
    
    acct_bal = Label(balwin, text=f'Account Balance: {balance}')
    acct_bal.grid(row=1, column=0)

def withdrawal_win():
    global withdrawalwin
    withdrawalwin = Tk()
    withdrawalwin.geometry('400x400')
    withdrawalwin.title('Withdraw')

    account = query(acct_num)
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

    w_sub = Button(withdrawalwin, text='Withdraw', command=lambda: Withdrawal(int(w_amount.get()), int(w_pin.get())))
    w_sub.grid(row=4, column=0, columnspan=2, padx=10, pady=(15,0), ipadx=146)

def Withdrawal(amount, wd_pin):
    account = query(acct_num)
    if wd_pin in account[0]:
        if amount > account[0][-2]:
            withdrawalwin.destroy()
            messagebox.showerror('error', f'Insufficient Balance')
        else:
            account = query(acct_num)
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

    depositwin = Tk()
    depositwin.geometry('400x400')
    depositwin.title('Deposit')
    account = query(acct_num)
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

    d_sub = Button(depositwin, text='Deposit', command=lambda: Deposit(int(d_amount.get()), int(d_pin.get())))
    d_sub.grid(row=4, column=0, columnspan=2, padx=10, pady=(15,0), ipadx=146)

def Deposit(amount, dp_pin):
    account = query(acct_num)
    if dp_pin in account[0]:
            account = query(acct_num)
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

def transfer_win():
    global transferwin
    transferwin = Tk()
    transferwin.geometry('400x500')
    transferwin.title('Transfer')

    account = query(acct_num)
    balance = account[0][-2]

    acct_bal = Label(transferwin, text=f'Account Balance: {balance}')
    acct_bal.grid(row=0, column=0)

    bene_acct_lb = Label(transferwin, text='Enter Beneficiary Account: ')
    bene_acct_lb.grid(row=1, column=0)

    bene_acct = Entry(transferwin, width=30)
    bene_acct.grid(row=2, column=0)

    amount_lb = Label(transferwin, text='Enter Amount to Transfer: ')
    amount_lb.grid(row=3, column=0)

    t_amount = Entry(transferwin, width= 30)
    t_amount.grid(row=4, column=0, padx=20, pady=(10, 0))

    pin_lb = Label(transferwin, text='Enter Pin: ')
    pin_lb.grid(row=5, column=0)

    t_pin = Entry(transferwin, width= 30)
    t_pin.grid(row=5, column=1, padx=20, pady=(10, 0))

    t_sub = Button(transferwin, text='Transfer', command=lambda: Transfer(bene_acct.get(), t_amount.get(), t_pin.get()))
    t_sub.grid(row=6, column=0, columnspan=2, padx=10, pady=(15,0), ipadx=146)

def Transfer(account_number, amount, t_pin):
    account = query(acct_num)
    conn = sqlite3.connect('Bank_Accounts.db')
    c = conn.cursor()

    c.execute('SELECT * FROM Accounts where oid = ' + account_number)
    account = query(acct_num)
    bene_account = c.fetchall()

    if int(t_pin) == account[0][1]:
        if float(amount) > account[0][2]:
            messagebox.showerror('error', f'Insufficient Balance')
        else:
            conn = sqlite3.connect('Bank_Accounts.db')
            c = conn.cursor()
            c.execute('''
                        UPDATE Accounts SET
                        Balance = :Balance
                        WHERE oid = :oid
                    ''',
                    {
                            'Balance': account[0][2] - float(amount),
                            'oid': account[0][-1]
                    })

            c.execute('''
                        UPDATE Accounts SET
                        Balance = :Balance
                        WHERE oid = :oid
                    ''',
                    {
                            'Balance': bene_account[0][2] + float(amount),
                            'oid': account_number
                    })

            messagebox.showinfo('information', f'Transaction Successful')
    else:
        messagebox.showerror('error', f'Pin Incorrect')
    
    transferwin.destroy()
    #commit changes
    conn.commit()
    #close connection
    conn.close()

print(query_all())
start_win()
mainloop()

