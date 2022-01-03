#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__description__ = "The script maps publication IDs from ORCID and publication IDs from Wikidata to one data set"
__author__ = "Eva Seidlmayer <seidlmayer@zbmed.de>"
__copyright__ = "2020 by Eva Seidlmayer"
__license__ = "ISC license"
__email__ = "seidlmayer@zbmed.de"
__version__ = "1 "

import pandas as pd
import argparse

def main():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("ORCID_publication_ID_file")
    parser.add_argument("Wikidata_publication_ID_file")
    parser.add_argument("orcid_for_wikidata_publications")
    args = parser.parse_args()

    #available columns: orcid,pmid,pmc,doi,wosuid,eid,dnb
    col_list = ['orcid','pmid','pmc','doi','eid','dnb']
    ORCID = pd.read_csv(args.ORCID_publication_ID_file, dtype=str, usecols=col_list, chunksize=1000000)
    print(ORCID.head())

    wd = pd.read_csv(args.Wikidata_publication_ID_file, dtype=str)
    print(wd.head())

    result = pd.DataFrame()

    for chunk in ORCID:
        print("processing next!! :) ")
        #interim =  pd.merge(ORCID_ids, chunk,  how='inner', on=[ 'pmc', 'doi', 'pmid','dnb','eid'])
        interim =  pd.concat([pd.merge(chunk.dropna(subset=['doi']),wd.dropna(subset=['doi']),on='doi')[['qID','orcid', 'doi']],
                              pd.merge(chunk.dropna(subset=['pmc']),wd.dropna(subset=['pmc']),on='pmc')[['qID','orcid','pmc']],
                                pd.merge(chunk.dropna(subset=['pmid']),wd.dropna(subset=['pmid']),on='pmid')[['qID','orcid','pmid']],
                                pd.merge(chunk.dropna(subset=['dnb']),wd.dropna(subset=['dnb']),on='dnb')[['qID','orcid','dnb']],
                                pd.merge(chunk.dropna(subset=['eid']),wd.dropna(subset=['eid']),on='eid')[['qID','orcid','eid']]
                            ])
    result =  pd.concat([result, interim])
    result = result.reset_index(drop=True)

    print(len(result))
    result.to_csv(args.orcid_for_wikidata_publications, index=False)
main()