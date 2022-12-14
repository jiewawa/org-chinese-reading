#!/usr/bin/env python
import re
import io
import sys
import zipfile
from bs4 import BeautifulSoup
from os.path import exists

input_file = sys.argv[1]

def print_book_title(soup):
    if soup.find("doctitle"):
        book_title = soup.find("doctitle").text
    elif soup.find("docTitle"):
        book_title = soup.find("docTitle").text
    print("* " + book_title.replace("\n", ""))

def output_as_org(hanzi_list):
    print(":PROPERTIES:")
    print(":characters: " + str(len(hanzi_list)))
    print(":END:")

def print_chapter_details(soup, archive):
    chapters = soup.find_all("navpoint")
    for chapter in chapters:
        title = chapter.text
        src = chapter.content['src']

        if "html" in src:
            html_src = src.split("html")[0] + "html"
            for page in archive.namelist():
                if html_src in page:
                    html_src = page
                    print("** " + title.replace("\n", ""))
                    with io.TextIOWrapper(archive.open(html_src), encoding="utf-8") as f:
                        # Remove the title tag from the file
                        title = r'<title>.*<\/title>'
                        modif_hanzi = re.sub(title, '', f.read())
                        # Return only chinese characters
                        hanzi_regex = re.compile(r'[\u4E00-\u9FA5]')
                        hanzi_list = hanzi_regex.findall(modif_hanzi)
                        output_as_org(hanzi_list)

def count_chinese_characters_in_chapter(epub):
    with zipfile.ZipFile(epub, mode="r") as archive:
        for name in archive.namelist():
            if name.endswith(".ncx"):
                with io.TextIOWrapper(archive.open(name), encoding="utf-8") as f:
                    toc = f.read()
                    soup = BeautifulSoup (toc, features="lxml")

                    print_book_title(soup)
                    print_chapter_details(soup, archive)

def check_if_epub(input_file):
    if input_file.endswith(".epub") and exists(input_file):
        return True
    else:
        print(input_file + " is not an epub file.")

if check_if_epub(input_file):
    count_chinese_characters_in_chapter(input_file)

