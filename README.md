# ORCID for Wikidata

This repository contains scripts to import authors with information about affiliation and education from [ORCID database] into [Wikidata]. Afterwards the author items can be connected to their scienctific articles in Wikidata.

[ORCID database]: https://orcid.org/
[Wikidata]: https://www.wikidata.org/

## Background

This work is part of the project *[Nachnutzung von strukturierten Daten aus Wikidata für bibliometrische Analysen](https://de.wikiversity.org/wiki/Wikiversity:Wikiversity:Fellow-Programm_Freies_Wissen/Einreichungen/Nachnutzung_von_strukturierten_Daten_aus_Wikidata_f%C3%BCr_bibliometrische_Analysen)*.  
Although we find a lot of scientific articles in Wikidata (actually 31,5% (Jan 2020 see Wikidata-statistics)), most of the publications are not connected with an author item. In order to allocate researchers and articles we like to introduce information on researchers from ORCID. 

As a first step we harvest articles with PMID and DOI listed in ORCID. Second, we request Wikidata Public API for existing items of articles in Wikidata. Only for already existing publications we import basic author items, if there is no item already. If there is an author item we enhanche information registered in wikidata. One of those information is the qualifier "is author of an publication" (wdt:P50) annotated with the PMID and/or DOI. By this the matching of authors and publications is fullfilled. 



## Requirements

Scripts in this repository requiry 

* Python 3
* Python libraries listed in `requirements.txt` (install with `pip3 install -r requirements.txt`)
* [wikibase-edit]

To process full ORCID dumps you also need enough disk space and some time.

[wikibase-edit]: https://www.npmjs.com/package/wikibase-edit

## Usage

### Preparation

Download the ORCID database dump (see <https://orcid.org/content/orcid-public-data-file-use-policy>), e.g. <https://doi.org/10.23640/07243.9988322.v2> for October 2019. You do not need to unpack the  tar.gz-archive. Besides the multiple _activities_-files containing information on works, affiliation, education, fundings, memberships etc. of the regirsterd researchers only a single meta-file contains the basic information on the researchers called _summaries_. 

### 1. Harvest publication-IDs in ORCID

With ORCID-ids-harvesting.py you **harvest PMID, PMC, DOI, WOS-ID, DNB and author ORCID from the ORCID.tar.gz archive**.
With adding the ORCID.tar.gz path as input-file and an output file:

     ./analysis/ORCID-ids-harvesting.py ORCID_2019_activities_1.tar.gz ORCID-ids_1.csv

...you get a csv like this: 

| orcid | pmid | pmc | doi | wosuid | eid | dnb |
|----|:----:|:----:|:----:|:----:|:----:|----:|
| 0000-0003-2760-1191 | | | 10.1111/j.1540-8175.2010.01316.x | | 2-s2.0-79952755968 | |
| 0000-0001-9154-8191 | 26093915 | PMC4491368 | 10.1007/s10482-015-0502-7 | | | |
| 0000-0002-8639-5191 | |  | 10.1111/J.1747-4949.2007.00119.X | WOS:000247202000017 | | |


**From ORCID_2019_activites_1.tar.gz we retrieved 3 804 784 4publications indicated by PMID, PMC, DOI, WOS-id, Scopus-ID, DNB. From ORCID_2019_activites_2.tar.gz we retrieved 3 752 394 publications indicated by these IDs.**

Then we check if those articles are already listed in Wikidata.



*******************************
### 2. Check for existing publication-items in Wikidata

Afterwards we can **check if those articles indicated with PMID, PMC, DOI, Scopus ID (eid) and/or DNB are listed in Wikidata** applying check-ids-in-wd.py. Use it like this: 
     
     ./analysis/check-IDs-in-wikidata.py ORCID-ids_1.csv available-articles-in-wd_1.csv 

Use the file you just created in the last step as input-file!
As output-file you get information like this: 

| orcid | pmid | pmc | doi | eid | dnb | article-qnr|
|----|:-----:|:-----:|:-----:|:-----:|:-----:|-----:|
| 0000-0002-7499-1391 | 17147832 | nan | 10.1186/1471-2458-6-293 | 000242933800001 | 2-s2.0-33845506869 | Q33265524 |
| 0000-0002-7499-1391 | 8478144 | nan | nan | nan | 2-s2.0-0027309495 | Q70670731 |
| 0000-0002-2255-0391 | 28583742 | PMC5478201 | 10.1016/j.ebiom.2017.04.029 | nan | nan | Q29571127 |

The Web of Science-ID (wosuid) is not supported by Wikidata yet and can not be used for retrieval. 

If we check in Wikidata we see these Q-Nrs refer to:

[Q70670731](https://www.wikidata.org/wiki/Q70670731)  "Calcium intake and 28-year gastro-intestinal cancer mortality in Dutch civil servants"
 
[Q29571127](https://www.wikidata.org/wiki/Q29571127)  "Visual and Motor Deficits in Grown-up Mice with Congenital Zika Virus Infection" 


Of 2 785 993 identified publications **from ORCID_2019_activites_1.tar.gz we found 457 417 Wikidata-items** of scientific papers identified by PMID, PMC, DOI, Scopus-ID (eid) and DNB. Applying only PMID and DOI in a former check, we had been able to detected only 751 Wikidata-items. Of 2 742 008 publications identified with PMID and DOI **from ORCID_2019_activites_2.tar.gz we retrieved 1 560 items in Wikidata by PMID and DOI**. The relatively small quantity of items detected could also be related to the poor performance of the public API for large query volumns. 



*******************************
### 3. Check for existing author items of publications in Wikidata 

Take the file we produced in step 2. containig all the publications listed in Wikidata indicated by an existing Q-Nr. 
For every article-Q-Nr we request the public Wikidata-API if there is already an author indicated.  

     ./analysis/check-authors-of-available-articles.py available-articles-in-wd_1.csv available-articles-available-authors_1.csv

| orcid_origin | pmid | doi | article_qnr | all_authors_qnr |
|----|:---:|:----:|:----:|----:|
| 0000-0001-8724-3942 | 20530968.0 | 10.1159/000315458 | Q33597585 | "['Q42798270', 'Q43055649', 'Q43055657', 'Q64764410'] |
| 0000-0001-8724-3942 | 19258708.0 | 10.1159/000206635 | Q43481032 | "['Q37828665', 'Q41111247', 'Q42798270', 'Q43055649', 'Q53203014', 'Q64495393']" |
| 0000-0001-8724-3942 | 23435897.0 | 10.1128/AEM.03207-12 | Q39761768 | "['Q16733372', 'Q42798270']" |
| 0000-0001-8724-3942 | 16415592.0 | 10.1159/000089647 | Q36369661 | "['Q42798270', 'Q43055649']" |


For 134 843 articles from ORCID_2019_activites_1.tar.gz we identified registered authors.

In the previous step we had been able to deteced 457 417 papers listed in Wikidata. **322 574 articles-items currently not connected to their authors can be improved with data enrichment based on ORCID only for ORCID_2019_activites_1.tar.gz.**  


****************

### 4. Harvest author-information in ORCID
In order to match the publications-items in Wikidata with their author-items we prepare a set of basic information containing ORCID, name and current affiliation. The script ORCID-author-infos-harvesting.py harvests the basic informations from ORCID_year_summaries.tar.gz archive. 

     ./analysis/ORCID-author-infos-harvesting.py ORCID_2019_summaries.tar.gz ORCID-author-infos.csv
     
..this delivers content like:

| orcid | given_name | family_name | affiliation | affiliation_id | affiliation_id_source | start_date_year|
|----|:---:|:----:|:----:|:----:|:----:|----:|
| 0000-0002-4807-379X | 'Esha' | 'Kundu' | 'Curtin University', '1649', 'RINGGOLD', '2019' |
| 0000-0002-8182-679X | 'Alla' | None | 'Pavlo Tychyna Uman State Pedagogical University' |  '416526' | 'RINGGOLD' | '1971' |
| 0000-0002-1792-079X | 'Cilene' | 'Canda' | 'Universidade Federal da Bahia' | '28111' | 'RINGGOLD' | '2015' |
| 0000-0003-0554-179X | 'Shinya' | 'Ariyasu' | 'Nagoya University' | 'http://dx.doi.org/10.13039/501100004823' | 'FUNDREF' | '2016' |

**From the ORCID_summaries_2019.tar.gz archive we retrieved basic information on 673 058 researchers.**


*******************

### 5. Check for existing author-items in Wikidata for complete number of ORCID-authors

Analogue to the check for existing Q-Nr for publication-items in Wikidata, we also check for existing author-items. Applying the just poduced file we request the public Wikidata-API for items containig the given ORCID (wdt:P496) or names as alias (skos:altLabel) or label (rdfs:label).

     ./analysis/check-author-in-wikidata.py ORCID-author-infos.csv available-authors-in-wd.csv
     
Here we get: 

| author_qnr| orcid | given_name | family_name | affiliation | affiliation_id | affiliation_id_source | start_date_year|
|----|:---:|:----:|:----:|:----:|:----:|:----:|----:|
| 59151132 | 0000-0003-1808-679X | 'Marek' | 'Radkowski' | 'Medical University of Warsaw' |  'grid.13339.3b' | 'GRID' | '1986' | nan | nan | nan | nan |
| Q54452584 | 0000-0002-0171-879X | 'Barbara' | 'van Asch'| 'Stellenbosch University | '26697' | 'RINGGOLD' | '2015'| nan | nan | nan | nan |
| Q61110015 | 0000-0002-7844-079X | 'Janika' | 'Nättinen' | 'Tampere University' | 'grid.5509.9' | 'GRID' | '2014' | nan | nan | nan | nan |
| Q60042671 | 0000-0001-9494-179X | 'Georgios' | 'Dimitriadis' | 'University of California Santa Cruz' | '8787' | 'RINGGOLD' | '2017' | nan | nan | nan | nan |

**of 673 058 authors listed in ORCID_2019_summaries.tar.gz we detected 134 843 authors registered in Wikidata.



******************************
### 6. Register missing authors in Wikidata-article-items

Via Wikibase-CLI we retrieve the json files of article items. We check the P50 qualifier for listed authors and add the missing ones applying our prepared data from step 3. 




*******************
### 7. Create author-items for not existing authors of publications listed in Wikidata

In order to pepare for matching publication-items and author-items in the following we create the author-items in Wikidata that are not existing yet. 




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
   
