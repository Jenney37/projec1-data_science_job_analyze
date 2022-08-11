# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 09:32:36 2020
author: Kenarapfaik
url: https://github.com/arapfaik/scraping-glassdoor-selenium
"""
import selenium
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from sklearn.metrics import average_precision_score



def get_jobs(keyword, num_jobs, verbose, slp_time):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    
    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')
    
    #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path='/Users/liminzhenscc/Documents/study/python_data_analyze/project/2data_sc_salary/chromedriver', options=options)
    driver.set_window_size(1120, 1000)
    
    url = 'https://www.glassdoor.com.au/Job/data-science-jobs-SRCH_KO0,12.htm'
    #url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword="+keyword+"&sc.keyword="+keyword+"&locT=&locId=&jobType="
    #url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="' + keyword + '"&locT=C&locId=1147401&locKeyword=San%20Francisco,%20CA&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
        
    
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.

        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(slp_time)

        #Test for the "Sign Up" prompt and get rid of it.
        # try:
        #     driver.find_element(By.CLASS_NAME, "selected").click()
        # except ElementClickInterceptedException:
        #     pass

        # time.sleep(.1)



        print('------put items in list-------')
        #Going through each job in this page
        job_buttons = driver.find_elements(By.CLASS_NAME,"react-job-listing")  #jl for Job Listing. These are the buttons we're going to click.
        print('item number is:', len(job_buttons))
         


        i=0
        for job_button in job_buttons:  

            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break
            
            if len(jobs)>1100:
                df = pd.DataFrame(jobs)
                df.to_csv('/Users/liminzhenscc/Documents/study/python_data_analyze/project/2data_sc_salary/glassdoor_jobs.csv', index = False)

            job_button.click()  #You might 
            try:
                driver.find_element(By.CLASS_NAME, 'modal_closeIcon').click() #clicking to the X.  #class="SVGInline modal_closeIcon"
                print(' x out worked')
            except NoSuchElementException:
                print(' x out failed')
                pass
            time.sleep(1)



            collected_successfully = False
            try:
                driver.find_element(By.XPATH, './/div[@class="css-t3xrds e856ufb2"]').click()#click see more to show all content
            except NoSuchElementException:
                pass

            while not collected_successfully:
                try:
                    company_name = driver.find_element(By.XPATH, './/div[@class="css-xuk5ye e1tk4kwz5"]').text
                    print(company_name)

                    location = driver.find_element(By.XPATH, './/div[@class="css-56kyx5 e1tk4kwz1"]').text
           
                    job_title = driver.find_element(By.XPATH, './/div[@class="css-1j389vi e1tk4kwz2"]').text

                    container = driver.find_element(By.XPATH, './/div[@class="p-std css-1k5huso e856ufb7"]')
                    job_description = container.text
                    # print(len(jd))
                    # job_description=''
                    # for i in range(len(jd)):

                    #     job_description = job_description+jd[i].text
                    #     print(job_description, i)
                    collected_successfully = True
                    
                except:
                    time.sleep(5)

            try:
                
                salary_estimate = driver.find_element(By.XPATH, './/span[@data-test="detailSalary"]').text
                print('salary collected')
            except NoSuchElementException:
                salary_estimate = -1 #You need to set a "not found value. It's important."
                print('salary not found')
            
            try:
                ave_salary = driver.find_element(By.XPATH, './/div[@class="css-y2jiyn e2u4hf18"]').text
                print('ave_salary collected')
            except NoSuchElementException:
                salary_estimate = -1 #You need to set a "not found value. It's important."
                print('ave_salary not found')

            try:
                rating = driver.find_element(By.XPATH, './/span[@data-test="detailRating"]').text
                print('rating found')
            except NoSuchElementException:
                rating = -1 #You need to set a "not found value. It's important."

            #Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Average salary: {}".format(ave_salary))
                print("Job Description: {}".format(job_description[:500]))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))

            #Going to the Company tab...
            #clicking on this:
            #<div class="tab" data-tab-type="overview"><span>Company</span></div>


            # try:
            #     driver.find_element(By.XPATH, './/div[@class="tab" and @data-tab-type="overview"]').click()

                # try:
                #     #<div class="infoEntity">
                #     #    <label>Headquarters</label>
                #     #    <span class="value">San Francisco, CA</span>
                #     #</div>
                #     headquarters = driver.find_element(By.XPATH, './/div[@class="infoEntity"]//label[text()="Headquarters"]//following-sibling::*').text
                # except NoSuchElementException:
                #     headquarters = -1


            columns = ['Size', 'Founded', 'Type', 'Industry', 'Sector', 'Revenue']

            try:
                key_ls = driver.find_elements(By.CSS_SELECTOR, ".css-1pldt9b.e1pvx6aw1")
                value_ls = driver.find_elements(By.CSS_SELECTOR, ".css-1ff36h2.e1pvx6aw0")

                print('find company information:-------')
                
                inf_dic = {}
                if len(key_ls) > 0:
                    for i in range(len(key_ls)):
                        inf_dic[str(key_ls[i].text)] = value_ls[i].text

                    keys =  list(inf_dic.keys())#list the keys that collected in this page about company information
                    print(keys)
                    for item in columns:
                        print(item)
                        if item not in keys:
                            inf_dic[item] = -1
                        else:
                            pass

                    print(inf_dic)
                else:
                    for item in columns:
                        inf_dic[item] = -1
            except NoSuchElementException: 
                    for item in columns:
                        inf_dic[item] = -1
            
            
            # try:
            #     size = driver.find_elements(By.CSS_SELECTOR, ".css-1ff36h2.e1pvx6aw0")[0].text
            # except NoSuchElementException:
            #     size = -1


            # try:
            #     founded = driver.find_elements(By.CSS_SELECTOR,  ".css-1ff36h2.e1pvx6aw0")[1].text
            # except NoSuchElementException:
            #     founded = -1

            # try:
            #     type_of_ownership = driver.find_element(By.CSS_SELECTOR,  ".css-1ff36h2.e1pvx6aw0")[2].text
            # except NoSuchElementException:
            #     type_of_ownership = -1

            # try:
            #     industry = driver.find_element(By.CSS_SELECTOR,  ".css-1ff36h2.e1pvx6aw0")[3].text
            # except NoSuchElementException:
            #     industry = -1

            # try:
            #     sector = driver.find_element(By.CSS_SELECTOR,  ".css-1ff36h2.e1pvx6aw0")[4].text
            # except NoSuchElementException:
            #     sector = -1

            # try:
            #     revenue = driver.find_element(By.CSS_SELECTOR,  ".css-1ff36h2.e1pvx6aw0")[5].text
            # except NoSuchElementException:
            #     revenue = -1

            # try:
            #     competitors = driver.find_element(By.XPATH, './/div[@class="infoEntity"]//label[text()="Competitors"]//following-sibling::*').text
            # except NoSuchElementException:
            #     competitors = -1

            # except NoSuchElementException:  #Rarely, some job postings do not have the "Company" tab.
            #     headquarters = -1
            #     size = -1
            #     founded = -1
            #     type_of_ownership = -1
            #     industry = -1
            #     sector = -1
            #     revenue = -1
            #     competitors = -1

                
            if verbose:
                #print("Headquarters: {}".format(headquarters))
                print("Size: {}".format(inf_dic['Size']))
                print("Founded: {}".format(inf_dic['Founded']))
                print("Type: {}".format(inf_dic['Type']))
                print("Industry: {}".format(inf_dic['Industry']))
                print("Sector: {}".format(inf_dic['Sector']))
                print("Revenue: {}".format(inf_dic['Revenue']))
                # print("Competitors: {}".format(competitors))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({"Job Title" : job_title,
            "Salary Estimate" : salary_estimate,
            "Average Salary" : ave_salary,
            "Job Description" : job_description,
            "Rating" : rating,
            "Company Name" : company_name,
            "Location" : location,
            #"Headquarters" : headquarters,
            "Size" : inf_dic['Size'],
            "Founded" : inf_dic['Founded'],
            "Type of ownership" : inf_dic['Type'],
            "Industry" : inf_dic['Industry'],
            "Sector" : inf_dic['Sector'],
            "Revenue" : inf_dic['Revenue'],
            # "Competitors" : competitors
            })
            #add job to jobs
            
            
        #Clicking on the "next page" button
        try:
            driver.find_element(By.CLASS_NAME, 'nextButton').click()

        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

        # df = pd.DataFrame(jobs)
        # df.to_csv('/Users/liminzhenscc/Documents/study/python_data_analyze/project/2data_sc_salary/glassdoor_jobs.csv', index = False)
    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.