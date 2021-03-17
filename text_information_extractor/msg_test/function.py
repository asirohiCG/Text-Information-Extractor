# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 18:13:16 2020

@author: pkansal
"""

import re
import requests
import html

class TicketProcessor:
    
    def __init__(self, iie_url, tie_url):
        self.invoice_information_extractor_url = iie_url
        self.text_information_extractor_url = tie_url

    def post_processing_number(self, txt, lang):
        if txt == None:
            txt = ""
        if lang == "eng":
            return re.sub('[^0-9a-zA-Z]+', '', ''.join(txt.strip().split())).upper().replace("O", "0")
        elif lang == "fra":
            # The line below is for French Packaging
            return re.sub('[^0-9a-zA-Z]+', '', ''.join(txt.strip().split())).upper()
            # The line below is for French Papers, but we need to find a way to distinguish between these documents
            # return ''.join(text.strip().split()).upper().replace('_', '')
        elif lang == "spa":
            return re.sub('[^0-9a-zA-Z_]+', '', ''.join(txt.strip().split())).upper().replace("O", "0")
        elif lang == "ita":
            return ''.join(txt.strip().split()).upper()
        else:
            return re.sub('[^0-9a-zA-Z]+', '', ''.join(txt.strip().split())).upper().replace("O", "0")

    def IIE(self, pdf_binary):
        
        ticket_number = 'TEST'

        inv_extractor_query_body = []
        output = []
        inv_extractor_query_body.append({
            'ticket': ticket_number,
            'pdf_binary': pdf_binary.decode('latin')
        })

        if len(inv_extractor_query_body) > 0:
            url_call = "{}/ocr/extract".format(self.invoice_information_extractor_url)
            response = requests.post(url_call, json=inv_extractor_query_body, verify=False)
            response_data = response.json()
            if len(response_data) == 0:
                response_data = [
                    {'date': None, 'date_score': 'Unavailable', 'number': '', 'number_score': 'Unavailable',
                     'found_page': 0, 'language': ''}]

            for index, attachment_invoices in enumerate(response_data):
                for invoice in attachment_invoices:
                    if invoice["number"]:
                        invoice['number'] = self.post_processing_number(invoice['number'], invoice["language"])
                    output.append(invoice)
        return(output)


    def TIE(self, title, description):

        ticket_number = 'TEST'
        output = []

        description = re.sub(r"(?=<!--)([\s\S]*?)-->", " ", description)
        description = re.sub(r"<\/?(p|div|span|b|strong|br)\s?\/?>", " ", description)
        description = re.sub(r"<[^>]*>|\xa0", " ", description)
        description = re.sub(r"\s\s+", " ", description)
        description = html.unescape(description)

        text_extractor_query_body = {
            'ticket': ticket_number,
            'title': title,
            'description': description
        }
        url_call = "{}/text/extract".format(self.text_information_extractor_url)
        response = requests.post(url_call, json=text_extractor_query_body, verify=False)
        response_data = response.json()
        if len(response_data) == 0:
            response_data = [
                {'date': None, 'date_score': 'Unavailable', 'number': '', 'number_score': 'Unavailable', 'language': ''}]
        for item in response_data:
            if item["number"]:
                item['number'] = self.post_processing_number(item['number'], item['language'])
            output.append(item)
            
        return(output)
