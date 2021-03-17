from app import app
import sys

sys.path.append("..")
from tie_functions import text_extract

@app.route('/text/extract', methods=['POST'])
def extract():
    return text_extract()
