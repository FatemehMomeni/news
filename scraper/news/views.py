from django.shortcuts import render
from requests import get
from bs4 import BeautifulSoup
from warnings import warn


def index(request):
    if request.method == "POST":
        start_date = request.POST['start-date']
        end_date = request.POST['end-date']
        number = request.POST['number']
        # *******************************************************************************************
        # function filter time for isna
        def filter_time(dy, mn, dy_e):
            if int(dy) != int(dy_e):
                filter_time(str(int(dy) + 1), mn, dy_e)
            else:
                page = get('https://www.isna.ir/archive?pi=1&ms=0&dy=' + dy + '&mn=' + mn + '&yr=1399')
                soup = BeautifulSoup(page.content, 'html.parser')
                news = soup.find_all('div', class_='desc')
                for n in news:
                    h3 = n.find('h3')
                    url = 'https://www.isna.ir' + [a["href"] for a in n.find_all("a", href=True)][0]
                    h2 = h3.text
                    p = n.p.text
                    time = n.find("a", title=True)["title"]
                    day = str(time).split('-')[0]
                    news_dic_filter_time.setdefault(day, []).append(h2)
                    news_dic_filter_time.setdefault(day, []).append(p)
                    news_dic_filter_time.setdefault(day, []).append(url)
                    news_dic_filter_time.setdefault(day, []).append(time)

        # function filter time for irna
        def filter_time2(dy, mn, dy_e):
            if int(dy) != int(dy_e):
                filter_time2(str(int(dy) + 1), mn, dy_e)
            else:
                page = get(
                    'https://www.irna.ir/page/archive.xhtml?mn=' + mn + '&wide=0&dy=' + dy + '&ms=0&pi=1&yr=1399')
                soup = BeautifulSoup(page.content, 'html.parser')
                news = soup.find_all('div', class_='desc')
                for n in news:
                    h3 = n.find('h3')
                    url = 'https://www.isna.ir' + [a["href"] for a in n.find_all("a", href=True)][0]
                    h2 = h3.text
                    p = n.p.text
                    time = n.find("time").text
                    day = str(time).split('-')[2].split(' ')[0]
                    news_dic_filter_time2.setdefault(day, []).append(h2)
                    news_dic_filter_time2.setdefault(day, []).append(p)
                    news_dic_filter_time2.setdefault(day, []).append(url)
                    news_dic_filter_time2.setdefault(day, []).append(time)

        # --------------------------------------------------------------------------------------- Start Scrapping www.isna.ir

        news_dic = dict()
        news_dic_filter_time = dict()

        #print("add number of news :")
        num = number
        page = get('https://www.isna.ir/archive')
        # Throw a warning for non-200 status codes
        if page.status_code != 200:
            warn('Status code: {}'.format(page.status_code))

        soup = BeautifulSoup(page.content, 'html.parser')
        news = soup.find_all('div', class_='desc')
        # filter by number of news
        for n in news[0:int(num)]:
            h3 = n.find('h3')
            url = 'https://www.isna.ir' + [a["href"] for a in n.find_all("a", href=True)][0]
            h2 = h3.text
            p = n.p.text
            time = n.find("a", title=True)["title"]
            day = str(time).split('-')[0]
            news_dic.setdefault(day, []).append(h2)
            news_dic.setdefault(day, []).append(p)
            news_dic.setdefault(day, []).append(url)
            news_dic.setdefault(day, []).append(time)

        # filter by time
        #print("add start and end time to filter news : ")
        start = start_date
        end = end_date
        day_s = str(start).split('/')[0]
        month_s = str(start).split('/')[1]
        day_e = str(end).split('/')[0]
        month_e = str(end).split('/')[1]

        if month_e == month_s:
            filter_time(day_s, month_s, day_e)
        elif month_e != month_s:
            filter_time(day_s, month_s, '30')
            filter_time('1', month_e, day_e)

        # --------------------------------------------------------------------------------------- Start Scrapping www.irna.ir
        news_dic2 = dict()
        news_dic_filter_time2 = dict()
        #print("add number of news :")
        num2 = number
        page2 = get('https://www.irna.ir/archive')
        # Throw a warning for non-200 status codes
        if page2.status_code != 200:
            warn('Status code: {}'.format(page2.status_code))

        soup2 = BeautifulSoup(page2.content, 'html.parser')
        news2 = soup2.find_all('div', class_='desc')
        # filter by number of news
        for n in news2[0:int(num2)]:
            h3 = n.find('h3')
            url = 'https://www.irna.ir' + [a["href"] for a in n.find_all("a", href=True)][0]
            h2 = h3.text
            p = n.p.text
            time = n.find("time").text
            day = str(time).split('-')[2].split(' ')[0]
            print(time, day)
            news_dic2.setdefault(day, []).append(h2)
            news_dic2.setdefault(day, []).append(p)
            news_dic2.setdefault(day, []).append(url)
            news_dic2.setdefault(day, []).append(time)

        # filter by time
        #print("add start and end time to filter news : ")
        start2 = start_date
        end2 = end_date
        day_s2 = str(start2).split('/')[0]
        month_s2 = str(start2).split('/')[1]
        day_e2 = str(end2).split('/')[0]
        month_e2 = str(end2).split('/')[1]

        if month_e2 == month_s2:
            filter_time2(day_s2, month_s2, day_e2)
        elif month_e2 != month_s2:
            filter_time2(day_s2, month_s2, '30')
            filter_time2('1', month_e2, day_e2)

        # *******************************************************************************************

        return render(request, 'blog.html', {})
    else:
        #return page
        return render(request, 'index.html', {})


def blog(request):
    return render(request, 'blog.html', {})



