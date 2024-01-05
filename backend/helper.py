import logging

import requests
from bs4 import BeautifulSoup

from backend.schemas import Message


def extract_messages(response: requests.Response) -> list[Message]:
    soup = BeautifulSoup(response.content, "lxml")
    tgpost = soup.find_all("div", class_="tgme_widget_message")
    messages = []

    for content in tgpost:
        full_message = {}
        try:
            full_message["views"] = content.find(
                "span", class_="tgme_widget_message_views"
            ).text
            full_message["timestamp"] = content.find("time", class_="time").text
            full_message["text"] = content.find(
                "div", class_="tgme_widget_message_text"
            ).text

            messages.append(full_message)
        except AttributeError:
            logging.info("AttributeError")

    return messages
