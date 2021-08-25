#!/bin/bash

iconv -f iso-8859-1 -t utf-8 < PCD_OA_LSOA_MSOA_LAD_AUG21_UK_LU.csv > PCD_utf-8.csv
cat PCD_utf-8.csv | csvcut -c pcds,oa11cd,lsoa11cd,msoa11cd,ladcd,lsoa11nm,msoa11nm,ladnm,ladnmw > postcode_lookup.csv
