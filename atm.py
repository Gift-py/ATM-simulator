#importing libraries
from tkinter import *
import tkinter as tk
from customtkinter import *
import customtkinter as ctk
from tkinter import messagebox
from atm_utils import *

#setting default theme for gui
ctk.set_appearance_mode('light')
ctk.set_default_color_theme('dark-blue')

#global variable for pin trial
TRIES = 0

#root window init
global root
root = ctk.CTk()
root.title('Root Win')
root.geometry('400x400')
f_name_lb = CTkLabel(root, text='PYTHON ATM SIMULATOR')
f_name_lb.grid(row=0, column=0, columnspan=2, padx=90, pady=15)
ctk.CTkButton(root, text='Quit', command=lambda: root.destroy()).grid(row=1, column=0)
ctk.CTkButton(root, text='Start', command=lambda: [root.destroy(), start_win()]).grid(row=1, column=1)

#Start page gui
def start_win():  
    """
        gui design for start window
    """  
    global root2
    root2 = CTk()
    root2.title('KNAB EHT')
    root2.geometry('400x400')

    f_name_lb = CTkLabel(root2, text='WELCOME TO KNAB EHT!')
    f_name_lb.grid(row=0, column=1, columnspan=2, padx=90, pady=15)

    lb = CTkFrame(root2, width=300, height=200, corner_radius=8)
    lb.grid(row=1, column=1, padx=90, pady=10)

    f_name_lb = CTkLabel(lb, text='ATM Services')
    f_name_lb.grid(row=2, column=0, columnspan=3, padx=(50, 50), pady=(30, 5))

    create_acct_btn = CTkButton(lb, text="Create Account", command=create_acct_win)
    create_acct_btn.grid(row=3, column=0, columnspan=3, padx=(50, 50), pady=(15,5))

    login_btn = CTkButton(lb, text="Input Card (Acct No.)", command=lambda: [reset_tries(TRIES), login_win()])
    login_btn.grid(row=4, column=0, columnspan=3, padx=(50, 50), pady=(5, 50))
    
    CTkButton(root2, text='Quit', command=lambda: [root2.destroy(), messagebox.showinfo('information', f'Thank You for Banking with us 😄👋🏿')]).grid(row=5, column=1, padx=90, pady=(15, 10))

    root2.mainloop()


def create_acct_win():
    """
        gui design for account creation window
    """
    global createwin
    createwin = CTk()
    createwin.title('KNAB EHT')
    createwin.geometry('400x350')

    f_name_lb = CTkLabel(createwin, text='Create Account')
    f_name_lb.grid(row=0, column=0, padx=50, pady=(20,5))

    fr = CTkFrame(createwin, width=300, height=300)
    fr.grid(row=1, column=0, padx=20, pady=(10, 15))

    name_lb = CTkLabel(fr, text='Enter Name: ')
    name_lb.grid(row=1, column=0, pady=(10, 0))

    pin_lb = CTkLabel(fr, text='Enter Pin: ')
    pin_lb.grid(row=2, column=0)

    balance_lb = CTkLabel(fr, text='Deposit: ')
    balance_lb.grid(row=3, column=0)

    name = CTkEntry(fr, width= 150, corner_radius=8, border_width=1, placeholder_text='Full Name')
    name.grid(row=1, column=1, padx=20, pady=(10, 0))

    pin = CTkEntry(fr, width= 150, corner_radius=8, border_width=1, placeholder_text='4 digit pin')
    pin.grid(row=2, column=1)

    balance = CTkEntry(fr, width= 150, corner_radius=8, border_width=1, placeholder_text='Initial Deposit')
    balance.grid(row=3, column=1)

    acct_create = CTkButton(fr, text='Create Now', command=lambda: create_acct(name.get(), pin.get(), balance.get()))
    acct_create.grid(row=4, column=1, padx=10, pady=(15,10), ipadx=30)

    CTkButton(createwin, text='Quit', command=lambda: [createwin.destroy(), start_win()]).grid(row=6, column=0, padx=50, pady=15)

    root2.destroy()

    createwin.mainloop()

