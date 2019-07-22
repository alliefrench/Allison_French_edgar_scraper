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

    # Isolate 13F report links
    links = soup.find(class_='tableFile2').find_all(
        id='documentsbutton', recursive='False')

    # Make a request for the first (most recent) report link
    # A build out would be to offer a second argument where the user could
    # Request a number representing a previous report
    s = requests.get('https://www.sec.gov' + links[0]['href'])
    s_soup = BeautifulSoup(s.text, "xml")

    # Isolate the xml information table link
    xml_link = s_soup.select('a[href*=xslForm13F]')[1]['href']

    # Request the xml information table data
    t = requests.get('https://www.sec.gov' + xml_link)
    t_soup = BeautifulSoup(t.text, "xml")

    # Isolate first row of the table
    first_row = t_soup.body.tbody.tr

    # Generate report
    write_doc(first_row)


def write_doc(soup_obj):

    # Create the tsv file in our program directory
    with open("fund_holdings.tsv", 'w') as tsv_doc:
        tsv_writer = csv.writer(tsv_doc, delimiter='\t')

        # Grab header row of table
        row = soup_obj.find_next_sibling()

        # While there are further rows, we grab the td elements and put
        # the inner text into a new list. The list representing the row text
        # is then written to the .tsv
        while row:
            inner_text = []
            row_cells = row.find_all('td')
            for cell in row_cells:
                inner_text.append(cell.text)
            tsv_writer.writerow(inner_text)
            row = row.find_next_sibling()


# sys.argv allows us to run the CIK argument in the command line
def main(argv):
    get_fund_holdings(argv)


if __name__ == "__main__":
    main(*sys.argv[1:])
