#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__description__ = " check if PMID or DOI are already listed in Wikidata"
__author__ = "Eva Seidlmayer <eva.seidlmayer@gmx.net>"
__copyright__ = "2020 by Eva Seidlmayer"
__license__ = "ISC license"
__email__ = "seidlmayer@zbmed.de"
__version__ = "1 "


import argparse
import time
import pandas as pd
from pandas import read_csv
import logging
from SPARQLWrapper import SPARQLWrapper, JSON

user_agent = "TakeItPersonally, https://github.com/foerstner-lab/TIP-lib, seidlmayer@zbmed.de"
wd_url = SPARQLWrapper("https://query.wikidata.org/sparql", agent=user_agent)


def main():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("input_file_name")
    parser.add_argument("log_file_name")
    args = parser.parse_args()


    orcid_data = read_csv(args.input_file_name)

    wd_check = []

    for _, row in orcid_data.iterrows():
        if item_exists(row, wd_url):
            row = row['orcid'], row['pmid'], row['doi'], qnr
            wd_check.append(row)
        else:
            row = row['orcid'], row['pmid'], row['doi'], ''
            wd_check.append(row)
            time.sleep(3)

    df_wd_check = pd.DataFrame(wd_check, columns=['orcid', 'pmid', 'doi', 'qnr'])
    df_wd_check.to_csv('args.log_file_name', index=False)


def item_exists(row, wd_url):
    """
    Check by querying for article items with PMID and DOI
    """
    pmid = row['pmid']
    doi = row['doi']

    query = f'''SELECT ?item WHERE {{
        {{ ?item wdt:P698  "{pmid}" }} OR
        {{ ?item wdt:356 "{doi}" }} .
            ?item wdt:P31 wd:Q13442814.
            SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE], ar,be,bg,bn,ca,cs,da,de,el,en,es,et,fa,fi, fr,he,hi,hu,hy,id,it,ja,jv,ko,nb,nl,eo,pa,pl,pt,ro,ru,sh,sk,sr,sv,sw,te,th,tr,uk,yue,vec,vi,zh"}}
    }} }}'''
    logging.debug(query)

    wd_url.setQuery(query)
    print(query)
    wd_url.setReturnFormat(JSON)
    results = wd_url.query().convert()
    logging.debug(results)

    if len(results['results']['bindings']) > 0:
        qnr = results['results']['bindings'][0]['item']['value'].rsplit('/', 1)[1]
    else:
        qnr = ''
    return qnr

main()
