import re
import string
import sys
from typing import Optional
import xml.etree.ElementTree as ET
from datetime import datetime

from mloader.constants import Language

def is_oneshot(chapter_name: str, chapter_subtitle: str) -> bool:
    chapter_number = chapter_name_to_int(chapter_name)

    if chapter_number is not None:
        return False

    for name in (chapter_name, chapter_subtitle):
        name = name.lower()
        if "one" in name and "shot" in name:
            return True
    return False


def chapter_name_to_int(name: str) -> Optional[int]:
    try:
        return int(name.lstrip("#"))
    except ValueError:
        return None


def escape_path(path: str) -> str:
    return re.sub(r"[^\w]+", " ", path).strip(string.punctuation + " ")


def is_windows() -> bool:
    return sys.platform == "win32"

def generate_comic_info(chapter_title, chapter_release_date, chapter_number, series_name, author, language, is_manga = True):
    release_date = datetime.fromtimestamp(chapter_release_date)
    comic_info = ET.Element('ComicInfo')
    ET.SubElement(comic_info, 'Title').text = chapter_title
    ET.SubElement(comic_info, 'Series').text = series_name
    ET.SubElement(comic_info, 'Number').text = str(chapter_number)
    ET.SubElement(comic_info, 'Year').text = release_date.strftime("%Y")
    ET.SubElement(comic_info, 'Month').text = release_date.strftime("%m")
    ET.SubElement(comic_info, 'Day').text = release_date.strftime("%d")
    ET.SubElement(comic_info, 'Writer').text = author
    ET.SubElement(comic_info, 'LanguageISO').text = Language(language).name
    ET.SubElement(comic_info, 'Manga').text = "YesAndRightToLeft" if is_manga else "No"
    return ET.tostring(comic_info)