import requests
from bs4 import BeautifulSoup


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

      return links

w = Weather("https://rp5.ru/Погода_в_России")
w.get_cities()
