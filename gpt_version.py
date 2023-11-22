import requests
from bs4 import BeautifulSoup
from tkinter import *

class Weather:
    def __init__(self, link):
        self.link = link
        r = requests.get(self.link).text
        self.soup = BeautifulSoup(r, "html.parser")

    def get_cities(self):
        data = self.soup.find_all('a')
        print(data)

        links = {}
        for block in data:
            text = str(block)  # Changed from block.str() to str(block)
            name = block.get_text()
            text = text[text.find('href="'):][6:]
            last = text.find('"')
            text = text[:last]
            if name not in ('Мобильная версия', 'Главная', 'О сайте', 'Частые вопросы (FAQ)', 'Контакты',
                             'Литва', 'Беларусь', 'Россия', 'Украина', 'Все страны', '>>>', 'См. на карте', ''):
                links[name] = "https://rp5.ru" + text
                print(links[name])

        print(links)
        return Window(links).root.mainloop()

class Window:
    def __init__(self, links):
        self.root = Tk()
        self.root.geometry("800x600")
        self.root.title("Прогноз погоды")
        self.check = []
        self.label = Label(self.root, wraplength=800, font=("Trebuchet MS", 11))
        self.label.grid(row=0, column=0, columnspan=2)
        self.set_text(links)
        self.entry = Entry(self.root, width=50)
        self.entry.grid(row=1, column=0, sticky='E')
        self.btn = Button(self.root, text="Ввод", command=lambda: self.check_input(links))  # Removed parameter from lambda
        self.btn.grid(row=1, column=1, sticky='W')

    def set_text(self, links):
        text = ""
        for city in links:
            self.check.append(city)
            text += city + ', '
        text = text[:-2]
        self.label.configure(text=text)

    def check_input(self, links):
        choice = self.entry.get()
        if choice not in self.check:
            return
        self.parse_weather(links[choice])

    def parse_weather(self, link):
        w = Weather(link)
        data = w.soup.find('div', {'id': 'archiveString'})
        if data:
            temp_element = data.find('span', {'class': 't_0'})
            if temp_element:
                temp = temp_element.text
            else:
                temp = "Temperature not found"

            text_element = data.find('a', {'class': 'ArchiveStrLink'})
            if text_element is None:
                text_element = data.find('div', {'class': 'ArchiveInfo'})

            if text_element:
                text = text_element.text.replace("Архив погоды на метеостанции", "")
            else:
                text = "Additional information not found"

            self.label.configure(text=temp + "\n" + text)


w = Weather("https://rp5.ru/Погода_в_России")
w.get_cities()
