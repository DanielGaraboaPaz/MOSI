#!/bin/bash
echo "-> Running test for CMEMS download..."
echo "..."
python -m MOSI -j ./CMEMS_template.json -s CMEMS

echo "-> Running test for a THREDDS download..."
echo "..."
python -m MOSI -j ./THREDDS_file_template.json -s THREDDS

echo "-> Running test for a CDS donwload ..."
echo "..."
python -m MOSI -j ./CDS_template.json -s CDS
