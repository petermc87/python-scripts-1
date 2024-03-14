import imapclient
import pyzmail
from bs4 import BeautifulSoup

conn = imapclient.IMAPClient('imap.gmail.com', ssl=True)
checker = conn.login('peter@mapandsnap.org', 'ivwp odox lswn ekbz')

#### FUNCTION TO SELECT A FOLDER ####
def get_folder(folder):
    # Select the folder
    conn.select_folder(folder, readonly=False)


    # Retrieve all message IDs from INBOX
    messages = conn.search("ALL")
    
    return messages
    # print(messages)


#### FUNCTION TO CHECK EACH MESSAGE ####
def message_check(messages):

    for i in messages:
        ### TEST ONLY 3 ###
        if i < 3:
            # Fetch an email
            rawMessage = conn.fetch([i], ['BODY[]', 'FLAGS'])
            # print(rawMessage)

            # Use pyzmail to retrieve the message info.
            message = pyzmail.PyzMessage.factory(rawMessage[i][b'BODY[]'])

            # Get subject, from, to and bcc
            print(message.get_addresses('from')[0][1], message.get_addresses('to')[0][1], message.get_addresses('bcc'))
            print(message.get_subject())


            # Make sure the email is html and not plain text type.
            if message.html_part != None:
                # Get the email in HTML form
                html_payload = message.html_part.get_payload().decode(message.html_part.charset)
                # Parse the html doc for the body of the email using beautiful soup.
                soup = BeautifulSoup(html_payload, 'html.parser')

                text_body = soup.get_text()
                print(text_body)
        else: return 
    
    


# Create an input to ask to user what folder to search
inputted_folder = input('What folder do you want to search:')

# Convert the input to a string and to uppercase
converted_input = str(inputted_folder).upper()

# Pass the message into the get folder function
returned_messages = get_folder(converted_input)

# Return the message information contained within each
message_check(returned_messages)





    
    
    
    

    
    
    
    
    




# ---> SEARCHING BY DATE <--- #
#
# date_str = "01-Jan-2024"
# # Convert the string to a datetime object
# date_obj = datetime.strptime(date_str, "%d-%b-%Y")
# # Pass the formatted string into conn.search
# formatted_date_str = date_obj.strftime("%Y-%m-%d")
# UUIds = conn.search(['SINCE 01-Jan-2024'])
# print(UUIds)
