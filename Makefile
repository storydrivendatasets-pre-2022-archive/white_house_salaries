.DEFAULT_GOAL := help

SOURCE_STASHES = data/stashed/originals/2012.csv \
		         data/stashed/originals/2013.zip \
		         data/stashed/originals/2014.zip \
		         data/stashed/originals/2015.zip \
		         data/stashed/originals/2016.zip \
				 data/stashed/handcleaned/2017.txt \
				 data/stashed/handcleaned/2018.txt \
				 data/stashed/handcleaned/2019.txt

help:
	@echo 'Under construction!'




## processed files

data/stashed/processed: $(SOURCE_STASHES)
	@echo "Processing stashed originals and sources..."

data/stashed/processed/2012.csv: data/stashed/originals/2012.csv

	cp $< $@
