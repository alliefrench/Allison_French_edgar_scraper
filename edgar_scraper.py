import requests
from bs4 import BeautifulSoup
import csv
import sys


def get_fund_holdings(cik):

    # Make a request with desired CIK number, returning all 13F reports
    req_url = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=%s&type=13F-HR&dateb=&owner=exclude&count=80' % (
        cik)
    r = requests.get(req_url)
    soup = BeautifulSoup(r.text, "xml")

    # Isolate report links
    links = soup.find(class_='tableFile2').find_all(
        id='documentsbutton', recursive='False')

    # Make a request for the first (most recent) report link
    s = requests.get('https://www.sec.gov' + links[0]['href'])
    s_soup = BeautifulSoup(s.text, "xml")

    # Isolate the xml information table link
    xml_link = s_soup.select('a[href*=xslForm13F]')[1]['href']

    # Request the xml information table data
    t = requests.get('https://www.sec.gov' + xml_link)
    t_soup = BeautifulSoup(t.text, "xml")

    first_row = t_soup.body.tbody.tr
    write_doc(first_row)


def write_doc(soup_obj):
    with open("fund_holdings.tsv", 'w') as tsv_doc:
        tsv_writer = csv.writer(tsv_doc, delimiter='\t')
        row = soup_obj.find_next_sibling()
        while row:
            inner_text = []
            row_cells = row.find_all('td')
            for cell in row_cells:
                inner_text.append(cell.text)
            tsv_writer.writerow(inner_text)
            row = row.find_next_sibling()


def main(argv):
    get_fund_holdings(argv)


if __name__ == "__main__":
    main(*sys.argv[1:])
