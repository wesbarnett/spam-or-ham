from app import app
from joblib import load
from bs4 import BeautifulSoup
from email import message_from_bytes, message_from_string
from nltk.stem.porter import PorterStemmer
from re import sub
from string import punctuation
from sklearn.feature_extraction.text import CountVectorizer

def process_email(txt):
    """
    Takes an email message and cleans it up for use with CountVectorizer().
    """
    if (type(txt) == bytes):
        msg_email = message_from_bytes(txt)
    else:
        msg_email = message_from_string(txt)
        
    # Only use the message body
    # https://stackoverflow.com/a/32840516    
    msg = ''
    if msg_email.is_multipart():
        for part in msg_email.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))
            # skip any text/plain (txt) attachments
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                body = part.get_payload()
                break
    else:
        msg = msg_email.get_payload()
        
    # Conver to all lowercase
    msg = msg.lower()
    
    # Remove line breaks
    msg = sub('\n', ' ', msg)
    msg = sub('\t', ' ', msg)
    
    # Stip HTML
    soup = BeautifulSoup(msg, 'lxml')
    msg = soup.get_text()
    
    # Convert numbers, urls, email addresses, and dollar signs
    msg = sub('[0-9]+', 'number', msg)
    msg = sub('(http|https)://[^\s]*', 'httpaddr', msg)
    msg = sub('[^\s]+@[^\s]+', 'emailaddr', msg)
    msg = sub('[$]+', 'dollar', msg)
    
    # Remove additional punctuation
    table = str.maketrans({key: None for key in punctuation})
    msg = msg.translate(table)
    return msg

def stemmed_words(doc):
    """
    Calls the email cleaner and then does stemming. This should be defined as the 'analyzer' in CountVectorizer().
    """
    doc = process_email(doc)
    return (stemmer.stem(w) for w in analyzer(doc))

if __name__ == '__main__':
    stemmer = PorterStemmer()
    analyzer = CountVectorizer(decode_error='ignore').build_analyzer()
    app.run(port=8080)
