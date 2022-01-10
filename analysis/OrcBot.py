#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__description__ = (
    "compares known authors from ORCID with author statements in Wikidata article item; "
    "if the author statement is not complete the article item is modified applying Wikibase CLI"
    "we introduce reference statement 'ORCID public data 2021' (Q110411020)"
    "if already given in P2093 author string name we transfer P1545 series ordinal to the P50 statement "
    "we delete the P2093 author string name claim after registration of P50"
)
__author__ = "Eva Seidlmayer <seidlmayer@zbmed.de>"
__copyright__ = "2022 by Eva Seidlmayer"
__license__ = "ISC license"
__email__ = "seidlmayer@zbmed.de"
__version__ = "3.1"


import argparse
import json
import subprocess
from pandas import read_csv
import logging
import pandas as pd
import sys
from ast import literal_eval
import time


# harvest all name labels and alias for an author_QID from Wikidata and put the in a dictionary
def create_author_QID_dict(row):
    print(
        "2: check for all labels and alias of author identified with author QID and not registered to article yet"
    )
    author_QID = row["author_qID"]
    author_variants = {}
    creation_result = subprocess.run(
        f"wb d {author_QID}  | jq -r '.labels,(.aliases|.[])|.[].value' | sort | uniq ".split(
            "/n"
        ),
        capture_output=True,
        shell=True,
    )
    p50names = creation_result.stdout.decode("UTF-8").splitlines()
    author_variants[author_QID] = p50names
    time.sleep(3)
    return author_variants


# harvest author name string P2093 and - if existing - related series ordinal P1545 for a given article_QID via Wikibase CLI
def create_author_string_dict(row):
    print(
        "3: check for all listed author string names and related series ordinal for a given article"
    )
    p2093_infos = []
    article_qID = row["article_qID"]
    tmp_json_file = "tmp_20210105.json"
    with open(tmp_json_file, "w") as f:
        creation_result = subprocess.run(
            f"wb gt {article_qID} --format json".split(), capture_output=True
        )
        article = creation_result.stdout.decode("UTF-8")
        result = json.loads(article)
        try:
            for element in result["claims"]["P2093"]:
                author_plain = {}
                guid = element.get("id")
                author = element.get("value")
                try:
                    for item in element["qualifiers"]["P1545"]:
                        series_ordinal = item
                except:
                    series_ordinal = ""
                    return series_ordinal
                author_plain[f"{author}"] = f"{series_ordinal}"
                p2093_infos.append(author_plain)
            pass

        except KeyError:
            print("No P2093 for article", article_qID)
        return p2093_infos, guid


# compare if the P50 author is already listed as P2093 author name string and has a series ordinal.
def check_name_variations_in_p2093(
    author_variants, p2093_infos, guid, row, log_file_name
):
    print("4: check if the author is already listed as author name string P2093")
    try:
        for names in author_variants.values():
            for name in names:
                for author_dict in p2093_infos:
                    for p2093name in author_dict.keys():
                        if name == p2093name:
                            print("yes")
                            edit_item_p2093(p2093name, author_dict, row, log_file_name)
                            remove_p2093_claims(guid)
    except:
        edit_item_plain(row, log_file_name)
        print("Article", row["article_qID"], "was operated")


# start a subprocess applying Wikibase-CLI to modify the article item using the above created template containig the missing author statement
def edit_item_p2093(p2093name, author_dict, row, log_file_name):
    print("4a: Edit Wikidata item under consideration of P2093 infos")
    with open(log_file_name, "a") as f:
        item = create_p2093_template(p2093name, author_dict, row)
        logging.info(f"item is {item}")
        tmp_json_file = f"{row['article_qID']}.json"

        with open(tmp_json_file, "w") as entity_json_fh:
            entity_json_fh.write(json.dumps(item))

        creation_result = subprocess.run(
            f"wb edit-entity ./{tmp_json_file} --dry".split(), capture_output=True
        )
        logging.info(creation_result)
        if creation_result.returncode == 0:
            result = json.loads(creation_result.stdout.decode("UTF-8"))
            f.write(json.dumps(result) + "\n")


def edit_item_plain(row, log_file_name):
    print("4b: Edit Wikidata item")
    with open(log_file_name, "a") as f:
        item = create_plain_template(row)
        logging.info(f"item is {item}")
        tmp_json_file = f"{row['article_qID']}.json"

        with open(tmp_json_file, "w") as entity_json_fh:
            entity_json_fh.write(json.dumps(item))

        creation_result = subprocess.run(
            f"wb edit-entity ./{tmp_json_file} --dry".split(), capture_output=True
        )
        logging.info(creation_result)
        if creation_result.returncode == 0:
            result = json.loads(creation_result.stdout.decode("UTF-8"))
            f.write(json.dumps(result) + "\n")


