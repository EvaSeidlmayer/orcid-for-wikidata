#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__description__ = "harvesting an dimplementing ORCID information for Wikidata applying SPARQLWrapper and Wikidata-CLI"
__author__ = "Eva Seidlmayer <eva.seidlmayer@gmx.net>, Jakob Voß <voss@gbv.de>, Konrad Foerstner <konrad@foerstner.org>"
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


def create_template_article_item(all_df):
    for row in all_df:
        return''' {
            "id": row['article_qnr'],
            "claims": {
                "P50": {
                    "value": row['author_qnr'],
                    "qualifier": [{"P1932": row['given_name']}]
                }
            }
        }'''

def edit_item(row, wikidata_cli_executable, log_file_name):
    with open(log_file_name, 'a') as f:
        item = create_template_article_item(row)
        tmp_json_file = "tmp.json"

        with open(tmp_json_file, "w") as entity_json_fh:
            entity_json_fh.write(json.dumps(item))

        creation_result = subprocess.run(f"{wikidata_cli_executable} edit-entity ./{tmp_json_file}".split(), capture_output=True)
        logging.info(creation_result)
        print(creation_result)
        if creation_result.returncode == 0:
            result = json.loads(creation_result.stdout.decode('utf-8'))
            f.write(str(result) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("--wikidata_cli_executable", default="wb")
    parser.add_argument("--dry", action='store_true')
    parser.add_argument("--quiet", action='store_true')
    parser.add_argument("available_articles_available_authors_csv")
    parser.add_argument("log_file_name")
    #parser.add_argument("year")
    args = parser.parse_args()

    if (args.quiet):
        logging.basicConfig(format='%(message)s', level=logging.WARNING)
    else:
        logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    wikidata_authors = read_csv(args.available_articles_available_authors_csv)
    orcid_authors = read_csv("../available-authors-in-wd-2020-06-20.csv")
    #print(orcid_authors.head())
    wikidata_authors = wikidata_authors.rename(columns={'orcid_origin' : 'orcid'})
    all_df = pd.merge(wikidata_authors, orcid_authors, on='orcid')
    #all_df = all_df.fillna(0)
    #print('all:', all_df.head().to_string())

    already_registered = 0
    needs_to_be_registered = 0
    authors_not_registered = 0


    for index, row in all_df.iterrows():
        print(row['author_qnr'], row['all_authors_qnr'], type(row['all_authors_qnr']), row['given_name'])
        try:
            if row['author_qnr'] is float():
                authors_not_registered += 1
                print('author needs to be registered')
            if pd.isna(row['author_qnr']):
                authors_not_registered += 1
                print('author needs to be registered')
            #if  row['all_authors_qnr'] is list:
             #   if row['author_qnr'] in list(row['all_authors_qnr']):
              #      already_registered +=1
               #     print('already registered')
                #else:
                 #   needs_to_be_registered += 1
                  #  print('article-qnr:', row['article_qnr'], 'needs to be registered')
            if row['all_authors_qnr'] is float():
                needs_to_be_registered += 1
                print('no authors in article item', row['article_qnr'], 'needs to be registered')

            else:
                if row['author_qnr'] in row['all_authors_qnr']:
                    already_registered += 1
                    print('already registered')
                if row['author_qnr'] == row['all_authors_qnr']:
                    already_registered += 1
                    print('already registered')

                elif pd.isna(row['all_authors_qnr']):
                    needs_to_be_registered +=1
                    print('no authors in article item', row['article_qnr'], 'needs to be registered')
                    #edit_item(row, args.wikidata_cli_executable, args.log_file_name)

                else:
                    needs_to_be_registered += 1
                    print('article-qnr:', row['article_qnr'], 'needs to be registered')
                    #edit_item(row, args.wikidata_cli_executable, args.log_file_name)

        except Exception as e:
            print(e)
    print('already registered authors:', already_registered)
    print('authors needs to be registered in article item:', needs_to_be_registered)
    print('authors needs to get registered', authors_not_registered)

main()



'''
for article_qnr in all_df['article_qnr']:
    article_file = subprocess.run(f"{args.wikidata_cli_executable} gt ./{article_qnr}".split(),
                                  capture_output=True)
    logging.info(article_file)
    if article_file.returncode == 0:
        result = json.loads(article_file.stdout.decode('utf-8'))
        authors = []
        #print('P50', result['claims']['P50'])
        try:
            if isinstance(result['claims']['P50'], str):
                authors.append(result['claims']['P50'])

            elif isinstance(result['claims']['P50'], list):
                for item in result['claims']['P50']:
                    for key in item.keys():
                        authors.append(item[key])
                        # print('item key:', item[key])
                        print('authors', authors)
                        print('XXXXXXXXXXXXXXXXXXXxx')
        except Exception as e:
            print(e)
'''