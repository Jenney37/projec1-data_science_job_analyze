# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 11:47:44 2020
@author: Ken
"""

import glassdoor_scraper as gs 
import pandas as pd 

#path = "/Users/liminzhenscc/Documents/study/python_data_analyze/project/2data_sc_salary/chromedriver"

df = gs.get_jobs('data science',2000, False, 15)

df.to_csv('/Users/liminzhenscc/Documents/study/python_data_analyze/project/2data_sc_salary/glassdoor_jobs.csv', index = False)