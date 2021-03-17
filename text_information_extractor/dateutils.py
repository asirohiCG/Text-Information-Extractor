import dateparser
import datetime


class DateUtils:
    def __init__(self, date_format, date_order):
        self.date_format = date_format
        self.date_order = date_order

    def parse(self, date):
        if date is None:
            return None
        if len(date) - sum(c.isdigit() for c in date) < 2:
            return None
        parsed = dateparser.parse(date, settings={'STRICT_PARSING': True, 'DATE_ORDER': self.date_order})
        if parsed is not None and datetime.datetime.now().year + 2 > parsed.year > datetime.datetime.now().year - 2:
            return parsed
        else:
            return None

    def convert_to_vrt_format(self, date_obj):
        if date_obj is not None:
            return date_obj.strftime(self.date_format)
        else:
            return None

    def extract_year(self, date_obj):
        if date_obj is not None:
            return date_obj.strftime("%Y")
        else:
            return None
