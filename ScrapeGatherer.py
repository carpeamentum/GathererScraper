from lxml import html
from lxml import etree
import requests
import os
import sys
from StringIO import StringIO
import easygui

color_folders=True
if len(sys.argv)<2:
    set_name = easygui.enterbox("Which set would you like pictures for? ", "Gatherer Scraper" )
    print "Downloading :" + set_name

else:
    if len(sys.argv)>2:
        color_folders=False
    set_name = sys.argv[1]

url_set_name = set_name.replace(' ','+')
template_url = "http://gatherer.wizards.com/Pages/Search/Default.aspx?page={page}&output=spoiler&method=visual&set=%5b{mtgset}%5d"
color_template_url = "http://gatherer.wizards.com/Pages/Search/Default.aspx?output=spoiler&method=visual&action=advanced{color}&set=+%5b\"{mtgset}\"%5d"
url_base = 'http://gatherer.wizards.com'
image_directory_base=set_name+' '+'Card Images'

ColorSelectors = [ ('Gold and Colorless','&color=+[C]'),
                   ('W','&color=+%40(+%5bW%5d)'),
                   ('U','&color=+%40(+%5bU%5d)'),
                   ('B','&color=+%40(+%5bB%5d)'),
                   ('R','&color=+%40(+%5bR%5d)'),
                   ('G','&color=+%40(+%5bG%5d)'),
                   ('Gold and Colorless','&color=+^(|[W]|[U]|[B]|[R]|[G])')
                    ]


if not os.path.exists(image_directory_base):
    os.makedirs(image_directory_base)
if color_folders:
    for color in ColorSelectors:
        color_directory = image_directory_base+'/'+color[0]
        if not os.path.exists(color_directory):
            os.makedirs(color_directory)

def extract_card_images_from_page(url, image_directory):
    card_page = requests.get(url, stream=True)
    card_page.raw.decode_content = True
    card_tree = html.parse(card_page.raw)
    card_images = card_tree.xpath("//img[contains(@src,'multiverseid=')]")
    for image in  card_images:
        path = image_directory+"/"+ (image.get('alt').replace('!','').replace('//','and').replace('/','')) +".png"
        card_url = image.get('src').replace('../..',url_base)
        print path
        img_data = requests.get(card_url, stream=True)
        if img_data.status_code == 200:
            with open(path, 'wb') as f:
                for chunk in img_data.iter_content(1024):
                    f.write(chunk)

if color_folders:
        for color in ColorSelectors:
            page_url = color_template_url.format(page=0,mtgset=url_set_name,color=color[1])
            image_dir = image_directory_base+'/'+color[0]
            page = requests.get(page_url, stream=True)
            page.raw.decode_content = True
            tree = html.parse(page.raw)
            page_links = tree.xpath("//div[@class='paging']/a")
            if page_links == []:
                extract_card_images_from_page(page_url,image_dir)
            else:
                
                for page in page_links:
                    page_url = url_base+page.get('href')
                    extract_card_images_from_page(page_url, image_dir)


            






    
