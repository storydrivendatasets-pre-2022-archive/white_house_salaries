.DEFAULT_GOAL := help
.PHONY : clean help

ORG_STASHES = data/stashed/originals/2012.csv \
		         data/stashed/originals/2013.zip \
		         data/stashed/originals/2014.zip \
		         data/stashed/originals/2015.zip \
		         data/stashed/originals/2016.zip \
				 data/stashed/handcleaned/2017.txt \
				 data/stashed/handcleaned/2018.txt \
				 data/stashed/handcleaned/2019.txt

PROCESSED_STASHES = data/stashed/processed/2012.csv \
		         data/stashed/processed/2013.csv \
		         data/stashed/processed/2014.csv \
		         data/stashed/processed/2015.csv \
		         data/stashed/processed/2016.csv \
				 data/stashed/processed/2017.csv \
				 data/stashed/processed/2018.csv \
				 data/stashed/processed/2019.csv


help:
	@echo 'Under construction!'


clean:
	rm -rf data/stashed/processed


## wrangled data
wrangle: data/wrangled/white_house_salaries.csv

data/wrangled/white_house_salaries.csv: collate

#### collated data
collate: data/collated/white_house_salaries.csv

data/collated/white_house_salaries.csv: process


#### processed files
process: $(PROCESSED_STASHES)


$(PROCESSED_STASHES): $(ORG_STASHES)
	@echo "Processing stashed originals and sources..."
	mkdir -p data/stashed/processed
	# handle 2012
	cp data/stashed/originals/2012.csv data/stashed/processed/2012.csv

	# handle 2013-2016
	./whsal/stash/zip_to_csv.py

	# handle 2017-2019
	./whsal/stash/pdftotext_to_csv.py
