from os import name
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

from string import Template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MY_ADDRESS = "Email_HERE"
PASSWORD = "PASSWOED"

s = smtplib.SMTP(host='smtp.gmail.com', port=587)
s.starttls()
s.login(MY_ADDRESS, PASSWORD)

my_url = 'https://kfc.com.tn/lamarsa/31-hot-now'

uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, "html.parser")

# page_soup.h1

containers = page_soup.find_all("div", {"class": "thumbrel"})
# print(len(containers))

contain = containers[0]


# # this is the name of the meal
# contain.find("div", {"class": "wb-product-desc"}).h2.a

# # this is the desc of the meal
# contain.find("div", {"class": "wb-product-desc"}).p


# # this is the price of the meal

# contain.find("div", {"class": "product-price-and-shipping pricehv"}).span


def get_contacts():
    names = "name of receiver"
    emails = "email of receiver"
    return names, emails


def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


# set up the SMTP server


def notify():

    names, emails = get_contacts()
    message_template = read_template('message.txt')
   
    # For each contact, send the email:

    msg = MIMEMultipart()       # create a message

    # add in the actual person name to the message template
    message = message_template.substitute(
        PERSON_NAME=names.title(), MENU_NAME=item.title())

    # setup the parameters of the message
    msg['From'] = MY_ADDRESS
    msg['To'] = emails
    msg['Subject'] = "kfc Deal"

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    # send the message via the server set up earlier.
    s.send_message(msg)

    del msg


for contain in containers:
    item = contain.find("div", {"class": "wb-product-desc"}).h2.a.text
    price = contain.find(
        "div", {"class": "product-price-and-shipping pricehv"}).span.text
    print(item, price)
    if  price < "15.00 TND":
        notify()
