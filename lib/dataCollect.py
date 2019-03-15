import json
from requests import Session
from bs4 import BeautifulSoup

### Reverse Engineering API Call ###
session = Session()

session.head('https://www.brewersassociation.org/directories/breweries/')

response = session.post(
    url = 'https://www.brewersassociation.org/wp-admin/admin-ajax.php',
    headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
           'Accept-Encoding': 'gzip, deflate, br',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
           'Referer': 'https://www.brewersassociation.org/directories/breweries/'
           },
    data = {'action': 'get_breweries',
           '_id': 'United States',
           'search_by': 'country'
           }
    )

content = BeautifulSoup(response.text, 'html5lib')
breweryList = content.findAll('li', attrs={'class': 'name'})

breweryData = []

### Gathering critical brewery information ###
for brewery in breweryList:
    name = brewery.getText()
    if name == '':
        pass
    else:
        address = brewery.find_next_sibling('li', attrs={'class': 'address'})
        addressText = address.getText()
        city = address.find_next_sibling('li')
        cityText = city.getText().split(', ')[0]
        state = city.getText().split(', ')[1].split(' ')[0]
        try:
            zipCode = city.getText().split(', ')[1].split(' ')[1].split(' |')[0]
            zipCode = city.getText().split(', ')[1].split(' ')[1].split(' |')[0].split('-')[0]
        except IndexError:
            zipCode = '27403'
        phoneNumber = brewery.find_next_sibling('li', attrs={'class': 'telephone'})
        try:
            phoneNumber.getText().split(': ')[1]
            phoneNumberText = phoneNumber.getText().split(': ')[1]
        except AttributeError:
            phoneNumberText = 'Not Listed'
        try:
            brewery.find_next_sibling('li', attrs={'class': 'brewery_type'}).getText().split(': ')[1]
            breweryType = brewery.find_next_sibling('li', attrs={'class': 'brewery_type'}).getText().split(': ')[1]
        except AttributeError:
            breweryType = 'Not Listed'
        toAppend = {'name': name,
                    'street': addressText,
                    'city': cityText,
                    'state': state,
                    'zip code': zipCode,
                    'phone number': phoneNumberText,
                    'brewery size': breweryType
                    }
        breweryData.append(toAppend)

### Writing to JSON ###
with open('breweryData.json', 'w') as outfile:
    json.dump(breweryData, outfile)



