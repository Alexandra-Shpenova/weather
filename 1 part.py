import requests
from bs4 import BeautifulSoup


class Weather:
   def __init__(self):
      self.link = f"https://rp5.ru/Погода_в_России"

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
         links[name] = "https://rp5.ru" + text
         print(block)

      print(links)

      return links

w = Weather()
w.get_cities()
