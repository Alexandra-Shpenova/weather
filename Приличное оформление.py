import requests
from bs4 import BeautifulSoup
from tkinter import *
from PIL import Image, ImageTk


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

class Window:
   def __init__(self, links):
      self.root = Tk()
      self.root.geometry("800x600")
      self.root.title("Прогноз погоды")
      self.root['bg']='#8ad4ff'
      self.check = []

      #Настройки текста
      self.label = Label(self.root, wraplength=200, bg = '#c9e9ff',fg='#142129', font=("Trebuchet MS", 11),pady=2)
      self.label.place(x = 0,y = 55, width = 265,height=745)

      self.label2 = Label(self.root, wraplength=200, bg='#c9e9ff',fg='#142129', font=("Trebuchet MS", 11),pady=2)
      self.label2.place(x = 267,y = 55, width = 265,height=745)

      self.label3 = Label(self.root, wraplength=200, bg='#c9e9ff',fg='#142129', font=("Trebuchet MS", 11),pady=2)
      self.label3.place(x=534, y=55, width=265, height=745)

      self.set_text(links)

      #Поле ввода
      self.entry = Entry(self.root, width=50)
      self.entry.place(x = 5,y = 12,width=600, height=30)

      #Создание кнопки
      self.btn = Button(self.root, text="Поиск",font=("Trebuchet MS", 20),
                        bg = '#215b77', command=lambda x=links: self.check_input(links))
      self.btn.place(x = 550,y = 5,width=255, height=45)


   '''Создадим функцию установки текста на экране. 
   Она будет трансформировать словарь links в строку.'''
   def set_text(self, links):
      text1 = ""
      text2 = ''
      text3 = ''
      n = 0

      for city in links:
         if n < 64:
             self.check.append(city)
             text1 += city + ', '
             n += 1
             print(n)
         elif 64 <= n <= 128:
             self.check.append(city)
             text2 += city + ', '
             n += 1
             print(n)
         else:
             self.check.append(city)
             text3 += city + ', '
             n += 1
             print(n)

      text1 = text1[:-2]
      text2 = text2[:-2]
      text3 = text3[:-2]
      self.label2.configure(text=text1)
      self.label.configure(text=text2)
      self.label3.configure(text=text3)


   '''Добавим функцию проверки 
   введённых пользователем значений.'''

   def check_input(self, links):
      choice = self.entry.get()
      if choice not in self.check:
         return
      self.parse_weather(links[choice])
      #self.parse_weather(links[choice])

   def parse_weather(self, link):
      w = Weather(link)
      data = w.soup.find('div', {'id': 'archiveString'})
      temp = data.find('span', {'class': 't_0'}).text
      text = data.find('a', {'class': 'ArchiveStrLink'})
      if text is None:
         text = data.find('div', {'class': 'ArchiveInfo'})
      text = text.text.replace("Архив погоды на метеостанции", "")
      self.label2.configure(text=temp + "\n" + text, fg = '#142129')
      self.label2.place( x = 200,y = 150, width = 400, height=350)
      self.label.destroy()
      self.label3.destroy()

      #img = ImageTk.PhotoImage(Image.open("snow_.png"))
      #b = Label(image=img)

      #b.pack()

w = Weather("https://rp5.ru/Погода_в_России")
w.get_cities()
#window = Window("https://rp5.ru/Погода_в_России")
#window.root.mainloop()
