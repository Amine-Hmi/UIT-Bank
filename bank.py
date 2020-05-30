from tkinter import *
from db import Database
from tkinter import messagebox
from tkinter import ttk
import os

cwd = os.path.dirname(os.path.abspath(__file__))
db = Database(cwd+'\\bank.db')

#Monitors account type selection on reigster screen
def callbackFunc(event):
  #print(account_entry.get()+" Selected")
  if (account_entry.get()) == 'Savings':
    amount_entry.selection_clear()
    amount_entry.config(from_ = 500)
  elif (account_entry.get() == 'Current'):
      amount_entry.selection_clear()
      amount_entry.delete(0,'end')
      amount_entry.config(from_ = 200)

def register_user():
  username_info = username.get()
  password_info = password.get()
  account_info = account.get()
  amount_info = amount.get()
  if (len(username_info) >= 5) :
    if (username_info.isalnum()):
      if (len(password_info) >= 6) :
        res = db.add_user(username_info,password_info,account_info,amount_info)
        if res != 'Error':
          messagebox.showinfo('Success','User registered Successfully')
          Register_screen.destroy()
        else:
        #Label(Register_screen, text = "Registration Sucess", fg = "green" ,font = ("calibri bold", 11)).pack()
          messagebox.showerror('Username Taken','Please select a different username')
      else:
        messagebox.showerror('Password too short','Password must contain at least 6 characters')   
        password_entry.delete(0, END)
        password_entry.focus()
    else:
      messagebox.showerror('Invalid Username','Username must contain only letters and/or numbers')
      username_entry.delete(0, END)
      username_entry.focus()
  else :
    messagebox.showerror('Username too short','Username must contain at least 5 characters')
    username_entry.delete(0, END)
    username_entry.focus()

    #Label(screen1, text = "Password/Username Blank!", fg = "red" ,font = ("calibri bold", 11)).pack()

# Register user window
def register():
  global Register_screen
  Register_screen = Toplevel(screen)
  Register_screen.title("Register")
  Register_screen.geometry("300x350")
  Register_screen.resizable(False,False)
  global username
  username = StringVar()
  global password
  password = StringVar()
  global amount
  amount = IntVar()
  amount.set(200)
  global account
  account = StringVar()

  Label(Register_screen, text = "Please enter details below").pack()
  Label(Register_screen, text = "").pack()
  Label(Register_screen, text = "Username * ").pack()

  global username_entry
  username_entry = Entry(Register_screen, textvariable = username)
  username_entry.pack()
  username_entry.focus()

  Label(Register_screen, text = "Password * ").pack()
  global password_entry
  password_entry =  Entry(Register_screen, show="•",textvariable = password)
  password_entry.pack()
  Label(Register_screen, text = "Account type ").pack()
  password_entry.bind('<Return>',lambda event:register_user())
  
  
  global account_entry
  account_entry = ttk.Combobox(Register_screen, values=["Savings", "Current"],width = 17,textvariable = account)
  account_entry.current(1)
  account_entry.bind("<Key>", lambda a: "break")
  account_entry.bind("<<ComboboxSelected>>", callbackFunc)
  account_entry.pack()
  choices= {"Savings", "Current"}
  account.set('Current')
  Label(Register_screen, text = "Amount").pack()

  global amount_entry
  amount_entry = Spinbox(Register_screen, from_=200, to=9999999,increment =10 ,textvariable = amount)
  amount_entry.pack()
  amount_entry.bind('<Return>',lambda event:register_user())
  Label(Register_screen, text = "").pack()

  Button(Register_screen, text = "Register", width = 10, height = 1, command = register_user).pack()
  Register_screen.transient(screen)
  Register_screen.grab_set()
  Register_screen.mainloop()

"""# Function that returns the index of selected element in the listbox
def select_item(event):
    try:
        global selected_item
        index = Users_list.curselection()[0]
        selected_item = Users_list.get(index)        
        customer_entry.delete(0, END)
        customer_entry.insert(END, selected_item[0])
        account_entry.delete(0, END)
        account_entry.insert(END, selected_item[1])
        balance_entry.delete(0, END)
        balance_entry.insert(END, selected_item[2])
        rib_entry.delete(0, END)
        rib_entry.insert(END, selected_item[3])
        #selected_item[0] = username;selected_item[2]=balance, ...
    except IndexError:
        pass"""

