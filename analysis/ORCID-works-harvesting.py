#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Eva Seidlmayer"
__copyright__ = ""
__credits__ = ["Eva Seidlmayer", "Konrad U. Foerstner"]
__license__ = ""
__version__ = "1.0"
__maintainer__ = "Eva Seidlmayer"
__github__ = "https://github.com/foerstner-lab/TIP-lib"
__status__ = "Production"
__description__ = "Extraction of publications (author ORCID, IDs as DOI, WOS, PubMed-ID, title, subtitel) from ORCID XML"

import urllib.request
import csv
import re
import sys
import pandas as pd
import tarfile
import xmltodict
from pprint import pprint
import subprocess
from collections import defaultdict
import glob
import argparse


class ORCIDData:
    def __init__(self, works_xml_txt=None):
        self.works_xml_txt = works_xml_txt
        self.xmldict = None
        self.orcid = None
        self.ids = defaultdict(str)
        self.results = None
        self.title = None
        self.subtitle = None
        pass

        if works_xml_txt is not None:
            self._preprocess_data()
            #print('funktioniert auch 1')
        else:
            print('Enter ORCID archive or download URL')



    def _preprocess_data(self):
        with open(self.works_xml_txt) as file:
            self.xmldict = xmltodict.parse(file.read())

        # get info from xml
        ##get orcid
            try:
                self.orcid = self.xmldict['work:work'].get('@path').rsplit('/')[1]
            except:
                pass

        ##get titel of article
            try:
                self.title = self.xmldict['work:work']['work:title'].get('common:title')
            except:
                pass

        ##get subtitle of article
            try:
                self.subtitle = self.xmldict['work:work']['work:title'].get('common:subtitle')
            except:
                pass

        ##get value  and type of ids
            #pprint(self.xmldict)
            if 'common:external-ids' in self.xmldict['work:work'] and self.xmldict['work:work']['common:external-ids'] is not None:
                ex_ids = self.xmldict['work:work']['common:external-ids'].get('common:external-id', [])

                if isinstance(ex_ids, list):
                    for ex_id in ex_ids:
                        self.ids[ex_id.get('common:external-id-type')] = ex_id.get('common:external-id-value')
                else:
                    self.ids[ex_ids.get('common:external-id-type')] = ex_ids.get('common:external-id-value')
            #print(self.ids)

            ##get citation
            try:
                self.citation = self.xmldict['work:work']['work:citation'].get('work:citation-value')
            except:
                pass

            #combine infos
            results = [self.orcid, self.title, self.subtitle, self.ids['pmid'], self.ids['pmc'], self.ids['doi'], self.ids['eid'], self.ids['dnb'], self.ids['wosuid']]
            print(results)
            self.results = results

            csv_infos = pd.DataFrame.from_records([self.results])
            csv_infos.to_csv(args.output_csv, mode='a', index=False, header=False)


            #print(','.join(results))

    def __str__(self):
        return f"""ORCID: {self.orcid}:\n
            Work_title: {self.title}:\n
            Work_subtitle: {self.subtitle}:\n
            Work_ID_Dict: {self.ids}
            """



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('orcid_xml_path')
    parser.add_argument('output_csv')
    args = parser.parse_args()

    files = glob.glob(f'{args.orcid_xml_path}/**/*works*.xml' , recursive=True)
    #print(files)
    #sys.exit()

    for file in files:
        publication = ORCIDData(works_xml_txt=file)
        print(publication)
