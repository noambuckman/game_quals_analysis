#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import os
import matplotlib.pyplot as plt
from helper import replace_values, combine_subject_questions, create_bar_chart, pivot_to_csv, agreement_strings_to_numbers
from survey_questions import *
import numpy as np
from argparse import ArgumentParser
from scipy.stats import ttest_ind


if __name__== "__main__":
    
    parser = ArgumentParser()
    parser.add_argument("--survey_file_name1", type=str, default="GAME Post-Quals Survey (Jan 2022) (Responses).xlsx", help="name of survey file")
    parser.add_argument("--survey_file_name2", type=str, default="GAME Post-Quals Survey (May 2022) (Responses).xlsx", help="name of survey file")

    parser.add_argument("--survey-dir", default="survey_results", type=str, help="Name of the dir that holds all the survey data")
    args = parser.parse_args()
    
    SURVEY_FILEPATH1 = os.path.join(args.survey_dir, args.survey_file_name1)
    survey_data1 = pd.read_excel(SURVEY_FILEPATH1)
    survey_data1 = replace_values(survey_data1)

    ## Make subject exam #2 and #3 into extra entries making dataframe 3x long
    survey_data1 = combine_subject_questions(survey_data1)
    survey_data1 = agreement_strings_to_numbers(survey_data1)
    survey_data1["QualName"] = "Jan2022"
    survey_data1 = survey_data1.replace("Not applicable", np.nan)

    SURVEY_FILEPATH2 = os.path.join(args.survey_dir, args.survey_file_name2)
    survey_data2 = pd.read_excel(SURVEY_FILEPATH2)
    survey_data2 = replace_values(survey_data2)
    
    ## Make subject exam #2 and #3 into extra entries making dataframe 3x long
    survey_data2 = combine_subject_questions(survey_data2)    
    survey_data2 = agreement_strings_to_numbers(survey_data2)
    survey_data2 = survey_data2.replace("Not applicable", np.nan)
    survey_data2["QualName"] = "May2022"

    survey_data_combined = pd.concat([survey_data1, survey_data2])

    
    for q in section_1_1.survey_questions:
        print(q)
        pop1 = survey_data1[q].dropna().to_numpy()
        
        pop2 = survey_data2[q].dropna().to_numpy()

        res = ttest_ind(pop1, pop2)
        print("T value: %.03f    P_Value %.03f"%(res.statistic, res.pvalue))
        # break
    # dept = args.out_dir
    # survey_data1 = survey_data1
    # for section in all_sections:
    #     ax = create_bar_chart(survey_data1, section.survey_questions, section.title, section.color_mapping, section.prefix, count_annotate=True)

    #     os.makedirs("%s_results/graphs/"%dept, exist_ok=True)
    #     plt.savefig("%s_results/graphs/%s_%s.png"%(dept, dept, section.title), facecolor='white', bbox_inches='tight', pad_inches=.1)
    #     plt.close()

    #     os.makedirs("%s_results/tables/"%dept, exist_ok=True)
    #     pivot_to_csv(survey_data1, section, dept)

    # #     plt.show()