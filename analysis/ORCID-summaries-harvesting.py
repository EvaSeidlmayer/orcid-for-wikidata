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
__description__ = "Extraction of information on authors like ORCID ID, given name, familiy name and current affiliation"

import pandas as pd
import xmltodict
import argparse
import glob



class ORCIDData:
    def __init__(self, summaries_xml_txt=None):
        self.summaries_xml_txt = summaries_xml_txt
        self.xmldict = None
        self.orcid = None
        self.results = None
        self.given_name = None
        self.family_name = None
        self.affiliation_name = None
        self.affiliation_address = None
        self.affiliation_year = None
        self.affiliation_month = None
        self.affiliation_day = None

        pass

        if summaries_xml_txt is not None:
            #self._prepare_txt_files_for_preprocessing()
            self._preprocess_data()
            #self.initiate_author_instance()

        else:
            print('Enter ORCID archive or download URL')


    def _preprocess_data(self):
        summ = pd.read_csv(self.summaries_xml_txt, header=None, names=['name'])
        summ = summ['name'].tolist()
        file = summ[0]
        for file in summ:
            with open(file) as infile:
                self.xmldict = xmltodict.parse(infile.read())
                #print(self.xmldict['record:record']['activities:activities-summary']['activities:employments']['activities:affiliation-group']['employment:employment-summary'].get('common:start-date'))
                #print(self.xmldict['employment:employment']['common:organization'].keys())


        # get info from xml
        ## get ORCID
            try:
                self.orcid = self.xmldict['record:record']['common:orcid-identifier'].get('common:path')
            except:
                pass

            try:
                self.given_name = self.xmldict['record:record']['person:person']['person:name'].get('personal-details:given-names')
                self.family_name = self.xmldict['record:record']['person:person']['person:name'].get('personal-details:family-name')
            except:
                pass

        ## get affiliation
            try:
                self.affiliation_name = self.xmldict['record:record']['activities:activities-summary']['activities:employments']['activities:affiliation-group']['employment:employment-summary']['common:organization'].get('common:name')
                self.affiliation_address = self.xmldict['record:record']['activities:activities-summary']['activities:employments']['activities:affiliation-group']['employment:employment-summary']['common:organization'].get('common:adress')
            except:
                pass

        ## get start date
            try:
                self.affiliation_year = self.xmldict['record:record']['activities:activities-summary']['activities:employments']['activities:affiliation-group']['employment:employment-summary']['common:start-date'].get('common:year')
                self.affiliation_month = self.xmldict['record:record']['activities:activities-summary']['activities:employments']['activities:affiliation-group']['employment:employment-summary']['common:start-date'].get('common:month')
                self.affiliation_day = self.xmldict['record:record']['activities:activities-summary']['activities:employments']['activities:affiliation-group']['employment:employment-summary']['common:start-date'].get('common:day')
            except:
                pass

            #combine infos
            results = [self.orcid, self.given_name, self.family_name, self.affiliation_name, self.affiliation_address, self.affiliation_year, self.affiliation_month, self.affiliation_day]
            print(results)
            self.results = results

            #df = pd.DataFrame(columns=['ORCID','title','subtitle','id_type','id_value','citation'])
            #df.to_csv('../data/2020-03-29_ORCID-author-works-1.csv', index=False, header=True)
            csv_infos = pd.DataFrame.from_records([self.results])
            csv_infos.to_csv(args.output_csv, mode='a', index=False, header=False)




    def __str__(self):
        return f"""ORCID: {self.orcid}:\n
            Author Name: {self.given_name} {self.family_name}:\n
            Affiliation: {self.affiliation_name}:\n
            Affiliation address: {self.affiliation_address}:\n
            Affiliation start date year: {self.affiliation_year}:\n
            Affiliation start date month: {self.affiliation_month}:\n
            Affiliation start date day: {self.affiliation_day}:\n
            """

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('orcid_xml_path')
    parser.add_argument('output_csv')
    args = parser.parse_args()

    files = glob.glob(f'{args.orcid_xml_path}/**/.xml' , recursive=True)
    #print(files)
    #sys.exit()

    for file in files:
        researcher = ORCIDData(summaries_xml_txt=file)
        print(researcher)