def create_acct(name, pin, balance=0):
    """
        collects user's name, pin and initial deposit\n
        stores this information in the database\n
        and generates an account number for the new user
    """
    if(name == '' or pin == ''):
        messagebox.showerror('error', 'You need a name and a pin number to create an account')
    else:
        assert pin.isdigit() and len(pin) == 4, messagebox.showerror('error', 'You need a four digit pin please 😅')
        if balance == '':
            messagebox.showinfo('information', 'Your Bank Balance is NGN 0.00')
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
    """
        gui design for login window
    """
    global loginwin
    
    loginwin = CTk()
    loginwin.title('KNAB EHT')
    loginwin.geometry('350x200')

    card_lb = CTkLabel(loginwin, text='Card Received !')
    card_lb.grid(row=0, column=0, columnspan=2)

    num_lb = CTkLabel(loginwin, text='Account No: ')
    num_lb.grid(row=1, column=0)
    
    a_num = CTkEntry(loginwin, width= 150, corner_radius=8, border_width=1)
    a_num.grid(row=1, column=1, padx=20, pady=(10, 0))

    pin_lb = CTkLabel(loginwin, text='Enter Pin: ')
    pin_lb.grid(row=2, column=0)

    enter_pin = CTkEntry(loginwin, width= 150, corner_radius=8, border_width=1)
    enter_pin.grid(row=2, column=1, padx=20, pady=(10, 0))

    login_acct = CTkButton(loginwin, text='Login', command=lambda: login(a_num.get(), enter_pin.get()))
    login_acct.grid(row=3, column=0, columnspan=2, padx=10, pady=(25,0), ipadx=30)

    loginwin.mainloop()

def login(acct_number, pin):
    """
        Login account functionality\n
        collects the user's account number and pin\n
        queries database to return account details and grant access\n
        user get only 3 attempts at loggin in
    """
    global TRIES 
    global acct_num

    assert acct_number != '', messagebox.showerror('error', 'Please, Input your account number')
    assert acct_number.isdigit(), messagebox.showerror('error', 'Letters not Allowed')
    assert pin != '', messagebox.showerror('error', 'Please, Input your pin')
    assert pin.isdigit(), messagebox.showerror('error', 'Letters Forbidden, Input your pin')

    acct_num = acct_number
    conn = sqlite3.connect('Bank_Accounts.db')
    c = conn.cursor()
        
    c.execute('SELECT *, oid from Accounts WHERE oid='+acct_num)
    account = c.fetchall()

    if account == []:
        messagebox.showerror('error', 'This Account... Does not exist...')
        messagebox.showinfo('information', 'If you do not have an account try creating one.. It is really easy')
        return

    pin_value = int(pin)
    if TRIES >= 3:
        messagebox.showerror('error', f'Tries Limit Reached !!')
        loginwin.destroy()
        return
        
    if pin_value == account[0][1]:
        messagebox.showinfo('information', f'Pin Correct \n Welcome {account[0][0]}')
        main_win()
            
    else:
        messagebox.showerror('error', f'Pin Incorrect \n {3-TRIES} more trie(s)')
        print(TRIES, "try: ", pin_value)
        TRIES = TRIES + 1
        loginwin.destroy()
        login_win()

def main_win():
    """
        gui design from main window
    """
    global mainwin
    account = query(acct_num)
    name = account[0][0]
    mainwin = CTk()
    mainwin.title('KNAB EHT')
    mainwin.geometry('265x350')

    f_name_lb = CTkLabel(mainwin, text=f'Welcome {name}')
    f_name_lb.grid(row=0, column=0, padx=60, pady=10)

    fr = CTkFrame(mainwin)
    fr.grid(row=1, column=0, pady=10, padx=60)

    check_bal = CTkButton(fr, text='Check Balance', command=check_balance)
    check_bal.grid(row=2, column=0, padx=10, pady=(15,0))
    
    withdraw = CTkButton(fr, text='Withdraw', command=withdrawal_win)
    withdraw.grid(row=3, column=0, padx=10, pady=(15,0))

    deposit = CTkButton(fr, text='Deposit', command=deposit_win)
    deposit.grid(row=4, column=0, padx=10, pady=(15,0))
    
    transfer = CTkButton(fr, text='Transfer', command=transfer_win)
    transfer.grid(row=5, column=0, padx=10, pady=(15,10))

    CTkButton(mainwin, text='Quit', command=lambda: [mainwin.destroy(), messagebox.showinfo
    ('information', f'Thank You for Banking with us 😄👋🏿')]).grid(row=6, column=0, pady=(15, 10))

    loginwin.destroy()
    root2.destroy()

    mainwin.mainloop()

