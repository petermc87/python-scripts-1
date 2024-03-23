import imapclient
import pyzmail
import re
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

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


def word_match(body, addresses, subject, keywords):
    
    # Combine the strings
    email = f'{addresses} {subject} {body}'
    
    # Parsing to check if it exists in the email.
    # NOTE: The escape is used to escape special characters so that they
    # dont affect the regular expression syntax. \b is used to search a 
    # whole word.
    # keywordRegex = re.compile(r'\b' + re.escape(keywords) + r'\b')
    # 1. r -> Raw string literal, 
    # 2. \b -> Matching the boundary between a word and non word
    # 3. '|'.join(map(re.escape, keywords) -> This is using the escape on characters that may 
    # appear in the word that could affect the regex function.
    # 4. r')\b -> Ending of the boundary between a word that is not part of a larger word.
    pattern = r'\b(?:' + '|'.join(map(re.escape, keywords)) + r')\b'
    
    keywordRegex = re.compile(pattern)
    
    # Checking for a match
    match = keywordRegex.search(email)
    
    # if match:
    #     print('Keyword found in: ', subject)
    if match:
        return True
    return False


#### FUNCTION TO CHECK EACH MESSAGE ####
def message_check(messageId):

    global keywords
    print(messageId, keywords) # --> ARGUMENTS GETTING PASSED.
    # for i in messages:
    # Fetch an email
    rawMessage = conn.fetch([messageId], ['BODY[]', 'FLAGS'])
    
    print(rawMessage)
    
    
    # Use pyzmail to retrieve the message info.
    messageBody = pyzmail.PyzMessage.factory(rawMessage[messageId][b'BODY[]'])

    # Get subject, from, to and bcc
    addresses = messageBody.get_addresses('from')[0][1], messageBody.get_addresses('to')[0][1], messageBody.get_addresses('bcc')
    subject = messageBody.get_subject()


    # print(messageBody, addresses, subject) # --> NOTHING RETURNED.
    # Make sure the email is html and not plain text type.
    if messageBody.html_part != None:
        # Get the email in HTML form
        html_payload = messageBody.html_part.get_payload().decode(messageBody.html_part.charset)
        # Parse the html doc for the body of the email using beautiful soup.
        soup = BeautifulSoup(html_payload, 'html.parser')
        text_body = soup.get_text()
        if word_match(text_body, addresses, subject, keywords):
            print('Keyword found in: ', subject)
            
            
        #     # Check if a word match gets returned
        # word_match(text_body, addresses, subject, keywords)
                
    # else: return 
    
    


# Create an input to ask to user what folder to search
inputted_folder = 'inbox'

keywords = []

enter_more = 'y'

while enter_more == 'y':
    # Input asking for keyword
    keyword = input("Enter a keyword: ").lower()
    keywords.append(keyword)
    enter_more = input("Do you want to enter more keywords? (y/n): ").lower()
    


# Pass the message into the get folder function
returned_messages = get_folder(inputted_folder)


# Use threadpool to check multiple messages at once (parallelism).
# NOTE: This will mean that the regex expression will only be
# compiled once, which is happening in the loop (for) within the
# the message check method.
with ThreadPoolExecutor() as executor:
    executor.map(lambda messageId: message_check(messageId), returned_messages)
    
    
    
# Return the message information contained within each
# message_check(returned_messages, keywords)





    
    
    
    

    
    
    
    
    




# ---> SEARCHING BY DATE <--- #
#
# date_str = "01-Jan-2024"
# # Convert the string to a datetime object
# date_obj = datetime.strptime(date_str, "%d-%b-%Y")
# # Pass the formatted string into conn.search
# formatted_date_str = date_obj.strftime("%Y-%m-%d")
# UUIds = conn.search(['SINCE 01-Jan-2024'])
# print(UUIds)
