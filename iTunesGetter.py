from email.mime.text import MIMEText
import requests
import json
import smtplib

# Email credentials
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_user = 'tuliloaspauga@gmail.com'
#app password
smtp_password = 'rntg tjnl ateo fswi'
# Recipient's email address
recipient_email = '7605002405@txt.att.net'

def sendSMS(movie,price):
    prettyMovie = prettifyMovieName(movie)
    subject = f"Update for movie '{prettyMovie}'"
    body = f"The price has fallen to {price}"

    message = MIMEText(body)
    message['Subject'] = subject
    message['From'] = smtp_user
    message['To'] = recipient_email

    # SMTP server setup
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.set_debuglevel(1)
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, recipient_email, message.as_string())

    print("Email sent successfully!")


def keepTrackOfSMSDelivered(movieName):
    try:
        #open json file in read only 'r'
        with open('SMStracking.json','r') as file:

            #read JSON data
            data = json.load(file)
            if data[movieName] == "true":
                return False
            else:
                data[movieName] = "true"
                newData = json.dumps(data)
                with open('SMStracking.json','w') as file:
                    file.write(newData)
                return True
            

    except Exception as e:
        print(f"Error: {e}")

def ensureToSendLater(movieName):
    try:
        #open JSON file in write only 'r'
        with open('SMStracking.json','r') as file:
            #read JSON data
            data = json.load(file)
            data[movieName] = "false"
            newData = json.dumps(data)
            with open('SMStracking.json','w') as file:
                file.write(newData)


    except Exception as e:
        print(f"Error: {e}")

def prettifyMovieName(movie):
    words = movie.split("+")
    newStr = ' '.join(word.capitalize() for word in words)  
    return newStr

# Base URL
URL = "http://itunes.apple.com/search?term="

#Array of movies, URL format
myDictOfMovies = ["guy+ritchies+the+covenant","killers+of+the+flower+moon","dream+scenario","the+babadook"]

for movie in myDictOfMovies:
    #concatanate base URL with movie
    newURL = URL + movie
    # HTTP GET request with the new URL
    response = requests.get(newURL)
    if response:
        # load the text version of the data from the HTTP GET request into myDict
        myDict = json.loads(response.text)
        if not myDict['resultCount'] == 0:
            if 'results' in myDict and isinstance(myDict['results'],list):
                results = myDict['results'][0]
                if 'trackHdPrice' in results:
                    price = results['trackHdPrice']
                    # print("The price for " + movie + " is $" + str(price))
                    if price < 10:
                        if keepTrackOfSMSDelivered(movie):
                            print("send sms")
                            sendSMS(movie,price)
                        else:
                            print("dont send sms")
                    else:
                        ensureToSendLater(movie)
                        print(f"{movie} is still overpriced")
                else:
                    print("Couldn't find it")
            else:
                print("Results not in the get request")
        else:
            print("Couldn't find a movie by that name")
