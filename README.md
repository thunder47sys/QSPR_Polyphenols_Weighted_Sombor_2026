# QSPR_Polyphenols_Weighted_Sombor_2026
Supplementary data for the research paper: QSPR Analysis of Polyphenols using Weighted Sombor Indices
Supplementary Data: QSPR Analysis of Polyphenols using Weighted Sombor Indices
Authors: Shehroze et al. Institution: Department of Mathematics, University of Sargodha, Punjab, Pakistan. Year: 2026

📌 Overview
This repository contains the supplementary material, datasets, and source code for the research paper:

"QSPR Analysis of Polyphenolic Compounds using Weighted Sombor Indices via Machine Learning."

In this study, we introduced novel weighted Sombor indices (weighted by atomic mass, radius, electronegativity, and ionization energy) to predict six physicochemical properties of 50 polyphenolic compounds.

📂 Repository Structure
1. Dataset (/01_Dataset)
Polyphenols_Weighted_Rounded.csv: The primary dataset containing the calculated weighted Sombor indices for all 50 molecules.

Properties.xlsx: The reference dataset containing the Compound Names, SMILES codes, CID numbers, and the 6 experimental physicochemical properties for all 50 compounds.

2. Results (/02_Results)
S3_Detailed_Predictions_With_Errors.xlsx: Detailed table showing the Actual vs. Predicted values for all compounds (Training & Test sets) across 6 properties. Includes Absolute Error calculations to verify model accuracy.

Table3_Full_28_Indices.xlsx: A complete list of importance scores for all 28 weighted indices, categorized by atomic property.

Table1_Descriptive_Statistics.xlsx: Summary statistics (Mean, Max, Min, Std Dev) for all topological indices used in the study.

3. Figures (/03_Figures)
Figure1_ScatterPlots.png: Experimental vs. Predicted scatter plots for the best performing models.

FigureS1_Feature_Importance.png: Bar charts visualizing the top 10 most significant indices for each property.

FigureS2_Correlation_Heatmap.png: Pearson correlation heatmap of the top weighted indices, demonstrating feature relationships.

4. Code (/04_Code)
Polyphenolsweightedrounded.py: The calculation script.

Function: Generates the 74 weighted Sombor indices.

Input: Requires an input file (like Properties.xlsx) containing 50 polyphenols with columns for SMILES, Compound Name, and CID.

Master_QSPR_Script.py: The machine learning analysis script.

Function: Performs the QSPR modeling.

Features: Splits data using "Golden Seeds", trains models (XGBoost, RF, LR), and generates performance metrics/feature importance scores.

⚙️ Methodology & Validation
Validation Strategy: A "Golden Split" method was used to ensure statistically identical Training (80%) and Test (20%) sets.

Reproducibility: The random seeds used for each property are listed below to ensure reproducibility:

Boiling Point: Seed 36

Density: Seed 846

Flash Point: Seed 214

Molar Volume: Seed 60

Polarizability: Seed 38

Surface Tension: Seed 898

📞 Contact
For questions regarding the data or code, please open an issue in this repository.
