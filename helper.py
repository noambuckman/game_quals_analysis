#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from survey_questions import get_label
from textwrap import wrap
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)


SURVEY_FILEPATH = "survey_results/GAME Post-Quals Survey (Jan 2022) (Responses).xlsx"
data = pd.read_excel(SURVEY_FILEPATH)

def replace_values(df):

    df = df.replace("Strongly disagree (1)", "Strongly disagree")
    df = df.replace(1, "Strongly disagree")
    df = df.replace(2, 'Somewhat disagree')
    df = df.replace(3, 'Neither agree nor disagree')
    df = df.replace(4, 'Somewhat agree')
    df = df.replace(5, "Strongly agree")
    df = df.replace("Strongly agree (5)", 'Strongly agree')

    return df

def agreement_strings_to_numbers(df):
    df = df.replace("Strongly disagree", 1)
    df = df.replace('Somewhat disagree', 2)
    df = df.replace('Neither agree nor disagree', 3)
    df = df.replace('Somewhat agree', 4)
    df = df.replace("Strongly agree", 5)
    return df

def combine_subject_questions(data):
    data1 = pd.DataFrame(data=None, columns=data.columns, index=data.index)
    data2 = pd.DataFrame(data=None, columns=data.columns, index=data.index)
    data1.iloc[:,40:59] = data.iloc[:, 59:78].values
    data2.iloc[:,40:59] = data.iloc[:, 78:97].values
    data_concat = pd.concat((data, data1, data2))

    return data_concat     
data = replace_values(data)

## Make subject exam #2 and #3 into extra entries making dataframe 3x long
data = combine_subject_questions(data)




def generate_pivot_table(column):
    
    pivot_table = column.value_counts()
    
    total_count = pivot_table.sum()
    
    pivot_table["percentage"] = pivot_table/total_count

    return pivot_table

def generate_array(data, section_questions, color_mapping, ):
    ordered_values = list(color_mapping.keys())
    n_questions = len(section_questions)
    n_values = len(ordered_values)
    arr = np.zeros((n_questions,n_values))
    arr_counts = np.zeros((n_questions, n_values))
    counts = []
    for ci, column in enumerate(data[section_questions]):
        pt = generate_pivot_table(data[section_questions][column])


        for i in range(arr.shape[1]):
            try:
                arr_counts[ci,i] = pt[ordered_values[i]]                    
                arr[ci,i] = pt["percentage"][ordered_values[i]]                    
            except KeyError:
                arr[ci,i] = 0.00
        # renormalize
        percentage_sum = arr[ci,:].sum()
        arr[ci,:] = arr[ci,:]/percentage_sum
        counts += [data[column].value_counts().sum()]

    return arr, arr_counts, counts


def sort_by_agreement(pivot_array, pivot_array_counts, counts, section_questions):
    sorted_questions_idx = np.argsort(np.sum(pivot_array[:,0:2], axis=1))
    
    sorted_questions = list(np.array(section_questions)[sorted_questions_idx])
    sorted_counts = list(np.array(counts)[sorted_questions_idx])
    
    sorted_array = pivot_array[sorted_questions_idx, :]
    sorted_array_counts = pivot_array_counts[sorted_questions_idx, :]
    return sorted_array, sorted_array_counts, sorted_questions, sorted_counts, sorted_questions_idx

def split_ylabel_over_rows(label):
    max_row_length = 20
    # if len(label) <= max_row_length:
    #     return label


    new_label = ""
    string_to_split = label
    while len(string_to_split) > 0:
        if len(string_to_split) <= max_row_length:
            new_label += string_to_split
            return new_label

        location_to_split = max_row_length
        while (string_to_split[location_to_split] != " " and string_to_split[location_to_split] != "/") and location_to_split>0:
            location_to_split -= 1
        if string_to_split[location_to_split] == "/":
            location_to_split += 1
        if location_to_split == 0:
            location_to_split = max_row_length
        new_label += string_to_split[:location_to_split] + '\n'
        string_to_split = string_to_split[location_to_split:]
    return new_label

