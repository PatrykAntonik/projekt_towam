import tkinter as tk
import sqlite3
from tkinter import messagebox, font
import tkcalendar as tkc
import matplotlib.pyplot as plt
import numpy as np

login_window = tk.Tk()
login_window.title("Login")
login_window.geometry('400x300+400+200')
font2 = tk.font.Font(family="Ubuntu", size=15, weight="bold")
font1 = tk.font.Font(family="Ubuntu", size=15)
login_window.configure(bg='#483434')

#! Create the database connection
conn = sqlite3.connect("database.db")
cursor = conn.cursor()


#! Create the login function
def login():
    username = username_input.get()
    password = password_input.get()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()

    if result:

        messagebox.showinfo(title='info', message='Login successful')

        def logout():
            logged_window.destroy()
            messagebox.showinfo(message='Logout successful')

        def elo_calc():

            if (oponent_elo.get().isnumeric() == True and numOfEx.get().isnumeric() == True) and not (int(oponent_elo.get()) > 3000 or int(oponent_elo.get()) < 500):

                Res = GameResult.get()
                Typ = GameType.get()
                ChosenDate = date.get()
                ex = numOfEx.get()

                K = 16
                i = cursor.execute(
                    "SELECT id FROM users WHERE username=?", (username,)).fetchone()[0]

                if Typ == elo_options[0]:
                    cursor.execute(
                        "SELECT elo FROM user_data WHERE user_id=? and type=? ORDER BY date DESC LIMIT 1", (i, 'Blitz'))
                elif Typ == elo_options[1]:
                    cursor.execute(
                        "SELECT elo FROM user_data WHERE user_id=? and type=? ORDER BY date DESC LIMIT 1", (i, 'Rapid'))
                elif Typ == elo_options[2]:
                    cursor.execute(
                        "SELECT elo FROM user_data WHERE user_id=? and type=? ORDER BY date DESC LIMIT 1", (i, 'Classic'))

                Ra = cursor.fetchone()[0]
                Rb = int(oponent_elo.get())

                if Res == result_options[0]:
                    Res = 1
                elif Res == result_options[1]:
                    Res = 0
                elif Res == result_options[2]:
                    Res = 0.5

                Qa = 10 ** (Ra / 400)
                Qb = 10 ** (Rb / 400)
                Ea = Qa / (Qa + Qb)
                Ra_new = Ra + K * (Res - Ea)
                Ra_new = int(Ra_new)

                messagebox.showinfo(message=f'Your new elo is {Ra_new}')

                if Typ == elo_options[0]:
                    cursor.execute("INSERT INTO user_data (user_id, date, elo, type, ex) VALUES (?, ?, ?, ?, ?)", (
                        i, ChosenDate, Ra_new, 'Blitz', ex))
                if Typ == elo_options[1]:
                    cursor.execute("INSERT INTO user_data (user_id, date, elo, type, ex) VALUES (?, ?, ?, ?, ?)", (
                        i, ChosenDate, Ra_new, 'Rapid', ex))
                if Typ == elo_options[2]:
                    cursor.execute("INSERT INTO user_data (user_id, date, elo, type, ex) VALUES (?, ?, ?, ?, ?)", (
                        i, ChosenDate, Ra_new, 'Classic', ex))

                conn.commit()

            else:
                messagebox.showerror(message='Please enter a valid number')

        def visualize():
            i = cursor.execute(
                "SELECT id FROM users WHERE username=?", (username,)).fetchone()[0]

            cursor.execute(
                "SELECT elo, date FROM user_data WHERE user_id=? and type=?", (i, 'Blitz'))
            elo_blitz = cursor.fetchall()

            cursor.execute(
                "SELECT elo, date FROM user_data WHERE user_id=? and type=?", (i, 'Rapid'))
            elo_rapid = cursor.fetchall()

            cursor.execute(
                "SELECT elo, date FROM user_data WHERE user_id=? and type=?", (i, 'Classic'))
            elo_classic = cursor.fetchall()

            cursor.execute(
                "SELECT ex, date FROM user_data WHERE user_id=?", (i,))
            exerc = cursor.fetchall()

            dates_blitz = [result[1] for result in elo_blitz]
            elos_blitz = [result[0] for result in elo_blitz]

            dates_rapid = [result[1] for result in elo_rapid]
            elos_rapid = [result[0] for result in elo_rapid]

            dates_classic = [result[1] for result in elo_classic]
            elos_classic = [result[0] for result in elo_classic]

            dates_ex = [result[1] for result in exerc]
            exs = [result[0] for result in exerc]

            if checkBlitz.get() == 1 and checkRapid.get() == 1 and checkClassic.get() == 1:
                plt.plot(dates_blitz, elos_blitz,
                         label='Blitz', marker='o', ms=5)
                plt.plot(dates_rapid, elos_rapid,
                         label='Rapid', marker='o', ms=5)
                plt.plot(dates_classic, elos_classic,
                         label='Classic', marker='o', ms=5)
                plt.title('ELO over time')
                plt.xlabel('Date')
                plt.xticks(rotation=45)
                plt.ylabel('ELO')
                plt.legend()
                plt.show()

            elif checkBlitz.get() == 1 and checkRapid.get() == 1:
                plt.plot(dates_blitz, elos_blitz,
                         label='Blitz', marker='o', ms=5)
                plt.plot(dates_rapid, elos_rapid,
                         label='Rapid', marker='o', ms=5)
                plt.title('ELO over time')
                plt.xlabel('Date')
                plt.ylabel('ELO')
                plt.xticks(rotation=45)
                plt.legend()
                plt.show()

            elif checkBlitz.get() == 1 and checkClassic.get() == 1:
                plt.plot(dates_blitz, elos_blitz,
                         label='Blitz', marker='o', ms=5)
                plt.plot(dates_classic, elos_classic,
                         label='Classic', marker='o', ms=5)
                plt.title('ELO over time')
                plt.xlabel('Date')
                plt.ylabel('ELO')
                plt.xticks(rotation=45)
                plt.legend()
                plt.show()

            elif checkRapid.get() == 1 and checkClassic.get() == 1:
                plt.plot(dates_rapid, elos_rapid,
                         label='Rapid', marker='o', ms=5)
                plt.plot(dates_classic, elos_classic,
                         label='Classic', marker='o', ms=5)
                plt.title('ELO over time')
                plt.xlabel('Date')
                plt.ylabel('ELO')
                plt.xticks(rotation=45)
                plt.legend()
                plt.show()

            elif checkBlitz.get() == 1:
                plt.plot(dates_blitz, elos_blitz, marker='o', ms=5)
                plt.title('ELO over time')
                plt.xlabel('Date')
                plt.ylabel('ELO')
                plt.xticks(rotation=45)
                plt.show()

            elif checkRapid.get() == 1:
                plt.plot(dates_rapid, elos_rapid, marker='o', ms=5)
                plt.title('ELO over time')
                plt.xlabel('Date')
                plt.ylabel('ELO')
                plt.xticks(rotation=45)
                plt.show()

            elif checkClassic.get() == 1:
                plt.plot(dates_classic, elos_classic, marker='o', ms=5)
                plt.title('ELO over time')
                plt.xlabel('Date')
                plt.ylabel('ELO')
                plt.xticks(rotation=45)
                plt.show()

            elif checkEx.get() == 1:
                plt.bar(dates_ex, exs)
                plt.title('Exercises done over time')
                plt.xlabel('Date')
                plt.ylabel('Exercises done')
                plt.xticks(rotation=45)
                plt.show()

            else:
                messagebox.showerror(message='Choose something to analyse')

        def visualizeWindow():

            visualize_window = tk.Toplevel()
            visualize_window.title("Visualize Data")
            visualize_window.configure(bg="#483434")
            visualize_window.geometry('600x200+700+400')

            n_rows = 7
            n_columns = 4
            for i in range(n_rows):
                visualize_window.grid_rowconfigure(i,  weight=1)
            for i in range(n_columns):
                visualize_window.grid_columnconfigure(i,  weight=1)

            tk.Label(visualize_window, text="Choose which data to analyse: ", bg='#483434',
                     fg='#FFF', font=font3).grid(row=0, columnspan=4, sticky='nsew', pady=10)
            tk.Button(visualize_window, text="Show Data", command=visualize, bg="#FFF3E4",
                      font=font4).grid(row=2, columnspan=4, sticky='nsew', pady=15, padx=10)

            global checkBlitz, checkRapid, checkClassic, checkEx
            checkBlitz = tk.IntVar()
            checkRapid = tk.IntVar()
            checkClassic = tk.IntVar()
            checkEx = tk.IntVar()

            check1 = tk.Checkbutton(visualize_window, text="Blitz", variable=checkBlitz,
                                    width=10, indicatoron=0, selectcolor='lightgreen', bg='#FFF', font=font4)
            check2 = tk.Checkbutton(visualize_window, text="Rapid", variable=checkRapid,
                                    width=10, indicatoron=0, selectcolor='lightgreen', bg='#FFF', font=font4)
            check3 = tk.Checkbutton(visualize_window, text="Classic", variable=checkClassic,
                                    width=10, indicatoron=0, selectcolor='lightgreen', bg='#FFF', font=font4)
            check4 = tk.Checkbutton(visualize_window, text="Exercises", variable=checkEx,
                                    width=10, indicatoron=0, selectcolor='lightgreen', bg='#FFF', font=font4)
            check1.grid(row=1, column=0, sticky='nsew', pady=10, padx=10)
            check2.grid(row=1, column=1, sticky='nsew', pady=10, padx=10)
            check3.grid(row=1, column=2, sticky='nsew', pady=10, padx=10)
            check4.grid(row=1, column=3, sticky='nsew', pady=10, padx=10)
            visualize_window.columnconfigure(0, minsize=150)
            visualize_window.columnconfigure(1, minsize=150)
            visualize_window.columnconfigure(2, minsize=150)
            visualize_window.columnconfigure(3, minsize=150)

            visualize_window.mainloop()

        #! new window after login

        login_window.destroy()
        logged_window = tk.Tk()
        logged_window.title(f"Welcome {result[1]}")
        logged_window.configure(bg="#483434")
        logged_window.geometry('600x480+500+300')
        font3 = tk.font.Font(family="Ubuntu", size=15, weight="bold")
        font4 = tk.font.Font(family="Ubuntu", size=15)

        n_rows = 7
        n_columns = 2
        for i in range(n_rows):
            logged_window.grid_rowconfigure(i,  weight=1)
        for i in range(n_columns):
            logged_window.grid_columnconfigure(i,  weight=1)

        global oponent_elo
        oponent_elo = tk.Entry(logged_window, font=font1, width=17)
        global date
        date = tkc.DateEntry(logged_window, font=font1,
                             date_pattern='yyyy/mm/dd', bg='#FFF3E4', width=15)
        global numOfEx
        numOfEx = tk.Entry(logged_window, font=font1, width=15)
        numOfEx.insert(0, 0)

        result_options = ['Win', 'Lose', 'Draw']
        global GameResult
        GameResult = tk.StringVar(logged_window)
        GameResult.set("Select an Option")
        question_menu = tk.OptionMenu(
            logged_window, GameResult, *result_options)
        question_menu.configure(bg='#FFF3E4', font=font1,
                                activebackground='#FFF3E4', width=15)

        elo_options = ['Blitz', 'Rapid', 'Classic']
        global GameType
        GameType = tk.StringVar(logged_window)
        GameType.set('Choose game type')
        elo_menu = tk.OptionMenu(logged_window, GameType, *elo_options)
        elo_menu.configure(bg='#FFF3E4', font=font1,
                           activebackground='#FFF3E4', width=15)

        tk.Label(logged_window, text="Opponent Elo:", bg="#483434",
                 fg='#FFF', font=font3).grid(row=0, column=0, sticky='nsew', pady=7)
        tk.Label(logged_window, text="Date:", bg="#483434", fg='#FFF',
                 font=font3).grid(row=1, column=0, sticky='nsew', pady=7)
        tk.Label(logged_window, text="Result:", bg="#483434", fg='#FFF',
                 font=font3).grid(row=2, column=0, sticky='nsew', pady=7)
        tk.Label(logged_window, text="Game type:", bg="#483434", fg='#FFF',
                 font=font3).grid(row=3, column=0, sticky='nsew', pady=7)
        tk.Label(logged_window, text="Number of exercises:", bg="#483434",
                 fg='#FFF', font=font3).grid(row=4, column=0, sticky='nsew', pady=7)

        oponent_elo.grid(row=0, column=1, sticky='nsew', padx=10, pady=7)
        date.grid(row=1, column=1, sticky='nsew', padx=10, pady=7)
        question_menu.grid(row=2, column=1, sticky='nsew', padx=10, pady=7)
        elo_menu.grid(row=3, column=1, sticky='nsew', padx=10, pady=7)
        numOfEx.grid(row=4, column=1, sticky='nsew', padx=10, pady=7)

        tk.Button(logged_window, text="Calculate Elo and save", command=elo_calc,
                  bg="#FFF3E4", font=font4).grid(row=5, column=0, pady=20, sticky='nsew', padx=10)
        tk.Button(logged_window, text="Visualize Data", command=visualizeWindow,
                  bg="#FFF3E4", font=font4).grid(row=5, column=1, sticky='nsew', pady=20, padx=10)
        tk.Button(logged_window, text="Logout", command=logout, bg="#FFF3E4", font=font4).grid(
            row=6, column=0, sticky='nsew', pady=20, padx=10, columnspan=2)

        logged_window.columnconfigure(0, minsize=250)
        logged_window.columnconfigure(1, minsize=250)

        logged_window.mainloop()

    else:
        messagebox.showerror(
            message="Incorrect username or password", title='Error')


