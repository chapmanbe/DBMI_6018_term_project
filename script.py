#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 19:12:19 2017

@author: Bennett

Script to run data analysis on mouse genome expression data
"""

import datetime as dt
import heat_map as hm
import pandas as pd
import read_excel as re
import seaborn as sns

# make instances of gene from rows of Excel sheet containing gene information
# =============================================================================
# get Excel workbook of gene data
gene_file = input("Enter address of Excel file with gene information.")
# read excel file with pandas
data = pd.read_excel(gene_file)
# check for correct file type?: P5 data, P15 data, or Adult data?
# could handle by requiring the workbook to have one sheet for each

# check for needed columns
# a list of needed input columns
columns = ["external_gene_id", "EnsembleID", "Chr", "Tissue", "Age",
           "MeanExpressionLevel_SNPAligningReads_CPM", "ra_value", "BCV",
           "rab_value_95%CI_LowerLimit",
           "rab_value_95%CI_UpperLimit"]
for c in columns:
    if c not in list(data.columns):  # if any needed column is not in the sheet
        raise ValueError("Excel sheet missing needed columns.")

if data.Age[0].lower() not in ["p5", "p15", "adult"]:
    raise ValueError("Age must be p5, p15, or adult.")

# make instances of gene from the rows of the data frame
genes = []
for _, r in data.iterrows():
    genes.append(re.make_instance(r))

# extract CI_width and AEE from instances and add to data frame
data_CIwidth = data.assign(CI_width=[i.CI_width for i in genes])
data_CIwidth_AEE = data.assign(AEE=[i.AEE for i in genes])

# output new excel file
end_file = input("Enter desired file name.")
data_CIwidth_AEE.to_excel(end_file+".xlsx", index=False)
# =============================================================================


# make a heat map
# =============================================================================
# ask the user if they want a heat map and get their file address
decision = input("If you want to make a heat map, enter y.")
if decision == "y":
    map_file = input("Enter address of Excel file with expression data.")

# make expression data frame for all ages
exp_df = hm.make_age_data(map_file)

# get input eIDs from user
eIDs = hm.input_genes()
# select those rows from the data frame
exp_subset = exp_df.loc[eIDs]

# ask the user for their choices
options = hm.get_options(exp_subset)
# make cluster map using user's choices
htm = sns.clustermap(exp_subset, row_cluster=True, col_cluster=False,
                     # apparently you need ticklabels with clustermap or else
                     # IndexError: list index out of range
                     yticklabels=["<--Genes"], xticklabels=["FPKM-->"],
                     # user's choices
                     col_colors=options["col_colors"],
                     cmap=options["cmap"],
                     figsize=options["figsize"])

# export heat map via savefig method
save = input("To save heat map, enter y.")
if save == "y":
    name = input("Enter desired file name.")
    htm.savefig(name+".png")

# add other heat map metadata to options
options["created"] = str(dt.datetime.today())
options["genes"] = eIDs
options["row_cluster"] = "True"
options["col_cluster"] = "False"
options["yticklabels"] = "<--Genes"
options["xticklabels"] = "FPKM-->"
# change col_colors to something readable by humans
options["col_colors"] = "P5 is red, P15 is blue, Adult is green."

# create file object by opening it in write mode
with open(name+"_metadata.txt", "w") as f:
    for item in options.items():
        f.write(str(item))  # write each item on one line
        f.write("\n")  # start a new line for the next item
# =============================================================================
