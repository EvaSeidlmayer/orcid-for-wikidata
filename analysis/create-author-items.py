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
import time
from pandas import read_csv
import logging
from SPARQLWrapper import SPARQLWrapper, JSON

user_agent = "TakeItPersonally, https://github.com/foerstner-lab/TIP-lib, seidlmayer@zbmed.de"
wd_url = SPARQLWrapper("https://query.wikidata.org/sparql", agent=user_agent)



def main():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("--wikidata_cli_executable", default="wd")
    parser.add_argument("--dry", action='store_true')
    parser.add_argument("--quiet", action='store_true')
    parser.add_argument("orcid_summaries_csv")
    parser.add_argument("log_file_name")
    args = parser.parse_args()

    if (args.quiet):
        logging.basicConfig(format='%(message)s', level=logging.WARNING)
    else:
        logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    orcid_data = read_csv(args.orcid_summaries_csv)

    for _, row in orcid_data.iterrows():
        if item_exists(row, wd_url):
            continue
        else:
            item = row_to_item(row)
            if args.dry:
                print(json.dumps(item))
            else:
                create_new_item(row, args.wikidata_cli_executable, args.log_file_name)
                time.sleep(3)


# create json_dictionary with information for uploading to wikidata
def row_to_item(row):
    name = _generate_name_list(row)
    #date = _generate_date_list(row)
    affiliation = row['affiliation_name']

    return {
        "labels": {"en": name}, # given_name and family_name
        "descriptions": {"en": f"researcher at {affiliation}" },
        "claims": {
            "P31": "Q5", # human
            "P496": row['orcid'], # orcid
            "P106": "Q42240", # researcher
            "P6424": {'value': affiliation,
                       "qualifiers": {
                        "P580": row['affiliation_year'] } 
                     }    # start date employment
            #"P735": row['given_name'].title(),  # given_name
            #"P734": row['family_name'].title(),  # family_name
        }
    }

def create_new_item(row, wikidata_cli_executable, log_file_name):

    # create logging-file
    with open(log_file_name, 'a') as f:
        item = row_to_item(row)
        tmp_json_file = "tmp.json"

        with open(tmp_json_file, "w") as entity_json_fh:
            entity_json_fh.write(json.dumps(item))

        creation_result = subprocess.run(f"{wikidata_cli_executable} create-entity ./{tmp_json_file}".split(), capture_output=True)
        logging.info(creation_result)
        if creation_result.returncode == 0:
            result = json.loads(creation_result.stdout.decode('utf-8'))
            f.write(str(result) + '\n')



def _generate_name_list(row):
    '''
    create a 'complete name' from given_name and family_name
    '''
    name = ''
    if (not "given_name" in row.keys()) or (not "family_name" in row.keys()):
            pass
    else:
            given = row['given_name']
            family = row['family_name']
            name = (str(given) + ' ' + str(family))
    return name.title()


def _generate_date_list(row):
    '''
    create a 'complete starting date' of employment from affiliation_year, affiliation_month and affiliation_day
    maybe better to have only the start year as date
    '''
    year =  row['affiliation_year']
    month = row['affiliation_month']
    day = row['affiliation_day']
    #date = (int(year), int(month), int(day))
    date = int(year)
    return date



def item_exists(row, wd_url):
    """
    Check by querying for items with a specific name, alias, or orcid.
    """
    name = _generate_name_list(row)
    orcid = row['orcid']

    #with open(tmp_sparql_file, "w") as output_fh:
    query = f'''SELECT ?item WHERE {{
        {{ ?item wdt:P496 "{orcid}" }} UNION
        {{ ?item rdfs:label "{name}" }} UNION
        {{ ?item skos:altLabel "{name}" .
            ?item wdt:P31 wd:Q5 .
            SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE], ar,be,bg,bn,ca,cs,da,de,el,en,es,et,fa,fi, fr,he,hi,hu,hy,id,it,ja,jv,ko,nb,nl,eo,pa,pl,pt,ro,ru,sh,sk,sr,sv,sw,te,th,tr,uk,yue,vec,vi,zh"}}
    }} }}'''
    #output_fh.write(query)
    logging.debug(query)

    wd_url.setQuery(query)
    wd_url.setReturnFormat(JSON)
    results = wd_url.query().convert()
    print('WIKIDATA answer', results)
    if len(results['results']['bindings']) > 0:
        qnr = results['results']['bindings'][0]['item']['value'].rsplit('/', 1)[1]
        print('item exists already:',qnr)
    else:
        return True



    '''
    try:
        query_result = subprocess.check_output(
            f"{wikidata_cli_executable} sparql "
            f"{tmp_sparql_file} -e https://query.wikidata.org/sparql".split()
        )
    except subprocess.CalledProcessError:
        logging.warning("SPARQL request failed! Skipping entry...")
        return True

    # If this string is return the item is not existing
    return "no result found by name" in str(query_result)
    '''

main()