def user_withdraw(event = None):
  max_overdraft = 1000
  balance = int(balance_entry.get())
  rib = rib_entry.get()
  x = withdraw_amount.get()
  if (x > 0):
    #print (balance,type(rib),withdraw_amount,withdraw_amount.get())
    if ((balance - x) < - max_overdraft):
      messagebox.showerror('Insufficient Funds', ('You are only allowed '+str(max_overdraft)+' dinars overdraft !'))
    else:
      withdraw.destroy()
      db.withdraw(x,rib)
      db.add_transaction(rib,x,'Withdraw',(balance-x),rib)
      populate_fields()
  
def user_deposit(event = None):
  #balance = selected_item[2]
  balance = int(balance_entry.get())
  #rib = selected_item[3]
  rib = rib_entry.get()
  x = deposit_amount.get()
  if(x > 0):
    db.add_transaction(rib_entry.get(),deposit_amount.get(),'Deposit',(balance+x),rib_entry.get())
    db.deposit(deposit_amount.get(),rib_entry.get())
    deposit.destroy()
    populate_fields()

def display_users():
  #tree.grid_forget()
  Users_info = Tk()
  Users_info.geometry('294x227')
  Users_info.title('Users Informations')
  global Users_list
  Users_list = Listbox(Users_info,border = 1,relief = GROOVE,width = 40,bg='blue',fg='white',justify=CENTER)
  Users_info.resizable(False,False)
  #Users_list.bind('<<ListboxSelect>>', select_item)
  res = db.fetch_users()
  Users_list.delete('0','end')
  Users_list.grid(row=1, column=1,ipadx=25,ipady=10,sticky=NSEW)
  for i,row in enumerate(res):
    Users_list.insert('end','Name: '+row[0].title()+'  -  Account N°: '+row[1])
  UsersNb=Label(Users_info, text='', font='bold',relief=SUNKEN,border = 2,fg='white',bg='green',pady=10)
  UsersNb.configure(text="Total Number of Clients: "+str(len(res)))
  UsersNb.grid(row=2,column=1,sticky=S+E+W)

def send_moneny(event= None):  
    reciever_acc = recipient_account.get().split(": ")[1]
    sender = rib_entry.get()
    x = amount_sent.get()
    if x > 0:
      my_balance = int(balance_entry.get())
      rec_balance = db.user_fetch_infos(reciever_acc)[3]
      #log transfer as wthdraw from my account balance
      db.add_transaction(sender,x,'Transfer',(my_balance-x),sender)
      #log transfer as deposit to reciepient account balance
      db.add_transaction(reciever_acc,x,'Transfer',(rec_balance+x),sender)
      #substract from my account balance
      db.withdraw(x,sender)
      #Add to recipient account balance
      db.deposit(x,reciever_acc)
      populate_fields()
      recipient.destroy()
  
#def selected_combo(event):
  #print (recipient_account.get().strip().split(": ")[1])

def send_screen():
  global recipient
  recipient = Toplevel(dash)
  recipient.geometry('380x120')
  recipient.title('Send money to:')
  recipient.resizable(False,False)

  recipient_text = IntVar()
  Recipient_label = Label(recipient, text='Recipient Account:')
  Recipient_label.grid(row=1, column=0, sticky=W,pady=10,padx=10)

  amount_sent_label = Label(recipient, text='Amount:').grid(row=2, column=0, sticky=W,padx=10)

  global recipient_account
  recipient_account = StringVar()
  combo_rec_list = ttk.Combobox(recipient, values=rec_list,width = 25,justify=CENTER,textvariable = recipient_account)
  combo_rec_list.current(0)
  combo_rec_list.grid(row = 1,column = 1)
  #combo_rec_list.bind("<<ComboboxSelected>>",selected_combo)
  
  global amount_sent
  amount_sent = IntVar()
  amount_set_entry = Entry(recipient, textvariable=amount_sent,justify=CENTER)
  amount_set_entry.grid(row=2, column=1, sticky=W,pady=10)
  amount_set_entry.bind("<Return>", send_moneny)
  Button(recipient, text='Ok',relief=GROOVE,command=send_moneny).grid(row=2,column=2,pady=10)
  

  recipient.transient(dash)
  recipient.grab_set()
  recipient.mainloop()

