import sqlite3

DB_NAME = 'SpecialReport.db'

def OpenConn():
    return sqlite3.connect(DB_NAME)

def CloseConn(conn):
    conn.commit()
    conn.close()

def CreateDB():
    conn = OpenConn()

    conn.execute('''CREATE TABLE IF NOT EXISTS Soldiers
             (PersonalNumber TEXT PRIMARY KEY    NOT NULL,
             Name                       TEXT     NOT NULL,
             CommanderPersonalNumber    TEXT     NOT NULL,
             HasArrived                 INT,
             Mood                       TEXT);''')

    conn.execute('''CREATE TABLE IF NOT EXISTS Reporters
             (PersonalNumber TEXT PRIMARY KEY    NOT NULL,
             Phone           TEXT);''')

    CloseConn(conn)

def FillDB():
    conn = OpenConn()

    conn.execute('''INSERT INTO Soldiers
            (PersonalNumber, Name, CommanderPersonalNumber) VALUES
            ("8082128", "Lee Wainer", "11111110"),
            ("5853948", "Roei Levi", "11111110"),
            ("11111100", "MinervaMcGonagall", "11111100"),
            ("8049079", "Yuval Goldberg", "11111110");''')
    conn.execute('''INSERT INTO Reporters VALUES
            ("11111100", "972525848125"),
            ("11111110", "972547772771");''')

    CloseConn(conn)

def learn_SelectAll():
    conn = OpenConn()

    cur = conn.cursor()
    cur.execute("SELECT * FROM Soldiers")
    rows = cur.fetchall()
    print("~Soldiers~")
    for row in rows:
        print(row)
    cur.execute("SELECT * FROM Reporters")
    rows = cur.fetchall()
    print("~Reporters~")
    for row in rows:
        print(row)
    print("after select")

    CloseConn(conn)

def DB_SetArrival(personalNumber, mood):
    '''
    Logs the arrival of the soldier.
    :param personalNumber: Soldier's personal number.
    :return:
    '''
    conn = OpenConn()
    conn.execute("UPDATE Soldiers set HasArrived = 1 where PersonalNumber = ?", (personalNumber,))
    conn.execute("UPDATE Soldiers set Mood = ? where PersonalNumber = ?", (mood, personalNumber,))
    CloseConn(conn)

def DB_ResetArrivals():
    conn = OpenConn()
    conn.execute("UPDATE Soldiers set HasArrived = NULL")
    CloseConn(conn)

def GetPersonalNumberByPhone(conn, phone):
    cur = conn.cursor()
    cur.execute("SELECT PersonalNumber FROM Reporters WHERE Phone = ?", (phone,))
    rows = cur.fetchall()

    if rows:
        return rows[0][0]
    else:
        return None

def DB_GetReport(phone):
    '''
    Gets the list&status of the Soldiers of the required reporter.
    :param phoneNumber: Reporter's phone number.
    :return: Pairs of name and status: none marks no arrival, 1 marks arrival.
    '''
    conn = OpenConn()
    reporterPersonalNumber = GetPersonalNumberByPhone(conn, phone)

    if reporterPersonalNumber:
        cur = conn.cursor()
        cur.execute("SELECT Name, HasArrived FROM Soldiers WHERE CommanderPersonalNumber = ?", (reporterPersonalNumber,))
        rows = cur.fetchall()

        CloseConn(conn)

        return rows
    else:
        return []

def DB_GetPhoneNumber(personalNumber):
    conn = OpenConn()

    CloseConn(conn)

if __name__ == '__main__':
	CreateDB()
	FillDB()
	learn_SelectAll()
	DB_SetArrival("11111102", "Thrilled")
	learn_SelectAll()
	DB_GetReport("050111100")
	DB_ResetArrivals()
	learn_SelectAll()
	print("Hi2!")
	input()