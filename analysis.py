import pandas as pd
import matplotlib.pyplot as plt
import time
import numpy as np
from survey_questions import get_label


agreement_color_mapping = {
    "Strongly disagree": (1.0, 0.5, 0.0, 1.0),
    "Somewhat disagree": (1.0, 0.5, 0.0, 0.5),
    "Neither agree nor disagree": (211/255, 211/255, 211/255, 0.5),
    "Somewhat agree": (44/255, 130/255, 201/255, 0.5),
    "Strongly agree": (44/255, 130/255, 201/255, 1.0),   
}
agreement_color_mapping = {
    1: (1.0, 0.5, 0.0, 1.0),
    2: (1.0, 0.5, 0.0, 0.5),
    3: (211/255, 211/255, 211/255, 0.5),
    4: (44/255, 130/255, 201/255, 0.5),
    5: (44/255, 130/255, 201/255, 1.0),   
}
ordered_values = ["Strongly disagree", "Somewhat disagree", "Neither agree nor disagree", "Somewhat agree", "Strongly agree"]
ordered_values = [1, 2, 3, 4, 5]

def replace_values(df):

    df = df.replace("Strongly disagree (1)", 1)
    df = df.replace("Strongly agree (5)", 5)
    

    return df


def generate_pivot_table(column):
    
    pivot_table = column.value_counts()
    
    total_count = pivot_table.sum()
    
    pivot_table["percentage"] = pivot_table/total_count 
    return pivot_table

def generate_array(data, section_questions):

    n_questions = len(section_questions)
    arr = np.zeros((n_questions,5))
    counts = []
    for ci, column in enumerate(data[section_questions]):
        pt = generate_pivot_table(data[section_questions][column])

        for i in range(arr.shape[1]):
            try:
                arr[ci,i] = pt["percentage"][ordered_values[i]]
            except KeyError:
                arr[ci,i] = 0.00
        counts += [data[column].value_counts().sum()]

    return arr, counts    

def sort_by_agreement(pivot_array, counts, section_questions):
    sorted_questions_idx = np.argsort(np.sum(pivot_array[:,0:2], axis=1))
    
    sorted_questions = list(np.array(section_questions)[sorted_questions_idx])
    sorted_counts = list(np.array(counts)[sorted_questions_idx])
    
    sorted_array = pivot_array[sorted_questions_idx, :]
    
    return sorted_array, sorted_questions, sorted_counts, sorted_questions_idx

def create_bar_chart(data, section_questions, title):

    pivot_array, counts = generate_array(data, section_questions)
    
    sorted_array, sorted_questions, sorted_counts, sorted_idxs = sort_by_agreement(pivot_array, counts, section_questions)
    
    
    df2 = pd.DataFrame(sorted_array, columns=ordered_values)

    ax = df2.plot.barh(stacked=True, color = list(agreement_color_mapping.values()), figsize=(12, 4))
    for p in ax.patches:
        if p.get_width()< 0.05:
            d = 50
        else:
            d = 0
        ax.annotate('%d%%'%(100*p.get_width()), (p.get_x() * 1.005 + p.get_width()*0.4, p.get_y() + p.get_height()* .3), rotation=d)

    for i in range(len(sorted_counts)):
        ax.annotate("%d"%sorted_counts[i], (1.0, i))
    
    ax.set_xlabel("Percentage Respondants")
    # ax.set_ylabel("Questions")
    clean_question_labels = [get_label(q) for q in sorted_questions]
#     ax.set_title(title, loc="left")
    ax.set_yticklabels(clean_question_labels)
    ax.set_ylabel(title, loc="top", rotation=0, x=0)
    ax.set_xlim([0.0, 1.1])
    ax.legend(bbox_to_anchor=(0.01, 1.01), ncol=5)    
    return ax

if __name__=="__main__":
    SURVEY_FILEPATH = "survey_results/GAME Post-Quals Survey (Jan 2022) (Responses).xlsx"

    df = pd.read_excel(SURVEY_FILEPATH)
    df = replace_values(df)
    print(df.columns)


    question = 'To what extent do you agree or disagree with the following statements: [The virtual format had a negative impact on my ability to study with others.]'
    print(df[question])
    print(df[question].value_counts())
    y = df[question].value_counts()
    print(y[1])

    create_bar_chart(df, [question], "")

