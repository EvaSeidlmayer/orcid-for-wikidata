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
__version__ = "3.2"


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
def create_author_string_dict(row, log_file_name):
    flag = True
    print(
        "3: check for all listed author string names and related series ordinal for a given article"
    )
    p2093_infos = []
    article_qID = row["article_qID"]
    tmp_json_file = "tmp_Orcbot.json"
    with open(tmp_json_file, "w") as f:
        creation_result = subprocess.run(
            f"wb gt {article_qID} --format json".split(), capture_output=True
        )
        article = creation_result.stdout.decode("UTF-8")
        result = json.loads(article)
        author_plain = {}
        try:
            # more than one already listed author_name_string
            if type(result["claims"]["P2093"]) is list:
                for element in result["claims"]["P2093"]:
                    author = element.get("value")
                    guid = element.get("id")
                    try:
                        series_ordinal = element["qualifiers"]["P1545"]
                    except KeyError:
                        series_ordinal = ""
                    info = [series_ordinal, guid]
                    author_plain[author] = info
                    p2093_infos.append(author_plain)

            # only one already listed author_name_string
            else:
                author = result["claims"]["P2093"]["value"]
                guid = result["claims"]["P2093"]["id"]
                try:
                    series_ordinal = result["claims"]["P2093"]["qualifiers"]["P1545"]
                except KeyError:
                    series_ordinal = ""
                info = [series_ordinal, guid]
                author_plain[author] = info
                p2093_infos.append(author_plain)
                flag = True
        # no author_name_string yet listed
        except KeyError:
            print("4: No P2093 author name string for article", article_qID)
            print(
                "5a: Prepare for edit of Wikidata item without P2093 and without deleting P2093"
            )
            with open(log_file_name, "a") as f:
                item = create_plain_template(row)
                print(item)
                logging.info(f"item is {item}")
                tmp_json_file = f"{row['article_qID']}.json"
                with open(tmp_json_file, "w") as entity_json_fh:
                    entity_json_fh.write(json.dumps(item))

                creation_result = subprocess.run(
                    f"wb edit-entity ./{tmp_json_file} ".split(), capture_output=True
                )
                print("5c: item was edited")
                logging.info(creation_result)
                if creation_result.returncode == 0:
                    result = json.loads(creation_result.stdout.decode("UTF-8"))
                    f.write(json.dumps(result) + "\n")
                flag = False

        return flag, p2093_infos


# compare if the P50 author is already listed as P2093 author name string and has a series ordinal.
def check_name_variations_in_p2093(author_variants, p2093_infos):
    print(
        "4: make use of information if author is already listed as author name string (P2093)"
    )
    flag = False
    for alias in author_variants.values():
        print(alias)
        for name in alias:
            print(name)
            for author_dict in p2093_infos:
                for p2093name in author_dict.keys():
                    if name == p2093name:
                        print("yes, already listed in P2093")
                        flag = True
                        return flag, p2093name, author_dict
                        break
            if flag == True:
                break
    else:
        p2093name = ""
        author_dict = {}
        print("5: author is not listed yet with author name string (P2093)")
        flag = False
        return flag, p2093name, author_dict


# start a subprocess applying Wikibase-CLI to modify the article item using the above created template containig the missing author statement
def edit_item_p2093(p2093name, author_dict, row, log_file_name):
    print("4a: Prepare for edit of Wikidata item under consideration of P2093 infos")
    print("p2093name", p2093name)
    print("author_dict", author_dict)
    with open(log_file_name, "a") as f:
        item = create_p2093_template(author_dict, p2093name, row)
        logging.info(f"item is {item}")
        tmp_json_file = f"{row['article_qID']}.json"

        with open(tmp_json_file, "w") as entity_json_fh:
            entity_json_fh.write(json.dumps(item))

        creation_result = subprocess.run(
            f"wb edit-entity ./{tmp_json_file} ".split(), capture_output=True
        )
        # print(creation_result)
        print("4c: Item was edited under consideration of P2093 infos")
        logging.info(creation_result)
        if creation_result.returncode == 0:
            result = json.loads(creation_result.stdout.decode("UTF-8"))
            f.write(json.dumps(result) + "\n")
        remove_p2093_claims(p2093name, author_dict)


