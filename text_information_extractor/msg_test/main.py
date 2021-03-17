# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 13:58:55 2020

@author: pkansal
"""

import win32com.client
import os
import pytesseract
import argparse
from dotenv import load_dotenv

from function import TicketProcessor

# Invoice Information Extractor
def IIE(port, pdf_bin):
    invoice_information_extractor_url = "http://localhost:{}".format(port)
    text_information_extractor_url = "http://localhost"
    tp = TicketProcessor(invoice_information_extractor_url, text_information_extractor_url)
    return(tp.IIE(pdf_binary=pdf_bin))

# Text Information Extractor
def TIE(port, mail_subject, mail_body):
    invoice_information_extractor_url = "http://localhost"
    text_information_extractor_url = "http://localhost:{}".format(port)
    tp = TicketProcessor(invoice_information_extractor_url, text_information_extractor_url)
    return(tp.TIE(title=mail_subject, description=mail_body))

def msg_extract(msg_file_path):
    msg = outlook.OpenSharedItem(msg_file_path)
    out = {}
    out['SenderName'] = msg.SenderName
    out['SenderEmail'] = msg.SenderEmailAddress
    out['Time'] = msg.SentOn
    out['To'] = msg.To
    out['Cc'] = msg.CC
    out['BCc'] = msg.BCC
    out['Subject'] = msg.Subject
    out['Body'] = msg.Body
    out['Attachments'] = {}
    count_attachments = msg.Attachments.Count
    if count_attachments > 0:
        for item in range(count_attachments):
            out['Attachments'][msg.Attachments.Item(item + 1).Filename.lower()] = msg.Attachments.Item(item + 1)
    return(out)

if __name__ == "__main__":

    lang = 'eng'
    FILE_TYPES = ['pdf','png','jpg']
    
    dotenv_path = os.path.join('.', '.env')
    load_dotenv(dotenv_path)
    iie_port = os.getenv('IIE_PORT')
    tie_port = os.getenv('TIE_PORT')
    temp_path = os.getenv('TEMP_PATH')

    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--msg', type=str)
    args = parser.parse_known_args()

    iie_res = []
    tie_res = []
    
    if not args[0].msg is None:
        outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        out = msg_extract(args[0].msg)
        if out['Body'] or out['Subject'] or out['Attachments']:
            if out['Attachments']:
                print("Running Invoice Information Extractor")
                for i in out['Attachments']:
                    if i.split('.')[-1] in FILE_TYPES:
                        out['Attachments'][i].SaveAsFile(os.path.join(temp_path,i))
                        if os.path.join(temp_path,i).endswith('pdf'):
                            try:    
                                with open(os.path.join(temp_path,i), "rb") as f:
                                    pdf_binary = f.read()
                            except:
                                print("\tPDF File could not be read properly")
                        else:
                            pdf_binary = pytesseract.image_to_pdf_or_hocr(os.path.join(temp_path,i), extension='pdf')
                        print("\tProcessing Attachment: {}".format(i))
                        iie_res.append(IIE(iie_port, pdf_binary))
                    else:
                        print("\tAttachment of unsupported file type - {}".format(i))
            if out['Body'] or out['Subject']:
                print("Running Text Information Extractor")
                tie_res = TIE(tie_port, out['Subject'], out['Body'])
            
            print("\nIIE Results: {}\n\nTIE Results: {}".format(iie_res, tie_res))
        else:
            print("Empty mail")
    else:
        print('Error - required: msg_path')
