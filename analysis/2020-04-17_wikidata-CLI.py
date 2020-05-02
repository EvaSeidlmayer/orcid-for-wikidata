#!/usr/bin/env python

__description__ = "adaption of wikidata CLI for ORCID data"
__author__ = "Eva Seidlmayer <eva.seidlmayer@gmx.net>, Konrad Foerstner <konrad@foerstner.org>"
__copyright__ = "2020 by Eva Seidlmayer and Konrad Foerstner"
__license__ = "ISC license"
__email__ = "seidlmayer@zbmed.de"
__version__ = "2 - adaption for ORCID"


import argparse
import json
import subprocess
import time
import pandas as pd
import pprint as pp

user_agent = "TakeItPersonally, https://github.com/foerstner-lab/TIP-lib, seidlmayer@zbmed.de"

def main():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("--wikidata_cli_executable", default="wd")
    parser.add_argument("orcid_summaries_csv")
    parser.add_argument("log_file_name")
    args = parser.parse_args()


    orcid_data = pd.read_csv(args.orcid_summaries_csv)

    for _, row in orcid_data.iterrows():
        if ( item_exists('orcid', row, args.wikidata_cli_executable) or
        item_exists('name', row, args.wikidata_cli_executable) or
        item_exists('alias', row, args.wikidata_cli_executable)):
            continue

        else:
            create_new_item(row, args.wikidata_cli_executable, args.log_file_name)
            time.sleep(3)



def create_new_item(row, wikidata_cli_executable, log_file_name):
    # create logging-file

    with open(log_file_name, 'a') as f:
        name = _generate_name_list(row)
        #date = _generate_date_list(row)

    # create json_dictionary with information for uploading to wikidata
        entity_dict = {
            "labels": {"en": name}, # given_name and family_name
            "descriptions": {"en": "researcher"}, # standard declaration as 'researcher'
            "claims": {
                "P31": "Q5", # human
                "P496": row['orcid'], # orcid
                "P106": "Q42240", # researcher
                "P6424": {'value': row['affiliation_name'],# affiliation
                           "qualifiers": {
                            "P580": row['affiliation_year']} }    # start date employment
                #"P735": row['given_name'].title(),  # given_name
                #"P734": row['family_name'].title(),  # family_name
            }}
        pp.pprint(entity_dict)
        tmp_json_file = "tmp.json"

        with open(tmp_json_file, "w") as entity_json_fh:
            entity_json_fh.write(json.dumps(entity_dict))

        creation_result = subprocess.run(f"{wikidata_cli_executable} create-entity ./{tmp_json_file}".split(), capture_output=True)
        print(creation_result)
        if creation_result.returncode == 0:
            result = json.loads(creation_result.stdout.decode('utf-8'))
            f.write(str(result) + '\n')



def _generate_name_list(row):
    '''
    create a 'complete name' from given_name and family_name
    '''
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



def item_exists(switch, row, wikidata_cli_executable):
    """
    Check by querying for items with a specific name, alias, or orcid.
    """

    value = _generate_name_list(row)
    tmp_sparql_file = "tmp.sparql"
    property = {'name': 'rdfs:label',
                'alias': 'skos:altLabel',
                'orcid': 'wdt:P496'}[switch]

    value = {'name': _generate_name_list(row),
             'alias': _generate_name_list(row),
             'orcid': row['orcid']}[switch]

    with open(tmp_sparql_file, "w") as output_fh:
        sparql_query = f'''SELECT  ?hallo WHERE {{ ?hallo {property}  "{value}".
                        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" }}
                        }}'''
        output_fh.write(sparql_query)
        print(sparql_query)
    try:
        query_result = subprocess.check_output(
            f"{wikidata_cli_executable} sparql "
            f"{tmp_sparql_file} -e https://query.wikidata.org/sparql".split()
        )
    except subprocess.CalledProcessError:
        return False
    # If this string is return the item is not existing
    return "no result found by name" in str(query_result)

main()
