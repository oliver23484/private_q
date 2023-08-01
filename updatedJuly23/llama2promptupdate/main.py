import box
import timeit
import yaml
import argparse
from dotenv import find_dotenv, load_dotenv
from src.utils import setup_dbqa

# Load environment variables from .env file
load_dotenv(find_dotenv())

# Import config vars
with open('config/config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))


def main():
    #args = parse_arguments()
    dbqa = setup_dbqa()
    # Setup DBQA
    while True:
        query = input("\nEnter a query: ")
        if query == "exit":
            break
        if query.strip() == "":
            continue
        start = timeit.default_timer()
        response = dbqa({'query': query})
        end = timeit.default_timer()

        print(f'\nAnswer: {response["result"]}')
        print('='*50)
        print(f"Time to retrieve response: {end - start}")

        # Process source documents
        source_docs = response['source_documents']
        for i, doc in enumerate(source_docs):
            print(f'\nSource Document {i+1}\n')
            print(f'Source Text: {doc.page_content}')
            print(f'Document Name: {doc.metadata["source"]}')
            print(f'Page Number: {doc.metadata["page"]}\n')
            print('='* 60)



# def parse_arguments():
#     parser = argparse.ArgumentParser()
#     parser.add_argument('input',
#                         type=str,
#                         help='Enter the query to pass into the LLM')
#     return parser.parse_args()


if __name__ == "__main__":
    main()