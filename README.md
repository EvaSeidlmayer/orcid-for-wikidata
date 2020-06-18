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

Download the ORCID database dump (see <https://orcid.org/content/orcid-public-data-file-use-policy>), e.g. <https://doi.org/10.23640/07243.9988322.v2> for October 2019.

### Harvest publication-IDs in ORCID

With ORCID-PMID-DOI-harvesting.py you **harvest PMID, DOI and author ORCID from the ORCID.tar.gz archive**.
With adding the ORCID.tar.gz path as input-file and an output file:

     ./analysis/ORCID-PMID-DOI-harvesting.py ORCID_2019_activities_1.tar.gz ORCID-PMID-DOI_activities-1.csv

...you get a csv like this: 

| orcid | pmid | doi |
|----|:----:|----:|
| 0000-0002-3406-2942| |10.21914/anziamj.v56i0.9343 |
| 0000-0002-3406-2942 | |10.1051/mmnp/2018047 |

From ORCID_2019_activites_2.tar.gz we retrieved 2 742 008 publications indicated by PMID and DOI.
From ORCID_2019_activites_1.tar.gz we retrieved 2 785 993 publications indicated by PMID and DOI.

Check for existing articles in Wikidata

### Check for existing publication-items in Wikidata

Afterwards we can **check if those articles indicated with PMID and/or DOI are listed in Wikidata** applying check-PMID-DOI-in-wd.py. Use it like this: 
     
     ./analysis/check-PMID-DOI-in-wd.py ORCID-PMID-DOI_activities-1.csv available-articles-in-wd-1.csv 

Use the file you just created in the last step as input-file!
As output-file you get information like this: 

| orcid | pmid | doi | qnr|
|----|:-----:|:-----:|-----:|
| 0000-0003-3891-0942 | 20504363 | 10.1186/1758-3284-2-12 | Q33931069 |
| 0000-0003-4898-3942 | nan | 10.1016/S0924-9338(13)76302-8 | Q59191594 |

If we check in Wikidata we see these Q-Nrs refer to:

[Q33931069](https://www.wikidata.org/wiki/Q33931069)  "Sustained response of carcinoma ex pleomorphic adenoma treated with trastuzumab and capecitabine" 

 [Q59191594](https://www.wikidata.org/wiki/Q59191594)  "Executive functions, visuoconstructive ability and memory in institutionalized elderly"

**Of 2 742 008 publications identified with PMID and DOI from ORCID_2019_activites_2.tar.gz we retrieved 1 560 items in Wikidata. Of 2 785 993 identified publications from ORCID_2019_activites_1.tar.gz we we found 751 Wikidata-items.** The relatively small quantity of items detached could also be related to the poor performance of the public API for large query volumns. 



### Harvest author-information in ORCID

The script ORCID-author-infos-harvesting.py we harvest basic informations  as name and affiliation from ORCID_year_summaries.tar.gz archive. 

     ./analysis/ORCID-author-infos-harvesting.py ORCID_2019_summaries.tar.gz ORCID-author-infos.csv
     
..this delivers:

| orcid | given_name | family_name | affiliation | affiliation_id | affiliation_id_source | start_date_year|
|----|:---:|:----:|:----:|:----:|:----:|----:|
| 0000-0002-4807-379X | 'Esha' | 'Kundu' | 'Curtin University', '1649', 'RINGGOLD', '2019' |
| 0000-0002-8182-679X | 'Alla' | None | 'Pavlo Tychyna Uman State Pedagogical University' |  '416526' | 'RINGGOLD' | '1971' |
| 0000-0002-1792-079X | 'Cilene' | 'Canda' | 'Universidade Federal da Bahia' | '28111' | 'RINGGOLD' | '2015' |
| 0000-0003-0554-179X | 'Shinya' | 'Ariyasu' | 'Nagoya University' | 'http://dx.doi.org/10.13039/501100004823' | 'FUNDREF' | '2016' |


### Check for existing author-items in Wikidata

Analogue to the check for existing Q-Nr for publication-items in Wikidata, we also check for existing author-items. Applying the just poduced file we request the public Wikidata-API for items containig the given ORCID (wdt:P496) or names as alias (skos:altLabel) or label (rdfs:label).

     ./analysis/check-author-in-wikidata.py ORCID-author-infos.csv available-authors-in-wd.csv
     
Here we get: 

| author_qnr| orcid | given_name | family_name | affiliation | affiliation_id | affiliation_id_source | start_date_year|
|----|:---:|:----:|:----:|:----:|:----:|:----:|----:|
| 59151132 | 0000-0003-1808-679X | 'Marek' | 'Radkowski' | 'Medical University of Warsaw' |  'grid.13339.3b' | 'GRID' | '1986' | nan | nan | nan | nan |
| Q54452584 | 0000-0002-0171-879X | 'Barbara' | 'van Asch'| 'Stellenbosch University | '26697' | 'RINGGOLD' | '2015'| nan | nan | nan | nan |
| Q61110015 | 0000-0002-7844-079X | 'Janika' | 'Nättinen' | 'Tampere University' | 'grid.5509.9' | 'GRID' | '2014' | nan | nan | nan | nan |
| Q60042671 | 0000-0001-9494-179X | 'Georgios' | 'Dimitriadis' | 'University of California Santa Cruz' | '8787' | 'RINGGOLD' | '2017' | nan | nan | nan | nan |


'''

### Basic author information

Then use the author summaries to create Wikidata items for missing authors, based on an ORCID dump of given year:

    ./analysis/create-author-items.py orcid_summaries.csv logfile.txt 2019

To avoid creation of duplicates, a new item is only created if no Wikidata item of a person (Q5) exists with the same ORCID identifier or with the same (as label or alias). Add option `--dry` to never add new items and in addition option `--quiet` to only emit what would be added to Wikidata. Otherwise the script calls [wikidata-cli] for write-access to Wikidata.
   
### Affiliation history

* Harvesting of affiliation information and upload to basic item in Wikidata
* **Harvest affiliations** by using ORCID-affiliations-harvesting.py for **ORCID, affiliation name, affiliation adress, affiliation id for disambiguation** with args-statements for path of extracted ORCID-activities.xml and output-csv

      ./analysis/ORCID-affiliations-harvesting.py orcid_activities_1.xml orcid-affiliations_1.csv

* to be continued: upload script for **enrich basic items of researchers in Wikidata with further information about affiliation, education, and other**

### Publications

Harvest publications and matching publication items and author items in Wikidata  

**Harvest publications** by using ORCID-works-harvesting.py for **ORCID of author, title and subtitle of publication, ids of publication** with args-statements for path of extracted ORCID-activities.xml and output-csv

      ./analysis/ORCID-works-harvesting.py orcid_activities_1.xml orcid-publications_1.csv

* upload script for **matching publications recoreded in Wikidata and ORCID of authors in order to establish connection between publications and authors.**

### Education information

Harvesting of education information and upload to basic item in Wikidata: *not implemented yet*

'''
  
    
   
## License

All source code licensed under [ISC license](https://www.isc.org/downloads/software-support-policy/isc-license/)
