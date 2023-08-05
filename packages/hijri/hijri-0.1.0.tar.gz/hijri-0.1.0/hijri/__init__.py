"""A package to fetch hijri date in Arabic"""

__version__ = '0.1.0'

# -*- coding: utf-8 -*-

import os, arabic_reshaper
from bidi.algorithm import get_display

os.system("touch temp_hijri_date_fetcher.txt")
os.system("wget -q --no-check-certificate -O - http://alriyadh.com | xmllint --html --xpath '/html/body/div[1]/nav/div/div[2]/span/text()' - 2>/dev/null | xargs > temp_hijri_date_fetcher.txt")

class Hijri:
    def __init__(self):
        pass

    def fetch(self):
        with open("temp_hijri_date_fetcher.txt", "r") as file:
            date_obtained = file.readline()
            os.system("rm temp_hijri_date_fetcher.txt")
            arabic_reshaped_text = arabic_reshaper.reshape(date_obtained)
            bidi_text = arabic_reshaped_text

        hijri_date = str(bidi_text).replace("GMT+3", "")
        get_display("\n" + hijri_date[:hijri_date.index('ـ')])

        return get_display(hijri_date[:hijri_date.index('ـ')])
