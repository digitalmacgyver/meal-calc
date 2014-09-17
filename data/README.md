Food Nutrition Data
===================

This is the raw data, in ```gzip``` compressed form, from:

US Department of Agriculture, Agricultural Research Service, Nutrient
Data Laboratory.  USDA Nutrient Database for Standard Reference,
Release 27.  Version Current: August 2014. Internet:
[http://www.ars.usda.gov/ba/bhnrc/ndl]

To prepare the data for import into our database using our
```populate.py``` utility, we:

* Converted it to UNIX style newlines using the ```dos2unix``` utility.
* Edited the NUTR_DEF.txt file and replaced the ISO/IEC 8859-1 (Latin 1) encoded micro symbol with the ASCII u character.

