import csv, requests

URL = 'https://raw.githubusercontent.com/projectbenyehuda/public_domain_dump/master/pseudocatalogue.csv'

with requests.Session() as s:
    download = s.get(URL)

    decoded_content = download.content.decode('utf-8')

    legend = list(csv.reader(decoded_content.splitlines(), delimiter=','))[1:]

#    for i in range(10):
#        print(legend[i])