def dashboard():
    global dash
    dash = Toplevel(screen)
    dash.resizable(False,False)

    # Customer
    global customer_entry
    customer_text = StringVar()
    customer_label = Label(dash, text='Customer Name', font=('bold', 14), pady=20,padx = 20)
    customer_label.grid(row=0, column=0, sticky=W)
    customer_entry = Entry(dash, textvariable=customer_text,justify=CENTER)
    #set to readonly
    customer_entry.bind("<Key>", lambda a: "break")
    customer_entry.grid(row=0, column=1)
    # Account_Type
    global account_entry
    account_text = StringVar()
    account_label = Label(dash, text='Account Type', font=('bold', 14),padx = 20)
    account_label.grid(row=0, column=2, sticky=W)
    account_entry = Entry(dash, textvariable=account_text,justify=CENTER)
    account_entry.bind("<Key>", lambda a: "break")
    account_entry.grid(row=0, column=3)
    
    # Balance
    global balance_entry
    balance_text = IntVar()
    balance_label = Label(dash, text='Balance', font=('bold', 14),padx = 20)
    balance_label.grid(row=1, column=0, sticky=W)
    balance_entry = Entry(dash, textvariable=balance_text,justify=CENTER)
    #set to readonly
    balance_entry.bind("<Key>", lambda a: "break")
    balance_entry.grid(row=1, column=1)

    # RIB
    global rib_entry
    rib_text = StringVar()
    rib_label = Label(dash, text='Account N°', font=('bold', 14),padx = 20)
    rib_label.grid(row=1, column=2, sticky=W)
    rib_entry = Entry(dash, textvariable=rib_text,justify=CENTER)
    #set to readonly
    rib_entry.bind("<Key>", lambda a: "break")
    rib_entry.grid(row=1, column=3)
    '''rib_list = Listbox(dash, height=8, width=50, border=0)
    rib_list.grid(row=3, column=0, columnspan=3, rowspan=6, pady=20, padx=20)'''
    
    # Buttons
    add_btn_img = PhotoImage(file=cwd+"\\icons\\deposit.png")
    add_btn = Button(dash,compound=LEFT, image=add_btn_img,text='  Deposit', width=10,command= Deposit_screen,relief=GROOVE)
    add_btn.grid(row=2, column=0, pady=20, padx=20,sticky=EW)
    
    #Withdraw btn
    remove_btn_img = PhotoImage(file=cwd+"\\icons\\withdraw.png")
    remove_btn = Button(dash,compound=LEFT, image=remove_btn_img,text='Withdraw',command= Withdraw_screen,relief=GROOVE)
    remove_btn.grid(row=2, column=1,pady=20,sticky=NSEW)

    #Users list btn
    user_list_btn_img = PhotoImage(file=cwd+"\\icons\\list.png")
    user_list_btn = Button(dash,image=user_list_btn_img,compound=LEFT, text='   Users List',command= display_users,relief=GROOVE,width=17)
    user_list_btn.grid(row=2, column=3,padx=0,sticky=EW)
    
    #Close Account btn
    close_btn_img = PhotoImage(file=cwd+"\\icons\\eliminate.png")
    close_btn = Button(dash,image=close_btn_img,compound=LEFT,text='    Close Account',width = 20,command= Unregister,relief=GROOVE)
    close_btn.grid(row=3, column=0,padx=20,sticky=NSEW)

    #Change Account type
    global update_btn
    update_btn_img = PhotoImage(file=cwd+"\\icons\\toggle.png")
    update_btn = Button(dash,image=update_btn_img,compound=LEFT,text='', width=20,command=Update_screen,relief=GROOVE)
    #update_btn.bind(<Button-1>,upd_callback)
    update_btn.grid(row=3, column=3,stick=NSEW)

#Transfer
    global send_btn
    send_btn_img = PhotoImage(file=cwd+"\\icons\\transfer.png")
    send_btn = Button(dash,compound=LEFT,image=send_btn_img,text='   Transfer',width = 17,command=send_screen,relief=GROOVE)
    send_btn.grid(row=2, column=2,padx=20,sticky=EW)
#Tree
    global tree
    tree=ttk.Treeview(dash)
    tree["columns"]=("Operation","Amount","Balance","Time","From")
    tree.column("#0", width=35, minwidth=35, stretch=YES)
    tree.column("Operation", width=80, minwidth=80,stretch=YES)
    tree.column("Amount", width=80, minwidth=50, stretch=YES)
    tree.column("Balance", width=80, minwidth=50, stretch=YES)
    tree.column("Time", width=140, minwidth=140, stretch=YES)
    tree.column("From", width=140, minwidth=140, stretch=YES)
    tree.heading("#0",text=" # ",anchor=W)
    tree.heading("Operation", text="Operation",anchor=W)
    tree.heading("Amount", text="Amount",anchor=W)
    tree.heading("Balance", text="Balance",anchor=W)
    tree.heading("Time", text="Time",anchor=W)
    tree.heading("From", text="From",anchor=W)
    tree.grid(row=4, column=0, columnspan=8, rowspan=20, padx=27,pady=15,sticky=EW)
    #Scrollbox
    treeScroll = ttk.Scrollbar(dash,orient="vertical",command=tree.yview)
    treeScroll.grid(row=5, column=5,rowspan=20,padx=10,sticky=NS)    
    #treeScroll.configure(command=tree.yview)
    tree.configure(yscrollcommand=treeScroll.set)
    dash.geometry("620x475")
    dash.title("My Dashboard")
    populate_fields()
    dash.transient(screen)
    dash.grab_set()
    dash.mainloop()
