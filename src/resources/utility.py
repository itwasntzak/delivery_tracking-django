

class To_Datetime:
    def __init__(self, string):
        self.string = string

    def from_date(self):
        import datetime
        return datetime.datetime.strptime(self.string, '%Y-%m-%d')

    def from_datetime(self):
        import datetime
        import re

        if not re.search(r'[\d]+:+[\d]+:+[\d]+.+[\d]', self.string):
            return datetime.datetime.strptime(self.string, '%Y-%m-%d %H:%M:%S')

        return datetime.datetime.strptime(self.string, '%Y-%m-%d %H:%M:%S.%f')

    def from_time(self):
        import datetime
        import re

        if not re.search(r'[\d]+:+[\d]+:+[\d]+.+[\d]', self.string):
            return datetime.datetime.strptime(self.string, '%H:%M:%S')

        return datetime.datetime.strptime(self.string, '%H:%M:%S.%f')
