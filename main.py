
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from helper import *
from survey_questions import *


for section in all_sections:
    ax = create_bar_chart(data, section.survey_questions, section.title, section.color_mapping, section.prefix, count_annotate=True)
