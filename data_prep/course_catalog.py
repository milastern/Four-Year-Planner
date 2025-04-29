import subprocess
import sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4"])

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


# Setup Chrome options for headless execution in Colab
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
links = [] 
pages = 27 
for i in range(1, pages+1): 
    links.append(f"https://catalog.wm.edu/content.php?catoid=30&catoid=30&navoid=4698&filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1&filter%5Bcpage%5D={i}#acalog_template_course_filter")
all_courses_data = []
page = 0 
for i in links: 
    course_preview_links = []
    page += 1
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(i)

        # Wait for the course listings to load and extract preview links
        course_elements = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr td.width a[href*='preview_course_nopop.php']"))
        )
        for course_link_element in course_elements:
            href = course_link_element.get_attribute('href')
            course_preview_links.append(href)

        # Iterate through each preview link and scrape data
        for link in course_preview_links:
            try:
                driver.get(link)
                time.sleep(1)  # Give the page time to load
                soup = BeautifulSoup(driver.page_source, 'html.parser')

                title_element = soup.select_one('#course_preview_title')
                credits_label = soup.find('em', string='Credits:')
                prerequisite_element = soup.find('em', string='Prerequisite(s):')
                coreq_element = soup.find('em', string='Corequisite(s):')
                prereq_coreq_element = soup.find('em', string='Prereq/Corequisite(s):')
                coll_curriculum_element = soup.find('em', string='College Curriculum:')
                domain_anchored_element = soup.find('em', string=re.compile(r'Domain \(Anchored\):\s*'))
                #domain_reaching_element = soup.find('em', string=re.compile(r'Domain \(Reaching Out\):\s*'))
                additional_domain_element = soup.find('em', string=re.compile(r'Additional Domain \(if applicable\):\s*'))
               

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

                credits = None
                if credits_label:
                    credits_em = credits_label.find_next('em')
                    if credits_em:
                        credits_text = credits_em.text.strip('() ')
                        if credits_text.isdigit():
                            credits = int(credits_text)

                prerequisites = []
                if prerequisite_element:
                    for a_tag in prerequisite_element.find_all_next('a'):
                        prerequisites.append(a_tag.text.strip())

                if prereq_coreq_element:
                    for a_tag in prereq_coreq_element.find_all_next('a'):
                        prerequisites.append(a_tag.text.strip())

                # Remove duplicates if needed
                prerequisites = list(set(prerequisites))

                coreqs = [] 
                if coreq_element: 
                    for a_tag in coreq_element.find_all_next('a'):
                        coreqs.append(a_tag.text.strip())


                coll = None
                if coll_curriculum_element:
                    sibling_text = coll_curriculum_element.find_next_sibling(text=True)
                    if sibling_text:
                        coll = sibling_text.strip()

                domains = []
                if domain_anchored_element and domain_anchored_element.next_sibling:
                    anchored = domain_anchored_element.next_sibling.strip()
                    if anchored:
                        domains.append(anchored)

                # if domain_reaching_element and domain_reaching_element.next_sibling:
                #     reaching = domain_reaching_element.next_sibling.strip()
                #     if reaching:
                #         domains.append(reaching)

                if additional_domain_element and additional_domain_element.next_sibling:
                    additional = additional_domain_element.next_sibling.strip()
                    if additional: 
                        domains.append(additional)

                course_data = {
                    "course_code": course_code,
                    "credits": credits,
                    "prereqs": prerequisites,
                    "coreqs": coreqs,
                    "coll": coll,
                    "domain": domains,
                }
                all_courses_data.append(course_data)
            except Exception as inner_e:
                print(f"Error scraping data from {link}: {inner_e}")

    except Exception as outer_e:
        print(f"An error occurred: {outer_e}")

    finally:
        if 'driver' in locals() and driver is not None:
            driver.quit()

    os.makedirs("data", exist_ok=True)
    np.save(os.path.join("data", 'course_catalog.npy'), all_courses_data)
    print(f"Page {page} done!")

print(str(len(all_courses_data)))


