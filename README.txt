BACKGROUND
Our DNA is like the cookbook for proteins, which are the building blocks of our bodies. Our DNA, collectively called the genome, is subdivided into genes – like recipes (genes) in a cookbook (the genome). Genes are transcribed into mRNA; the equivalent of copying out a recipe from the cookbook. The amount of mRNA produced from a gene is often referred to as the gene’s expression.

Every gene has two physical copies, one from the father and one from the mother. This suggests that each allele makes up have of the gene’s overall expression. However, that is not always the case. An example is in the case of genes on the X chromosome. In individuals with two X chromosomes (who have two copies of each gene on the X chromosome), one copy is always silenced. This prevents the individual from having too much expression of the genes on the X chromosome.

Recently, my lab discovered that in a certain region of the brain, there are genes on the autosomes (the collective term for chromosomes 1-22), that have similar expression patterns as X chromosome genes. In other words, there are some genes where the maternal copy is consistently expressed more than the paternal copy (or vice versa). We say that such genes show allelic expression effects (AEEs), which we sub-divide into different types.

To determine if a gene is showing an AEE, we have to analyze the expression level of each copy over many mice. Unfortunately, the technical noise inherent to sample processing distorts the “true” biological variation. We therefore use R to model the effects of technical noise on a given biological variation, resulting in a range of possible observed correlations. That range is the 95% confidence interval (CI) containing the “true” biological variation. Based on the value of the CI’s lower and upper bounds, we determine if the gene is showing an AEE and which type. 

This project is intended to (1) computationally determine whether a gene is showing an AEE (and which type), and (2) produce a heat map of the overall gene expression for a given set of genes. The output will allow us to determine if AEEs change with age and are correlated with overall gene expression. 

INPUT DATA FORMAT
For determining AEEs, the required input is an Excel sheet where each row is a gene and the columns are information about the gene. The necessary columns are:
1. EnsembleID (the gene’s name in a particular naming scheme)
2. external_gene_id (the gene’s common name)
3. Age (the age at which the sample was taken, allowed values are postnatal day (P)5, P15, and Adult)
4. Tissue (the tissue that was sampled)
5. Chr (the chromosome that the gene is on, must be in the format chrN, where N = 1-22 or X)
6. MeanExpressionLevel_SNPAligningReads_CPM (the mean expression across all biological replicates)
7. ra_value (the observed correlation over all replicates)
8.  BCV (the projected biological coefficient of variation)
9. rab_value_95%CI_UpperLimit (the upper bound of the 95% CI calculated by R)
10. rab_value_95%CI_LowerLimit (the lower bound of the 95% CI calculated by R)

For producing heat maps, the required input is an Excel workbook where each sheet is the gene expression data for one age. Sheet1 must be P5, Sheet2 must be P15, and Sheet3 must be Adult. The rows in each sheet are the genes and each column is a biological replicate.


TO USE
The files script.py, gene_class.py, read_excel.py, and heat_map.py must be in the same directory. Run the script.py file from the command line or your IDE of choice. In addition to the paths of the input data, you will be asked for a list of EnsembleIDs to make the heat map. 

The outputs should be:
1. An Excel sheet consisting of the input gene information sheet with additional columns for CI width and AEE.
2. A .png heat map.
3. A .txt file containing information about how the heat map was generated.

I have provided three test input files (test_information.xlsx, test_expression.xlsx, test_eIDs.txt) and the expected output for those input files (expected_information.xlsx, expected_heat_map.png, and expected_heat_map_metadata.txt).
