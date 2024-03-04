import requests
import os
import lxml
from bs4 import BeautifulSoup
import smtplib

TARGET_PRICE = 100
PRODUCT_URL = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"
USER_AGENT = os.environ["USER_AGENT"]
headers = {
    "User-Agent": USER_AGENT,
    "Accept-Language": "en-US,en;q=0.9",
    "sec-ch-ua-platform": "Windows",
}
MY_EMAIL = os.environ["MY_EMAIL"]
APP_PASSWORD = os.environ["APP_PASSWORD"]

response = requests.get(url=PRODUCT_URL, headers=headers)
contents = response.text
soup = BeautifulSoup(markup=contents, features="lxml")

price_dollars = soup.find(class_="a-price-whole").getText()
price_cents = soup.find(class_="a-price-fraction").getText()
product_name = soup.find(id="productTitle").getText().strip()
product_price = float(price_dollars + price_cents)

# Check's if the price of the product is low enough before sending email:
if product_price < TARGET_PRICE:
    # Here, the email I'm using is a gmail account:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=APP_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=MY_EMAIL,
                            msg=f"Subject: Amazon Price Alert!\n\n"
                                f"The product '{product_name}' is now ${product_price}.\n"
                                f"Check it out now: {PRODUCT_URL}".encode("utf-8"))
