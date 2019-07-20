import requests
from bs4 import BeautifulSoup
import csv


def get_fund_holdings(cik):

    req_url = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=%s&type=13F-HR&dateb=&owner=exclude&count=1000' % (
        cik)
    r = requests.get(req_url)
    soup = BeautifulSoup(r.content, "html.parser")
    table = soup.find('table', class_='tableFile2')
    for line in table:
        if line is:
            print(line)

    with open("/Users/allisonfrench/Python/Plaid/fund_holdings.tsv", 'w') as tsv_doc:
        tsv_writer = csv.writer(tsv_doc, delimiter='\t')
        tsv_writer.writerow(['test', 'Allison'])

    holdings = {}

    return holdings


def main():
    fund_holdings = get_fund_holdings('0001166559')
    print(fund_holdings)


if __name__ == "__main__":
    main()
