from flask import request, jsonify
from description import DescriptionFactory
from tie_logger import tie_logger
import sys
import pandas as pd
df=pd.read_excel(r"C:\Users\asirohi\Documents\COE\Classification Component\Invoice_Subject_Body.xlsx")
df.head()
for index,row in df.iterrows():
    print(row['Subject'],row['Body'])
    #head = sys.argv[1]
    #body = sys.argv[2]
    head = row['Subject']
    body = row['Body']

    def text_extract(head, body):
    #   tie_logger.info('Request received. Request body: {}'.format(request.json))
        desc_factory = DescriptionFactory()
    #    return jsonify(desc_factory.entity_extraction(request.json['title'], request.json['description'])) #
        return desc_factory.entity_extraction(head, body)

    text_extract(head, body)