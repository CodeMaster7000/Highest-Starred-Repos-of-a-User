import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import http.cookiejar
import requests
from lxml import html
from lxml import etree
from bs4 import BeautifulSoup
import re
import operator

top_limit = 10
def openWebsite():
	username = str(input("Enter GitHub username: "))

	repo_dict = {}

	url = "https://github.com/"+username+"?tab=repositories"
  
	while True:
		cj = http.cookiejar.CookieJar()
		opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
		resp = opener.open(url)
		doc = html.fromstring(resp.read())
		repo_name = doc.xpath('//li[@class="col-12 d-block width-full py-4 border-bottom public source"]/div[@class="d-inline-block mb-1"]/h3/a/text()')
		repo_list = []
    
		for name in repo_name:
			name = ' '.join(''.join(name).split())
			repo_list.append(name)
			repo_dict[name] = 0
		response = requests.get(url)
		soup = BeautifulSoup(response.text, 'html.parser')
		soup = BeautifulSoup(response.text, 'html.parser')
		div = soup.find_all('li', {'class': 'col-12 d-block width-full py-4 border-bottom public source'})

		for d in div:
			temp = d.find_all('div',{'class':'f6 text-gray mt-2'})
			for t in temp:
				x = t.find_all('a', attrs={'href': re.compile("^\/[a-zA-Z0-9\-\_\.]+\/[a-zA-Z0-9\.\-\_]+\/stargazers")})
        
				if len(x) is not 0:
					name = x[0].get('href')
					name = name[len(username)+2:-11]
					repo_dict[name] = int(x[0].text)

		div = soup.find('a',{'class':'next_page'})
		if div is not None:
			url = div.get('href')
			url = "https://github.com/"+url
		else:
			break

	i = 0
	sorted_repo = sorted(iter(repo_dict.items()), key = operator.itemgetter(1))

	for val in reversed(sorted_repo):
		repo_url = "https://github.com/" + username + "/" + val[0]
		print("\nrepo name : ",val[0], "\nRepo URL : ",repo_url, "\nStars	 : ",val[1])
		i = i + 1
		if i > top_limit:
			break

if __name__ == "__main__":
	openWebsite()
