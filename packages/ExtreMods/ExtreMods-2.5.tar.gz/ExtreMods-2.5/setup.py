import re

import setuptools



with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

name = "ExtreMods"
author = "AmanPandey"
author_email = "paman7647@gmail.com"
description = "A Secure  and Powerful Python-Telethon Based Library For ExtemePro Userbot."
license = "GNU AFFERO GENERAL PUBLIC LICENSE (v3)"
url = "https://github.com/TeamExtremePro/ExtremeProUserbot"

setuptools.setup(
    name=name,
    version=2.5,
    author=author,
    author_email=author_email,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=url,
    license=license,
    packages=setuptools.find_packages(),
    install_requires=[
"aiofiles",
"aiohttp[speedups]",
"cloudscraper",
"colour",
"covid",
"cowpy",
"dataclasses",
"DateTime",
"emoji",
"fonttools",
"geopy",
"gitpython",
"glitch_this",
"google-api-python-client",
"google-auth-httplib2",
"google-auth-oauthlib",
"googletrans==4.0.0-rc1",
"gtts",
"hachoir",
"heroku3",
"html-telegraph-poster",
"humanize",
"jikanpy",
"justwatch",
"lottie",
"lyricsgenius",
"motor",
"moviepy",
"nekos.py",
"Pillow",
"prettytable",
"prsaw",
"psutil",
"psycopg2",
"PyDictionary",
"pyfiglet",
"PyGithub",
"pygments",
"pylast",
"pymediainfo",
"pySmartDL",
"python-barcode",
"python-dotenv",
"pytz",
"qrcode",
"regex",
"requests",
"search-engine-parser",
"selenium",
"setuptools",
"ShazamAPI",
"spamwatch",
"speedtest-cli",
"sqlalchemy-json",
"sqlalchemy==1.3.23",
"telegraph",
"Telethon",
"TgCrypto",
"tswift",
"ujson",
"urlextract",
"validators",
"vcsi",
"wand",
"wget",
"wikipedia",
"youtube-search-python",
"youtube_dl",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
