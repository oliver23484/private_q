import box
import timeit
import yaml
import argparse
from dotenv import find_dotenv, load_dotenv
from src.utils import setup_dbqa
from flask import Flask
from flask import request
from flask_restful import Resource, Api, reqparse
import threading
import queue


app = Flask(__name__)
api = Api(app)
# Load environment variables from .env file
load_dotenv(find_dotenv())

# Import config vars
with open('config/config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))

q = queue.Queue()
dbqa = setup_dbqa()
processing = False
def target_method():
    global processing
    while not processing:

        print("Inside while loop")
        if not q.empty():
            query = q.get()
            print("Inside if condition")
            processing = True
            print("Enter a query:-")
            start = timeit.default_timer()
            response = dbqa({'query': query})
            end = timeit.default_timer()

            print(f'\nAnswer: {response["result"]}')
            print('=' * 50)
            print(f"Time to retrieve response: {end - start}")
            processing = False
        else:
            break

    # # Process source documents
    # source_docs = response['source_documents']
    # for i, doc in enumerate(source_docs):
    #     print(f'\nSource Document {i + 1}\n')
    #     print(f'Source Text: {doc.page_content}')
    #     print(f'Document Name: {doc.metadata["source"]}')
    #     print(f'Page Number: {doc.metadata["page"]}\n')
    #     print('=' * 60)


class getSuggestions(Resource):
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("query", type=str)
        args = parser.parse_args()
        query = args["query"]
        q.put(query)
        t = threading.Thread(target=target_method, daemon=True)
        t.start()



api.add_resource(getSuggestions, '/')

if __name__ == '__main__':
    app.run(debug=True)