def check_balance():
    """
        window displays basic account details\n
        i.e account balance, account name, and account number
    """
    global balwin
    balwin = CTk()
    balwin.title('KNAB EHT')
    balwin.geometry('400x400')
    
    account = query(acct_num)
    balance = account[0][-2]

    f_name_lb = CTkLabel(balwin, text='Account Details')
    f_name_lb.grid(row=0, column=1, padx=50, pady=(20,5))

    fr = CTkFrame(balwin)
    fr.grid(row=1, column=0, pady=10, padx=60, columnspan=3)

    name = CTkLabel(fr, text=f'Account Name:')
    name.grid(row=2, column=0, pady=15)

    a_name = CTkLabel(fr, text=f'{account[0][0]}', anchor='w')
    a_name.grid(row=2, column=2, pady=15)

    num = CTkLabel(fr, text=f'Account Number:')
    num.grid(row=3, column=0, pady=15)

    a_num = CTkLabel(fr,  text = f'{account[0][-1]}', anchor='w')
    a_num.grid(row=3, column=2, pady=15)

    acct_bal = CTkLabel(fr, text=f'Account Balance:')
    acct_bal.grid(row=4, column=0, pady=(15, 10))

    bal = CTkLabel(fr, text=f'{balance}', anchor='w')
    bal.grid(row=4, column=2, pady=15)

    CTkButton(balwin, text='Quit', command=lambda: balwin.destroy()).grid(row=5, column=1, padx=75, pady=(15, 0))

    balwin.mainloop()

def withdrawal_win():
    """
        gui design for withdrawal window
    """
    global withdrawalwin
    withdrawalwin = CTk()
    withdrawalwin.geometry('400x400')
    withdrawalwin.title('KNAB EHT')

    account = query(acct_num)
    balance = account[0][-2]

    f_name_lb = CTkLabel(withdrawalwin, text='Withdrawal Menu')
    f_name_lb.grid(row=0, column=0, padx=60, pady=10, columnspan=2)

    fr = CTkFrame(withdrawalwin)
    fr.grid(row=1, column=0, pady=10, padx=40, columnspan=2)

    acct_bal = CTkLabel(fr, text=f'Account Balance: {balance}')
    acct_bal.grid(row=2, column=0, columnspan=2)

    amount_lb = CTkLabel(fr, text='Withdrawal Amount: ')
    amount_lb.grid(row=3, column=0)

    w_amount = CTkEntry(fr, width= 150, corner_radius=8, border_width=1)
    w_amount.grid(row=3, column=1, padx=20, pady=(10, 0))

    pin_lb = CTkLabel(fr, text='Enter Pin: ')
    pin_lb.grid(row=4, column=0)

    w_pin = CTkEntry(fr, width= 150, corner_radius=8, border_width=1)
    w_pin.grid(row=4, column=1, padx=20, pady=(10, 0))

    w_sub = CTkButton(fr, text='Withdraw', command=lambda: Withdrawal(w_amount.get(), w_pin.get()))
    w_sub.grid(row=5, column=0, columnspan=2, padx=20, pady=(15,10))

    CTkButton(withdrawalwin, text='Quit', command=lambda: withdrawalwin.destroy()).grid(row=6, column=0, columnspan=2, padx=60, pady=(15, 0))

    withdrawalwin.mainloop()

