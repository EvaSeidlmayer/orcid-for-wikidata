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
__description__ = "Extraction of information on authors: ORCID, affiliation, affiliation adress"


import pandas as pd
import xmltodict
import glob
import argparse

class ORCIDData:
    def __init__(self, affiliations_xml=None):
        self.affiliations_xml = affiliations_xml
        self.xmldict = None
        self.orcid = None
        self.results = None
        self.org_name = None
        self.org_address_city = None
        self.org_address_country = None
        self.org_disambigiation = None


        if affiliations_xml is not None:
            self._preprocess_data()
        else:
            print('Enter ORCID archive or download URL')


    def _preprocess_data(self):
        with open(self.affiliations_xml) as file:
            self.xmldict = xmltodict.parse(file.read())

    # get info from xml
        ## get ORCID
            try:
                self.orcid = self.xmldict['employment:employment']['common:source']['common:source-orcid'].get('common:path')
            except:
                pass

        ##get organization
            try:
                self.org_name = self.xmldict['employment:employment']['common:organization'].get('common:name')
                self.org_address_city = self.xmldict['employment:employment']['common:organization']['common:address'].get('common:city')
                self.org_address_country = self.xmldict['employment:employment']['common:organization']['common:address'].get('common:country')
                self.org_disambigiation = self.xmldict['employment:employment']['common:organization'].get('common:disambiguated-organization')
            except:
                pass


        #combine infos
            results = [self.orcid, self.org_name, self.org_address_city, self.org_address_country, self.org_disambigiation]
            #print(results)
            self.results = results

            csv_infos = pd.DataFrame.from_records([self.results])
            csv_infos.to_csv(args.output_csv, mode='a', index=False, header=False)




    def __str__(self):
        return f"""ORCID: {self.orcid}:\n
            Affiliation Organization Name: {self.org_name}\n
            Affiliation Organization City: {self.org_address_city}\n
            Affiliation Organization Country: {self.org_address_country}\n
            Affiliation Organization Disambigiation: {self.org_disambigiation}     
            """

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('orcid_xml_path')
    parser.add_argument('output_csv')
    args = parser.parse_args()

    files = glob.glob(f'{args.orcid_xml_path}/**/*employments*.xml', recursive=True)

    for file in files:
        Example = ORCIDData(affiliations_xml=file)
        print(Example)