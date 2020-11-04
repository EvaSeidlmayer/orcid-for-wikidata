#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__description__ = " check if PMID or DOI are already listed in Wikidata"
__author__ = "Eva Seidlmayer <eva.seidlmayer@gmx.net>"
__copyright__ = "2020 by Eva Seidlmayer"
__license__ = "ISC license"
__email__ = "seidlmayer@zbmed.de"
__version__ = "1 "


import argparse
from SPARQLWrapper import SPARQLWrapper, JSON
import csv

user_agent = "TakeItPersonally, https://github.com/foerstner-lab/TIP-lib, seidlmayer@zbmed.de"
wd_url = SPARQLWrapper("https://query.wikidata.org/sparql", agent=user_agent)


def get_result(query, id):
    infos = None
    if id:
        wd_url.setQuery(query)
        print(query)
        wd_url.setReturnFormat(JSON)
        try:
            results = wd_url.query().convert()
            print('result:', results)
        except Exception as e:
            print(f'incorrect ID at {e}')
        try:
            if (len(results['results']['bindings'])) > 0:
                for res in results['results']['bindings']:
                    article_qID = res['item']['value'].rsplit('/', 1)[1]
                    # print(article_qID)
                    infos = id[0], id[1], id[2], id[3], id[4], id[5], id[6], article_qID
                    print('infos', infos)
            #if results == QueryBadFormed :
             #   continue
        except Exception:
            pass
    return infos



def main():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("input_file_name")
    parser.add_argument("output_file_name")
    args = parser.parse_args()

    with open(args.output_file_name, 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['orcid','pmid','pmc','doi', 'wosuid', 'eid','dnb', 'article-qID'])

        with open(args.input_file_name) as csvfile:
            csv_reader = csv.reader(csvfile)


            try:
                for id in csv_reader:
                    if id[3] and id[3].isspace():
                        print('doi', id[3])

                        if '\n' in id[3]:
                            #ID =  id[3].split('\n')[1]
                            continue
                        if ' ' in id[3]:
                            ID = id[3].split(' ')[1]
                            query = f'''SELECT ?item WHERE {{
                                {{ ?item wdt:P356 "{ID}" }}.
                                SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE], ar,be,bg,bn,ca,cs,da,de,el,en,es,et,fa,fi, fr,he,hi,hu,hy,id,it,ja,jv,ko,nb,nl,eo,pa,pl,pt,ro,ru,sh,sk,sr,sv,sw,te,th,tr,uk,yue,vec,vi,zh"}}
                                }}'''
                            infos = get_result(query, id)
                            if infos:
                                csv_writer.writerow(infos)

                        else:
                            query = f'''SELECT ?item WHERE {{
                            {{ ?item wdt:P356 "{id[3]}" }}.
                            SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE], ar,be,bg,bn,ca,cs,da,de,el,en,es,et,fa,fi, fr,he,hi,hu,hy,id,it,ja,jv,ko,nb,nl,eo,pa,pl,pt,ro,ru,sh,sk,sr,sv,sw,te,th,tr,uk,yue,vec,vi,zh"}}
                            }}'''
                            infos = get_result(query, id)
                            if infos:
                                csv_writer.writerow(infos)


                    if id[1]:
                        print("pmid:", id[1])
                        query = f'''SELECT ?item WHERE {{
                            {{ ?item wdt:P698  "{id[1]}" }} 
                            ?item wdt:P31 wd:Q13442814.
                            SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE], ar,be,bg,bn,ca,cs,da,de,el,en,es,et,fa,fi, fr,he,hi,hu,hy,id,it,ja,jv,ko,nb,nl,eo,pa,pl,pt,ro,ru,sh,sk,sr,sv,sw,te,th,tr,uk,yue,vec,vi,zh"}}
                            }}'''
                        infos = get_result(query, id)
                        if infos:
                            csv_writer.writerow(infos)

                    if id[2]:
                        print("PMC:", id[2])
                        PMC = id[2][3:]
                        query = f'''SELECT ?item WHERE {{
                                {{ ?item wdt:P932  "{PMC}" }} .
                                    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE], ar,be,bg,bn,ca,cs,da,de,el,en,es,et,fa,fi, fr,he,hi,hu,hy,id,it,ja,jv,ko,nb,nl,eo,pa,pl,pt,ro,ru,sh,sk,sr,sv,sw,te,th,tr,uk,yue,vec,vi,zh"}}
                                }}'''
                        infos = get_result(query, id)
                        if infos:
                            csv_writer.writerow(infos)

                    if id[5]:
                        print("scopus:", id[5])
                        query = f'''SELECT ?item WHERE {{
                                    {{ ?item wdt:P1154 "{id[5]}"}}.
                                SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE], ar,be,bg,bn,ca,cs,da,de,el,en,es,et,fa,fi, fr,he,hi,hu,hy,id,it,ja,jv,ko,nb,nl,eo,pa,pl,pt,ro,ru,sh,sk,sr,sv,sw,te,th,tr,uk,yue,vec,vi,zh"}}
                                }}'''
                        infos = get_result(query, id)
                        if infos:
                            csv_writer.writerow(infos)

                    if id[6]:
                        print("DNB:", id[6])
                        query = f'''SELECT ?item WHERE {{
                            {{ ?item wdt:P1292 "{id[6]}"}}.
                        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE], ar,be,bg,bn,ca,cs,da,de,el,en,es,et,fa,fi, fr,he,hi,hu,hy,id,it,ja,jv,ko,nb,nl,eo,pa,pl,pt,ro,ru,sh,sk,sr,sv,sw,te,th,tr,uk,yue,vec,vi,zh"}}
                        }}'''
                        infos = get_result(query, id)
                        if infos:
                            csv_writer.writerow(infos)

            except Exception as e:
                print(e)

main()
