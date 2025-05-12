import subprocess
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import re
import numpy as np
import os

# Install required dependencies via pip
subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4"])

# Setup Chrome options for headless execution in Colab or other environments without GUI
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# List to hold the URLs of the course catalog pages
links = [] 
pages = 27  #Number of pages in the W&M course catalog 
for i in range(1, pages+1): 
    links.append(f"https://catalog.wm.edu/content.php?catoid=30&catoid=30&navoid=4698&filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1&filter%5Bcpage%5D={i}#acalog_template_course_filter")

# List to store all course data
all_courses_data = []
page = 0 #page counter for status tracking
for i in links: 
    course_preview_links = [] # List to store course preview links on each page
    page += 1

    # Initialize the Chrome driver for scraping
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(i)

        # Wait for the course listings to load and extract preview links
        course_elements = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr td.width a[href*='preview_course_nopop.php']"))
        )
        
         # Extract preview links for each course
        for course_link_element in course_elements:
            href = course_link_element.get_attribute('href')
            course_preview_links.append(href)

        # Iterate through each preview link and scrape data
        for link in course_preview_links:
            try:
                driver.get(link)
                time.sleep(1)  # Give the page time to load
                soup = BeautifulSoup(driver.page_source, 'html.parser')

                 # Extract course title, credits, prerequisites, corequisites, etc.
                title_element = soup.select_one('#course_preview_title')
                credits_label = soup.find('em', string='Credits:')
                prerequisite_element = soup.find('em', string='Prerequisite(s):')
                coreq_element = soup.find('em', string='Corequisite(s):')
                prereq_coreq_element = soup.find('em', string='Prereq/Corequisite(s):')
                coll_curriculum_element = soup.find('em', string='College Curriculum:')
                domain_anchored_element = soup.find('em', string=re.compile(r'Domain \(Anchored\):\s*'))
                #domain_reaching_element = soup.find('em', string=re.compile(r'Domain \(Reaching Out\):\s*'))
                additional_domain_element = soup.find('em', string=re.compile(r'Additional Domain \(if applicable\):\s*'))
               
                 # Extract course code (if available)
                course_code = None
                if title_element and title_element.text:
                    title_text = title_element.text.strip()
                    # Just split on the first dash
                    # if ' - ' in title_text:
                    #     course_code = title_text.split(" - ", 1)[0].strip()
                    parts = re.split(r'\s*[-–—]\s*', title_text)
                    if len(parts) >= 2:
                        course_code = parts[0].strip()
                    else:
                        print(f"Warning: No dash found in '{title_text}'")
                 
                 # Extract credits (if available)
                credits = None
                if credits_label:
                    credits_em = credits_label.find_next('em')
                    if credits_em:
                        credits_text = credits_em.text.strip('() ')
                        if credits_text.isdigit():
                            credits = int(credits_text)

                # Extract prerequisites and logic (if available)
                prerequisites = []
                if prerequisite_element:
                    for a_tag in prerequisite_element.find_all_next('a'):
                        prerequisites.append(a_tag.text.strip())

                if prerequisite_element:
                    logic_keywords = []
                    #Capture logic between 'and' and 'or' if present
                    for sibling in prerequisite_element.find_next_siblings():
                        if isinstance(sibling, str):
                            cleaned_text = sibling.strip().lower()
                            if cleaned_text == 'or':
                                logic_keywords.append('or')
                            elif cleaned_text == 'and':
                                logic_keywords.append('and')
                        elif sibling.name == 'a':
                            pass # Ignore the prerequisite course links themselves
                     
                     # Determine logic type for prerequisites
                    if 'and' in logic_keywords and 'or' in logic_keywords:
                        prereq_logic =  'mixed'
                    elif 'and' in logic_keywords:
                        prereq_logic = 'and'
                    elif 'or' in logic_keywords:
                        prereq_logic = 'or'
                    else:
                        prereq_logic = 'none'  # Or potentially 'single' if there's one prereq without logic

                else:
                    prereq_logic = None # No prerequisite section found


                if prereq_coreq_element:
                    for a_tag in prereq_coreq_element.find_all_next('a'):
                        prerequisites.append(a_tag.text.strip())

                # Remove duplicates if needed
                prerequisites = list(set(prerequisites))

                # Extract corequisites (if available)
                coreqs = [] 
                if coreq_element: 
                    for a_tag in coreq_element.find_all_next('a'):
                        coreqs.append(a_tag.text.strip())

                # Extract curriculum (if available)
                coll = None
                if coll_curriculum_element:
                    sibling_text = coll_curriculum_element.find_next_sibling(text=True)
                    if sibling_text:
                        coll = sibling_text.strip()

                # Extract domain information (if available)
                domains = []
                if domain_anchored_element and domain_anchored_element.next_sibling:
                    anchored = domain_anchored_element.next_sibling.strip()
                    if anchored:
                        domains.append(anchored)


                if additional_domain_element and additional_domain_element.next_sibling:
                    additional = additional_domain_element.next_sibling.strip()
                    if additional: 
                        domains.append(additional)

                 # Compile all course data into a dictionary
                course_data = {
                    "course_code": course_code,
                    "credits": credits,
                    "prereqs": prerequisites,
                    "logic" : prereq_logic,
                    "coreqs": coreqs,
                    "coll": coll,
                    "domain": domains,
                }
                all_courses_data.append(course_data)   # Append the course data to the main list

            except Exception as inner_e:
                print(f"Error scraping data from {link}: {inner_e}")

    except Exception as outer_e:
        print(f"An error occurred: {outer_e}")

    finally: # Ensure the driver is quit after processing each page
        if 'driver' in locals() and driver is not None:
            driver.quit()

     # Create directory for storing data if it doesn't exist
    os.makedirs("data", exist_ok=True)
     
     # Save all scraped course data to a .npy file
    np.save(os.path.join("data", 'course_catalog.npy'), all_courses_data)
    print(f"Page {page} done!")

print(str(len(all_courses_data)))


