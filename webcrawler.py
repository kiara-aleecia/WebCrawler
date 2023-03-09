import sys
import pathlib
from bs4 import BeautifulSoup
import requests
import urllib
from urllib import request

def webcrawler():
    starter_url = "https://www.nature.com/articles/44751"

    r = requests.get(starter_url)

    data = r.text
    soup = BeautifulSoup(data)

    # write urls to a file
    with open('urls.txt', 'w') as f:
        for link in soup.find_all('a'):
            link_str = str(link.get('href'))
            print(link_str)
            if link_str.startswith('/url?q='):
                link_str = link_str[7:]
                print('MOD:', link_str)
            if '&' in link_str:
                i = link_str.find('&')
                link_str = link_str[:i]
            if link_str.startswith('http') and 'google' not in link_str:
                f.write(link_str + '\n')

    # end of function
    f.close()
    print("end of crawler")

def webscraper():
    file = open('urls.txt', 'r')
    urls = file.readlines()
    count = 1
    forbidden = ['harvard', 'copyright', 'subscribe', 'protocolexchange']

    # Creates files of all text from all urls
    for url in urls:
        for f in forbidden:
            if f in url:
                is_forbidden = True
                break
            else:
                is_forbidden = False

        if count > 3 and not is_forbidden:
            print(url)
            html = request.urlopen(url).read().decode('utf8')
            soup = BeautifulSoup(html)

            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()  # rip it out

            # extract text, writes text to new file
            text = soup.get_text()
            newfile = open('url' + str(count) + '.txt', 'w', encoding="utf-8")
            newfile.writelines(text[:])
            newfile.close()
        count += 1

    return count - 1

def cleanup(fileamnt):
    for i in range(fileamnt):
        print()

def main():
    webcrawler()
    webscraper()

# Starts program
if __name__ == '__main__':
    main()