# create a template with article_qID, missing author statement P50, author_qID and name string of author
def create_p2093_template(author_dict, p2093name, row):
    print("4b: Create template including P2093 (author string) infos")
    print("author_dict", author_dict)
    # no series ordinal
    if not author_dict[p2093name][0]:
        return {
            "id": row["article_qID"],
            "claims": {
                "P50": {
                    "value": row["author_qID"],
                    "qualifiers": {"P1932": p2093name},
                    "references": [{"P248": "Q110411020"}],
                }
            },
        }
    # with series ordinal
    else:
        return {
            "id": row["article_qID"],
            "claims": {
                "P50": {
                    "value": row["author_qID"],
                    "qualifiers": {
                        "P1932": p2093name,
                        "P1545": author_dict[p2093name][0],
                    },
                    "references": [{"P248": "Q110411020"}],
                }
            },
        }


def remove_p2093_claims(p2093name, author_dict):
    print("4d: Remove P2093 statement")
    guid = author_dict[p2093name][1]
    creation_result = subprocess.run(
        f"wb  remove-claim {guid} ".split(), capture_output=True
    )
    print("4e:", "P2093 removed")
    logging.info(creation_result)


def edit_item_plain(row, log_file_name):
    print(
        "5a: Prepare for edit of Wikidata item without P2093 and without deleting P2093"
    )
    with open(log_file_name, "a") as f:
        item = create_plain_template(row)
        print(item)
        logging.info(f"item is {item}")
        tmp_json_file = f"{row['article_qID']}.json"
        with open(tmp_json_file, "w") as entity_json_fh:
            entity_json_fh.write(json.dumps(item))

        creation_result = subprocess.run(
            f"wb edit-entity ./{tmp_json_file} ".split(), capture_output=True
        )
        print("5c: item was edited")
        logging.info(creation_result)
        if creation_result.returncode == 0:
            result = json.loads(creation_result.stdout.decode("UTF-8"))
            f.write(json.dumps(result) + "\n")


def create_plain_template(row):
    # no alias or lable
    print("5b: Create plain template")
    return {
        "id": row["article_qID"],
        "claims": {
            "P50": {
                "value": row["author_qID"],
                "references": [{"P248": "Q110411020"}],
            }
        },
    }
    print("5b: Create plain template")


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

    # open data set containing all information on authors from ORCID including author QID (if existing)
    orcid_authors = read_csv(args.available_ORCID_authors_in_WD, index_col=False)
    orcid_authors = orcid_authors.drop_duplicates()
    orcid_authors = orcid_authors.rename(columns={"qID": "author_qID"})

    # combining both data sets using ORCID-ID as key
    # this is needed for the check if a authorQID is already part of the listed all_author-QIDs of an article
    all_df = pd.merge(orcid_authors, wikidata_authors, how="right", on="orcid")
    all_df["all_authors_qID"].fillna("[]", inplace=True)
    all_df["all_authors_qID"] = all_df["all_authors_qID"].apply(literal_eval)
    print("0: data sets had been merged", all_df.head())

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
                # we check for all labels and alias - all other writings of the name listed in author QID
                author_variants = create_author_QID_dict(row)

                # afterwards we check the article for information on author name string (P2093) and related series ordnial (P1545)
                flag, p2093_infos = create_author_string_dict(row, args.log_file_name)

                # we combine both information and check if there is information  in P2093 on the person that should be introduced as P50 to the article.
                if flag == True:
                    flag, p2093name, author_dict = check_name_variations_in_p2093(
                        author_variants, p2093_infos
                    )
                    if flag == True:
                        edit_item_p2093(p2093name, author_dict, row, args.log_file_name)
                    else:
                        edit_item_plain(row, args.log_file_name)
                else:
                    continue
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
