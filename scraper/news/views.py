from django.shortcuts import render

import requests
from bs4 import BeautifulSoup

isna_html = requests.get('https://www.isna.ir')
isna_soup = BeautifulSoup(isna_html.content, 'html.parser')
isna_heading = isna_soup.find_all('h3')
isna_news = []
for isna_header in isna_heading:
    isna_news.append(isna_header.get_text())


irna_html = requests.get('https://www.irna.ir')
irna_soup = BeautifulSoup(irna_html.content, 'html.parser')
irna_heading = irna_soup.find_all('h3')
irna_news = []
for irna_header in irna_heading:
    irna_news.append(irna_header.get_text())

print(isna_news)
print(irna_news)


"""def index(request):
    return render(request, 'news/index.html', {"isna_news": isna_news, "irna_news": irna_news})
"""