def Withdrawal(amount, wd_pin):
    """
        collects the amount (in naira) the user wants to withdraw\n
        and user's pin, returns a massage box showing the transaction status\n
        (successful or unsuccessful -- as the case maybe)
    """
    account = query(acct_num)

    assert amount != '', messagebox.showerror('error', 'Please, Enter withdrawal amount')
    assert amount.isdigit(), messagebox.showerror('error', 'Letters Forbidden')
    assert wd_pin != '', messagebox.showerror('error', 'Piease, Input your pin')
    assert wd_pin.isdigit(), messagebox.showerror('error', 'Letters Forbidden, Input your pin')

    amount, wd_pin = int(amount), int(wd_pin)

    if wd_pin == account[0][1]:
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
    """
        gui display for deposit window
    """
    global depositwin

    depositwin = CTk()
    depositwin.geometry('400x400')
    depositwin.title('Deposit')
    
    account = query(acct_num)
    balance = account[0][-2]

    f_name_lb = CTkLabel(depositwin, text='Deposit Menu')
    f_name_lb.grid(row=0, column=0, padx=60, pady=10, columnspan=2)

    fr = CTkFrame(depositwin)
    fr.grid(row=1, column=0, pady=10, padx=40, columnspan=2)

    acct_bal = CTkLabel(fr, text=f'Account Balance: {balance}')
    acct_bal.grid(row=1, column=0, columnspan=2)

    amount_lb = CTkLabel(fr, text='Deposit Amount: ')
    amount_lb.grid(row=2, column=0)

    d_amount = CTkEntry(fr, width= 150, corner_radius=8, border_width=1,)
    d_amount.grid(row=2, column=1, padx=20, pady=(10, 0))

    pin_lb = CTkLabel(fr, text='Enter Pin: ')
    pin_lb.grid(row=3, column=0)

    d_pin = CTkEntry(fr, width= 150, corner_radius=8, border_width=1,)
    d_pin.grid(row=3, column=1, padx=20, pady=(10, 0))

    d_sub = CTkButton(fr, text='Deposit', command=lambda: Deposit(d_amount.get(), d_pin.get()))
    d_sub.grid(row=4, column=0, columnspan=2, padx=10, pady=(15,10))

    CTkButton(depositwin, text='Quit', command=lambda: depositwin.destroy()).grid(row=6, column=0, columnspan=2, padx=60, pady=(15, 0))

    depositwin.mainloop()

def Deposit(amount, dp_pin):
    """
        collects the amount (in naira) the user wants to deposit\n
        and user's pin, returns a massage box showing the transaction status\n
        (successful or unsuccessful -- as the case maybe)
    """
    account = query(acct_num)

    assert amount != '', messagebox.showerror('error', 'Please, Enter Deposit amount')
    assert amount.isdigit(), messagebox.showerror('error', 'You can\'t deposit letters')
    assert dp_pin != '', messagebox.showerror('error', 'Please, Input your pin')
    assert dp_pin.isdigit(), messagebox.showerror('error', 'Your pin are not letters')

    amount, dp_pin = int(amount), int(dp_pin)

    if dp_pin == account[0][1]:
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
    """
        gui design for transfer window
    """
    bank_list = ['KNAB EHT','UBA', 'Access Bank', 'First Bank', 'GT Bank']
    global transferwin
    transferwin = CTk()
    transferwin.geometry('400x500')
    transferwin.title('KNAB EHT')

    account = query(acct_num)
    balance = account[0][-2]

    f_name_lb = CTkLabel(transferwin, text='Transfer Menu')
    f_name_lb.grid(row=0, column=0, padx=60, pady=10, columnspan=2)

    fr = CTkFrame(transferwin)
    fr.grid(row=1, column=0, pady=10, padx=40, columnspan=2)

    acct_bal = CTkLabel(fr, text=f'Account Balance: {balance}')
    acct_bal.grid(row=2, column=0, columnspan=2)

    bene_acct_lb = CTkLabel(fr, text='Beneficiary Account: ')
    bene_acct_lb.grid(row=3, column=0)

    bene_acct = CTkEntry(fr, width=150, corner_radius=8, border_width=1,)
    bene_acct.grid(row=3, column=1)

    amount_lb = CTkLabel(fr, text='Amount: ')
    amount_lb.grid(row=4, column=0)

    t_amount = CTkEntry(fr, width= 150, corner_radius=8, border_width=1,)
    t_amount.grid(row=4, column=1, padx=20, pady=(10, 0))

    pin_lb = CTkLabel(fr, text='Enter Pin: ')
    pin_lb.grid(row=5, column=0)

    t_pin = CTkEntry(fr, width=150, corner_radius=8, border_width=1,)
    t_pin.grid(row=5, column=1, padx=20, pady=(10, 0))

    pin_lb = CTkLabel(fr, text='Choose Bank: ')
    pin_lb.grid(row=6, column=0)

    bank_choice = CTkComboBox(master=fr, width=150, corner_radius=8, border_width=1, values=bank_list)
    bank_choice.grid(row=6, column=1, padx=20, pady=(10, 0))

    t_sub = CTkButton(fr, text='Transfer', command=lambda: t_confirm_win(bene_acct.get(), t_amount.get(), bank_choice.get(), t_pin.get()))
    t_sub.grid(row=7, column=0, columnspan=2, padx=10, pady=(15,10))

    CTkButton(transferwin, text='Quit', command=lambda: transferwin.destroy()).grid(row=8, column=0, columnspan=2, padx=60, pady=(15, 0))

    transferwin.mainloop()

