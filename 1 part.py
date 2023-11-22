import requests
from bs4 import BeautifulSoup
from tkinter import *

class Window:
   def __init__(self, links):
      self.root = Tk()
      self.root.geometry("800x600")
      self.root.title("Прогноз погоды")
      self.check = []

      #Настройки текста
      self.label = Label(self.root, wraplength=800, font=("Trebuchet MS", 11))
      self.label.grid(row=0, column=0, columnspan=2)
      self.set_text(links)

      #Поле ввода
      self.entry = Entry(self.root, width=50)
      self.entry.grid(row=1, column=0, sticky='E')

      #Создание кнопки
      self.btn = Button(self.root, text="Ввод", command=lambda x=links: self.check_input(links))
      self.btn.grid(row=1, column=1, sticky='W')

   '''Создадим функцию установки текста на экране. 
   Она будет трансформировать словарь links в строку.'''
   def set_text(self, links):
      text = ""
      for city in links:
         self.check.append(city)
         text += city + ', '
      text = text[:-2]
      self.label.configure(text=text)

   '''Добавим функцию проверки 
   введённых пользователем значений.'''

   def check_input(self, links):
      choice = self.entry.get()
      if choice not in self.check:
         return
      #self.parse_weather(links[choice])



class Weather:
   def __init__(self,link):
      self.link = link

      r = requests.get(self.link).text
      self.soup = BeautifulSoup(r, "html.parser")

   def get_cities(self):
      data = self.soup.find_all('a')
      print(data)

      links = {}
      for block in data:
         text = block.__str__()
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



w = Weather("https://rp5.ru/Погода_в_России")
w.get_cities()
#window = Window("https://rp5.ru/Погода_в_России")
#window.root.mainloop()
