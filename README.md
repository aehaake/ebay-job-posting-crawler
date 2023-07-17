# Job Scrapper and Textual Analysis

This project is a Python script to scrape job listings from ebay-kleinanzeigen.de, perform some textual analysis, and save the results to an Excel file. It might be usefull to conduct a analysis about job posting activities of a business competitor.

## ⚠️ Disclaimer / Warning!
This repository/project is intended for Educational Purposes ONLY.
The project and corresponding python script should not be used for any purpose other than learning. Please do not use it for any other reason than to learn about webscrapping. Make sure you adhere to the terms and conditions of the site!

## Description

The script uses Selenium and BeautifulSoup to scrape job listings and extract relevant details such as job title, description, company, city, and date. This data is cleaned and organized into a pandas DataFrame.

The script also performs an examplatory simple textual analysis on the job titles, specifically it uses n-grams to examine common phrases in the job titles. The n-grams results are then saved to an Excel file.

## Installation

First, clone the repository:

```bash
git clone https://github.com/aehaake/ebay-job-posting-crawler.git
```

Then, navigate to the project directory:

```bash
cd ebay-job-posting-crawler
```

Next, create a virtual environment (optional):

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Finally, install the requirements:

```bash
pip install -r requirements.txt
```

## Usage
Change the code of a job search. In this example all job postings made by heyjobs are listed.
Run the script using the following command:

```bash
python crawl-ebay-jobs.py
```

## License

This project is licensed under the terms of the MIT license.