#update account type
def Update_screen():
  bal = int(balance_entry.get())
  if(account_entry.get()=='Savings'):
    MsgBox = messagebox.askquestion ('Change Account ?','Switch\n your account type to \"Current\" ?',icon = 'warning',default='no')
    if MsgBox == 'yes':
        if (bal < 200) :
          messagebox.showerror('insufficient funds','You must posess at least 200 Dinars')
        else:
          db.update("Current",rib_entry.get())
          messagebox.showinfo('Success','Account set to \"Current\"successfuly')
          populate_fields()
          update_btn.configure(text ='Savings  ← ')
          update_btn.configure(compound = RIGHT)

  else:
    MsgBox = messagebox.askquestion ('Change Account ?','Switch\n your account type to \"Savings\" ?',icon = 'warning',default='no')
    if MsgBox == 'yes':
      if (bal < 500) :
        messagebox.showerror('insufficient funds','You must posess at least 500 Dinars')
      else:
        db.update("Savings",rib_entry.get())
        messagebox.showinfo('Succes','Account set to \"Savings\"successfuly')
        populate_fields()
        update_btn.configure(text = ' →  Current')
        update_btn.configure(compound= LEFT)
  #Update.mainloop()

def Withdraw_screen():
  global withdraw
  withdraw = Toplevel(dash)
  withdraw.resizable(False,False)
  #withdraw.tkraise(dash)
  withdraw.title("Select amount to withdraw")
  withdraw.geometry("300x120")
  global withdraw_amount
  Label(withdraw, text = "Amount to withdraw").pack()
  withdraw_amount = IntVar()
  withdraw_amount_entry = Entry(withdraw,textvariable = withdraw_amount)
  withdraw_amount_entry.delete('0',END)
  withdraw_amount_entry.focus()
  withdraw_amount_entry.bind("<Return>", user_withdraw)
  withdraw_amount_entry.pack()
  Label(withdraw, text = "").pack()
  Button(withdraw, text = "Confirm", width = 10, height = 1,pady=3, command = user_withdraw).pack()
  withdraw.transient(dash)
  withdraw.grab_set()
  withdraw.mainloop()

def Deposit_screen():
  global deposit
  deposit = Toplevel(dash)
  deposit.title("Select amount to deposit")
  deposit.geometry("300x120")
  deposit.resizable(False,False)
  global deposit_amount
  Label(deposit, text = "Amount to deposit").pack()
  deposit_amount = IntVar()
  deposit_amount_entry = Entry(deposit,textvariable = deposit_amount)
  deposit_amount_entry.delete('0',END)
  deposit.bind("<Return>", user_deposit)
  deposit_amount_entry.pack()
  deposit_amount_entry.focus()
  Label(deposit, text = "").pack()
  Button(deposit, text = "Confirm", width = 10, height = 1,pady=3, command = user_deposit).pack()
  deposit.transient(dash)
  deposit.grab_set()
  deposit.mainloop()

#Authentification function (Needs improvements)
def login_user(event = None):
  
  username_log_info = username_log.get()
  password_log_info = password_log.get()
  if username_log_info or password_log_info != '':
    res = db.user_fetch(username_log_info,password_log_info)
    #username_log_entry.delete(0, END)
    #password_log_entry.delete(0, END)
    #Label(Login_screen, text = "Login Sucess", fg = "green" ,font = ("calibri bold", 11)).pack()
    #print (res)
    if (res) == 'User Not Found Or Wrong Password !':
      messagebox.showerror('Login Failed', res)
    elif (res) == 'Logged in':
      #messagebox.showinfo('Success',res)
      Login_screen.destroy()
      dashboard()
  else :
    messagebox.showerror('Required Fields', 'Please include all fields')
    return

