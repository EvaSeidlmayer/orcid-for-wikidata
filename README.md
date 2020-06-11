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

### Check for existing articles in Wikidata

With ORCID-PMID-DOI-harvesting.py you **harvest PMID, DOI and author ORCID from the ORCID.tar.gz archive**.
With adding the ORCID.tar.gz path as input-file and an output file:

     ./analysis/ORCID-PMID-DOI-harvesting.py ORCID_2019_activities_1.tar.gz ORCID-PMID-DOI_activities-1.csv

...you get a csv like this: 

| orcid | pmid | doi |
|----|:----:|----:|
| 0000-0002-3406-2942| |10.21914/anziamj.v56i0.9343 |
| 0000-0002-3406-2942 | |10.1051/mmnp/2018047 |


Afterwards we can **check if those articles indicated with PMID and/or DOI are listed in Wikidata** applying check-PMID-DOI-in-wd.py. Use it like this: 
     
     ./analysis/check-PMID-DOI-in-wd.py ORCID-PMID-DOI_activities-1.csv available-articles-in-wd-1.csv 

Use the file you just created in the step before as input-file!
As output-file you get information like this: 

| orcid | pmid | doi | qnr|
|----|:-----:|-----:|
| 0000-0003-3891-0942 | 20504363 | 10.1186/1758-3284-2-12 | Q33931069 |
| 0000-0003-4898-3942 | nan | 10.1016/S0924-9338(13)76302-8 | Q59191594 |

If we check we see these Q-Nr refer to:
"Sustained response of carcinoma ex pleomorphic adenoma treated with trastuzumab and capecitabine" (Q33931069) 
"Executive functions, visuoconstructive ability and memory in institutionalized elderly" (Q59191594) 



### Basic author information

First **harvest author summaries** from extracted `orcid_summaries.xml` with **ORCID, given name, family name, current affiliation (including its start date)** written as CSV:

     ./analysis/ORCID-summaries-harvesting.py orcid_summaries.xml orcid_summaries.csv

An short example CSV file is given in directory `data`.

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

 
   
  
    
   
## License

All source code licensed under [ISC license](https://www.isc.org/downloads/software-support-policy/isc-license/)
