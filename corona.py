import requests
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

# Requisição da web
url = 'https://www.worldometers.info/coronavirus/'
requisicao = requests.get(url)

# parsing da requisição
data = requisicao.text
soup = BeautifulSoup(data,'html.parser')

print(soup.title.text)
print()
# Pegando a informação da div que queremos
live_data = soup.find_all('div',id='maincounter-wrap')
for i in live_data:
    print(i.text)

print()
print('Análise dos países individualmente')
print()

# Extraindo informações
table_body = soup.find('tbody')
table_rows = table_body.find_all('tr')

countries = []
cases = []
todays = []
deaths = []

for tr in table_rows:
    td = tr.find_all('td')
    countries.append(td[0].text)
    cases.append(td[1].text)
    todays.append(td[2].text.strip())
    deaths.append(td[3].text.strip())

indices = [i for i in range(1,len(countries)+1)]
headers = ['Countries','Total Cases','Todays Cases','Total Deaths']
df = pd.DataFrame(list(zip(countries,cases,todays,deaths)),index=indices,columns=headers)

print(df)

# Salvando em arquivo csv
df.to_csv('corona-virus-cases.csv')

# plotting a graph
y_pos = list(range(len(countries)))

plt.bar(y_pos,cases[::-1],align='center',alpha=0.5)
plt.xticks(y_pos,countries[::-1],rotation=70)
plt.ylabel('Total cases')
plt.title('Persons affected by Corona virus')
plt.savefig('Corona-analysis.png',dpi=600)
plt.show()
