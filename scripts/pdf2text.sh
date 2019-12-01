#!/bin/sh

SRC_DIR=data/collected
DEST_DIR=data/collected/pdftotext

mkdir -p ${DEST_DIR}

find ${SRC_DIR} -name *.pdf | while read -r pdfname; do
    txtname=${DEST_DIR}/$(basename $pdfname).txt
    echo "pdftotext ${pdfname} -layout - > ${txtname}"
    pdftotext ${pdfname} -layout - > ${txtname}
done

