#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__description__ = "Harvest work-files from ORCID database; output ORCID of authors, author's publication PMID and DOI"
__author__ = "Lukas Galke, Eva Seidlmayer <eva.seidlmayer@gmx.net>"
__copyright__ = "2020 by Lukas Galke & Eva Seidlmayer"
__license__ = "ISC license"
__email__ = "seidlmayer@zbmed.de"
__version__ = "1 "

import tarfile
import xmltodict
import re
import glob
from collections import defaultdict
import argparse
import csv


WORKS_RE = re.compile(r".*/(.*)_works_\d*.xml")


def maybe_map(apply_fn, maybe_list):
    """
    Applies `apply_fn` to all elements of `maybe_list` if it is a list,
    else applies `apply_fn` to `maybe_list`.
    Result is always list. Empty list if `maybe_list` is None.
    """
    if maybe_list is None:
        return []
    elif isinstance(maybe_list, list):
        return [apply_fn(item) for item in maybe_list]
    else:
        return [apply_fn(maybe_list)]


def get_single_identifier(ext_id):
    """
    Returns (type, value) tuple from a single external-id
    """
    return ext_id.get('common:external-id-type'), ext_id.get('common:external-id-value')


def get_identifiers(orcid_work):
    """
    Returns default dict filled with (type, value) tuples from an orcid work
    """
    if 'common:external-ids' in orcid_work and orcid_work['common:external-ids']:
        identifiers = maybe_map(get_single_identifier, orcid_work['common:external-ids'].get('common:external-id'))
    else:
        identifiers = []
    return defaultdict(str, identifiers)



def harvest_author_paper(path, output):
    """
    Extract ORCID-activities.tar.gz archive
    Calling get_identifiers
    """

    with open(output, 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['orcid', 'pmid', 'pmc', 'doi', 'wosuid', 'eid', 'dnb'])

        author_paper = []
        with tarfile.open(path) as f:
            for member in f:
                if not member.isfile(): continue
                m =WORKS_RE.match(member.name)
                if m:
                    #print(m)
                    orcid = m[1]
                    xf = f.extractfile(member)
                    data = xmltodict.parse(xf.read())
                try:
                    identifiers = get_identifiers(data['work:work'])
                    if identifiers['pmid'] or identifiers['pmc'] or identifiers['doi'] or identifiers['wosuid'] or identifiers['eid'] or identifiers['dnb'] :
                        row = orcid, identifiers['pmid'], identifiers['pmc'], identifiers['doi'], identifiers['wosuid'], identifiers['eid'], identifiers['dnb']
                        print(row)
                        csv_writer.writerow(row)
                        author_paper.append(row)
                except:
                    pass



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('orcid_path')
    parser.add_argument('output_file')
    args = parser.parse_args()
    #path = args.orcid_path
    output = args.output_file
    tarfile_paths = glob.glob("*.tar.gz")
    author_paper= []
    for tarfile_path in tarfile_paths:
        author_paper.extend(harvest_author_paper(tarfile_path, output))



    #harvest_author_paper(path, output)



if __name__ == '__main__':
    main()
