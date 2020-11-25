# ORCID for Wikidata

This repository contains scripts to import authors with information about affiliation and education from [ORCID database] into [Wikidata]. Afterwards the author items can be connected to their scienctific articles in Wikidata.

[ORCID database]: https://orcid.org/
[Wikidata]: https://www.wikidata.org/

## Background

Initally, this work was part of the project *[Nachnutzung von strukturierten Daten aus Wikidata für bibliometrische Analysen](https://de.wikiversity.org/wiki/Wikiversity:Wikiversity:Fellow-Programm_Freies_Wissen/Einreichungen/Nachnutzung_von_strukturierten_Daten_aus_Wikidata_f%C3%BCr_bibliometrische_Analysen)*.  
While we find a lot of scientific articles in Wikidata (actually 31,5% (Jan 2020 see Wikidata-statistics)) only 8.9% represent humans in general, not even researchers in particular. Often the publications are not linked to their creators which is a pitty for users of Wikidata.

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
Also the check for registered originator to an article item depend on the API. 
Ass we had a great loss during the recall we changed to download the complete Wikdiata dump. 
Since this, harvesting of the needed information by the provided shell script can be carried out much more fast and much more efficient in terms of quantity. 

***************+

### 1. Preparation ORCID data

Download the ORCID database dump (see <https://orcid.org/content/orcid-public-data-file-use-policy>), e.g. <https://doi.org/10.23640/07243.9988322.v2> for October 2019. You do not need to unpack the  tar.gz-archive. Besides the multiple _activities_-files containing information on works, affiliation, education, fundings, memberships etc. of the registered researchers only a single meta-file contains the basic information on the researchers called _summaries_. 
The ORCID data consists of eleven "activity" files containing information on publications, education, employement etc.
A meta file "summary" contain the overview information on the persons holding a ORCID iD.

From ORCID we create a data set on publications an IDs (1.1) and a data set on the researchers (1.2).  

*********************

#### 1.1  Harvest publication IDs from ORCID

With ORCID-ids-harvesting.py you **harvest PMID, PMC, DOI, WOS-ID, DNB and ORCID of the author from the ORCID.tar.gz archive**.
With adding the ORCID.tar.gz path as input-file and an output file:

     ./analysis/ORCID-ids-harvesting.py ORCID_2019_activities_1.tar.gz ORCID-ids_1.csv

...you get a csv like this: 

| orcid | pmid | pmc | doi | wosuid | eid | dnb |
|----|:----:|:----:|:----:|:----:|:----:|----:|
| 0000-0003-2760-1191 | | | 10.1111/j.1540-8175.2010.01316.x | | 2-s2.0-79952755968 | |
| 0000-0001-9154-8191 | 26093915 | PMC4491368 | 10.1007/s10482-015-0502-7 | | | |
| 0000-0002-8639-5191 | |  | 10.1111/J.1747-4949.2007.00119.X | WOS:000247202000017 | | |


From ORCID_2019_activites_1.tar.gz we retrieved **3 804 784 4 publications** indicated by PMID, PMC, DOI, WOS-id, Scopus-ID, DNB. From ORCID_2019_activites_2.tar.gz we retrieved **3 752 394 publications** indicated by these IDs.

Then we check if those articles are already listed in Wikidata. Only already existing paper-items shall enriched, in order not to flood the Wikidata platform with scientific papers.

********************

#### 1.2 Harvest author information from ORCID

We use ORCID-author-infos-harvesting.py to **harvest information on authors**.
Please add the summary file as input and define an output file name. 

    ./analysis/ORCID-author-infos-harvesting.py ORCID_2019_summary.tar.gz ORCID-authors-infos.csv
    
It will give you information like this:

| orcid | given_name | family_name | affiliation | affiliation_id | affiliation_id_source | start_date_year|
|----|:---:|:----:|:----:|:----:|:----:|----:|
0000-0002-4807-379X,"('Esha', 'Kundu')","('Curtin University', '1649', 'RINGGOLD', '2019')"
0000-0002-8182-679X,"('Alla', None)","('Pavlo Tychyna Uman State Pedagogical University', '416526', 'RINGGOLD', '1971')"         

From the ORCID_summaries_2019.tar.gz archive we retrieved basic information on 673 058 researchers. We could use these information to set up a basic information item for authors if needed.

******************************

### 2. Preparation Wikidata data 
As we experienced a much better result by using the Wikidata dump instead of the Wikidata API (ORCID-for-Wikidata v.1), we recommend to download a Wikidata dump:
 https://dumps.wikimedia.org/wikidatawiki/entities/latest-truthy.nt.bz2 (currently, 25GB compressed!) 

*********************************++++++

#### 2.1  Harvest data on publications from Wikdiata
Extract all properties on identifiers with the following  shell commands:
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

Those datasets needs to be combined in a csv-file we call WIKIDATA-publications-ids.csv which looks like:

| qID | pmc | dnb | pmid | doi | eid |
|----|:----:|:----:|:----:|:----:|:----:|
Q17485067,3121651,,21609473,10.1186/1475-2875-10-144,
Q17485680,3274487,,22185615,10.1186/1475-2875-10-378,
Q17485684,2885984,,20563310,10.1371/JOURNAL.PMED.1000290,
Q17485685,3146776,,21893544,10.1098/RSTB.2011.0091,

********************

#### 2.2 Harvest data on registered authors from Wikidata

* registered authors: P50
    bzcat latest-truthy.nt.bz2 | grep 'prop/direct/P50>' | perl -pe 's|<.+?/([^/]+)>|\1|g;s|"||g' > allauthors.txt
result: Q101012477 P50 Q1655369 .
reads: An article Q101012477 has an author (P50) with has the Wikidata Q-ID: Q1655369 .

* author who have an ORCID iD: P496 
    bzcat latest-truthy.nt.bz2 | grep 'prop/direct/P496>' | perl -pe 's|<.+?/([^/]+)>|\1|g;s|"||g' > orcid.txt
result: Q26322 P496 0000-0002-5494-8126 .
reads: A researcher with Q-ID Q26322 has an ORCID-iD (P496) which is: 0000-0002-5494-8126 . 

***************

### 3.1 Compiling the data set on publications by combining data from Wikidata and ORCID

* Merging ORCID based publication IDs created in 1.1 and Wikidata based publication IDs created in 2.1 with script wikidata-orcid-publication-ids-mapping.py   

    ./map_wikidata_orcid-publication_ids.py ORCID-ids_1.csv WIKIDATA-publication-ids.csv ORCID_publications_qid-1.csv

The result looks as follows:

|qID | orcid | doi | pmc | pmid | dnb |eid |
|----|:-----:|:-----:|:-----:|:-----:|:-----:|-----:|
Q61449719,0000-0003-4861-0636,10.3987/COM-14-S(K)73,,,,
Q60656124,0000-0003-4861-0636,10.1039/C6RA14435G,,,,
Q57858467,0000-0003-4861-0636,10.1039/C7GC00571G,,,,

It contains the subset of all publications listed in the chosen ORCID-file that have Q-IDs. Since they have a Q-ID we know they are registered in Wikidata.  


* Adding registered authors to the data set containing publication IDs
    ./analysis/wikidata_allauthors.py ORCID-ids-1.csv  orcid.txt final-publication-data-1.csv

The script wikidata_allauthors.py groups all listed authors of an article QID and produces internally a structure like this:
   
| publication QID | all_authors QID| 
|----|:----:|
Q101012477, Q1655369 Q25350074 Q1114742 Q25350074
Q101010935, Q57912454 Q2158896 Q6270412 

...then the script merges the authors of articles to the just generated publication file (ORCID-publications_qid-1.csv) using QID as key.

The final shape of the publication data set is:

|qID | orcid | doi | pmc | pmid | dnb | eid | all_authors_qID |
|----|:-----:|:-----:|:-----:|:-----:|:-----:|:----:|-----:|
Q42530171,0000-0003-2743-0337,,,16647637.0,,,"['Q42114754', 'Q42305518', 'Q89834128']"
Q48003384,0000-0002-0997-4384,,,,,2-s2.0-84994508140,"['Q47067377', 'Q60393087']"

*******************

### 3.2 Limiting down ORCID researchers to those who are registered to Wikidata

* In order to create the data set on authors based on ORCID supplemented with the Q-ID from Wikidata we just combine the data set we created from ORCID in 1.2 (ORCID-author-infos.csv) and
match it with the data we harvested from Wikidata in 2.2. (orcid.txt)

Performing an outer join of both data set on key "orcid" will give us a set of all ORCID researcher who are listed in Wikidata. Additionally, the author Q-ID will be added to the entry.
We call the generated data final-author-data.csv
  
| author_qID| orcid | given_name | family_name | affiliation | affiliation_id | affiliation_id_source | start_date_year|
|----|:---:|:----:|:----:|:----:|:----:|:----:|----:|
| 59151132 | 0000-0003-1808-679X | 'Marek' | 'Radkowski' | 'Medical University of Warsaw' |  'grid.13339.3b' | 'GRID' | '1986' | nan | nan | nan | nan |
| Q54452584 | 0000-0002-0171-879X | 'Barbara' | 'van Asch'| 'Stellenbosch University | '26697' | 'RINGGOLD' | '2015'| nan | nan | nan | nan |
| Q61110015 | 0000-0002-7844-079X | 'Janika' | 'Nättinen' | 'Tampere University' | 'grid.5509.9' | 'GRID' | '2014' | nan | nan | nan | nan |
| Q60042671 | 0000-0001-9494-179X | 'Georgios' | 'Dimitriadis' | 'University of California Santa Cruz' | '8787' | 'RINGGOLD' | '2017' | nan | nan | nan | nan |



******************************
### 4. Register missing authors to Wikidata publication items

the script combines both datasets generated in 3. using "orcid" as key. It checks if the author who claims in ORCID database to be originator of a work is already listed as author with property  P50.
     
     analysis/modify-author-statements-in-article-items.py  final-publication-data-1.csv final-author-data.csv log_2020-11-25.json


It generates a json file like this:
{"id": "Q27016918", "claims": {"P50": {"value": "Q18026282", "qualifier": [{"P1932": "('Natalie', 'Batalha')"}]}}}

..and uploads it using Wikidata CLI tool. 
example: Q27019745.json

*

## License

All source code licensed under [ISC license](https://www.isc.org/downloads/software-support-policy/isc-license/)



<!-- ### Basic author information --!>

<!--Then use the author summaries to create Wikidata items for missing authors, based on an ORCID dump of given year: --!>

    <!--./analysis/create-author-items.py orcid_summaries.csv logfile.txt 2019 --!>

<!--To avoid creation of duplicates, a new item is only created if no Wikidata item of a person (Q5) exists with the same ORCID identifier or with the same (as label or alias). Add option `--dry` to never add new items and in addition option `--quiet` to only emit what would be added to Wikidata. Otherwise the script calls [wikidata-cli] for write-access to Wikidata. --!>
   
<!-- ### Publications --!>

<!-- Harvest publications and matching publication items and author items in Wikidata  --!>

<!--**Harvest publications** by using ORCID-works-harvesting.py for **ORCID of author, title and subtitle of publication, ids of publication** with args-statements for path of extracted ORCID-activities.xml and output-csv --!>

    <!--  ./analysis/ORCID-works-harvesting.py orcid_activities_1.xml orcid-publications_1.csv  --!>

<!-- * upload script for **matching publications recoreded in Wikidata and ORCID of authors in order to establish connection between publications and authors.**  --!>

<!--
### Affiliation history

<!-- * Harvesting of affiliation information and upload to basic item in Wikidata
* **Harvest affiliations** by using ORCID-affiliations-harvesting.py for **ORCID, affiliation name, affiliation adress, affiliation id for disambiguation** with args-statements for path of extracted ORCID-activities.xml and output-csv

     <!-- ./analysis/ORCID-affiliations-harvesting.py orcid_activities_1.xml orcid-affiliations_1.csv

<!-- * to be continued: upload script for **enrich basic items of researchers in Wikidata with further information about affiliation, education, and other**

<!-- ### Education information

<!-- Harvesting of education information and upload to basic item in Wikidata: *not implemented yet*
   
