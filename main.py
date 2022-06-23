#!/usr/bin/env python
# coding: utf-8

import pandas as pd

from helper import replace_values, combine_subject_questions, create_bar_chart
from survey_questions import *


SURVEY_FILEPATH = "survey_results/GAME Post-Quals Survey (Jan 2022) (Responses).xlsx"
data = pd.read_excel(SURVEY_FILEPATH)
data = replace_values(data)

## Make subject exam #2 and #3 into extra entries making dataframe 3x long
data = combine_subject_questions(data)

for section in all_sections:
    ax = create_bar_chart(data, section.survey_questions, section.title, section.color_mapping, section.prefix, count_annotate=True)
