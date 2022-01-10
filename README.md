# ORCID for Wikidata

This repository contains scripts to import authors with information about affiliation and education from [ORCID database] into [Wikidata]. Afterwards the author items can be connected to their scienctific articles in Wikidata.

[ORCID database]: https://orcid.org/
[Wikidata]: https://www.wikidata.org/

## Background

Initally, this work was part of the project *[Nachnutzung von strukturierten Daten aus Wikidata für bibliometrische Analysen](https://de.wikiversity.org/wiki/Wikiversity:Wikiversity:Fellow-Programm_Freies_Wissen/Einreichungen/Nachnutzung_von_strukturierten_Daten_aus_Wikidata_f%C3%BCr_bibliometrische_Analysen)*.  
While we find a lot of scientific articles in Wikidata (actually 31,5% (Jan 2020 see Wikidata-statistics)) only 8.9% represent humans in general, not even researchers in particular. Often the publications are not linked to their creators which is a pity for users of Wikidata.

Missing author-items are one reason for this problem. Another issue we see is the frequent absent of relations between the publication and the authors although the author is already listed.
To fill this gap and to improve the databasis of Wikidata in general we established a workflow for matching authors and papers applying ORCID data base. Not only bibliometrical analysis would benefit from an improved data basis that connects article-items to their authors-items.

**As we prefer to avoid spamming Wikidata with additional articles and authors, we concentrate on the matching of existing author-items and article-items.** Only if there is an existing author-item we enhanche information registered in Wikidata. 

The next steps will be to to transfer the eries ordinal (P1445) which is frequently given in the author name string (P2093) to the author statement (P50)
Afterwards the author name string shall be removed in order not to disturb tools that get confused by the occurance of both P50 and P2093. 

As further improvement we can easily expand the workflow for introducing additional information from ORCID as on education or other biographical details to the author-items. 




## Requirements

Scripts in this repository requiry 

* Python 3
* Python libraries listed in `requirements.txt` (install with `pip3 install -r requirements.txt`)
* [wikibase-edit]

To process full ORCID dumps and full Wikidata dump you also need enough disk space and some time.

[wikibase-edit]: https://www.npmjs.com/package/wikibase-edit

## Usage

From our experiences the Wikidata API does not deal very well with huge amounts of queries. 
In the previous version we relied on the performance of the Wikidata API for the check, if publications and authors already exist as items in Wikidata. 
Also, the check for registered originator to an article item depend on the API. 
Ass we had a great loss during the recall we changed to download the complete Wikdiata dump. 
Since this, harvesting of the needed information by the provided shell script can be carried out much more fast and much more efficient in terms of quantity. 

***************

### 1. Preparation _ORCID_ data

Download the ORCID database dump from figshare (see <https://orcid.org/content/orcid-public-data-file-use-policy>) leads to <https://orcid.figshare.com/articles/dataset/ORCID_Public_Data_File_2020/13066970/1> for 2020 issue. You do not need to unpack the tar.gz archive. Besides the multiple _activities_-files containing information on works, affiliation, education, fundings, memberships etc. of the registered researchers only a single meta file contains the basic information on the researchers called _summaries_. 
The ORCID data consists of eleven "activity" files containing information on publications, education, employement etc.
A meta file "summaries" contain the overview information on the persons holding a ORCID iD.

From ORCID we create a data set on publications an IDs (1.1) and a data set on the researchers (1.2).  

*********************

#### 1.1  Harvest _publication_ IDs from ORCID

With ORCID-ids-harvesting.py you **harvest PMID, PMC, DOI, WOS-ID, DNB and ORCID of the author from the ORCID.tar.gz archive**.
With adding the ORCID.tar.gz path as input file and an output file:

     ./analysis/ORCID-ids-harvesting.py ORCID_2020_10_activities_1.tar.gz ORCID-ids_1.csv

...you get a csv like this: 

| orcid | pmid | pmc | doi | wosuid | eid | dnb |
|----|:----:|:----:|:----:|:----:|:----:|----:|
| 0000-0003-2760-1191 | | | 10.1111/j.1540-8175.2010.01316.x | | 2-s2.0-79952755968 | |
| 0000-0001-9154-8191 | 26093915 | PMC4491368 | 10.1007/s10482-015-0502-7 | | | |
| 0000-0002-8639-5191 | |  | 10.1111/J.1747-4949.2007.00119.X | WOS:000247202000017 | | |


From ORCID_2020_10_activities_1.tar.gz we retrieved **4 094 175 publications** (dedublicated) indicated by PMID, PMC, DOI, WOS-id, Scopus-ID, DNB. From ORCID_2020_10_activities_2.tar.gz we retrieved **4 019 965 publications** (dedublicated) indicated by these IDs.

Then we check if those articles are already listed in Wikidata. Only already existing paper-items shall enriched, in order not to flood the Wikidata platform with scientific papers.

********************

#### 1.2 Harvest _author_ information from ORCID

We use ORCID-author-infos-harvesting.py to **harvest information on authors**.
Please add the summary file as input and define an output file name. 

    ./analysis/ORCID-author-infos-harvesting.py ORCID_2020_10_summaries.tar.gz ORCID-authors-infos.csv
    
It will give you information like this:

| orcid | given_name | family_name | affiliation | affiliation_id | affiliation_id_source | start_date_year|
|----|:---:|:----:|:----:|:----:|:----:|----:|
| 0000-0002-4807-379X |"('Esha'| 'Kundu')" |"('Curtin University'| '1649' |'RINGGOLD'| '2019')" |
| 0000-0002-8182679X |"('Alla'| None)" | "('Pavlo Tychyna Uman State Pedagogical University' | '416526' | 'RINGGOLD' | '1971')" |        

From the ORCID_2020_10_summaries.tar.gz archive we retrieved basic information on 877 616 researchers. We could use the information to set up a basic information item for authors if needed.
From the ORCID 2021 file we retrieved information  on 1 061 170 researchers.  
******************************

### 2. Preparation _Wikidata_ data 
As we experienced a much better result by using the Wikidata dump instead of the Wikidata API (ORCID-for-Wikidata v.1), we recommend to download the complete Wikidata dump:
 https://dumps.wikimedia.org/wikidatawiki/entities/latest-truthy.nt.bz2 (currently, 25GB compressed) 

*********************************

#### 2.1  Harvest data on _publications_ from Wikdiata
Extract all identifiers (DOI, PMID, PMC, EID, DNB) and Q-IDs of articles with the following shell commands:

*DOI (Digital Object Identifier) = P356:  

    bzcat latest-truthy.nt.bz2 | grep 'prop/direct/P356>' | perl -pe 's|<.+?/([^/]+)>|\1|g;s|"||g' > doi.txt

 result: Q59755 P356 10.1002/(ISSN)1098-2353 .

 reads: Article with Q-ID Q59755 has a DOI (P356) that is: 10.1002/(ISSN)1098-2353.

*PMID (PubMed ID )= P698: 

    bzcat latest-truthy.nt.bz2 | grep 'prop/direct/P698>' | perl -pe 's|<.+?/([^/]+)>|\1|g;s|"||g' > pmid.txt

 result: Q3049558 P698 26647248 .  

 reads: Article with Q-ID Q3049558 has a PMID (P698) that is: 26647248.

*PMC (PubMed Central ID): P932  

    bzcat latest-truthy.nt.bz2 | grep 'prop/direct/P932>' | perl -pe 's|<.+?/([^/]+)>|\1|g;s|"||g' > pmc.txt

result: Q17485680 P932 3274487 .

 reads: Article with Q-ID  Q17485680 has a PMC (P932) that is: 3274487.

*EID (Scopus ID): P1154

    bzcat latest-truthy.nt.bz2 | grep 'prop/direct/P1154>' | perl -pe 's|<.+?/([^/]+)>|\1|g;s|"||g' > eid.txt

result: Q26739705 P1154 2-s2.0-84981240930 .

reads: An Article with Q-ID Q26739705 has an EID (P1154) that is: 2-s2.0-84981240930.

*DNB (Deutsche National Bibliothek ID):   P1292

    bzcat latest-truthy.nt.bz2 | grep 'prop/direct/P1292>' | perl -pe 's|<.+?/([^/]+)>|\1|g;s|"||g' > dnb.txt

result: Q655717 P1292 041382137 .

reads: An Article with Q-ID Q655717 has a DNB (P1292) that is: 041382137.


Those datasets need to be combined in a csv-file we call WIKIDATA-publications-ids.csv. Since the files are hugh we 
first merged doi.txt, pmid.txt and pmc.txt . In a second step we merge eid.txt and dnb.txt. It might also help to split big files (pmid.txt, doi.txt) in chunks
Your approach depends on your RAM.


 _load txt data - only those columns we need: article-QID and identifier_

    doi_df = pd.read_csv('/home/ruth/ProgrammingProjects/enrich_with_orcid/data/WD-2021-Orcbot2.0_doi.txt', sep= " ", error_bad_lines=False, usecols=[0,2], low_memory=False)
    pmc_df = pd.read_csv('/home/ruth/ProgrammingProjects/enrich_with_orcid/data/WD-2021-Orcbot2.0_pmc.txt', sep= " ",   error_bad_lines=False, usecols=[0,2], low_memory=False)
    pmid_df = pd.read_csv('/home/ruth/ProgrammingProjects/enrich_with_orcid/data/WD-2021-Orcbot2.0_pmid.txt', sep= " ", error_bad_lines=False, usecols=[0,2], low_memory=False)

_rename columns_

    doi_df.rename(columns={doi_df.columns[0]:"qID",doi_df.columns[1]:"doi"}, inplace = True)
    pmc_df.rename(columns={pmc_df.columns[0]:"qID",pmc_df.columns[1]:"pmc"}, inplace = True)
    pmid_df.rename(columns={pmid_df.columns[0]:"qID",pmid_df.columns[1]:"pmid"}, inplace = True)

_merge data frames in chunks_

    df_doi_pmc = pd.merge(doi_df,pmc_df, on='article-QID', how='outer')
    df_doi_pmc_pmid = pd.merge(df_doi_pmc, pmid_df, on="article-QID", how = 'outer')

_save to csv_

    df_doi_pmc_pmid.to_csv('../data/Wikidata-publications-ids.csv')

Repeat the process for eid.txt and dnb.txt.  WIKIDATA-publications-ids.csv looks like:

| qID | pmc | dnb | pmid | doi | eid |
|----|:----:|:----:|:----:|:----:|:----:|
| Q17485067 | 3121651 | | 21609473 | 10.1186/1475-2875-10-144 | 
| Q17485680 | 3274487 | | 22185615 | 10.1186/1475-2875-10-378 | 
| Q17485684 | 2885984 | | 20563310 | 10.1371/JOURNAL.PMED.1000290 | 
| Q17485685 | 3146776  | | 21893544 |10.1098/RSTB.2011.0091 | 

********************

#### 2.2 Harvest data on registered _authors_ from Wikidata
In order to add information only on those authors who are already listed in Wikidata (P50) we also harvest existing authors and ORCID-IDs. 
We need this file in 3.2.

    bzcat latest-truthy.nt.bz2 | grep 'prop/direct/P50>' | perl -pe 's|<.+?/([^/]+)>|\1|g;s|"||g' > allauthors.txt

result: Q101012477 P50 Q1655369 .

reads: An article Q101012477 has an author (P50) who has the Wikidata Q-ID: Q1655369 .

    bzcat latest-truthy.nt.bz2 | grep 'prop/direct/P496>' | perl -pe 's|<.+?/([^/]+)>|\1|g;s|"||g' > orcid.txt

result: Q26322 P496 0000-0002-5494-8126 .

reads: A researcher with Q-ID Q26322 has an ORCID-iD (P496) which is: 0000-0002-5494-8126 . 

***************

### 3.1 Reducing _publications_ data set to those which are already registered in Wikidata by combining Wikidata based data set and ORCID based data set

_map_wikipedia_orcid-publication_ids.py_

Merging ORCID based publication IDs created in 1.1 and Wikidata based publication IDs created in 2.1 with script map_wikidata-orcid-publication-ids.py   

    ./map_wikidata_orcid-publication_ids.py ORCID-ids_1.csv WIKIDATA-publication-ids.csv ORCID_publications_qid-1.csv

The result looks as follows:

|publication_qID | orcid | doi | pmc | pmid | dnb |eid |
|----|:-----:|:-----:|:-----:|:-----:|:-----:|-----:|
| Q61449719 | 0000-0003-4861-0636 | 10.3987/COM-14-S(K)73 ||||
| Q60656124 | 0000-0003-4861-0636 | 10.1039/C6RA14435G ||||
| Q57858467 | 0000-0003-4861-0636 | 10.1039/C7GC00571G |||| 

It contains the subset of all publications listed in the chosen ORCID-file that have QIDs. Since they have a QID we know they are registered in Wikidata.  

*******************
_map_allauthors_to_article.py_

Now we like to add also the authors QID to the data set:

    ./analysis/map_allauthors_to_article.py ORCID_publications_qid-1.csv allauthors.txt final-publication-data-1.csv

The script map_allauthors_to_article.py groups all listed authors of an article QID and produces a structure like this internally:
   
| publication_qID | all_authors_qID| 
|----|:----:|
| Q101012477 |  Q1655369 Q25350074 Q1114742 Q25350074 |
| Q101010935 | Q57912454 Q2158896 Q6270412 |

...then the script merges the authors of articles to the just generated publication file (ORCID-publications_qid-1.csv) using QID as key.

The final format of the publication data set is:

|publication_qID | orcid |                         doi                         |                    pmc                    | pmid | dnb | eid | all_authors_qID |
|----|:-----:|:---------------------------------------------------:|:-----------------------------------------:|:-----:|:-----:|:----:|-----:|
| Q42530171 | 0000-0003-2743-0337 |||    16647637.0    ||| "['Q42114754', 'Q42305518', 'Q89834128']" |
| Q48003384 | 0000-0002-0997-4384 ||| 2-s2.0-84994508140 |||        "['Q47067377', 'Q60393087']"       |

*******************

### 3.2 Limiting down ORCID _authors_ to those who are registered to Wikidata

* In order to create the data set on authors based on ORCID supplemented with the QID from Wikidata we combine the data set we created from ORCID in 1.2 (ORCID-author-infos.csv) and
match it with the data we harvested from Wikidata in 2.2. (orcid.txt)

Performing an outer join of both data set on key "orcid" will give us a set of all ORCID researcher who are listed in Wikidata. Additionally, the author QID will be added to the entry.
We call the generated data final-author-data.csv
  
| author_qID | orcid | given_name | family_name | affiliation | affiliation_id | affiliation_id_source | start_date_year|
|------------|:---:|:----:|:----:|:----:|:----:|:----:|----:|
| Q59151132  | 0000-0003-1808-679X | 'Marek' | 'Radkowski' | 'Medical University of Warsaw' |  'grid.13339.3b' | 'GRID' | '1986' | nan | nan | nan | nan |
| Q54452584  | 0000-0002-0171-879X | 'Barbara' | 'van Asch'| 'Stellenbosch University | '26697' | 'RINGGOLD' | '2015'| nan | nan | nan | nan |
| Q61110015  | 0000-0002-7844-079X | 'Janika' | 'Nättinen' | 'Tampere University' | 'grid.5509.9' | 'GRID' | '2014' | nan | nan | nan | nan |
| Q60042671  | 0000-0001-9494-179X | 'Georgios' | 'Dimitriadis' | 'University of California Santa Cruz' | '8787' | 'RINGGOLD' | '2017' | nan | nan | nan | nan |



******************************
### 4. Register missing authors to Wikidata publication items (OrcBot)

The script combines both datasets generated in 3. using "orcid" as key. It checks if the author who claims in ORCID database to be originator of a work is already listed as author with property  P50.
     
     analysis/OrcBot.py  final-publication-data-1.csv final-author-data.csv log_2020-11-25.json

_basic functionality_
![alt text](https://github.com/EvaSeidlmayer/orcid-for-wikidata/blob/master/OrcBot.png "basic functionality of OrcBot")
It generates a json file like this:
{"id": "Q27016918", "claims": {"P50": {"value": "Q18026282", "qualifier": [{"P1932": "('Natalie', 'Batalha')"}]}}}

..and uploads it using Wikidata CLI tool. 
example: Q27019745.json

Voilà!
