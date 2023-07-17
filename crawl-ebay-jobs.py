# Import required libraries
import pandas as pd
import re
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver


def fetch_job_details(post):
    """ Fetches job details from the post """
    try:
        titel = post.find("h2").text.strip()
    except Exception as e:
        titel = None
        print("Exception occurred while fetching 'titel':", e)

    try:
        titel_clean = post.find("h2").text.replace("(w/m/d)", "").replace("(m/w/d)", "").strip()
    except Exception as e:
        titel_clean = None
        print("Exception occurred while fetching 'titel clean':", e)

    try:
        descr = post.find("p", {"class": "aditem-main--middle--description"}).text.split(",")[0].strip()
    except Exception as e:
        descr = None
        print("Exception occurred while fetching 'descr':", e)

    try:
        company = post.find("p", {"class": "aditem-main--middle--description"}).text.split(",")[1].strip()
    except Exception as e:
        company = None
        print("Exception occurred while fetching 'company':", e)

    try:
        city = post.find("div", {"class": "aditem-main--top--left"}).text.strip()
    except Exception as e:
        city = None
        print("Exception occurred while fetching 'city':", e)

    try:
        date = post.find("div", {"class": "aditem-main--top--right"}).text.strip()
    except Exception as e:
        date = None
        print("Exception occurred while fetching 'date':", e)

    jobd = {
        "titel": titel,
        "titel clean": titel_clean,
        "descr": descr,
        "company": company,
        "city": city,
        "date": date
    }
    jobd["titel"]=jobd["titel"].replace(jobd["company"],"").replace("()","").strip()
    jobd["titel clean"]=jobd["titel clean"].replace(jobd["company"],"").replace("()","").strip()
    
    return jobd

def text_clean_up(jobList):
    """ Cleans up the text for textual analysis """
    jobList=jobList.replace("(","").replace("(m/wd)","").replace("(m/w/divers)","").replace("m w d","").replace(" m ","").replace(" w ","")
    chars = {'ö':'oe','ä':'ae','ü':'ue'} # usw.
    for char in chars:
        jobList = jobList.replace(char,chars[char])
    jobList=re.sub('[^A-Za-z0-9]+', ' ', jobList)
    jobList=jobList.replace(" m w ","").replace("w m x","").replace("w m d","").replace("mwd","").replace("f m d","")
    return jobList

def save_to_excel(all_counts):
    """ Saves the ngrams result to an excel file """
    res2Gram=[]
    for el in all_counts.most_common(9999):
        res2Gram.append({
            "job":re.sub('[^A-Za-z]+', ' ',  " ".join(sorted(el[0]))) ,
            "count":el[1]
        })
    pd.DataFrame(res2Gram).groupby(["job"]).sum().sort_values(["count"]).to_excel("Jobs ngram.xlsx")


# Configure and start the ChromeDriver
driver = webdriver.Chrome(ChromeDriverManager().install())

# Fetch webpage
driver.get("https://www.ebay-kleinanzeigen.de/pro/heyjobs?pageNum="+str(0))

# Accept cookies if prompted
try:
    cookie = driver.find_element("xpath",'//*[@id="gdpr-banner-accept"]/span/span')
    cookie.click()
except:
    pass

# Initialize jobs list
jobs=[]
for num in range(0,5):
    # Get page with jobs list
    r=driver.get("https://www.ebay-kleinanzeigen.de/pro/heyjobs?pageNum="+str(num))
    # Create a Beautiful Soup object to parse the page HTML
    soup=BeautifulSoup(driver.execute_script("return document.body.innerHTML;"),"lxml")

    # Scrape each job listing on the page
    for post in soup.find_all("li",{"class":"ad-listitem"}):
        # Clean up and process job listing details
        pattern = re.compile(r'\n+')
        sentence = re.sub(pattern, '\n', post.text)
        job=[el.strip() for el in sentence.split("\n") if len(el)>0]
        jobd = fetch_job_details(post)
        jobs.append(jobd)
    print(num)

# Create a DataFrame from the jobs list
jobDF=pd.DataFrame(jobs)

# Export the DataFrame to an Excel file
jobDF.to_excel("Ebay Jobs.xlsx")

# Simple Textual Analysis
jobList = " ".join(jobDF["titel clean"].values).lower()
jobList = text_clean_up(jobList)

# Textual analysis with ngrams
from nltk import ngrams, FreqDist
from nltk.tokenize import sent_tokenize, word_tokenize
all_counts = dict()
for size in 2, 3, 4, 5:
    all_counts[size] = FreqDist(ngrams(word_tokenize(jobList), size))

# Save results to excel
save_to_excel(all_counts[2])

# Display results
print(all_counts[2].most_common(9999))

