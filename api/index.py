from http.server import BaseHTTPRequestHandler
import requests
from bs4 import BeautifulSoup
import json

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Scrape website for currency data and serve as JSON
        url = "https://www.bct.gov.tn/bct/siteprod/liste_cours_m.jsp"
        response = requests.get(url)

        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            currency_data = {}

            rows = soup.find_all('tr', height='20px')

            for row in rows:
                columns = row.find_all('td')
                if len(columns) == 5:
                    unit_str = columns[3].find('center').get_text(strip=True).replace(',', '.')
                    value_str = columns[4].find('center').get_text(strip=True).replace(',', '.')

                    currency_code = columns[2].find('center').get_text(strip=True)
                    unit = float(unit_str)
                    value = float(value_str)

                    currency_data[currency_code] = {
                        "Devise": columns[1].get_text(strip=True),
                        "Valeur": value / unit
                    }

            json_data = json.dumps(currency_data, indent=2)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json_data.encode('utf-8'))
        else:
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f"Failed to retrieve data from {url}. Status code: {response.status_code}".encode('utf-8'))

