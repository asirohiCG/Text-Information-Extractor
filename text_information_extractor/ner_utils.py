import re
from html.parser import HTMLParser
from dateutils import DateUtils


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def remove_cdata_tags(input_html):
    return re.sub(r'<!--.*-->', ' ', strip_tags(input_html), flags=re.S)


def remove_css(input_html):
    return re.sub(r"[@.#]?.*{\s+[\w\s\d:;%!\-{}]+}"," ",input_html)


def remove_mulitple_newlines(input_text):
    return re.sub(r"(\r?\n)+","\r\n",input_text)


def clean_html_completely(input_html):
    return remove_mulitple_newlines(remove_css(remove_cdata_tags(strip_tags(input_html))))


def preprocess_input(text):
    input_data = re.sub(r'#([\dsSiI])', r'# \1', text)
    print("----input data-----",input_data)
    return input_data


def postprocess_entities(spacy_entities):
    date_utils = DateUtils('%m/%d/%Y', 'MDY')
    pred_ents_text = [(re.sub(r'[^\d\w.,/\-]', '', ent.text), ent.label_, ent.start_char) for ent in spacy_entities]
    #print("----Pred_ents_text------",pred_ents_text)
    pred_ents_text = [(re.sub(r'(\d+)[^\d]+', r'\1', ent[0]), ent[1], ent[2]) if ent[1] == "PO_NO" else ent for ent in
                      pred_ents_text]
    #print("----Pred_ents_text------",pred_ents_text)

    pred_ents_text = [e for e in pred_ents_text if len(e[0]) > 1]
    #print("----Pred_ents_text------",pred_ents_text)
    pred_ents_text = list(set(pred_ents_text))
    #print("----Pred_ents_text------",pred_ents_text)
    pred_ents_text.sort(key=lambda tup: tup[2])
    #print("----Pred_ents_text------",pred_ents_text.sort(key=lambda tup: tup[2]))
    pred_ents_text = [(date_utils.convert_to_vrt_format(date_utils.parse(ent[0])), ent[1], ent[2]) if ent[1] == "DATE" else ent for ent in pred_ents_text]
    #print("----Pred_ents_text------",pred_ents_text)
    pred_ents_text = [ent for ent in pred_ents_text if ent[0] is not None]
    #print("----Pred_ents_text------",pred_ents_text)
    return pred_ents_text