#! Create the registration function
def register():

    username = username_input_reg.get()
    password = password_input_reg.get()
    blitz = elo_blitz_input_reg.get()
    rapid = elo_rapid_input_reg.get()
    classic = elo_classic_input_reg.get()
    selected_date = date_entry.get_date()

    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    result = cursor.fetchone()

    if not result and (blitz.isnumeric() == True or rapid.isnumeric == True or classic.isnumeric == True) and not (int(blitz) > 3000 or int(blitz) < 500 or int(rapid) > 3000 or int(rapid) < 500 or int(classic) > 3000 or int(classic) < 500):
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        cursor.execute("SELECT id FROM users WHERE username=?", (username,))
        user_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO user_data (user_id,date,elo,type,ex) VALUES (?, ?, ?, ?, ?)",
                       (user_id, selected_date, blitz, 'Blitz', 0))
        cursor.execute("INSERT INTO user_data (user_id,date,elo,type,ex) VALUES (?, ?, ?, ?, ?)",
                       (user_id, selected_date, blitz, 'Rapid', 0))
        cursor.execute("INSERT INTO user_data (user_id,date,elo,type,ex) VALUES (?, ?, ?, ?, ?)",
                       (user_id, selected_date, blitz, 'Classic', 0))
        conn.commit()
        messagebox.showinfo(message='Registration successful')

    elif blitz.isdigit() == False or rapid.isdigit() == False or classic.isdigit() == False:
        messagebox.showerror(title='Error', message='Enter number')

    elif int(blitz) > 3000 or int(blitz) < 500 or int(rapid) > 3000 or int(rapid) < 500 or int(classic) > 3000 or int(classic) < 500:
        messagebox.showerror(
            title='Error', message="Please enter rating in range 500 - 3000")

    elif len(username) == 0 or len(password) == 0:
        messagebox.showerror(
            title='Error', message="Please enter username and password")

    else:
        messagebox.showerror(
            message="That username is already taken", title='Error')


