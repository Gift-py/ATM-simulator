from tkinter import *
from tkinter import messagebox
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
    root2.geometry('400x400')
    root2.configure(background="#efefef")

    f_name_lb = Label(root2, text='WELCOME TO KNAB EHT!', anchor='center')
    f_name_lb.grid(row=0, column=2, pady=(10, 0), padx=5)

    lb = LabelFrame(root2, text='Available Services')
    lb.grid(row=1, column=0, columnspan=4, pady=(10, 0), padx=10)

    create_acct_btn = Button(lb, text='Create Account', command=create_acct_win)
    create_acct_btn.grid(row=2, column=0, columnspan=3, padx=10, pady=5)
    create_acct_btn.config(width=50)

    login_btn = Button(lb, text='Input Card (Account No.)', command=login_win)
    login_btn.grid(row=3, column=0, columnspan=3, padx=10, pady=5)
    login_btn.config(width=50)

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
    
    if(name == '' or pin == ''):
        messagebox.showerror('error', 'Idiot we need a name and a pin for this to work 😭')
    else:
        assert pin.isdigit() and len(pin) == 4, messagebox.showerror('error', 'You need a four digit pin please 😅')
        if balance == '':
            balance = 0
            messagebox.showinfo('information', 'It seems you\'re suffering from Sapa')
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

    assert acct_number != '', messagebox.showerror('error', 'Bruhh!! Put in your account number')
    assert pin != '', messagebox.showerror('error', 'My guy, what \'bout your pin?!')
    assert acct_number.isdigit(), messagebox.showerror('error', 'It\'s called account NUMBER for a reson idiot!')
    assert pin.isdigit(), messagebox.showerror('error', 'Are you dumb fam, you need to type in your 4 DIGIT pin')

    acct_num = acct_number
    conn = sqlite3.connect('Bank_Accounts.db')
    c = conn.cursor()
        
    c.execute('SELECT *, oid from Accounts WHERE oid='+acct_num)
    account = c.fetchall()

    if account == []:
        messagebox.showerror('error', 'This Account... Does not exist... 😭')
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
    balwin.title('KNAB EHT')
    balwin.geometry('250x250')
    
    account = query(acct_num)
    balance = account[0][-2]

    fr = LabelFrame(balwin, text='Account Details')
    fr.grid(row=0, column=0, pady=10, padx=10, columnspan=3)

    name = Label(fr, text=f'Account Name:')
    name.grid(row=1, column=0, pady=15)

    a_name = Label(fr, text=f'{account[0][0]}', anchor='w')
    a_name.grid(row=1, column=2, pady=15)

    num = Label(fr, text=f'Account Number:')
    num.grid(row=2, column=0, pady=15)

    a_num = Label(fr,  text = f'{account[0][-1]}', anchor='w')
    a_num.grid(row=2, column=2, pady=15)

    acct_bal = Label(fr, text=f'Account Balance:')
    acct_bal.grid(row=3, column=0, pady=(15, 10))

    bal = Label(fr, text=f'{balance}', anchor='w')
    bal.grid(row=3, column=2, pady=15)

    Button(balwin, text='Quit', command=lambda: balwin.destroy()).grid(row=4, column=1, pady=(15, 0))

def withdrawal_win():
    global withdrawalwin
    withdrawalwin = Tk()
    withdrawalwin.geometry('400x400')
    withdrawalwin.title('KNAB EHT')

    account = query(acct_num)
    balance = account[0][-2]

    fr = LabelFrame(withdrawalwin, text='Withdrawal')
    fr.grid(row=0, column=0, pady=10, padx=10, columnspan=3)

    acct_bal = Label(fr, text=f'Account Balance: {balance}')
    acct_bal.grid(row=1, column=0, columnspan=2)

    amount_lb = Label(fr, text='Withdrawal Amount: ')
    amount_lb.grid(row=2, column=0)

    w_amount = Entry(fr, width= 30)
    w_amount.grid(row=2, column=1, padx=20, pady=(10, 0))

    pin_lb = Label(fr, text='Enter Pin: ')
    pin_lb.grid(row=3, column=0)

    w_pin = Entry(fr, width= 30)
    w_pin.grid(row=3, column=1, padx=20, pady=(10, 0))

    w_sub = Button(fr, text='Withdraw', command=lambda: Withdrawal(w_amount.get(), w_pin.get()))
    w_sub.grid(row=4, column=0, columnspan=2, padx=10, pady=(15,10))
    w_sub.config(width=50)

    Button(withdrawalwin, text='Quit', command=lambda: withdrawalwin.destroy()).grid(row=5, column=1, pady=(15, 0))

