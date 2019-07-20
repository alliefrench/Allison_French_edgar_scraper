import requests
from bs4 import BeautifulSoup
import csv


def get_fund_holdings(cik):

    req_url = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=%s&type=13F-HR&dateb=&owner=exclude&count=80' % (
        cik)
    r = requests.get(req_url)
    soup = BeautifulSoup(r.text, "xml")
    # header = soup.find(class_='tableFile2').find_all(
    #     'tr', parent='table', recursive='False')
    test = soup.table.tr.get_text()

    test_list = test.split('\n')
    clean_list = []
    for el in test_list:
        if len(el) > 0:
            clean_list.append(el)

    print(clean_list)

    with open("/Users/allisonfrench/Python/Plaid/fund_holdings.tsv", 'w') as tsv_doc:
        tsv_writer = csv.writer(tsv_doc, delimiter='\t')

        # for row in table:
        #     header_row = []
        #     cells = row.find_all('th')
        #     for cell in cells:
        #         header_row.append(cell.text)
        #     tsv_writer.writerow(header_row)

        # for row in table[1]:
        #     data_row = []
        #     cells = row.find_all('tr')
        #     for cell in cells:
        #         data_row.append(cell.text)
        #     tsv_writer.writerow(data_row)


def main():
    fund_holdings = get_fund_holdings('0001166559')
    print(fund_holdings)


if __name__ == "__main__":
    main()
