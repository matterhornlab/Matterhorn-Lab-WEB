from .wrapper import Session, CompanyManager, Company, Entry, EntryManager

class MatterhornLabAPI:
    def __init__(self, base_url=None):
        s = None

        if base_url is not None:
            s = Session(base_url)
        else:
            s = Session()

        self.companies = CompanyManager(s)
        self.entries = EntryManager(s)
