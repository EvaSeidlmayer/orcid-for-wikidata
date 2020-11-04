#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__description__ = "dedublicate dataset"
__author__ = "Eva Seidlmayer <eva.seidlmayer@gmx.net>"
__copyright__ = "2020 by Eva Seidlmayer"
__license__ = "ISC license"
__email__ = "seidlmayer@zbmed.de"
__version__ = "1 "


import argparse
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("input_file_name")
    parser.add_argument("output_file_name")
    args = parser.parse_args()

#    with open(args.output_file_name, 'w') as csvfile:
 #       csv_writer = csv.writer(csvfile)
  #      csv_writer.writerow(['orcid','pmid','pmc','doi', 'wosuid', 'eid','dnb', 'article-qID'])

    df = pd.read_csv(args.input_file_name)
    print(len(df))

    df_clean = df.drop_duplicates()
    print(len(df_clean))
    print(df_clean)
    df_clean.to_csv(args.output_file_name, index=False)

main()
