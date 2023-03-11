# Homework 5
# Crystal Ngo and Kiara Madeam
# https://github.com/cmn180003/NLP-Portfolio
# https://github.com/kiara-aleecia/nlp-portfolio

import sys
import pathlib
from bs4 import BeautifulSoup
import requests
import urllib
from urllib import request
import os
import re
from nltk import word_tokenize
from nltk import sent_tokenize
import math
from nltk import word_tokenize
from nltk.corpus import stopwords

'''
TO DO:
[X]- start with url representing a topic
[X]- output a list of at least 15 relevant urls
[X]- write function to loop through urls and scrape all text off each page
[X]- store each page's text in its own file
- write function to clean up text from each file
    - delete newlines and tabs
    - extract sentences with nltk sentence tokenizer
    - write sentences for each file to a new file (15 in, 15 out)
- write a function to extract at least 25 important terms
    - use term frequency or tf-idf
    - first lowercase everything, remove stopwords, remove punctuation
    - print top 25-40 terms
- manually determine the top 10 terms based on your domain knowledge
- build searchable knowledge base of facts related to the 10 terms for a chatbot
    - can be as simple as a pickled python dictionary
- complete write up
- link to portfolio on github
'''

def webcrawler():
    #starter_url = "https://www.nature.com/articles/44751"
    starter_url = 'https://link.springer.com/article/10.1007/s00359-015-1063-y'

    r = requests.get(starter_url)

    data = r.text
    soup = BeautifulSoup(data, features='html.parser')

    # write urls to a file
    with open('urls.txt', 'w') as f:
        f.write(starter_url + '\n')
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
    #forbidden = ['harvard', 'copyright', 'subscribe', 'protocolexchange', 'authorize', 'product',
    #             'partnerships']

    # ignore links that we cannot access
    ignore = ['login', 'Frspb', 'PMC1635474', '2F10236249509378941', 'Frstb', '2F156854068X00313', 'Fjeb',
                 'Fzootaxa.3722.1.2', '2F26.2.389', '2F156854005776759843', 'MediaObjects', 'licenses', 'copyright', '=Retrieve']
    
    # Creates files of all text from all urls
    for url in urls:
        for i in ignore:
            if i in url:
                is_ignored = True
                break
            else:
                is_ignored = False

        if not is_ignored:
            print(url)
            html = request.urlopen(url).read().decode('utf8')
            soup = BeautifulSoup(html, features='html.parser')

            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()  # rip it out

            # extract text, writes text to new file
            text = soup.get_text()
            newfile = open('url/url' + str(count) + '.txt', 'w', encoding="utf-8")
            newfile.writelines(text[:])
            newfile.close()
        count += 1

    return count - 1

def cleanup(fileamnt):
    substantial_urls = [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 18, 23, 24, 28, 32, 38, 42, 46]
    #remove files we don't need
    for i in range(fileamnt):
        curr_file = 'url/url' + i + '.txt'
        if i not in substantial_urls and os.path.exists(curr_file):
            os.remove(curr_file)
            fileamnt -= 1
        else:
            continue

    for i in range(fileamnt):
        filepath = 'url/url' + i + '.txt'
        file = open(filepath, 'r').read()
        text = re.sub(r'[.?!,:;()\-\n\d]', ' ', file.lower())
        print(text)
        #tokens = nltk.word_tokenize(text)

    print('done removing unnecessary files!!')

    for url in substantial_urls:
        filepath = 'url' + str(url) + '.txt'
        #file = open(filepath, 'w+', encoding='utf8')
        #cur_path = os.path.dirname(__file__)
        #new_path = cur_path + '\\url\\' + filepath
        #with open(new_path,'w+') as f:
            #text = re.sub(r'[.?!,:;()\-\n\d]', ' ', file.lower())
            #text = re.sub(r'[\s\s+]', ' ', file)
        f = open(filepath, 'r+', encoding='utf8').read()
        #text = f.read()
        text = " ".join(f.split())
        #print(text)
        filepath = 'url/clean' + str(url) + '.txt'

        #tokens = nltk.word_tokenize(text)
        sentences = sent_tokenize(text)
        f = open(filepath, 'w', encoding="utf-8")
        f.writelines(text[:])
        f.close()


'''
- write a function to extract at least 25 important terms
    - use term frequency or tf-idf
    - first lowercase everything, remove stopwords, remove punctuation
    - print top 25-40 terms
'''
def important_terms(substantial_urls):
    tf_dict = {}
    idf_dict = {}
    #Gets tf for all files
    for url in substantial_urls:
        #Gets file ready for extraction
        curr_file = ('url/clean' + str(url) + '.txt')
        curr_file = re.sub(r'[.?!,:;()\-\n\d]', ' ', curr_file.lower())
        tokens = word_tokenize(curr_file)

        #Removes stopwords
        stpwrds = set(stopwords.words('english'))
        tokens = [t for t in tokens if not t in stpwrds]

        #Gets term frequencies
        token_set = set(tokens)
        tf_dict = {t: tokens.count(t) for t in token_set}

        #Normalize tf by number of tokens
        for t in tf_dict.keys():
            tf_dict[t] = tf_dict[t] / len(tokens)

    vocab = set(tf_dict.keys())

    #Gets idf
    for term in vocab:
        temp = ['x' for voc in vocab if term in voc]
        idf_dict[term] = math.log((1+len(substantial_urls)) / (1+len(temp)))

    #Get tf-idf for all files
    tf_idf = {}
    for t in tf_dict.keys():
        tf_idf[t] = tf_dict[t] * idf_dict[t]

    #Prints top 25 words
    doc_term_weights = sorted(tf_idf.items(), key=lambda x: x[1], reverse=True)
    print("\nMost important: ", doc_term_weights[:25])


def main():
    #webcrawler()
    filecount = webscraper()
    print(f"filecount is : {filecount}")
    filecount, significant = cleanup(filecount)
    #filecount = 36
    print(f"new filecount is : {filecount}")
    important_terms(significant)

# Starts program
if __name__ == '__main__':
    main()