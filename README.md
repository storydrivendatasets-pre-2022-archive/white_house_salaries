# White House Salaries

This repo contains the code and data for compiling White House salaries from 2012 through 2019.

The wrangled data can be found at: [data/wrangled/white_house_salaries.csv](data/wrangled/white_house_salaries.csv). 

You can also preview the [data interactively in this Google Sheets copy](https://docs.google.com/spreadsheets/d/1dVjbdr7PzsmJ36WemlXWyZ2h-xuO9d0S7BFPzdIEvYI/edit#gid=0)


Besides compiling the multiyear dataset into a single file, the wrangled data has a few extra convenience fields:

- `president` to make it easier to pivot by administration
- the `name` field is parsed into `last_name`, `first_name`, `middle_name`, and `suffix`

A pivot summary of the data so far:

| Row Labels  |  employees   | Average salary | Total salaries|
| ----------- | ------------ | ---------------| ------------- |
| 2012        |          468 |       80,843   |    37,834,589 |
| 2013        |          460 |       82,303   |    37,859,780 |
| 2014        |          456 |       82,844   |    37,776,925 |
| 2015        |          474 |       84,864   |    40,225,595 |
| 2016        |          472 |       84,223   |    39,753,551 |
| 2017        |          377 |       94,872   |    35,766,744 |
| 2018        |          374 |       94,246   |    35,248,194 |
| 2019        |          418 |       98,766   |    41,284,244 |
| Total       |        3,499 |       87,382   |   305,749,622 |



# Inventory


The list of original data URLs and their corresponding years can be found in [data/stashed/filelist.csv](data/stashed/filelist.csv).

For safekeeping the original files are kept in [data/stashed/originals](data/stashed/originals).


## Scripts and code

All the code (mostly Python 3.x scripts) used to organize and wrangle the data can be found in the [whsal/](whsal/) subdirectory:

- [whsal/stash](whsal/stash) contains the **stash phase**: Fetching and storing the data, and doing the steps needed to get it from zip->csv and pdf->csv. Very little transformation if any




## About PDFs and CSVs

The Trump White House has chosen to publish its salaries list as PDF – you can see this in the 2017.pdf, 2018.pdf, and 2019.pdf files in [data/stashed/originals](data/stashed/originals). Converting the PDF documents into usable CSV data was by far the hardest and time-consuming part of this mini-project.

In [data/stashed/originals/abbyy](data/stashed/originals/abbyy), you can see my attempts to use ABBYY FineReader, which in the past has been my go-to tool (maybe the only commercial data tool I pay for). It did quite badly. Not only (understandably) making mistakes when trying to figure out the tabular layout, but also producing OCR-quality (i.e. **bad**) text, despite the PDFs being native text documents.

I then tried [tabula](https://github.com/tabulapdf/tabula-java), which is a solid tool but I haven't used much in the past because of ABBYY. It did a good job as expected in getting the text out, but when skimming the results, I saw more table-structure-mistakes than I wanted to deal with. 

I ended up using `pdftotext -layout`, a hacky trick [I used back in the Dollars for Docs days](https://www.propublica.org/nerds/turning-pdfs-to-text-doc-dollars-guide). Surprisingly, it worked very well, and seems to have correctly parsed all but ~15 of ~3500 rows. 

In [stashed/handcleaned](stashed/handcleaned) are the hand-cleaned text files for the pdf files for years 2017 through 2019. This handcleaned version of the data is what the rest of the data-processing pipeline uses, e.g. [whsal/stash/pdftotext_to_csv.py](whsal/stash/pdftotext_to_csv.py). Though I do keep the straight-from-pdftotext versions for comparison and double-checking: [data/originals/pdftotext](data/originals/pdftotext)