def create_bar_chart(data, section_questions, title, color_mapping, prefix, count_annotate=False):
    import matplotlib.patches as patches

    ordered_values = list(color_mapping.keys())

    pivot_array, pivot_array_counts, counts = generate_array(data, section_questions, color_mapping)
    
    sorted_array, sorted_array_counts, sorted_questions, sorted_counts, sorted_idxs = sort_by_agreement(pivot_array, pivot_array_counts, counts, section_questions)
    
    
    df2 = pd.DataFrame(sorted_array, columns=ordered_values)

    clean_question_labels = [get_label(q) for q in sorted_questions]
    clean_question_labels = [split_ylabel_over_rows(l) for l in clean_question_labels ]

    ax = df2.plot.barh(stacked=True, color = list(color_mapping.values()), figsize=(16, 12))
    for p in ax.patches:
        if p.get_width()< 0.05:
            d = 50
            y_offset = np.random.uniform(-.10, .10)
        else:
            d = 0
            y_offset = 0
        #Add percentages
        if p.get_width() > 0.00001:
            if not count_annotate:                
                ax.annotate('%.0f%%'%(100*p.get_width()), (p.get_x() * 1.005 + p.get_width()*0.4, p.get_y() + p.get_height()* .3 + y_offset), rotation=d)
            # else:
            #     ax.annotate('%.0f%%'%(100*p.get_width()), (p.get_x() * 1.005 + p.get_width()*0.4, p.get_y() + p.get_height()* .3 + y_offset), rotation=d)

    if count_annotate:
        for i in range(sorted_array_counts.shape[0]):
            for j in range(sorted_array_counts.shape[1]):
                if sorted_array_counts[i,j] > 0:
                    ax.annotate("%d"%sorted_array_counts[i,j], (np.sum(sorted_array[i,:j])+0.5*sorted_array[i,j], i))

    for i in range(len(sorted_counts)):
        ax.annotate("%d"%sorted_counts[i], (1.0, i))

        if sorted_counts[i] <= 5:
            box_patch = patches.Rectangle((0.00, i-p.get_height()/2.0), 1.0, p.get_height(), color='white', fill=True, facecolor="white", zorder=100)
            ax.text(0.5, i, "$\leq 5$ Responses", ha="center", va="center", bbox=dict(boxstyle="square", fc="white", ec="k", lw=2), zorder=101)
            ax.add_patch(box_patch)
    
    ax.set_xlabel("Percentage Respondents")
    # ax.set_ylabel("Questions")
    fig = plt.gcf()
    fig.set_size_inches(11, 8.5)
    fig.suptitle(title, x=0, y=1.0, ha='left')
    # ax.set_ylabel('\n'.join(wrap(prefix, 20)),  weight='bold', loc="top", rotation=0, x=0.0)
    ax.yaxis.set_label_coords(0, 1.0)    


    ax.set_yticklabels(clean_question_labels)
    ax.set_axisbelow(True)
    ax.set_xticks([0.0, 0.25, 0.5, .75, 1.0], )
    ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"])

    ax.xaxis.set_minor_locator(MultipleLocator(.125))

    ax.grid(which='major', axis='x', linestyle='-')
    ax.grid(which='minor', axis='x', linestyle='-')
    
    ax.set_xlim([0.0, 1.05])
    ax.legend(loc='lower left', bbox_to_anchor=(0.05, 1.01), ncol=len(ordered_values))    
    return ax




def pivot_to_csv(dept_data, section, dept_name ):
    import csv
    arr, arr_count, total_count = generate_array(dept_data, section.survey_questions, section.color_mapping)
    
    
    csv_name = "%s_results/tables/%s_%s.csv"%(dept_name, dept_name, section.title)
    
    
    
    with open(csv_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')

        first_row = ["Value"] + section.survey_questions
        writer.writerow(first_row)
        values = list(section.color_mapping.keys())

        for i in range(len(values)):
            list_of_values = list(arr_count[:,i].astype(int))
            list_of_values = [list_of_values[j] if total_count[j]>=5 else "n/a" for j in range(len(list_of_values))]
#                 list_of_values[i] = "n/a"
            writer.writerow([values[i]] + list_of_values)

        writer.writerow(["Count"] + total_count)
        