#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__description__ = " check if authors indicated by ORCIDs are already listed in Wikidata"
__author__ = "Eva Seidlmayer <eva.seidlmayer@gmx.net>"
__copyright__ = "2020 by Eva Seidlmayer"
__license__ = "ISC license"
__email__ = "seidlmayer@zbmed.de"
__version__ = "1 "


import argparse
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON
import csv
import time

user_agent = "TakeItPersonally, https://github.com/foerstner-lab/TIP-lib, seidlmayer@zbmed.de"
wd_url = SPARQLWrapper("https://query.wikidata.org/sparql", agent=user_agent)

def main():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("input_file_name")
    parser.add_argument("log_file_name")
    args = parser.parse_args()

    orcid_data = pd.read_csv(args.input_file_name)
    orcid_data.to_dict()
    print(orcid_data)


    with open(args.log_file_name, 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['orcid_origin', 'pmid','pmc', 'doi', 'wosuid', 'eid', 'dnb', 'article_qID', 'all_authors_qID'])
        try:
            for id in orcid_data.values:
                authors = []
                query= f'''SELECT distinct ?author
                        WHERE {{wd:{id[7]} wdt:P50 ?author }}'''
                time.sleep(1)

                print(query)
                wd_url.setQuery(query)
                wd_url.setReturnFormat(JSON)
                results = wd_url.query().convert()
                if (len(results['results']['bindings'])) > 0:
                    for res in results['results']['bindings']:
                        authors.append(res['author']['value'].rsplit('/', 1)[1])
                    author_qID = authors
                else:
                    author_qID = ''
                infos = id[0], id[1], id[2], id[3], id[4], id[5], id[6], id[7],  author_qID
                print(infos)
                csv_writer.writerow(infos)

        except:
            pass


main()