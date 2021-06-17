"""
utils.py
"""

import urllib
from math import floor, ceil
import random
import os
import cv2
import pandas
import requests
import numpy as np
from bs4 import BeautifulSoup
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from pyproj import Transformer
from classification.classifier import find_color_image
from .models import Tile, Classification, User
from .tokens import TOKEN_GENERATOR


def extract_available_years():
    """
    def extract_available_years()
    """

    page = requests.get("https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services")
    soup = BeautifulSoup(page.content, 'html.parser')
    years = {}

    for hyperlink in soup.select("ol[id=serviceList] > li > a[id=l1]"):
        if hyperlink.text.startswith("Historische_tijdreis_"):
            reference = hyperlink.text[len("Historische_tijdreis_"):]

            if "_" in reference:
                for i in range(int(reference[: reference.index("_")]), int(reference[reference.index("_") + 1:]) + 1):
                    years[i] = reference
            else:
                years[int(reference)] = reference

    if 2020 not in years:
        years[2020] = "2020"

    return years


def send_email(uid, domain, email_subject, email_template):
    """
    def send_email(uid, domain, email_subject, email_template)
    """

    try:
        user = User.objects.get(pk=uid)
    except ObjectDoesNotExist:
        user = None

    if user is not None:
        email_message = render_to_string(email_template, {
            "user": user,
            "domain": domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": TOKEN_GENERATOR.make_token(user),
        })
        email = EmailMessage(email_subject, email_message, to=[user.email])
        email.send()
        return True

    return False
