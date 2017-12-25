#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 19:31:10 2017

@author: Bennett

Functions for making heat maps
"""


import pandas as pd
# import matplotlib.pyplot as plt


def make_age_data(file_address):
    """Input: Excel workbook with sheets of FPKM biological replicate data
       by age (P5, P15, and Adult)
       Output: Expression data for all ages in one data frame ready for
       seaborn clustermap"""

    # read in file with pandas
    xls = pd.ExcelFile(file_address)
    # extract each sheet
    P5 = pd.read_excel(xls, "Sheet1")
    P15 = pd.read_excel(xls, "Sheet2")
    Adult = pd.read_excel(xls, "Sheet3")

    # add the age to end of column names
    P5.columns = ["eID"]+[i+" P5" for i in list(P5.columns)[1:]]
    P15.columns = ["eID"]+[i+" P15" for i in list(P15.columns)[1:]]
    Adult.columns = ["eID"]+[i+" Ad" for i in list(Adult.columns)[1:]]

    # make data frame with FPKM data from each age
    all_exp = pd.merge(P5, P15, on="eID", how="outer")
    all_exp = pd.merge(all_exp, Adult, on="eID", how="outer")  # note this has nans
    all_exp.set_index("eID", inplace=True)

    # clustermap won't take nans, so replace them with 0
    no_nan = all_exp.fillna(value=0)
    # remove index name to make the heat map look nicer
    no_nan = no_nan.reindex(no_nan.index.rename(None))

    return no_nan


# a function that forces the user to input ensembleIDs (eIDs)
def input_genes():
    """Input: none
       Output: list of eIDs"""

    user_genes = input("Enter a list of eIDs.")
    if isinstance(user_genes, str):
        user_genes = user_genes.split()
    check = [g[:7] == "ENSMUSG" for g in user_genes]
    if False in check:
        print("Not eIDs.")
        input_genes()
    else:
        return user_genes

# create color "legend" (color bar) for FPKM columns by age
# not sure why this doesn't generate a color bar
# =============================================================================
# # create a 3 color palette, one color for each age
# age_pal = sns.light_palette('red', 3)
# # create a dictionary: key = column name, value = color
# age_pal_dict = {}
# for i in list(no_nan.columns):
#     if i.split()[2] == "P5":
#         age_pal_dict[i] = age_pal[0]
#     elif i.split()[2] == "P15":
#         age_pal_dict[i] = age_pal[1]
#     elif i.split()[2] == "Ad":
#         age_pal_dict[i] = age_pal[2]
# # map the colors to the series of the mice
# age_colors = pd.Series(list(no_nan.columns)).map(age_pal_dict)
# =============================================================================


# but the following does generate a color bar:
def age_color_bar(edf):
    """Input: expression data frame
       Output: list of colors by age corresponding to FPKM column"""

    col_list = list(edf.columns)
    five = [i for i in col_list if "P5" in i]
    fif = [i for i in col_list if "P15" in i]
    adult = [i for i in col_list if "Ad" in i]

    age_colors = ["r" for i in range(0, len(five))] + ["b" for i in range(0, len(fif))] + ["g" for i in range(0, len(adult))]

    return age_colors


# function to ask for heat map options
def get_options(edf):
    """Input: expression data frame
       Output: a dictionary of options when creating a seaborn clustermap"""
    choices = {}

    # get width and height for figure size
    width = None
    height = None
    while width is None:
        try:
            width = int(input("Enter width (in inches) for figure."))
        except ValueError:
            print("Not a number.")
    while height is None:
        try:
            height = int(input("Enter height (in inches) for figure."))
        except ValueError:
            print("Not a number.")
    # create figsize entry in options
    choices["figsize"] = (width, height)

    # get choice of color map
    cs = input("Enter color scheme: default, YlgnBu, RdBu_r, or BuGn_r.")
    while cs not in ["default", "YlgnBu", "RdBu_r", "BuGn_r"]:
        print("Not a possible choice.")
        cs = input("Enter color scheme: default, YlgnBu, RdBu_r, or BuGn_r.")
    # create color map entry in options
    choices["cmap"] = cs

    # ask to color bar for ages
    color_bar = input("Enter y to color FPKM columns by age.")
    if color_bar == "y":
        choices["col_colors"] = age_color_bar(edf)
    else:
        choices["col_colors"] = None

    # return options dictionary
    return choices


# not sure why these label the color bar instead of the plot
# =============================================================================
# plt.xlabel("FPKM biological replicates", fontsize=14)
# plt.ylabel("Genes", fontsize=14)
# =============================================================================
# consider help(htm.[tab]) to investigate methods
