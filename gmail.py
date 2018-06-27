import email
import imaplib
import xml.etree.ElementTree as etree

def findnth(haystack, needle, n):
    parts= haystack.split(needle, n+1)
    if len(parts)<=n+1:
        return -1
    return len(haystack)-len(parts[-1])-len(needle)

username = "poiuytandrew@gmail.com"
password = "tytyuiop"

mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(username, password)

mail.select("inbox")

mail.create("Item2")

mail.list()

result, data = mail.uid("search", None, "ALL")

inbox = data[0].split()

recent = inbox[-1]

result2, email_data = mail.uid("fetch", recent, "(RFC822)")

raw_email = email_data[0][1].decode("utf-8")

message = email.message_from_string(raw_email)

print(message["Subject"])

def getEmail(message):
	string = str(message)
	x = findnth(string, "PayPal", 3)
	y = findnth(string, "Order Summary", 1)
	string = string[x:y]
	x = string.find("mailto:")
	string = string[x+7:]
	y = string.find('"')
	string = string[:y]
	return string

getEmail(message)
