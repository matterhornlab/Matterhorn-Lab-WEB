import requests

BASE_URL = "http://matterhorn-lab.herokuapp.com"

class Session:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url

    def post(self, endpoint, **kwargs):
        url = self.base_url + "/" + endpoint + "/"

        payload = {}
        for k,v in kwargs.items():
            payload[k] = v

        req = requests.post(url, json=payload, timeout=30)

        return req.json(), req.status_code

    def get(self, endpoint):
        url = self.base_url + "/" + endpoint + "/"

        req = requests.get(url)

        return req.json(), req.status_code

class Company:
    def __init__(self, name, ticker, url=None):
        self.name = name
        self.ticker = ticker
        self.url = url

    def set_url(self, url):
        self.url = url

    def __str__(self):
        return "{}({})".format(self.name, self.ticker)

class CompanyManager:
    def __init__(self, session):
        self.session = session
        self.endpoint = "company"

    def add(self, company):
        json, code = self.session.post(self.endpoint, name=company.name, ticker=company.ticker)
        company.set_url(json['url'])

        return company

    def get(self, id):
        url = "{}/{}".format(self.endpoint, id)
        json, code = self.session.get(url)

        c = Company(name=json['name'], ticker=json['ticker'], url=json['url'])
        return c

    def get_tickers(self, id):
        url = "{}/{}".format(self.endpoint, id)
        json, code = self.session.get(url)

        ticker=json['ticker']
        return ticker
    
    def list(self):
        url = "{}".format(self.endpoint)

        json, code = self.session.get(url)

        companies = []
        for entry in json:
            c = Company(name=entry['name'], ticker=entry['ticker'], url=entry['url'])
            companies.append(c)

        return companies

class Entry:
    def __init__(self, company, timestamp, price, url=None):
        self.company = company
        self.timestamp = timestamp
        self.price = price
        self.url = url

    def set_url(self, url):
        self.url = url

    def __str__(self):
        return "{}@{}".format(self.company, self.timestamp)

class EntryManager:
    def __init__(self, session):
        self.session = session
        self.endpoint = "entry"

    def add(self, entry):
        json, code = self.session.post(self.endpoint, company=str(entry.company.url), timestamp=entry.timestamp, price=entry.price)
        return entry

    def get(self, id):
        url = "{}/{}".format(self.endpoint, id)
        json, code = self.session.get(url)

        # Get company id
        company_id = json["company"]
        company_id = str(company_id).replace(self.session.base_url, "")
        company_id = str(company_id).replace("/", "")
        company_id = str(company_id).replace("company", "")

        #e = Entry(name=json['name'], ticker=json['ticker'], url=json['url'])
        #return e
