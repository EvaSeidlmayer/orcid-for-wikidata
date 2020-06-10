#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__description__ = " check if PMID or DOI are already listed in Wikidata"
__author__ = "Eva Seidlmayer <eva.seidlmayer@gmx.net>, Lukas Galke "
__copyright__ = "2020 by Eva Seidlmayer"
__license__ = "ISC license"
__email__ = "seidlmayer@zbmed.de"
__version__ = "1 "



import tarfile
import xmltodict
import re
import glob
from tqdm import tqdm
from collections import defaultdict
import pandas as pd
import argparse

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
    print('maybe_map klappt')

def get_single_identifier(ext_id):
    """ Returns (type, value) tuple from a single external-id """
    return ext_id.get('common:external-id-type'), ext_id.get('common:external-id-value')

def get_identifiers(orcid_work):
    """ Returns defaultdict filled with (type, value) tuples from an orcid work """
    if 'common:external-ids' in orcid_work and orcid_work['common:external-ids']:
        identifiers = maybe_map(get_single_identifier, orcid_work['common:external-ids'].get('common:external-id'))
    else:
        identifiers = []
    return defaultdict(str, identifiers)

def harvest_author_paper(args.orcid_path):
    author_paper = []
    parser = argparse.ArgumentParser()
    parser.add_argument('orcid_path')
    args = parser.parse_args()
    tarfile_path = glob.glob(f'{args.orcid_path}/**.tar.gz')

    with tarfile.open(tarfile_path) as tf:
        for member in tqdm(tf, desc=tarfile_path):
            if not member.isfile(): continue
            m = WORKS_RE.match(member.name)
            if m:
                orcid = m[1]
                xf = tf.extractfile(member)
                data = xmltodict.parse(xf.read())
                identifiers = get_identifiers(data['work:work'])
                if identifiers['pmid'] or identifiers['doi']:
                    row = orcid, identifiers['pmid'], identifiers['doi']
                    author_paper.append(row)
    return author_paper

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('orcid_path')
    args = parser.parse_args()

    author_paper = []
    author_paper.extend(harvest_author_paper(args.orcid_path))

    df_author_paper = pd.DataFrame(author_paper, columns=['orcid', 'pmid', 'doi'])
    df_author_paper.to_csv("authorship.csv", index=False)


if __name__ == '__main__':
    main()