def RegisterPage():
    register_window = tk.Toplevel(login_window)
    register_window.title("Registration")
    register_window.configure(bg="#483434")
    register_window.geometry('400x600+300-400')

    global username_input_reg
    global password_input_reg
    global elo_blitz_input_reg
    global elo_rapid_input_reg
    global elo_classic_input_reg
    global date_entry

    username_input_reg = tk.Entry(register_window, font=font1)
    password_input_reg = tk.Entry(register_window, show="*", font=font1)
    elo_blitz_input_reg = tk.Entry(register_window, font=font1)
    elo_rapid_input_reg = tk.Entry(register_window, font=font1)
    elo_classic_input_reg = tk.Entry(register_window, font=font1)
    date_entry = tkc.DateEntry(
        register_window, font=font1, date_pattern='yyyy/mm/dd', bg='#FFF3E4')

    n_rows = 12
    n_columns = 1
    for i in range(n_rows):
        register_window.grid_rowconfigure(i,  weight=1)
    for i in range(n_columns):
        register_window.grid_columnconfigure(i,  weight=1)

    username_input_reg.grid(row=1, sticky='nsew', pady=5, padx=15)
    password_input_reg.grid(row=3, sticky='nsew', pady=5, padx=15)
    elo_blitz_input_reg.grid(row=5, sticky='nsew', pady=5, padx=15)
    elo_rapid_input_reg.grid(row=7, sticky='nsew', pady=5, padx=15)
    elo_classic_input_reg.grid(row=9, sticky='nsew', pady=5, padx=15)
    date_entry.grid(row=11, sticky='nsew', padx=15, pady=5)

    tk.Label(register_window, text="Username:", bg='#483434', fg='#FFF',
             font=font2).grid(row=0, sticky='nsew', padx=15, pady=5)
    tk.Label(register_window, text="Password:", bg='#483434', fg='#FFF',
             font=font2).grid(row=2, sticky='nsew', padx=15, pady=5)
    tk.Label(register_window, text="Starting Elo in blitz:", bg='#483434',
             fg='#FFF', font=font2).grid(row=4, sticky='nsew', padx=15, pady=5)
    tk.Label(register_window, text="Starting Elo in rapid:", bg='#483434',
             fg='#FFF', font=font2).grid(row=6, sticky='nsew', padx=15, pady=5)
    tk.Label(register_window, text="Starting Elo in classic:", bg='#483434',
             fg='#FFF', font=font2).grid(row=8, sticky='nsew', padx=15, pady=5)
    tk.Label(register_window, text="Choose date of registration:", bg='#483434',
             fg='#FFF', font=font2).grid(row=10, sticky='nsew', padx=15, pady=5)

    tk.Button(register_window, text="Register", command=register, font=font1,
              bg='#FFF3E4').grid(row=12, sticky='nsew', padx=50, pady=10)


n_rows = 6
n_columns = 1
for i in range(n_rows):
    login_window.grid_rowconfigure(i,  weight=1)
for i in range(n_columns):
    login_window.grid_columnconfigure(i,  weight=1)


tk.Label(login_window, text="Username:", bg='#483434', fg='#FFF',
         font=font2).grid(row=0, column=0, sticky='nsew')
tk.Label(login_window, text="Password:", bg='#483434', fg='#FFF',
         font=font2).grid(row=2, column=0, sticky='nsew')

tk.Button(login_window, text="Login", command=login, font=font1,
          bg='#FFF3E4').grid(row=6, column=0, sticky='nsew', padx=70, pady=15)
tk.Button(login_window, text="Register", command=RegisterPage, font=font1,
          bg='#FFF3E4').grid(row=7, column=0, sticky='nsew', padx=70, pady=5)

username_input = tk.Entry(login_window, font=font1)
password_input = tk.Entry(login_window, show="*", font=font1)


password_input.grid(row=3, column=0, sticky='nsew', padx=100, pady=7)
username_input.grid(row=1, column=0, sticky='nsew', padx=100, pady=7)


login_window.mainloop()
