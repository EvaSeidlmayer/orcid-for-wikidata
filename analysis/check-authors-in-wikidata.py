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

    with open(args.log_file_name, 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['author_qnr', 'orcid', 'given_name', 'family_name', 'affiliation',
                                                          'affiliation_id', 'affiliation_id_source', 'start_date_year'])
        try:
            for orcid in orcid_data.values:
                name = str(orcid[1] + orcid[2])
                query = f'''SELECT ?item WHERE {{
                        {{ ?item wdt:P496 "{orcid[0]}" }}  
                            ?item wdt:P31 wd:Q5 .
                            SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE], ar,be,bg,bn,ca,cs,da,de,el,en,es,et,fa,fi, fr,he,hi,hu,hy,id,it,ja,jv,ko,nb,nl,eo,pa,pl,pt,ro,ru,sh,sk,sr,sv,sw,te,th,tr,uk,yue,vec,vi,zh"}}
                            }}'''
                #time.sleep(3)
                wd_url.setQuery(query)
                wd_url.setReturnFormat(JSON)
                results = wd_url.query().convert()
                if (len(results['results']['bindings'])) > 0:
                    for res in results['results']['bindings']:
                        author_qnr = res['item']['value'].rsplit('/', 1)[1]
                else:
                    author_qnr = ''

                infos = author_qnr, orcid[0], orcid[1], orcid[2], orcid[3], orcid[4], orcid[5], orcid[6]
                print(infos)
                csv_writer.writerow(infos)

        except:
            pass



main()