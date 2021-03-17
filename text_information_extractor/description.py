import re
import os
import spacy
from ipay import IPAYProcessor
import ner_utils
from dotenv import load_dotenv
from tie_logger import tie_logger
from ner_utils import strip_tags
import traceback
from langdetect import detect

dotenv_path = os.path.join('.', '.env')
print("Dot env----------",dotenv_path)
load_dotenv(dotenv_path)

ner_models_path = os.getenv("NER_MODELS_PATH")
print("Ner model Path--------",ner_models_path)

REPLACE_BY_SPACE_RE = re.compile('[/(){}[\\]|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')


class DescriptionFactory:

    def clean_html(self, raw_html):
        raw_html = raw_html.replace("&nbsp;", " ")
        cleanr = re.compile('<([\\w|\\W]*?)>')
        cleantext = re.sub(cleanr, ' ', raw_html)
        cleanr = re.compile('{.*?}')
        cleantext = re.sub(cleanr, ' ', cleantext)
        cleantext = re.sub(chr(160), ' ', cleantext)
        return cleantext

    def language_detector(self, textstring):
        code = detect(textstring)
        if code == 'en':
            language_code = 'eng'
        elif code == 'fr':
            language_code = 'fra'    
        elif code == 'it':
            language_code = 'ita'
        elif code == 'es':
            language_code = 'spa'
        else:
            language_code = 'Language not supported'
        return language_code

    def entity_extraction(self, title, text):
        text = text.lower()
        text = self.clean_html(text)
        title = title.lower()
        language = self.language_detector(text)
        invoices = []
        try:
            ipay_proc = IPAYProcessor()
            if ipay_proc.check_ipay_template(title):
                tie_logger.info('Checked and template matches IPAY template.')
                invoices_apay = ipay_proc.extract_entities(text)
                if ipay_proc.found_success:
                    tie_logger.info('Results from IPAY after post-processing: '+str(invoices_apay))
                    #print("Inside Language supported")
                    return invoices_apay

            if language != 'Language not supported':
                modelname = "spacymodel_{}".format(language)
                #print("-----Model Name : ",modelname,"--------")
                nlp = spacy.load(os.path.join(ner_models_path, modelname))
                doc = nlp(ner_utils.preprocess_input(text))
                ner_results = []
                processed_entities = ner_utils.postprocess_entities(doc.ents)
                tie_logger.info("Results after post-processing: "+str(processed_entities))
                #print("Inside Language supported")
                for result in processed_entities:
                    if result[1] == "INV_NO" and len(result[0].split(" ")) == 1 and len(result[0]) >= 4:
                        ner_result = {
                            "text": result[0],
                            "label": "INV_NUMBER",
                        }
                        ner_results.append(ner_result)
                    elif result[1] == "DATE" and len(result[0]) >= 4:
                        ner_result = {
                            "text": result[0],
                            "label": result[1],
                        }
                        ner_results.append(ner_result)
                    elif result[1] == "PO_NO" and len(result[0]) >= 4:
                        ner_result = {
                            "text": result[0],
                            "label": result[1],
                        }
                        ner_results.append(ner_result)
                for i in range(0, len(ner_results)):
                    if ner_results[i]["label"] == "INV_NUMBER":
                        try:
                            if ner_results[i + 1]["label"] == "DATE":
                                date = ner_results[i + 1]["text"]
                                date_score = "Unavailable"
                            else:
                                date = None
                                date_score = 0
                        except:
                            date = None
                            date_score = 0
                        invoice = {
                            "number": ner_results[i]["text"],
                            "number_score": "Unavailable",
                            "date": date,
                            "date_score": date_score,
                            "language": language
                        }
                        if invoice not in invoices:
                            invoices.append(invoice)
        except Exception as e:
            tie_logger.error('Error in TIE module. Empty invoices set will be returned.')
            tie_logger.error(traceback.format_exc())
        return invoices
