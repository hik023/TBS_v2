import lxml.html
import urllib.request
import requests
import xlrd
import sqlite3

class ITMM_parser():
    def __init__(self, url):
        self.base_url = url
        self.last_time = ''

    def getpage(self):

        try:
            r = requests.get(self.base_url)
        except requests.ConnectionError:
            return

        if r.status_code < 400:
            return r.content

    def parse(self, html):
        html_tree = lxml.html.fromstring(html)
        href = html_tree.xpath(".//p[text() = 'Расписание бакалавров ']/a")
        return href[0].get('href')

    def parse2(self, html):
        html_tree = lxml.html.fromstring(html)
        href = html_tree.xpath(".//p/a")
        hrefs = []
        for el in href:
            try:
                hrefs.append(el.get('href'))
            except:
                pass
        for key in hrefs:
            try:
                k = key.index('bak')
                return key
            except:
                pass
        return None

    def add_user(self, user):
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        c.execute("SELECT * FROM ids")
        rawdata = c.fetchall()
        list_users = [id[0] for id in rawdata]
        if user in list_users:
            print('User already in table')

        else:
            print(str(user) + " added.")
            c.execute("INSERT INTO ids VALUES ('{0}')".format(user))
            conn.commit()

        conn.close()

    def del_table(self):
        conn = sqlite3.connect('example.db')
        c = conn.cursor()

    def dispatch(self):
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        c.execute("SELECT * FROM ids")
        rawdata = c.fetchall()
        list_users = [id[0] for id in rawdata]
        return list_users

    def download(self, link):

        file_url = urllib.request.URLopener()
        file_url.retrieve(link, filename='table.xls')

    def update(self, link):
        with open('last_link.txt', 'r') as ll:
            ll_temp = ll.readlines()[-1]
        if link == ll_temp:
            return 0 #"Обновлений нет"
        else:
            with open('last_link.txt', 'w') as ll:
                ll.write(link)
                self.download(link)
            return 1 #"Расписание обновлено"

    def run(self):
        # открываем файл

        rb = xlrd.open_workbook('table.xls', formatting_info=True)

        # выбираем активный лист
        sheet = rb.sheet_by_index(0)

        columns = [sheet.col_values(col) for col in range(sheet.ncols)]
        for column in columns[1]:
            try:
                new_date = xlrd.xldate_as_tuple(column, rb.datemode)
                columns[1][columns[1].index(column)] = '{0}:{1}'.format(new_date[3], (
                lambda: '00' if new_date[4] == 0 else str(new_date[4]))())
            except:
                pass

        # for cell in range(len(columns)):
        #     print('{0:11}|{1:7}|{2:45}|{3:45}|'.format(columns[0][cell],columns[1][cell],(str(columns[4][cell])+str(columns[5][cell])),(str(columns[6][cell])+str(columns[7][cell]))))

        for crange in sheet.merged_cells:
            print(crange)

if __name__ == '__main__':
    prs = ITMM_parser("www.vk.com")
    prs.add_user('132')
    print(prs.dispatch())