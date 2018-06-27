import re

import email
import imaplib
import xml.etree.ElementTree as etree

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

def findnth(haystack, needle, n):
    parts= haystack.split(needle, n+1)
    if len(parts)<=n+1:
        return -1
    return len(haystack)-len(parts[-1])-len(needle)

# use creds to create a client to interact with the Google Drive API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("Test").sheet1

username = "poiuytandrew@gmail.com"
password = "tytyuiop"

mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(username, password)

mail.select("inbox")

mail.create("Item2")

mail.list()

result, data = mail.uid("search", None, "ALL")

inbox = data[0].split()

recent = inbox[-8]

result2, email_data = mail.uid("fetch", recent, "(RFC822)")

raw_email = email_data[0][1].decode("utf-8")

message = email.message_from_string(raw_email)

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

def getNumDate(message):
	string = str(message)
	x = findnth(string, "Order #", 1)
	num = string[x:x+12]
	l = string[x+20:x+50].split()
	date = l[2]+" "+l[3][:-1]
	return num, date

def getLink(message):
	string = str(message)
	x = findnth(string, "soundcloud.com", 1)
	print(x)
	string = string[x:x+200]
	y = findnth(string, " ", 1)
	string = string[:y]
	string = "https://" + re.sub('<[^<]+?>', '', string).strip()
	return string

def getCodeMoney(message):
	string = str(message)
	x = findnth(string, "Order Summary", 1)
	string = string[x:x+3600]
	x = findnth(string, "<span", 1)
	string = str(string[x:x+800])
	l = string.split()
	code = l[2][4:]
	for s in l:
		if s[0] == "$":
			money = s
	return code, money


if "Boost Collective: A New Order has Arrived" in message["Subject"]:
	print("working")
	rowNum = int(sheet.cell(2, 12).value)
	print(getLink(message), getEmail(message), getNumDate(message), getCodeMoney(message))

	cLink = getLink(message)
	cEmail = getEmail(message)
	cOrder, cDate = getNumDate(message)
	cCode, cMoney = getCodeMoney(message)

	sheet.update_cell(rowNum, 1, cDate);
	sheet.update_cell(rowNum, 2, cCode);
	sheet.update_cell(rowNum, 3, cEmail);
	sheet.update_cell(rowNum, 4, cLink);
	sheet.update_cell(rowNum, 5, cOrder);
	sheet.update_cell(rowNum, 6, cMoney);

	sheet.update_cell(2, 12, rowNum+1);


