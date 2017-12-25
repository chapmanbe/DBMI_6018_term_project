#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 19:27:42 2017

@author: Bennett

Functions to parse Excel sheet of gene information
"""


import gene_class as gc  # import the gene class


# makes an instance of gene from a row in the data frame
def make_instance(row):
    """Input: row of a gene data frame
       Output: instance of gene class"""
    row["EnsembleID"] = gc.gene(name=row["external_gene_id"],
                                eID=row["EnsembleID"],
                                chro=row["Chr"],
                                tissue=row["Tissue"],
                                age=row["Age"],
                                FPKM=row["MeanExpressionLevel_SNPAligningReads_CPM"],
                                obs_corr=row["ra_value"],
                                bcv=row["BCV"],
                                upperCI=row["rab_value_95%CI_UpperLimit"],
                                lowerCI=row["rab_value_95%CI_LowerLimit"])
    return row["EnsembleID"]
