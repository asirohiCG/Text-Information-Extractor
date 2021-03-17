import re
from dateutils import DateUtils


class IPAYProcessor:
    def __init__(self, desc_header=r"question about invoice\s?:"):
        self.header = desc_header
        self.found_success = False

    def check_ipay_template(self, title):
        return re.search(self.header, title) is not None

    def extract_entities(self, text):
        date_utils = DateUtils("%m/%d/%Y", "MDY")
        inv_no_regex = r"invoice number:?\s+(.*)\s+invoice date"
        inv_date_regex = r"invoice date:?\s+(.*)\s+invoice amount"
        inv_no = re.search(inv_no_regex, text)
        inv_date = re.search(inv_date_regex, text)
        if inv_no is not None:
            inv_no = inv_no.group(1).strip()
            inv_no = inv_no.split()[0]
        if inv_date is not None:
            inv_date = inv_date.group(1).strip()
        invoice = {
            "number": inv_no if inv_no != "" else None,
            "number_score": 100 if inv_no != "" else 0,
            "date": date_utils.convert_to_vrt_format(date_utils.parse(inv_date)) if inv_date != "" else None,
            "date_score": 100 if inv_date is not None else 0
        }
        self.found_success = invoice['number'] is not None
        return [invoice]
