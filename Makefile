.DEFAULT_GOAL := help
.PHONY : clean help

SQLIZED_DB=data/white_house_salaries.sqlite

CONVERTED_FILES = data/converted/2012.csv \
		         data/converted/2013.csv \
		         data/converted/2014.csv \
		         data/converted/2015.csv \
		         data/converted/2016.csv \
				 data/converted/2017.csv \
				 data/converted/2018.csv \
				 data/converted/2019.csv


HANDCLEANED_FILES = data/collected/handcleaned/2017.txt \
				    data/collected/handcleaned/2018.txt \
				    data/collected/handcleaned/2019.txt



COLLECTED_FILES = data/collected/originals/2012.csv \
					$(COLLECTED_ZIPS) \
					$(COLLECTED_PDFS)


COLLECTED_ZIPS = data/collected/2013.zip \
		         data/collected/2014.zip \
		         data/collected/2015.zip \
		         data/collected/2016.zip

COLLECTED_PDFS = data/collected/2017.pdf \
				 data/collected/2018.pdf \
				 data/collected/2019.pdf





help:
	@echo 'Under construction!'


ALL: clean sqlize

clean:
	rm -rf data/converted
	rm -rf data/fused
	rm -rf data/wrangled
	rm -f $(SQLIZED_DB)

sqlize: $(SQLIZED_DB)

$(SQLIZED_DB): wrangle
	sqlite3 $@ < scripts/sqlize.sql

	@echo -----------
	@echo $@

## wrangled data
wrangle: data/wrangled/white_house_salaries.csv

data/wrangled/white_house_salaries.csv: fuse
	./whsa/wrangle.py

#### fused data
fuse: data/fused/white_house_salaries.csv

data/fused/white_house_salaries.csv: convert
	./whsa/fuse.py


convert: convert_zips convert_pdftexts
	# 2012 is already a CSV, so we just copy it over
	cp data/collected/2012.csv data/converted/2012.csv


convert_zips: $(COLLECTED_ZIPS)
	./whsa/convert/zip2csv.py

convert_pdftexts: $(HANDCLEANED_FILES)
	./whsa/convert/pdftext2csv.py


# These tasks are only used to inform/warn the user that the
# data/collected/handcleaned files are expected to be *newer* than the corresponding files
# from which they derive from in data/collected/pdftotext
#
# Not much else to do except thrown an error

data/collected/handcleaned/%.txt: data/collected/pdftotext/%.pdf.txt
	@echo "Warning: $@"
	@echo " is expected to be newer than, i.e. derived from:"
	@echo "\t $?"
	@echo "\nRead data/handcleaned.log.yaml for more details"
	@exit 1


# Like the collect task, this is a task that really shouldn't be re-run
# because the next steps in the data transformation are dependent on
#  files in data/collected/handcleaned, which are manually produced, by hand
#  from data/collected/pdftotext. Thus, this task only exists as documentation,
#  showing how the PDFs in data/collected were turned into data/collected/pdftotext/*.txt

pdftotexts: $(COLLECTED_PDFS)
	./scripts/pdf2text.sh



# note that this collect_data.py script, by default,
#   will not overwrite existing files.
# In fact, you probably shouldn't ever re-fetch the data anew, assuming
#   that the historical PDFs and ZIP files aren't being updated...
collect: ./whsa/collect_data.py
	./whsa/collect_data.py