#obselete? remove?
def get_user_info():
  username_log_info = username_log.get()
  password_log_info = password_log.get()
  #print(len(selected_item[0]))
  res = db.user_fetch_infos(selected_item[0])
  messagebox.showinfo('Success',res)
  #Register_screen.destroy()

def Unregister():
    MsgBox = messagebox.askquestion ('Close Account','Are you sure you want to close this user\'s account ?',icon = 'warning',default='no')
    if MsgBox == 'yes':
      db.remove_user(rib_entry.get())
      messagebox.showinfo('Done','User account has been closed')
      dash.destroy()
        #clear_text()
    #populate_fields()

def login():
  global Login_screen
  Login_screen = Toplevel(screen)
  Login_screen.title("Login")
  Login_screen.geometry("300x150")
  Login_screen.resizable(False,False)
  global username_log
  global password_log
  username_log = StringVar()
  password_log = StringVar()
  Label(Login_screen, text = "Username *").pack()
  username_log_entry = Entry(Login_screen,textvariable = username_log)
  username_log_entry.pack()
  username_log_entry.focus()
  Label(Login_screen, text = "Password *").pack()
  password_log_entry = Entry(Login_screen,show="•", textvariable = password_log)
  password_log_entry.bind("<Return>", login_user)
  password_log_entry.pack()
  Label(Login_screen, text = "").pack()
  Button(Login_screen, text = "Login", width = 10, height = 1, command = login_user).pack()
  Login_screen.transient(screen)
  Login_screen.grab_set()
  Login_screen.mainloop()

def main_screen():
  global screen
  screen = Tk()
  screen.geometry("280x260")
  screen.title("UIT Bank v1.0")
  screen.resizable(False,False)
#Logo
  logo_img = PhotoImage(file=cwd+"\\icons\\logo.png")
  Label(width = "300", height = "65",border=2,relief=GROOVE,image=logo_img).pack()
  Label(text = "").pack()
#Login
  log_img = PhotoImage(file=cwd+"\\icons\\login.png")
  Button(compound=LEFT,text = "\t\tLogin   ", height = "32", width = "200",image =log_img, command = login,relief=GROOVE).pack()
  Label(text = "").pack()
#Register
  reg_img = PhotoImage(file=cwd+"\\icons\\signup.png")
  Button(compound=LEFT,text = "\t\tRegister",height = "32", width = "200",image =reg_img, command = register,relief=GROOVE).pack()
  Label(text = "").pack()
#About us
  info_img = PhotoImage(file=cwd+"\\icons\\about.png")
  Button(height = "32", width = "32",image =info_img,command = about_us,relief=GROOVE).pack(side=RIGHT,pady=5,padx=10)
  screen.mainloop()

def about_us():
  messagebox.showinfo('About us','This program is brought to you by:\n\n-  Amin Hammami\n-  Hachem Bahlous\n-  Malek ben Friha\n\n\n\tL2SI - UIT - 2019/2020')
#fetch user infos on lauch & refreshes fields upon each change
def populate_fields():    
  #transactions_info.delete(0, END)
  for row in db.fetch(username_log.get()):
  #transactions_info.insert('end',row)
    customer_entry.delete(0, END)
    account_entry.delete(0, END)
    balance_entry.delete(0, END)
    rib_entry.delete(0, END)
    customer_entry.insert(0,row[0].title())
    account_entry.insert(0,row[1])
    if row[1] == 'Savings':
      update_btn.configure(text = '→  Current')
      update_btn.configure(compound= LEFT)
    else:
      update_btn.configure(text ='Savings  ← ')
      update_btn.configure(compound = RIGHT)
    balance_entry.insert(0,row[2])
    rib_entry.insert(0,row[3])
    #print(row[2])
    tree.delete(*tree.get_children())
  for i,row in enumerate(db.user_fetch_transactions(rib_entry.get())):
  #print(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
    op_type=row[3]
    if row[2]=='Withdraw':
      op_type='- '+str(row[3])
    elif row[2]=='Deposit':
      op_type='+ '+str(row[3])
    tree.insert("", row[0], row[0], text=i+1, values=(row[2],op_type,row[4],row[5],row[6]))
  res = db.fetch_users()
  if(len(res)== 1):
    send_btn.configure(state=DISABLED)
  else :
    global rec_list
    rec_list = []
    for i,row in enumerate(res):
      if row[1]!= rib_entry.get():
        rec_list.append(row[0].title()+' - N°: '+row[1])
      #self,parent,index,
     
# Start program
main_screen() 