# create a template with article_qID, missing author statement P50, author_qID and name string of author
def create_p2093_template(p2093name, author_dict, row):
    print("5a: Create template including P2093 infos")
    return {
        "id": row["article_qID"],
        "claims": {
            "P50": {
                "value": row["author_qID"],
                "qualifier": [
                    {"P1932": row["name"]},
                    {"P1545": author_dict.get(p2093name)},
                ],
            "references": [{"P248": "Q104707600"}],
            }
        },
    }

def create_plain_template(row):
    print("5b: Create plain template")
    return {
        "id": row["article_qID"],
        "claims": {
            "P50": {
                "value": row["author_qID"],
                "qualifier": [{"P1932": row["name"]}],
                "references": [{"P248": "Q104707600"}],
            }
        },
    }


def remove_p2093_claims(guid):
    print("6: Remove P2093 statement")
    creation_result = subprocess.run(
        f"wb  remove-claim {guid} --dry".split(), capture_output=True
    )
    logging.info(creation_result)


def main():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("--dry", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("available_articles_available_authors_csv")
    parser.add_argument("available_ORCID_authors_in_WD")
    parser.add_argument("log_file_name")
    args = parser.parse_args()
    counter = 0
    if args.quiet:
        logging.basicConfig(format="%(message)s", level=logging.WARNING)
    else:
        logging.basicConfig(format="%(message)s", level=logging.DEBUG)
    if counter == 5:
        sys.exit()

    # open data set containing all information on articles and authors existing in Wikdiata
    wikidata_authors = read_csv(args.available_articles_available_authors_csv)
    wikidata_authors = wikidata_authors.rename(
        columns={"qID": "article_qID", "allauthors_QID": "all_authors_qID"}
    )
    print(wikidata_authors.head())

    # open data set containing all information on authors from ORCID including author QID (if existing)
    orcid_authors = read_csv(args.available_ORCID_authors_in_WD, index_col=False)
    orcid_authors = orcid_authors.drop_duplicates()
    orcid_authors = orcid_authors.rename(columns={"qID": "author_qID"})
    print(orcid_authors.head())

    # combining both data sets using ORCID-ID as key
    # this is needed for the check if a authorQID is already part of the listed all_author-QIDs of an article
    all_df = pd.merge(orcid_authors, wikidata_authors, how="right", on="orcid")
    all_df["all_authors_qID"].fillna("[]", inplace=True)
    all_df["all_authors_qID"] = all_df["all_authors_qID"].apply(literal_eval)
    print('0: data sets had been merged')

    # setting counters for statistical use
    no_author = 0
    no_all_authors = 0
    already_registered = 0
    needs_to_be_registered = 0

    # check if author identified with author QID is part of all registered authors of a given article
    for index, row in all_df.iterrows():
        try:
            if pd.isna(row["author_qID"]):
                no_author += 1
            if not row["all_authors_qID"]:
                no_all_authors += 1
            if row["author_qID"] in row["all_authors_qID"]:
                already_registered += 1

            if not (pd.isna(row["author_qID"])) and not (
                row["author_qID"] in row["all_authors_qID"]
            ):
                needs_to_be_registered += 1
                print(
                    "1: this author",
                    row["author_qID"],
                    "is not part of all authors:",
                    row["all_authors_qID"],
                    "of article",
                    row["article_qID"],
                )

                # if the author is not yet listed as P50 author in article
                # we check for all labels and alias - all other writing of the name listed in author QID
                author_variants = create_author_QID_dict(row)

                # afterwards we check the article for information on author name string (P2093) and related series ordnial (P1545)
                p2093_infos, guid = create_author_string_dict(row)

                # we combine both information and check if there is information  in P2093 on the person that should be introduced as P50 to the article.
                check_name_variations_in_p2093(
                    author_variants, p2093_infos, guid, row, args.log_file_name
                )
                print("article", row["article_qID"], "was processed")

        except Exception as e:
            print("Exeption", e)

    print("CASE 1: authors_qID is NaN", no_author)
    print("CASE 2: all_authors_qID is NaN:", no_all_authors)
    print("CASE 3: author is in all_author_qID", already_registered)
    print(
        "CASE 4: author-items exist but needed to be introduced to article_item:",
        needs_to_be_registered,
    )
    print("program done")


main()
