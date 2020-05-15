# ORCID for Wikidata

This repository contains scripts to import authors with information about affiliation and education from [ORCID database] into [Wikidata]. Afterwards the author items can be connected to their scienctific articles in Wikidata.

[ORCID database]: https://orcid.org/
[Wikidata]: https://www.wikidata.org/

## Background

This work is part of the project *[Nachnutzung von strukturierten Daten aus Wikidata für bibliometrische Analysen](https://de.wikiversity.org/wiki/Wikiversity:Wikiversity:Fellow-Programm_Freies_Wissen/Einreichungen/Nachnutzung_von_strukturierten_Daten_aus_Wikidata_f%C3%BCr_bibliometrische_Analysen)*. During this project it turned out many researchers referenced in Wikidata by author name string ([P2093](https://www.wikidata.org/wiki/Property:P2093)) lack an item in Wikidata.

## Requirements

Scripts in this repository requiry Python 3 and [wikidata-cli]. To process ORCID dumps you need enough disk space and some time.

[wikidata-cli]: https://www.npmjs.com/package/wikidata-cli

## Usage

### Preparation

* **Download ORCID archives** at figshare,  eg. for 2019: https://orcid.figshare.com/articles/ORCID_Public_Data_File_2019/9988322/2 

### Basic author information

* Harvesting of basic author information and upload to Wikidata
 * **Harvest summaries** by using ORCID-summaries-harvesting.py for **ORCID, given name, family name** and **current affiliation** with  arg-statements for path of extracted ORCID-summaries.xml and output-csv  
      ./analysis/ORCID-summaries-harvesting.py orcid_summaries.xml orcid-researchers.csv

* **Perform duplication check** for items of researchers and **create basic items in Wikidata** using: wikidata-CLI.py 
the script uses Wikibase CLI internally. Download and informatin on Wikibase CLI can you find here: https://github.com/maxlath/wikibase-cli

   Besides "wd" as standard input for Wikibase CLI is needed, the scripts expects args-input for input-file (should be that one you created in step 2) and logging-file for note those items for researchers that had been created

      ./analysis/wikidata-CLI.py  orcid-researchers.csv logging.txt
   
### Affiliation history

* Harvesting of affiliation information and upload to basic item in Wikidata
* **Harvest affiliations** by using ORCID-affiliations-harvesting.py for **ORCID, affiliation name, affiliation adress, affiliation id for disambiguation** with args-statements for path of extracted ORCID-activities.xml and output-csv

      ./analysis/ORCID-affiliations-harvesting.py orcid_activities_1.xml orcid-affiliations_1.csv

* to be continued: upload script for **enrich basic items of researchers in Wikidata with further information about affiliation, education, and other**

### Publications

4. Harvest publications and matching publication items and author items in Wikidata  
**Harvest publications** by using ORCID-works-harvesting.py for **ORCID of author, title and subtitle of publication, ids of publication** with args-statements for path of extracted ORCID-activities.xml and output-csv

      ./analysis/ORCID-works-harvesting.py orcid_activities_1.xml orcid-publications_1.csv

 * upload script for **matching publications recoreded in Wikidata and ORCID of authors in order to establish connection between publications and authors.**

### Education information

Harvesting of education information and upload to basic item in Wikidata: *not implemented yet*

 
   
  
    
   
## License

All source code licensed under [ISC license](https://www.isc.org/downloads/software-support-policy/isc-license/)
