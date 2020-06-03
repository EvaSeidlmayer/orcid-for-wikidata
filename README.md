# ORCID for Wikidata

This repository contains scripts to import authors with information about affiliation and education from [ORCID database] into [Wikidata]. Afterwards the author items can be connected to their scienctific articles in Wikidata.

[ORCID database]: https://orcid.org/
[Wikidata]: https://www.wikidata.org/

## Background

This work is part of the project *[Nachnutzung von strukturierten Daten aus Wikidata für bibliometrische Analysen](https://de.wikiversity.org/wiki/Wikiversity:Wikiversity:Fellow-Programm_Freies_Wissen/Einreichungen/Nachnutzung_von_strukturierten_Daten_aus_Wikidata_f%C3%BCr_bibliometrische_Analysen)*. During this project it turned out that many researchers are referenced in Wikidata by author name string ([P2093](https://www.wikidata.org/wiki/Property:P2093)) only but lack an item in Wikidata for disambiguation.

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
