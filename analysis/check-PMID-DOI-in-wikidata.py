#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__description__ = " check if PMID or DOI are already listed in Wikidata"
__author__ = "Eva Seidlmayer <eva.seidlmayer@gmx.net>"
__copyright__ = "2020 by Eva Seidlmayer"
__license__ = "ISC license"
__email__ = "seidlmayer@zbmed.de"
__version__ = "1 "


import argparse
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON
import csv

user_agent = "TakeItPersonally, https://github.com/foerstner-lab/TIP-lib, seidlmayer@zbmed.de"
wd_url = SPARQLWrapper("https://query.wikidata.org/sparql", agent=user_agent)
#wd_url = SPARQLWrapper("http://134.95.56.241:3030/dataset.html?tab=query&ds=/wikidata", agent=user_agent)

def main():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("input_file_name")
    parser.add_argument("log_file_name")
    args = parser.parse_args()


    orcid_data = pd.read_csv(args.input_file_name)
    orcid_data.to_dict()
    #print(orcid_data)

    with open(args.log_file_name, 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['orcid','pmid','doi', 'qnr'])

        try:
            for pmid in orcid_data.values:
                query = f'''SELECT ?item WHERE {{
                {{ ?item wdt:P698  "{pmid[1]}" }} 
                    ?item wdt:P31 wd:Q13442814.
                    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE], ar,be,bg,bn,ca,cs,da,de,el,en,es,et,fa,fi, fr,he,hi,hu,hy,id,it,ja,jv,ko,nb,nl,eo,pa,pl,pt,ro,ru,sh,sk,sr,sv,sw,te,th,tr,uk,yue,vec,vi,zh"}}
                    }}'''
                #print(query)
                wd_url.setQuery(query)
                wd_url.setReturnFormat(JSON)
                results = wd_url.query().convert()
                #print('pmid results:', results)
                if (len(results['results']['bindings'])) > 0:
                    for res in results['results']['bindings']:
                        qnr = res['item']['value'].rsplit('/', 1)[1]
                        print(qnr)
                        infos = doi[0], doi[1], doi[2], qnr
                        print('infos', infos)
                        #print(','.join(infos))
                        csv_writer.writerow(infos)
        except:
            pass

        try:
            for doi in orcid_data.values:
                #print(doi[2])
                query = f'''SELECT ?item WHERE {{
                {{ ?item wdt:P356  "{doi[2]}" }} .
                    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE], ar,be,bg,bn,ca,cs,da,de,el,en,es,et,fa,fi, fr,he,hi,hu,hy,id,it,ja,jv,ko,nb,nl,eo,pa,pl,pt,ro,ru,sh,sk,sr,sv,sw,te,th,tr,uk,yue,vec,vi,zh"}}
                }}'''
                #print(query)
                wd_url.setQuery(query)
                wd_url.setReturnFormat(JSON)
                results = wd_url.query().convert()
                #print('doi result:', results)
                if (len(results['results']['bindings'])) > 0:
                    for res in results['results']['bindings']:
                        qnr = res['item']['value'].rsplit('/', 1)[1]
                        print(qnr)
                        infos = doi[0], doi[1], doi[2], qnr
                        print('infos', infos)
                        #print(','.join(infos))
                        csv_writer.writerow(infos)
        except:
            pass


main()