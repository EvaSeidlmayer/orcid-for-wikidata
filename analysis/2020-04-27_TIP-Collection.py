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
__description__ = "Extraction of DOI and PubMed-ID from XML and retierval of ORCIDs for authors"

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
    def __init__(self, ORCID_download_url=None, ORCID_archive_file=None, ORCID_data=None, works_xml_txt=None, affiliations_xml_txt=None, educations_xml_txt=None):
        self.ORCID_download_url = ORCID_download_url
        self.ORCID_archive_file = ORCID_archive_file
        self.ORCID_data = ORCID_data
        self.works_xml_txt = works_xml_txt
        self.affiliations_xml_text = affiliations_xml_txt
        self.educations_xml_txt = educations_xml_txt
        self.xmldict = None
        self.orcid = None
        self.ids = defaultdict(str)
        self.results = None
        self.title = None
        self.subtitle = None
        self.citation = None
        pass


        if ORCID_download_url is not None:
            #self._download_data()
            #self._extract_archive()
            #self._prepare_txt_files_for_preprocessing()
            #self._preprocess_data()
            self.initiate_author_instance()

        elif ORCID_archive_file is not None:
            #self._extract_archive()
            #self._prepare_txt_files_for_preprocessing()
            #self._preprocess_data()
            #self.initiate_author_instance()
            print('yo!')

        elif ORCID_data is not None:
            #self._prepare_txt_files_for_preprocessing()
            self._preprocess_data()
            # self.initiate_author_instance()
            print('funktioniert!')

        elif works_xml_txt is not None:
            #self._prepare_txt_files_for_preprocessing()
            self._preprocess_data()
            #self._print_output_csv()
            #self.initiate_author_instance()
            print('funktioniert auch 1')

        elif educations_xml_txt is not None:
            #self._prepare_txt_files_for_preprocessing()
            #self._preprocess_data()
            self._print_output_csv()
            #self.initiate_author_instance()
            print('funktioniert auch 2')

        elif affiliations_xml_txt is not None:
            #self._prepare_txt_files_for_preprocessing()
            #self._preprocess_data()
            self._print_output_csv()
            #self.initiate_author_instance()
            print('funktioniert auch 3')

        else:
            print('Enter ORCID archive or download URL')

    def _download_data(self):
        #url ="https://orcid.figshare.com/articles/ORCID_Public_Data_File_2019/9988322/2/ORCID_2019_summaries.tar.gz"
        self.ORCID_archive_file = urllib.request.urlretrieve(url, 'ORCID_2019_summaries.tar.gz')

    def _extract_archive(self):
        self.ORCID_file = tarfile.open(self.ORCID_archive_file, 'r|gz')
        self.ORCID_data = self.ORCID_file.extractall()
        self.ORCID_file.close()

    def _prepare_txt_files_for_preprocessing(self):
        subprocess.call(['2020-03-25_make_collection_of_ORCID_works_educations_affiliations.sh', self.ORCID_data]) #parameter needs to be implemented for the correct path to the extracted ORCID-archive
        self.works_xml_txt = pd.read_csv('files_works_xml.txt')
        self.educations_xml_txt = pd.read_csv('files_educations_xml.txt')
        self.affiliations_xml_txt = pd.read_csv('files_affiliations_xml.txt')







    def _preprocess_data(self):
        '''
        works = pd.read_csv(self.works_xml_txt, header=None, names=['name'])
        works = works['name'].tolist()
        file = works[0]
        for file in works:
            with open(file) as infile:
                self.xmldict = xmltodict.parse(infile.read())
         '''
        with open(self.works_xml_txt) as file:
            self.xmldict = xmltodict.parse(file.read())

        # get info from xml
        ##get orcid
            try:
                self.orcid = self.xmldict['work:work']['common:source']['common:source-client-id'].get('common:path')
                #print(self.orcid)
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
            pprint(self.xmldict)
            if 'common:external-ids' in self.xmldict['work:work'] and self.xmldict['work:work']['common:external-ids'] is not None:
                ex_ids = self.xmldict['work:work']['common:external-ids'].get('common:external-id', [])
                #print('ich bin da')

                if isinstance(ex_ids, list):
                    for ex_id in ex_ids:
                        self.ids[ex_id.get('common:external-id-type')] = ex_id.get('common:external-id-value')
                else:
                    self.ids[ex_ids.get('common:external-id-type')] = ex_ids.get('common:external-id-value')
            print(self.ids)
            #sys.exit()

            ##get citation
            try:
                self.citation = self.xmldict['work:work']['work:citation'].get('work:citation-value')
            except:
                pass

            #combine infos
            results = [self.orcid, self.title, self.subtitle, self.ids['pmid'], self.ids['pmc'], self.ids['doi'], self.ids['eid'], self.ids['dnb'], self.ids['wosuid'], self.citation]
            print(results)
            self.results = results

            #df = pd.DataFrame(columns=['ORCID','title','subtitle','pmid','pmc','doi','eid','dnb',wosuid','citation'])
            #df.to_csv('../data/2020-03-29_ORCID-author-works-1.csv', index=False, header=True)
            csv_infos = pd.DataFrame.from_records([self.results])
            csv_infos.to_csv('2020-04-29_ORCID-author-works-9.csv', mode='a', index=False, header=False)


            #print(','.join(results))

    def __str__(self):
        return f"""ORCID: {self.orcid}:\n
            Work_title: {self.title}:\n
            Work_subtitle: {self.subtitle}:\n
            Work_ID_Dict: {self.ids}\n
            Work_citation: {self.citation}
            """



if __name__ == "__main__":
    #Example2 = ORCIDData(works_xml_txt='2020-04-20_author-works-9_xml.txt')
    #print(Example2)

    parser = argparse.ArgumentParser()
    parser.add_argument('orcid_xml_path')
    args = parser.parse_args()

    files = glob.glob(f'{args.orcid_xml_path}/**/*works*.xml' , recursive=True)
    print(files)
    #sys.exit()

    for file in files:
        Example3 = ORCIDData(works_xml_txt=file)
        print(Example3)
