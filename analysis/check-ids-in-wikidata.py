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
import numpy

user_agent = "TakeItPersonally, https://github.com/foerstner-lab/TIP-lib, seidlmayer@zbmed.de"
wd_url = SPARQLWrapper("https://query.wikidata.org/sparql", agent=user_agent)

def main():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("input_file_name")
    parser.add_argument("log_file_name")
    args = parser.parse_args()


    orcid_data = pd.read_csv(args.input_file_name)
    orcid_data.to_dict()
    orcid_data = orcid_data.fillna(0)
    print(orcid_data)

    with open(args.log_file_name, 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['orcid','pmid','pmc','doi','wosuid','eid','dnb', 'article-qnr'])

        try:
            for id in orcid_data.values:
                print("id[3]", id[3])
                if id[3]  != 0:
                    query = f'''SELECT ?item WHERE {{
                        {{ ?item wdt:P356 "{id[3]}" }}.
                        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE], ar,be,bg,bn,ca,cs,da,de,el,en,es,et,fa,fi, fr,he,hi,hu,hy,id,it,ja,jv,ko,nb,nl,eo,pa,pl,pt,ro,ru,sh,sk,sr,sv,sw,te,th,tr,uk,yue,vec,vi,zh"}}
                        }}'''
                    print(query)
                    wd_url.setQuery(query)
                    wd_url.setReturnFormat(JSON)
                    results = wd_url.query().convert()
                    print('doi result:', results)
                    if (len(results['results']['bindings'])) > 0:
                        for res in results['results']['bindings']:
                            article_qnr = res['item']['value'].rsplit('/', 1)[1]
                            #print(article_qnr)
                            infos = id[0], id[1], id[2], id[3], id[4], id[5], article_qnr
                            print('infos', infos)
                            csv_writer.writerow(infos)
                    else:
                        try:
                            for id in orcid_data.values:
                                if id[1] != 0:
                                    query = f'''SELECT ?item WHERE {{
                                    {{ ?item wdt:P698  "{id[1]}" }} 
                                    ?item wdt:P31 wd:Q13442814.
                                    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE], ar,be,bg,bn,ca,cs,da,de,el,en,es,et,fa,fi, fr,he,hi,hu,hy,id,it,ja,jv,ko,nb,nl,eo,pa,pl,pt,ro,ru,sh,sk,sr,sv,sw,te,th,tr,uk,yue,vec,vi,zh"}}
                                    }}'''
                                    print(query)
                                    wd_url.setQuery(query)
                                    wd_url.setReturnFormat(JSON)
                                    results = wd_url.query().convert()
                                    print('pmid results:', results)
                                    if (len(results['results']['bindings'])) > 0:
                                        for res in results['results']['bindings']:
                                            article_qnr = res['item']['value'].rsplit('/', 1)[1]
                                            print(article_qnr)
                                            infos = id[0], id[1], id[2], id[3], id[4], id[5], article_qnr
                                            print('infos', infos)
                                            csv_writer.writerow(infos)

                                    else:
                                        try:
                                            for id in orcid_data.values:
                                                if id[2] != 0:
                                                    PMC = id[2][3:]
                                                    query = f'''SELECT ?item WHERE {{
                                                            {{ ?item wdt:P932  "{PMC}" }} .
                                                                SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE], ar,be,bg,bn,ca,cs,da,de,el,en,es,et,fa,fi, fr,he,hi,hu,hy,id,it,ja,jv,ko,nb,nl,eo,pa,pl,pt,ro,ru,sh,sk,sr,sv,sw,te,th,tr,uk,yue,vec,vi,zh"}}
                                                            }}'''
                                                    print(query)
                                                    wd_url.setQuery(query)
                                                    wd_url.setReturnFormat(JSON)
                                                    results = wd_url.query().convert()
                                                    print('pmc result:', results)
                                                    if (len(results['results']['bindings'])) > 0:
                                                        for res in results['results']['bindings']:
                                                            article_qnr = res['item']['value'].rsplit('/', 1)[1]
                                                            print(article_qnr)
                                                            infos = id[0], id[1], id[2], id[3], id[4], id[5], article_qnr
                                                            print('infos', infos)
                                                            csv_writer.writerow(infos)
                                                    else:
                                                        try:
                                                            for id in orcid_data.values:
                                                                if id[5] != 0:
                                                                    query = f'''SELECT ?item WHERE {{
                                                                                {{ ?item wdt:P1154 "{id[5]}"}}.
                                                                            SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE], ar,be,bg,bn,ca,cs,da,de,el,en,es,et,fa,fi, fr,he,hi,hu,hy,id,it,ja,jv,ko,nb,nl,eo,pa,pl,pt,ro,ru,sh,sk,sr,sv,sw,te,th,tr,uk,yue,vec,vi,zh"}}
                                                                            }}'''
                                                                    print(query)
                                                                    wd_url.setQuery(query)
                                                                    wd_url.setReturnFormat(JSON)
                                                                    results = wd_url.query().convert()
                                                                    print('scopus result:', results)
                                                                    if (len(results['results']['bindings'])) > 0:
                                                                        for res in results['results']['bindings']:
                                                                            article_qnr = res['item']['value'].rsplit('/', 1)[1]
                                                                            print(article_qnr)
                                                                            infos = id[0], id[1], id[2], id[3], id[4], id[5], article_qnr
                                                                            print('infos', infos)
                                                                            csv_writer.writerow(infos)

                                                                    else:
                                                                        try:
                                                                            for id in orcid_data.values:
                                                                                if id[6] != 0:
                                                                                    query = f'''SELECT ?item WHERE {{
                                                                                        {{ ?item wdt:P1292 "{id[6]}"}}.
                                                                                    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE], ar,be,bg,bn,ca,cs,da,de,el,en,es,et,fa,fi, fr,he,hi,hu,hy,id,it,ja,jv,ko,nb,nl,eo,pa,pl,pt,ro,ru,sh,sk,sr,sv,sw,te,th,tr,uk,yue,vec,vi,zh"}}
                                                                                    }}'''
                                                                                    print(query)
                                                                                    wd_url.setQuery(query)
                                                                                    wd_url.setReturnFormat(JSON)
                                                                                    results = wd_url.query().convert()
                                                                                    print('DNB result:', results)
                                                                                    if (len(results['results']['bindings'])) > 0:
                                                                                        for res in results['results']['bindings']:
                                                                                            article_qnr = res['item']['value'].rsplit('/', 1)[1]
                                                                                            print(article_qnr)
                                                                                            infos = id[0], id[1], id[2], id[3], id[4], id[5], article_qnr
                                                                                            print('infos', infos)
                                                                                            csv_writer.writerow(infos)
                                                                                            
                                                                                    else:
                                                                                        continue
                                                                        except:
                                                                            pass
                                                        except:
                                                            pass
                                        except:
                                            pass
                        except:
                            pass
        except:
            pass

main()