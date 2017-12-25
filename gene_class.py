# -*- coding: utf-8 -*-
"""
define basic_gene class for gene names
define gene class for analyzing AEE status
define ontology class for analyzing functional annotation
"""


import pandas as pd


# creates a gene object with an eID and a name
class basic_gene(object):
    """creates a basic gene object with eID and name"""

    def __init__(self, name=None, eID=None, **kwargs):
        super(basic_gene, self).__init__(**kwargs)
        self.name = name
        self.eID = eID

    # each attribute entered in the constructor needs a getter and setter
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if isinstance(name, str):
            self.__name = name
        else:
            raise TypeError("Gene name must be a string.")

    @property
    def eID(self):
        return self.__eID

    @eID.setter
    def eID(self, eID):
        if isinstance(eID, str):
            self.__eID = eID
        else:
            raise TypeError("Ensembl ID must be a string.")

    def __str__(self):
        return "%s (%s)" % (self.eID, self.name)


# gene class inherits from basic_gene
# adds attributes desirable for AEE analysis
class gene(basic_gene):
    """creates a gene object"""
    def __init__(self,
                 chro=None,
                 tissue=None,
                 age=None,
                 FPKM=None,
                 obs_corr=None,
                 bcv=None,
                 upperCI=None,
                 lowerCI=None,
                 **kwargs):
        super(gene, self).__init__(**kwargs)
        self.chro = chro
        self.tissue = tissue
        self.age = age
        # counts per million for SNP aligning reads
        # presented as the mean across all replicates
        self.FPKM = FPKM
        # Pearson correlation
        # for observed maternal and paternal allele co-expression
        self.obs_corr = obs_corr
        # biological coefficient of variation
        # calculated using edgeR across all replicates
        self.bcv = bcv
        # lower limit of allele correlation 95% CI computed from modeling
        self.upperCI = upperCI
        # upper limit of allele correlation 95% CI computed from modeling
        self.lowerCI = lowerCI

    # each attribute entered in the constructor needs a getter and setter
    @property
    def chro(self):
        return self.__chro

    @chro.setter
    def chro(self, chro):
        if chro[-1] == "X":
            self.__chro = chro
        elif 1 <= int(chro[-1]) <= 22:
            self.__chro = chro
        else:
            raise ValueError("Chromosome must be between 1-22 or X.")

    @property
    def tissue(self):
        return self.__tissue

    @tissue.setter
    def tissue(self, tissue):
        if isinstance(tissue, str):
            self.__tissue = tissue
        else:
            raise TypeError("Tissue must be a string.")

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, age):
        if isinstance(age, str):
            self.__age = age
        else:
            raise TypeError("Age must be a string.")

    @property
    def FPKM(self):
        return self.__FPKM

    @FPKM.setter
    def FPKM(self, FPKM):
        if isinstance(FPKM, float):
            self.__FPKM = FPKM
        else:
            raise TypeError("FPKM must be a float.")

    @property
    def obs_corr(self):
        return self.__obs_corr

    @obs_corr.setter
    def obs_corr(self, obs_corr):
        if isinstance(obs_corr, float):
            self.__obs_corr = obs_corr
        else:
            raise TypeError("obs_corr must be a float.")

    @property
    def bcv(self):
        return self.__bcv

    @bcv.setter
    def bcv(self, bcv):
        if isinstance(bcv, float):
            self.__bcv = bcv
        else:
            raise TypeError("bcv must be a float.")

    @property
    def upperCI(self):
        return self.__upperCI

    @upperCI.setter
    def upperCI(self, upperCI):
        if -1 <= upperCI <= 1:
            self.__upperCI = upperCI
        else:
            raise ValueError("upperCI must be between -1 and 1.")

    @property
    def lowerCI(self):
        return self.__lowerCI

    @lowerCI.setter
    def lowerCI(self, lowerCI):
        if -1 <= lowerCI <= 1:
            self.__lowerCI = lowerCI
        else:
            raise ValueError("lowerCI must be between -1 and 1.")

    # define getters for attributes not entered in the constructor
    @property
    def CI_width(self):
        return abs(self.upperCI-self.lowerCI)

    @property
    def AEE(self):  # determine if CoEE, DAEE, AAEE, or no effect
        if self.lowerCI >= 0.75:
            category = "CoEE"
        elif 0 < self.upperCI <= 0.75:
            category = "DAEE"
        elif self.upperCI <= 0:
            category = "AAEE"
        else:
            category = "No effect"
        return category

    def __str__(self):
        return "%s (%s), at %s in the %s, is %s." % (self.eID, self.name, self.age, self.tissue, self.AEE)


# ontology class inherits from basic_gene
# adds functional annotation
# not used as of 12/24/17
class ontology(basic_gene):
    """creates a gene object with functional annotation"""
    def __init__(self, **kwargs):
        super(ontology, self).__init__(**kwargs)

    def fa(self, fad):
        if isinstance(fad, pd.core.frame.DataFrame):
            # extract the row of the gene by eID and make it be a series
            fa_row = fad[fad["ID"] == self.eID].squeeze()
        # create dictionary to store enrichments
        # key = category/database, value = terms
        terms = {}
        for cat in list(fad.columns)[4:]:
            terms[cat] = fa_row[cat]
        self.fa = terms

    def __str__(self):
        return "%s (%s) has the functional enrichments" % (self.eID, self.name)+" "+str(self.fa)
