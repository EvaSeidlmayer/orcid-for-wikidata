#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__description__ = "compares known authors from ORCID with author statements in Wikidata article item; " \
                  "if the author statement is not complete the article item is modified apllying Wikibase CLI "
__author__ = "Eva Seidlmayer <seidlmayer@zbmed.de>"
__copyright__ = "2020 by Eva Seidlmayer"
__license__ = "ISC license"
__email__ = "seidlmayer@zbmed.de"
__version__ = "1 "


import argparse
import json
import subprocess
from pandas import read_csv
import logging
import pandas as pd
import sys
from ast import literal_eval


# create a template with article_qID, missing author statement P50, author_qID and name string of author

def create_template_article_item(row):
    return {
        "id": row['article_qID'],
        "claims": {
            "P50": {
                "value": row['author_qID'],
                "qualifier": [{"P1932": row['given_name']}]
            }
        }
    }


# create template for test-instance containing specific properties
'''
def create_template_article_item(row):
    return {
        "id":row['article_qID'],
        "claims": {
            "P242": {
                "value": row['author_qID'],
                "qualifier": [{"P80807": row['given_name']}]
            }
        }
    }
'''

# start a subprocess applying Wikibase-CLI to modify the article item using the above created template containig the missing author statement

def edit_item(row, wikidata_cli_executable, log_file_name):
    with open(log_file_name, 'a') as f:
        item = create_template_article_item(row)
        logging.info(f'item is {item}')
        tmp_json_file = f"{row['article_qID']}.json"
        #tmp_json_file = "tmp.json"

        with open(tmp_json_file, "w") as entity_json_fh:
            entity_json_fh.write(json.dumps(item))

        creation_result = subprocess.run(f"{wikidata_cli_executable} edit-entity ./{tmp_json_file}".split(), capture_output=True)
        logging.info(creation_result)
        print(creation_result)
        if creation_result.returncode == 0:
            result = json.loads(creation_result.stdout.decode('utf-8'))
            f.write(str(result) + '\n')
            counter =+1


def main():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("--wikidata_cli_executable", default="wb")
    parser.add_argument("--dry", action='store_true')
    parser.add_argument("--quiet", action='store_true')
    parser.add_argument("available_articles_available_authors_csv")
    parser.add_argument("log_file_name")
    args = parser.parse_args()
    counter = 0
    if (args.quiet):
        logging.basicConfig(format='%(message)s', level=logging.WARNING)
    else:
        logging.basicConfig(format='%(message)s', level=logging.DEBUG)
    if counter == 5:
        sys.exit()
    wikidata_authors = read_csv(args.available_articles_available_authors_csv)
    orcid_authors = read_csv("../available-authors-in-wd-2020-06-20.csv")
    orcid_authors = orcid_authors.drop_duplicates()
    wikidata_authors = wikidata_authors.rename(columns={'orcid_origin' : 'orcid'})
    all_df = pd.merge(orcid_authors, wikidata_authors, how='right', on='orcid')
    all_df['all_authors_qID'].fillna('[]', inplace=True)
    all_df['all_authors_qID'] = all_df['all_authors_qID'].apply(literal_eval)



    # setting counters for statistical use
    no_author = 0
    no_all_authors = 0
    already_registered = 0
    needs_to_be_registered = 0

    for index, row in all_df.iterrows():
        try:
            if pd.isna(row['author_qID']):
                no_author += 1
            if not row['all_authors_qID']:
                no_all_authors += 1
            if row['author_qID'] in row['all_authors_qID']:
                already_registered += 1

            if  not (pd.isna(row['author_qID'])) and not (row['author_qID'] in row['all_authors_qID']):
                needs_to_be_registered += 1
                print('this author', row['author_qID'], 'is not part of all authors:', row['all_authors_qID'], 'of article', row['article_qID'])
                edit_item(row, args.wikidata_cli_executable, args.log_file_name)
        except Exception as e:
            print("Exeption", e)


    print('CASE 1: authors_qID is NaN', no_author)
    print('CASE 2: all_authors_qID is NaN:', no_all_authors)
    print('CASE 3: author is in all_author_qID', already_registered)
    print('CASE 4: author-items exist but needed to be introduced to article_item:', needs_to_be_registered)

main()
