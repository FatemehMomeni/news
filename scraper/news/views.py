from django.shortcuts import render
from requests import get
from bs4 import BeautifulSoup
from warnings import warn

isna_h2_list = []
isna_p1_list = []
isna_url_list = []
isna_time_list = []

irna_h2_list = []
irna_p1_list = []
irna_url_list = []
irna_time_list = []


#function filter time for isna
def filter_time(dy, mn, dy_e, num):
    while int(dy) <= int(dy_e):
        page = get('https://www.isna.ir/page/archive.xhtml?mn='+mn+'&wide=0&dy='+dy+'&ms=0&pi=2&yr=1399')
        soup = BeautifulSoup(page.content, 'html.parser')
        news = soup.find_all('div', class_='desc')
        for n in news[0:int(num)]:
            h3 = n.find('h3')
            url = 'https://www.isna.ir' + [a["href"] for a in n.find_all("a", href=True)][0]
            h2 = h3.text
            p1 = n.p.text
            time = n.find("a", title=True)["title"]
            isna_h2_list.append(h2)
            isna_p1_list.append(p1)
            isna_url_list.append(url)
            isna_time_list.append(time)
        dy = str(int(dy) + 1)


#function filter time for irna
def filter_time2(dy, mn, dy_e, num):
    while int(dy) <= int(dy_e):
        page = get('https://www.irna.ir/page/archive.xhtml?mn='+mn+'&wide=0&dy='+dy+'&ms=0&pi=1&yr=1399')
        soup = BeautifulSoup(page.content, 'html.parser')
        news = soup.find_all('div', class_='desc')
        for n in news[0:int(num)]:
            h3 = n.find('h3')
            url = 'https://www.irna.ir' + [a["href"] for a in n.find_all("a", href=True)][0]
            h2 = h3.text
            p1 = n.p.text
            time = n.find("time").text
            irna_h2_list.append(h2)
            irna_p1_list.append(p1)
            irna_url_list.append(url)
            irna_time_list.append(time)
        dy = str(int(dy) + 1)
# --------------------------------------------------------------------------------------- Start Scrapping www.isna.ir


def index(request):
    isna_h2_list.clear()
    isna_p1_list.clear()
    isna_url_list.clear()
    isna_time_list.clear()
    irna_h2_list.clear()
    irna_p1_list.clear()
    irna_url_list.clear()
    irna_time_list.clear()
    if request.method == "POST":
        start_date = request.POST['start-date']
        end_date = request.POST['end-date']
        number = request.POST['number']

        print("add number of news :")
        num = number
        # filter by time & number
        print("add start and end time to filter news : ")
        start = start_date
        end = end_date
        day_s = str(start).split('/')[0]
        month_s = str(start).split('/')[1]
        day_e = str(end).split('/')[0]
        month_e = str(end).split('/')[1]

        if month_e == month_s:
            filter_time(day_s, month_s, day_e, num)
        elif month_e != month_s:
            filter_time(day_s, month_s, '30', num)
            filter_time('1', month_e, day_e, num)

        # --------------------------------------------------------------------------------------- Start Scrapping www.irna.ir
        if month_e == month_s:
            filter_time2(day_s, month_s, day_e, num)
        elif month_e != month_s:
            filter_time2(day_s, month_s, '30', num)
            filter_time2('1', month_e, day_e, num)

        return render(request, 'blog.html', {'isna_h2_list': isna_h2_list, 'isna_p1_list': isna_p1_list,
                                             'isna_url_list': isna_url_list, 'isna_time_list': isna_time_list,
                                             'irna_h2_list': irna_h2_list, 'irna_p1_list': irna_p1_list,
                                             'irna_url_list': irna_url_list, 'irna_time_list': irna_time_list})
    else:
        return render(request, 'index.html', {})


def blog(request):
    return render(request, 'blog.html', {})


def blog2(request):
    return render(request, 'blog2.html', {})