def t_confirm_win(account_number, amount, bank_name, pin):
    """
       confirmation window for bank transfer
    """
    assert account_number != '', messagebox.showerror('error', 'Please Enter account number')
    assert account_number.isdigit(), messagebox.showerror('error', 'Please enter a valid numeric account number')
    assert amount != '', messagebox.showerror('error', 'Please, Enter amount to transfer')
    assert amount.isdigit(), messagebox.showerror('error', 'You can\'t transfer letters 💀')
    assert pin != '', messagebox.showerror('error', 'Please, you need to type in your 4 digit pin')
    assert pin.isdigit(), messagebox.showerror('error', 'Your pin are not letters 😩')
    
    if bank_name == 'KNAB EHT':
        bene_acct = query(account_number)
        assert bene_acct != [], messagebox.showerror('error', 'This account does not exist in our bank 🤔')
        bene_name = bene_acct[0][0]
    else:
        bene_acct = ['Another Bank']
        bene_name = '-- UNAVAILABLE --'
        messagebox.showwarning('warning', f'Transfering to foreign bank ({bank_name})')

    global confirmwin
    confirmwin = CTk()
    confirmwin.geometry('400x400')
    confirmwin.title('KNAB EHT')

    f_name_lb = CTkLabel(confirmwin, text='Confirm Transfer')
    f_name_lb.grid(row=0, column=0, padx=30, pady=10, columnspan=2)

    fr = CTkFrame(confirmwin)
    fr.grid(row=1, column=0, pady=10, padx=40, columnspan=2)

    bene_acct_lb = CTkLabel(fr, text='Beneficiary Account: ')
    bene_acct_lb.grid(row=2, column=0)

    bene_acct = CTkLabel(fr, text=account_number)
    bene_acct.grid(row=2, column=1)

    amount_lb = CTkLabel(fr, text='Amount: ')
    amount_lb.grid(row=3, column=0)

    t_amount = CTkLabel(fr, text=amount)
    t_amount.grid(row=3, column=1, padx=20, pady=(10, 0))

    pin_lb = CTkLabel(fr, text='Beneficiary Name: ')
    pin_lb.grid(row=4, column=0)

    t_pin = CTkLabel(fr, text=bene_name)
    t_pin.grid(row=4, column=1, padx=20, pady=(10, 0))

    bank_lb = CTkLabel(fr, text='Bank Name: ')
    bank_lb.grid(row=5, column=0)

    bank_name_lb = CTkLabel(fr, text=bank_name)
    bank_name_lb.grid(row=5, column=1, padx=20, pady=(10, 0))

    t_sub = CTkButton(confirmwin, text='Transfer', command=lambda:[Transfer(account_number, amount, pin, bank_name), confirmwin.destroy()])
    t_sub.grid(row=6, column=1, pady=(15,0))

    CTkButton(confirmwin, text='Cancel', command=lambda: confirmwin.destroy()).grid(row=6, column=0, pady=(15, 0))

    confirmwin.mainloop()

def Transfer(account_number, amount, t_pin, bank_name): 
    """
        collects the amount (in naira) the user wants to transfer,\n
        user's pin, beneficiary's account number and bank's name\n
        and returns a massage box showing the transaction status\n
        (successful or unsuccessful -- as the case maybe)       
    """
    conn = sqlite3.connect('Bank_Accounts.db')
    c = conn.cursor()

    account = query(acct_num)
        
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
            
            if bank_name == 'KNAB EHT':
                bene_account = query(account_number)
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
root.mainloop()

