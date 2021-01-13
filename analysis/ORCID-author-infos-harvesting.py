#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__description__ = "Harvest work-files from ORCID database; output ORCID of authors, author's publication PMID and DOI"
__author__ = " Eva Seidlmayer <eva.seidlmayer@gmx.net>"
__copyright__ = "2021 Eva Seidlmayer"
__license__ = "ISC license"
__email__ = "seidlmayer@zbmed.de"
__version__ = "3"

import tarfile
import xmltodict
import csv
import glob
import argparse



def get_orcid(orcid):
    """
    Returns orcid from ORCID summary file
    """
    return orcid['common:orcid-identifier'].get('common:path')


def get_name(name):
    """
    Returns (given_name, family_name) tuple of an author
    """
    return name['person:name'].get('personal-details:given-names'), \
           name['person:name'].get('personal-details:family-name')

def get_affiliation(affiliation):
    """
    Returns affiliation name and adress
    """
    #return affiliation['common:organization'].get('common:name'), affiliation['common:organization'].get('common:adress')
    return affiliation['common:organization'].get('common:name'), \
           affiliation['common:organization']['common:disambiguated-organization'].get('common:disambiguated-organization-identifier'), \
           affiliation['common:organization']['common:disambiguated-organization'].get('common:disambiguation-source'), \
           affiliation['common:start-date'].get('common:year')

def harvest_author_paper(orcid, output):
    """
    Extract ORCID-summaries.tar.gz archive
    Calling get infos functions
    """

    with open(output, 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['orcid', 'given_name', 'family_name', 'affiliation',
                             'affiliation_id', 'affiliation_id_source', 'start_date_year'])

        tars = glob.glob(orcid)
        for tar in tars:
            with tarfile.open(tar) as f:
                for member in f:
                    if not member.isfile(): continue
                    else:
                        xf = f.extractfile(member)
                        data = xmltodict.parse(xf.read())
                        try:
                            aff = []
                            orcid = get_orcid(data['record:record'])
                            name = get_name(data['record:record']['person:person'])
                            aff = get_affiliation(data['record:record']['activities:activities-summary']
                                                          ['activities:employments']['activities:affiliation-group']
                                                            ['employment:employment-summary'])

                            row = orcid, name, aff
                            print(row)
                            csv_writer.writerow(row)
                        except:
                            pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('orcid_summaries_archive')
    parser.add_argument('output_file')
    args = parser.parse_args()
    orcid = args.orcid_summaries_archive
    output = args.output_file

    harvest_author_paper(orcid, output)


if __name__ == '__main__':
    main()
