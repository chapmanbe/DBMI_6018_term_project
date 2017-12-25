# -*- coding: utf-8 -*-
"""
define gene class
define P5, P15, and Adult classes, which inherit from gene class
"""


# gene class defines all attributes and methods for genes
# there should never be instances of gene
class gene(object):
    """creates a gene object"""
    def __init__(self,
                 name=None,
                 eID=None,
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
        self.name = name
        self.eID = eID
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
