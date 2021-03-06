import sqlite3
import InfoGetter

'''
TABLE USER
(id, uid, isauditor, solved1, solved2, email, iscn)
'''

def get_data():
    conn = sqlite3.connect('info.db')
    cursor = conn.cursor()
    cursor = cursor.execute("SELECT uid, email, solved1, solved2, isauditor, iscn  FROM USER")
    infos = cursor.fetchall() # [uid, email, solved1, solved2, is_auditor, is_cn]
    return infos


def get_auditors():
    conn = sqlite3.connect('info.db')
    cursor = conn.cursor()
    cursor = cursor.execute("SELECT email FROM USER")
    auditors = cursor.fetchall()
    auditors = [row[0] for row in auditors]
    return auditors


def update_yestoday():
    conn = sqlite3.connect('info.db')
    conn.execute("UPDATE USER set solved1 = solved2;")
    print("update yesterday info done")
    conn.commit()
    conn.close()
    return


def update_today():
    conn = sqlite3.connect('info.db')
    cursor = conn.cursor()
    cursor = cursor.execute("SELECT uid, iscn FROM USER WHERE isauditor = 0")
    uids = cursor.fetchall()
    cursor.close()
    for uid in uids:
        info = InfoGetter.get_info(uid[0], uid[1])
        if info is None:
            continue
        conn.execute("UPDATE USER set solved2 = ? where uid = ?;", [info[1], info[0]])
        print("till now, " + info[0] + " solved " + str(info[1]) + " questions")
    print("update today info done")
    conn.commit()
    conn.close()
    return


def logon_user(uid, email, is_auditor, is_cn):
    conn = sqlite3.connect('info.db')
    cursor = conn.cursor()
    cursor = cursor.execute("SELECT *  FROM USER WHERE email = ?;", [email])
    rows = cursor.fetchall()
    cursor.close()
    if len(rows) > 0:
        conn.execute("UPDATE USER set uid = ?, isauditor = ?, iscn = ? where email = ?;", [uid, str(int(is_auditor)), str(int(is_cn)), email])
        print("user with email(" + email + ") already exists, update the settings (" + uid + ", " + email + ") done")
    else:
        conn.execute("INSERT INTO USER (uid, isauditor, iscn, email) VALUES (?, ?, ?, ?);", [uid, str(int(is_auditor)),  str(int(is_cn)), email])
        print("log on (" + uid + ", " + email + ") done")
    conn.commit()
    conn.close()
    return


def logoff_user(email):
    conn = sqlite3.connect('info.db')
    conn.execute("DELETE FROM USER WHERE email = ?;", [email])
    print("log off (" + email +") done")
    conn.commit()
    conn.close()
    return


def create_table():
    conn = sqlite3.connect('info.db')
    conn.execute("CREATE TABLE IF NOT EXISTS USER \
    (id INTEGER PRIMARY KEY, \
    uid VARCHAR(20) NOT NULL, \
    isauditor BOOLEAN DEFAULT 1, \
    solved1 INT NOT NULL DEFAULT 0,\
    solved2 INT NOT NULL DEFAULT 0,\
    email VARCHAR(25) NOT NULL,\
    iscn BOOLEAN DEFAULT 0);")
    print("create table done")
    conn.commit()
    conn.close()
    return


def drop_table(name):
    conn = sqlite3.connect('info.db')
    conn.execute("DROP TABLE " + name + ";")
    conn.commit()
    conn.close()
    print("drop table " + name + " done")
    return


if __name__ == '__main__':
    # drop_table("user")
    # create_table()
    # logon_user("huaji", "934422900@qq.com", False)
    # logon_user("we98", "1320018234@qq.com", False)
    # logon_user("rsy56640", "851911672@qq.com", False)
    # logon_user("rauthy", "3477074483@qq.com", False)
    # logoff_user("934422900@qq.com")
    # logoff_user("3477074483@qq.com")
    # logoff_user("851911672@qq.com")
    # update_yestoday()
    # update_today()
    conn = sqlite3.connect('info.db')
    conn.execute("ALTER TABLE USER ADD COLUMN iscn BOOLEAN DEFAULT 0;")
    print("add column done")
    conn.commit()
    conn.close()
    print(get_data())
    print("done")