#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__description__ = "merging all authors listed in Wikidata related to an article QID; " \
                  "creating a file with all in Wikidata available articles and its available authors"
__author__ = "Eva Seidlmayer <eva.seidlmayer@gmx.net>"
__copyright__ = "2020 by Eva Seidlmayer"
__license__ = "ISC license"
__email__ = "seidlmayer@zbmed.de"
__version__ = "1 "

import pandas as pd
import argparse



def main():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("ORCID_publication_ids")
    parser.add_argument("allauthors_QID")
    parser.add_argument("ORCID_publication_qID")
    args = parser.parse_args()

    #reading file containing publication IDs harvested from ORCID
    ORCID = pd.read_csv(args.ORCID_publication-IDs, dtype=str)

    #reading file harvetsed from Wikidata dump: bzcat latest-truthy.nt.bz2 | grep 'prop/direct/P356>' | perl -pe 's|<.+?/([^/]+)>|\1|g;s|"||g' > allauthors.txt
    col_list = ['qID','property', 'allauthors_QID', 'dot']
    _WD = pd.read_csv(args.allauthors_QID, sep=' ',  names=col_list, dtype=str)
    _WD.drop(columns={'property', 'dot'}, inplace=True)
    WD = _WD.groupby(['qID'])['allauthors_QID'].apply(list)
    print(WD)


    print("processing!")
    result =  pd.merge(ORCID, WD, how= 'left', on='qID')


    print("done!")
    print(len(result))
    result.to_csv(args.ORCID_publication_qID, index=False)


main()