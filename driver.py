import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def get_recipients():
    with open('recipients.txt', 'r') as f:
        recipients = f.read().splitlines()

    return recipients


url = 'https://www.musiciansfriend.com/'
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

name = soup.find("div", {"class":"stupidName"}).get_text().strip('\n')
price_orig = soup.find("span", {"class":"regular-price"}).get_text().replace("$", '').replace("\"", "")
price_new = soup.find("span", {"class":"now"}).get_text().replace("$", '').replace("\"", "").replace("Your Price", "").strip('\t')
price_savings = soup.find("span", {"class":"savings"}).get_text().replace("$", '').replace("\"", "").replace("Save:", "").replace("Savings:","").strip('\n').strip('\t')
image = soup.find("img", {"class":"stupidImage"})['src']

port = 465
smtp_server = "smtp.gmail.com"
context = ssl.create_default_context()
email = 'stupiddealbot@gmail.com'
password = 'StupidDeal!'
recipients = get_recipients()

message = MIMEMultipart("alternative")
message["Subject"] = "The Stupid Deal of the Day: " + name
message["From"] = email
html = """\
    <html>
    <body>
        <h1>Musician's Friend Stupid Deal of the Day</h1>
        <h2>{name}</h2>
        <h3>Available for ${price_new}</h3>
        <img src="{image}" />
        <p>Previously ${price_orig}, you save ${price_savings} by buying with this deal.</p>
        <p>This promotion ends at 7:00 A.M Central Time. Get <a href="https://www.musiciansfriend.com/stupid">Stupid</a>.</p>
        <p>This action was performed by a bot. If you wish to unsubscribe, you may not. That is not possible yet. Sorry.</p>
    </body>
    </html>

    """.format(**locals())

# message.attach(MIMEText(html, "html"))
print("Email successfully sent to:", recipients)
# with smtplib.SMTP_SSL(smtp_server, port=port, context=context) as server:
#     server.login(email, password)
#     for recipient in recipients:
#         server.sendmail(email, recipient, message.as_string())
