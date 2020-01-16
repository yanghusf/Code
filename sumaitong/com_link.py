import requests
from bs4 import BeautifulSoup


heards = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"}
respones = requests.get("https://www.aliexpress.com/w/wholesale-wall-sticker.html?seoChannel=wholesale&ltype=wholesale&d=y&CatId=0&SearchText=wall+sticker&trafficChannel=seo&SortType=create_desc&minPrice=1&page=1&groupsort=1&switch_new_app=y", headers=heards)


print(respones.cookies)
# with open("page-html.txt",'w', encoding='utf-8') as f:
#
#     f.write(respones.text)
#
# soup = BeautifulSoup(open('page-html.txt',encoding='utf-8'), 'lxml')
# print(soup.a)
# print(soup.find_all("a", class_='item-title'))