def Withdrawal(amount, wd_pin):
    account = query(acct_num)

    assert amount != '', messagebox.showerror('error', 'Bruhh 💀, how much you wanna draw??!')
    assert amount.isdigit(), messagebox.showerror('error', 'Bruhh, You can\'t withdraw letters 💀')
    assert wd_pin != '', messagebox.showerror('error', 'Are you dumb fam, you need to type in your 4 digit pin')
    assert wd_pin.isdigit(), messagebox.showerror('error', 'Are you dumb fam, you need to type in your 4 digit pin')

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
    global depositwin

    depositwin = Tk()
    depositwin.geometry('400x400')
    depositwin.title('Deposit')
    
    account = query(acct_num)
    balance = account[0][-2]

    fr = LabelFrame(depositwin, text='Deposit')
    fr.grid(row=0, column=0, pady=10, padx=10, columnspan=3)

    acct_bal = Label(fr, text=f'Account Balance: {balance}')
    acct_bal.grid(row=1, column=0, columnspan=2)

    amount_lb = Label(fr, text='Deposit Amount: ')
    amount_lb.grid(row=2, column=0)

    d_amount = Entry(fr, width= 30)
    d_amount.grid(row=2, column=1, padx=20, pady=(10, 0))

    pin_lb = Label(fr, text='Enter Pin: ')
    pin_lb.grid(row=3, column=0)

    d_pin = Entry(fr, width= 30)
    d_pin.grid(row=3, column=1, padx=20, pady=(10, 0))

    d_sub = Button(fr, text='Deposit', command=lambda: Deposit(d_amount.get(), d_pin.get()))
    d_sub.grid(row=4, column=0, columnspan=2, padx=10, pady=(15,10))
    d_sub.config(width=50)

    Button(depositwin, text='Quit', command=lambda: depositwin.destroy()).grid(row=5, column=1, pady=(15, 0))

def Deposit(amount, dp_pin):
    account = query(acct_num)

    assert amount != '', messagebox.showerror('error', 'Bruhh 💀, how much you wanna deposit??!')
    assert amount.isdigit(), messagebox.showerror('error', 'Bruhh, You can\'t deposit letters 💀')
    assert dp_pin != '', messagebox.showerror('error', 'Are you dumb fam, you need to type in your 4 digit pin')
    assert dp_pin.isdigit(), messagebox.showerror('error', 'Are you dumb fam, you need to type in your 4 digit pin')

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
    global transferwin
    transferwin = Tk()
    transferwin.geometry('400x500')
    transferwin.title('KNAB EHT')

    account = query(acct_num)
    balance = account[0][-2]

    fr = LabelFrame(transferwin, text='Transfer')
    fr.grid(row=0, column=0, pady=10, padx=10, columnspan=3)

    acct_bal = Label(fr, text=f'Account Balance: {balance}')
    acct_bal.grid(row=1, column=0, columnspan=2)

    bene_acct_lb = Label(fr, text='Beneficiary Account: ')
    bene_acct_lb.grid(row=2, column=0)

    bene_acct = Entry(fr, width=30)
    bene_acct.grid(row=2, column=1)

    amount_lb = Label(fr, text='Amount: ')
    amount_lb.grid(row=3, column=0)

    t_amount = Entry(fr, width= 30)
    t_amount.grid(row=3, column=1, padx=20, pady=(10, 0))

    pin_lb = Label(fr, text='Enter Pin: ')
    pin_lb.grid(row=4, column=0)

    t_pin = Entry(fr, width= 30)
    t_pin.grid(row=4, column=1, padx=20, pady=(10, 0))

    t_sub = Button(fr, text='Transfer', command=lambda: t_confirm_win(bene_acct.get(), t_amount.get(), t_pin.get()))
    t_sub.grid(row=6, column=0, columnspan=2, padx=10, pady=(15,10))
    t_sub.config(width=50)

    Button(transferwin, text='Quit', command=lambda: transferwin.destroy()).grid(row=5, column=1, pady=(15, 0))

def t_confirm_win(account_number, amount, pin):
    assert account_number != '', messagebox.showerror('error', 'Are you planning on transferring to a ghost ?!')
    assert account_number.isdigit(), messagebox.showerror('error', 'Imbecile, is called an account NUMBER for a reason!!')
    assert amount != '', messagebox.showerror('error', 'Bruhh 💀, how much you wanna Transfer??!')
    assert amount.isdigit(), messagebox.showerror('error', 'Idiot, You can\'t transfer letters 💀')
    assert pin != '', messagebox.showerror('error', 'Are you dumb fam, you need to type in your 4 digit pin')
    assert pin.isdigit(), messagebox.showerror('error', 'Are you dumb fam, you need to type in your 4 digit pin')

    bene_acct = query(account_number)
    if bene_acct != []:
        global confirmwin
        confirmwin = Tk()
        confirmwin.geometry('250x250')
        confirmwin.title('KNAB EHT')

        bene_name = bene_acct[0][0]

        fr = LabelFrame(confirmwin, text='Confirm Transfer')
        fr.grid(row=0, column=0, pady=10, padx=10, columnspan=3)

        bene_acct_lb = Label(fr, text='Beneficiary Account: ')
        bene_acct_lb.grid(row=1, column=0)

        bene_acct = Label(fr, text=account_number)
        bene_acct.grid(row=1, column=1)

        amount_lb = Label(fr, text='Amount: ')
        amount_lb.grid(row=2, column=0)

        t_amount = Label(fr, text=amount)
        t_amount.grid(row=2, column=1, padx=20, pady=(10, 0))

        pin_lb = Label(fr, text='Beneficiary Name: ')
        pin_lb.grid(row=3, column=0)

        t_pin = Label(fr, text=bene_name)
        t_pin.grid(row=3, column=1, padx=20, pady=(10, 0))

        t_sub = Button(confirmwin, text='Transfer', command=lambda: Transfer(account_number, amount, pin))
        t_sub.grid(row=4, column=2, padx=10, pady=(15,0))

        Button(confirmwin, text='Cancel', command=lambda: confirmwin.destroy()).grid(row=4, column=0, pady=(15, 0))
    else:
        messagebox.showerror('error', 'This account does not exist in our bank 🤔')

def Transfer(account_number, amount, t_pin):    
    conn = sqlite3.connect('Bank_Accounts.db')
    c = conn.cursor()

    account = query(acct_num)
    bene_account = query(account_number)

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

