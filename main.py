#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import os
import matplotlib.pyplot as plt
from helper import replace_values, combine_subject_questions, create_bar_chart, pivot_to_csv
from survey_questions import *

from argparse import ArgumentParser


if __name__== "__main__":
    
    parser = ArgumentParser()
    parser.add_argument("--survey_file_name", type=str, default="GAME Post-Quals Survey (Jan 2022) (Responses).xlsx", help="name of survey file")
    parser.add_argument("--survey-dir", default="survey_results", type=str, help="Name of the dir that holds all the survey data")
    parser.add_argument("--out-dir", type=str, default="Jan2022")
    args = parser.parse_args()
    
    SURVEY_FILEPATH = os.path.join(args.survey_dir, args.survey_file_name)
    print(SURVEY_FILEPATH)

    data = pd.read_excel(SURVEY_FILEPATH)
    data = replace_values(data)

    ## Make subject exam #2 and #3 into extra entries making dataframe 3x long
    data = combine_subject_questions(data)

    for section in all_sections:
        ax = create_bar_chart(data, section.survey_questions, section.title, section.color_mapping, section.prefix, count_annotate=True)


    # dept_data = data[data["What is your academic department?"] == dept]
    # dept="Jan2022"
    dept = args.out_dir
    dept_data = data
    for section in all_sections:
        ax = create_bar_chart(dept_data, section.survey_questions, section.title, section.color_mapping, section.prefix, count_annotate=True)

    #     fig = plt.gcf()
    #     ax.legend(loc='best')
        os.makedirs("%s_results/graphs/"%dept, exist_ok=True)

        plt.savefig("%s_results/graphs/%s_%s.png"%(dept, dept, section.title), facecolor='white', bbox_inches='tight', pad_inches=.1)
        plt.close()

        os.makedirs("%s_results/tables/"%dept, exist_ok=True)
        pivot_to_csv(dept_data, section, dept)

    #     plt.show()