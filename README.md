# Diabetes Predictor

## Authors

Inder Khera, Jenny Zhang, Jessica Kuo, Javier Martinez (alphabetically ordered)

## About

In this study, we aim to develop a classification model using the logistic regression (LR) algorithm to predict whether a patient is expected to have diabetes or not. Our final model performed decent on an unseen test dataset, achieving an overall accuracy of 0.80. Out of 231 test cases, the model correctly identified 185. However, it made 46 incorrect predictions, of which, 15 are false positives — incorrectly classifying non-diabetic subjects to diabetic- and 31 are false negatives - fail to diagnose diabetes when the patient is actually diabetic. Such errors could either lead to unnecessary treatment or delayed treatment, with the latter having more serious consequences, so we recommend further refinement of the model before it is deployed for clinical use.

The data set that was used for the analysis of this project was created by Jack W Smith, JE Everhart, WC Dickson, WC Knowler, RS Johannes. The data set was sourced from the National Library of Medicine database from the National Institues of Health. Access to their respective analysis can be found [here](https://pmc.ncbi.nlm.nih.gov/articles/PMC2245318/) and access to the dataset can be found via [kaggle](https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database/data) (Dua & Graff,2017). Each row/obersvation from the dataset is an individual that identifies to be a part of the Pima (also known as The Akimel O'odham) Indeginous group, located mainly in the Central and Southern regions of the United States. Each observation recorded has summary statistics regarding features that include the Age, BMI, Blood Pressure, Number of Pregnancies, as well as The Diabetes Pedigree Function (which is a score that gives an idea about how much correlation is between person with diabetes and their family history).

## Report

The final report can be found [here](https://github.com/UBC-MDS/diabetes_predictor_py/tree/main/analysis).

## Usage

First time running the project, run the following from the root of this repository:

```
conda-lock install --name diabetes-predictor conda-lock.yml
```

To run the analysis, run the following from the root of this repository:

```
jupyter lab 
```

Open `analysis/diabetes_analysis.ipynb` in Jupyter Lab and under Switch/Select Kernel choose "Python [conda env:diabetes-predictor]".

Next, under the "Kernel" menu click "Restart Kernel and Run All Cells...".

## Dependencies

- conda (version 23.9.0 or higher)
- conda-lock (version 2.5.7 or higher)
- mamba (version 1.5.8 or higher)
- jupyterlab (version 4.0.0 or higher)
- nb_conda_kernels (version 2.3.1 or higher)
- Python and packages listed in [`environment.yml`](https://github.com/UBC-MDS/diabetes_predictor_py/blob/main/environment.yml)

## License

The Diabetes Predictor report contained herein are licensed under the [Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) License](https://creativecommons.org/licenses/by-nc-nd/4.0/) See the [license file](https://github.com/UBC-MDS/diabetes_predictor_py/blob/main/LICENSE.md) for more information. If re-using/re-mixing please provide attribution and link to this webpage. The software code contained within this repository is licensed under the [MIT license](https://opensource.org/license/MIT). See the [license file](https://github.com/UBC-MDS/diabetes_predictor_py/blob/main/LICENSE.md) for more information.

## References

Dua, D., & Graff, C. (2017). Pima Indians Diabetes Database. UCI Machine Learning Repository. Retrieved from <https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database/data>.