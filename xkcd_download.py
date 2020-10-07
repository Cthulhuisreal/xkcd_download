#! python3
import requests
import os
import bs4
import shutil

# Стартовый url
url = 'https://xkcd.com/2338'
os.makedirs('xkcd', exist_ok=True)
# url последнего комикса заканчивается на #
while not url.endswith('#'):
    print('Downloading page %s...' % url)
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    # Находим url картинки с комиксом
    comicElem = soup.select('#comic img')
    if comicElem == []:
        print('Could not find comic image.')
    else:
        comicUrl = 'https:' + comicElem[0].get('src')
        # Загружаем картинку
        print('Downloading image %s...' % comicUrl)
        res = requests.get(comicUrl)
        res.raise_for_status()
        # Сохраняем картинку
        pathtofile = os.path.join('xkcd', os.path.basename(comicUrl))
        if os.path.exists(pathtofile):
            print(pathtofile + ' already exist, pass')
            nextLink = soup.select('a[rel="next"]')[0]
            url = 'https://xkcd.com' + nextLink.get('href')
            continue
        else:
            imageFile = open(os.path.join('xkcd', os.path.basename(comicUrl)),'wb')
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()
            shutil.copy(os.path.join('xkcd', os.path.basename(comicUrl)), r'C:\Users\ramse\Desktop')
    # Находим кнопку "Дальше" на странице с комиксом
    nextLink = soup.select('a[rel="next"]')[0]
    url = 'https://xkcd.com' + nextLink.get('href')
print('Done.')
