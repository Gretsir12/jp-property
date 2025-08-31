import requests
from bs4 import BeautifulSoup

class Convertor:
    """
    A currency converter for JPY to RUB or RUB to JPY using live exchange rates from Google Finance.

    Attributes:
        url (str): The URL to fetch the JPY-RUB exchange rate.
        rate (float): The current JPY to RUB exchange rate.
    """

    def __init__(self):
        """
        Initializes the Convertor by fetching the current JPY to RUB exchange rate.
        """
        self.url = "https://www.google.com/finance/quote/JPY-RUB"
        self.rate = self.get_jpy_rub_rate()

    def get_jpy_rub_rate(self):
        """
        Fetches the current JPY to RUB exchange rate from Google Finance.

        Returns:
            float: The current exchange rate.
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0'
        }
        response = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(response.content, features="html.parser")
        convert = soup.find_all('div', {'class': "YMlKec fxKbKc"})
        if convert:
            return float(convert[0].text.replace(',', ''))
        raise ValueError("Exchange rate not found on the page.")

    def convert_jpy(self, jpy):
        """
        Converts Japanese Yen (JPY) to Russian Ruble (RUB).

        Args:
            jpy (float): Amount in JPY.

        Returns:
            float: Equivalent amount in RUB.
        """
        return jpy * self.rate

    def convert_rub(self, rub):
        """
        Converts Russian Ruble (RUB) to Japanese Yen (JPY).

        Args:
            rub (float): Amount in RUB.

        Returns:
            float: Equivalent amount in JPY.
        """
        return rub / self.rate