#!/usr/bin/env python
# coding: utf-8

import os
from os import walk
import pandas as pd
import numpy as np
import chardet

class MCQrecord():
    def __init__(self, record_filename, markscheme_filename, encoding):
        self.original_record = pd.read_csv(record_filename, header=None, dtype='object', encoding=encoding)
        self.ID = df.iloc[ 0,1]
        self.StudentName = df.iloc[ 1 , 1]
        self.markscheme = pd.read_csv(markscheme_filename, header=None, dtype='object')
        self.letter_choices = self.markscheme.iloc[0,4]
        self.markscheme = self.markscheme.iloc[2:, :3]
        self.record_filename = record_filename

    def extract(self):
        student_solutions = self.original_record.copy()
        thecolumns = student_solutions.iloc[3 , :]
        thecolumns.name = None
        student_solutions.columns = thecolumns
        self.student_solutions = student_solutions[4:14].set_index( "Question", drop=True)
        self.markscheme.columns = ["Question", "Correct Answer", "Allocated Marks"]
        self.markscheme.set_index("Question" , drop=True, inplace=True)

    def compute_mark(self):
        student_answers = {}
        number_of_answers_list = []
        for question_number in self.student_solutions.index:
            number_of_answers = 0
            for letter_choice in self.letter_choices:
                if self.student_solutions.loc[ question_number, letter_choice] in {'X', 'x'}:
                    student_answers[question_number] = letter_choice
                    number_of_answers += 1
                else:
                    pass
            number_of_answers_list.append(number_of_answers)
        if max(number_of_answers_list) >1 :
            self.check_this_one = 1
        else:
            self.check_this_one = 0
        student_answers = pd.DataFrame.from_dict(student_answers, orient='index', columns=["Student Answer"])
        student_answers.index.name = "Question"
        self.question_scores = pd.merge(self.markscheme , student_answers, on="Question")
        self.totalscore = ( np.array([  (self.question_scores["Student Answer"][item] in self.question_scores["Correct Answer"][item]) 
                                      for item in range(len(self.question_scores["Correct Answer"]))  ])  
                           * self.question_scores["Allocated Marks"].astype(float).to_numpy() ).sum()
        
        
    def process(self):
        self.extract()
        self.compute_mark()
        self.row =  pd.DataFrame.from_dict({"Student ID" : [self.ID], "Name" : [self.StudentName], "Mark" : [self.totalscore], "Check" : [self.check_this_one], "filename":[self.record_filename]})


for root, dirs, files in os.walk(os.getcwd()):
    if "markscheme.csv" in set(files):
        directory_name = root.split('/')[-1].replace("/","")
        outputfile_name = directory_name + "_MCQ_marks.csv"
        no_csv_extension = []
        csv_but_not_a_record = []
        student_mark_records = pd.DataFrame(columns = ["Student ID" , "Name", "Mark", "Check", "filename"])# empty dataframe
        for filename in set(files) - set("markscheme.csv"):  
            if filename.split('.')[-1]!="csv":
                no_csv_extension.append(filename)
            else:
                print(f"{directory_name}/{filename}")
                f = open(f"{directory_name}/{filename}", "rb").read()
                chardet_dict = chardet.detect(f)
                df = pd.read_csv(f"{directory_name}/{filename}", header=None, dtype='object', encoding=chardet_dict['encoding'])
                if df.iloc[0,0] != "Student ID:":
                    csv_but_not_a_record.append(filename)
                else:
                    record = MCQrecord(f"{directory_name}/{filename}", f"{directory_name}/markscheme.csv", chardet_dict['encoding'])
                    record.process()
                    student_mark_records = pd.concat([student_mark_records, record.row])

        with open(f"{directory_name}/no_csv_extension.csv", "w") as outfile:
            outfile.write("\n".join(no_csv_extension))
        with open(f"{directory_name}/csv_but_not_a_record.csv", "w") as outfile:
            outfile.write("\n".join(csv_but_not_a_record))
        student_mark_records.to_csv(f"{directory_name}/{outputfile_name}" , index=False)

    


# In[ ]:




