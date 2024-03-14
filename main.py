import imapclient
import pyzmail
from datetime import datetime
from bs4 import BeautifulSoup

conn = imapclient.IMAPClient('imap.gmail.com', ssl=True)
checker = conn.login('peter@mapandsnap.org', 'ivwp odox lswn ekbz')
print(checker)

# Select the folder
conn.select_folder('INBOX', readonly=True)

date_str = "01-Jan-2022"
# Convert the string to a datetime object
date_obj = datetime.strptime(date_str, "%d-%b-%Y")
# Pass the formatted string into conn.search
formatted_date_str = date_obj.strftime("%Y-%m-%d")

# Convert data string to datetime object.
# messages = conn.search('SINCE', formatted_date_str)
messages = conn.search("ALL")
# print(messages)

# Fetch an email
rawMessage = conn.fetch([21], ['BODY[]', 'FLAGS'])
# print(rawMessage)

# Use pyzmail to retrieve the message info.
message = pyzmail.PyzMessage.factory(rawMessage[21][b'BODY[]'])

# Get the email in HTML for
# print(message.html_part)
html_payload = message.html_part.get_payload().decode(message.html_part.charset)

# Make sure the email is html and not plain text type.
if message.html_part != None:
    # Parse the html doc for the body of the email using beautiful soup.
    soup = BeautifulSoup(html_payload, 'html.parser')

    text_body = soup.get_text()
    print(text_body)
