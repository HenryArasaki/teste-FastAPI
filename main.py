from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "pikachumilkemail@gmail.com"
receiver_email = "henry_arasaki@hotmail.com"
password = input("Type your password and press enter:")


def enviar_email(html):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Aviso dos gatinhos"
    message["From"] = sender_email
    message["To"] = receiver_email

    message.attach(MIMEText(html, "html"))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )




app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    html = f"""\
    <html>
      <body>
        <p>Hi,{q}<br>
           How are you?{item_id}
        </p>
      </body>
    </html>
    """
    enviar_email(html)
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}