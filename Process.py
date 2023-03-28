from imaplib import IMAP4, IMAP4_SSL
import email
from datetime import timedelta, date
from datetime import datetime
import json

boxes = ["Inbox", '"&BB4EQgQ,BEAEMAQyBDsENQQ9BD0ESwQ1-"', '"&BCEEPwQwBDw-"', '"INBOX/Newsletters"']

def delete_all(address, imap_pas, p=0):
    global boxes
    imap = IMAP4_SSL('imap.mail.ru')
    try:
        imap.login(address, imap_pas)
    except:
        print(f'Shit {p}')
        return

    for box in boxes:
        imap.select(box)

        _, data = imap.search(None, 'ALL')

        for num in data[0].split():
            imap.store(num, "+FLAGS", "\\Deleted")
        try:
            imap.expange()
        except: pass

    imap.close()
    imap.logout()

def find_from(address, imap_pas, from_ad, p=0):
    imap = IMAP4_SSL('imap.mail.ru')
    try:
        imap.login(address, imap_pas)
    except:
        print(f'Shit {p}')
        return []

    global boxes
    res = []

    for box in boxes:
        imap.select(box)
        _, msum = imap.search(None, 'ALL')

        for num in msum[0].split():
            _, data = imap.fetch(num, "(RFC822)")

            message = email.message_from_bytes(data[0][1])

            if from_ad in message.get('From'):
                res.append(num)

    imap.close()
    imap.logout()
    return res

def find_by_key(address, imap_pas, key, p=0):
    imap = IMAP4_SSL('imap.mail.ru')
    try:
        imap.login(address, imap_pas)
    except:
        print(f'Shit {p}')
        return []

    global boxes
    res = []
    key = key.lower()

    for box in boxes:
        imap.select(box)
        _, msum = imap.search(None, 'ALL')

        for num in msum[0].split():
            _, data = imap.fetch(num, "(RFC822)")

            message = email.message_from_bytes(data[0][1])

            rem = 0
            for part in message.walk():
                if part.get_content_type() == "text/plain":
                    if key in part.as_string().lower():
                        rem = 1
                        break

            if rem == 1 or key in message.get('From').lower() or key in message.get('Subject').lower():
                res.append(num)

    imap.close()
    imap.logout()
    return res

def find_new(address, imap_pas, p=0):
    imap = IMAP4_SSL('imap.mail.ru')
    try:
        imap.login(address, imap_pas)
    except:
        print(f'Shit {p}')
        return []

    global boxes
    res = []

    for box in boxes:
        imap.select(box)
        _, msum = imap.search(None, 'ALL')

        for num in msum[0].split():
            res.append(num)

    imap.close()
    imap.logout()
    return res