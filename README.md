# Diabetes Predictor

## Authors

Inder Khera, Jenny Zhang, Jessica Kuo, Javier Martinez (alphabetically ordered)

## About

In this study, we aim to develop a classification model using the logistic regression (LR) algorithm to predict whether a patient is expected to have diabetes or not. 
Our final model performed decent on an unseen test dataset, achieving an overall accuracy of 0.75. Out of 218 test cases, the model correctly identified 164. 
However, it made 46 incorrect predictions, of which, 19 are false positives - incorrectly classifying non-diabetic subjects to diabetic- 
and 35 are false negatives - fail to diagnose diabetes when the patient is actually diabetic. 
Such errors could either lead to unnecessary treatment or delayed treatment, with the latter having more serious consequences, 
so we recommend further refinement of the model before it is deployed for clinical use.

The data set that was used for the analysis of this project was created by Jack W Smith, JE Everhart, WC Dickson, WC Knowler, RS Johannes. 
The data set was sourced from the National Library of Medicine database from the National Institues of Health. 
Access to their respective analysis can be found [here](https://pmc.ncbi.nlm.nih.gov/articles/PMC2245318/) 
and access to the dataset can be found via [kaggle](https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database/data) (Dua & Graff,2017). 
Each row/obersvation from the dataset is an individual that identifies to be a part of the Pima (also known as The Akimel O'odham) Indeginous group, 
located mainly in the Central and Southern regions of the United States. 
Each observation recorded has summary statistics regarding features that include the Age, BMI, Blood Pressure, Number of Pregnancies, 
as well as The Diabetes Pedigree Function (which is a score that gives an idea about how much correlation is between person with diabetes and their family history).

## Report

The final report can be found [here](https://github.com/UBC-MDS/diabetes_predictor_py/tree/main/analysis) or [this webpage](https://ubc-mds.github.io/diabetes_predictor_py/).

## Usage

To replicate this analysis, follow the steps below. You can run the analysis using one of two methods: **Docker** or **Conda**.

**Prerequisites**: Please note that the instructions in this section require executing them in a Unix-based shell.

### Setup

First, clone this GitHub repository and navigate to its root directory:
```bash
git clone https://github.com/UBC-MDS/diabetes_predictor_py.git
cd diabetes_predictor_py
```

---

### Option 1: Using Docker

**Prerequisites**: Install [Docker](https://www.docker.com/get-started) and ensure it is running on your system.

1. Build and run the Docker container using the provided script:
   ```bash
   chmod +x ./builders/docker_magic_builder.sh
   ./builders/docker_magic_builder.sh
   ```
   This will set up the Conda environment inside a Docker container and build the Docker image.

2. Once the container is running, access the server by opening the link shown in the terminal (e.g., http://127.0.0.1:8888/lab?token={your_token})

3. Open the JupyterLab link generated in the terminal. Navigate to:
   ```
   analysis/diabetes_analysis.ipynb
   ```

4. Under the **Kernel** menu, click:
   ```
   Restart Kernel and Run All Cells...
   ```

---

### Option 2: Using Conda

1. Set up the Conda environment and run JupyterLab using the provided script:
   ```bash
   chmod +x ./builders/conda_magic_builder.sh
   ./builders/conda_magic_builder.sh
   ```

2. Open:
   ```
   analysis/diabetes_analysis.ipynb
   ```

3. Under **Switch/Select Kernel**, choose:
   ```
   Python [conda env:diabetes_predictor]
   ```

4. Under the **Kernel** menu, click:
   ```
   Restart Kernel and Run All Cells...
   ```

---

These steps ensure you can run the analysis seamlessly using either Docker or Conda.

---
### Clean up

1. Docker: Type `Ctrl` + `C` in the terminal where you launched the container, 
and then type `docker compose rm` to shut down the container and clean up the resources

2. Conda: Type `Ctrl` + `C` in the terminal where Jupyter Notebook is launched, 
type `conda deactivate` to exit out of the project environment, 
and then type `conda env remove diabetes_predictor` to delete the environment and clean up the resources

## Dependencies

- conda (version 23.9.0 or higher)
- conda-lock (version 2.5.7 or higher)
- mamba (version 1.5.8 or higher)
- jupyterlab (version 4.0.0 or higher)
- nb_conda_kernels (version 2.3.1 or higher)
- Python and packages listed in [`environment.yml`](https://github.com/UBC-MDS/diabetes_predictor_py/blob/main/environment.yml)

### Adding a new dependency

1. Add the dependency to the `environment.yml` file on a new branch. 
If the package is `pip` installed, it should also be added to `Dockerfile` with command `RUN pip install <package_name> = <version>`

2. Run `conda-lock -k explicit --file environment.yml -p linux-64` to update the `conda-linux-64.lock` file.

3. Re-run the scripts above using the Docker or Conda option. 

## License

The Diabetes Predictor report contained herein are licensed under the [Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) License](https://creativecommons.org/licenses/by-nc-nd/4.0/) See the [license file](https://github.com/UBC-MDS/diabetes_predictor_py/blob/main/LICENSE.md) for more information. If re-using/re-mixing please provide attribution and link to this webpage. The software code contained within this repository is licensed under the [MIT license](https://opensource.org/license/MIT). See the [license file](https://github.com/UBC-MDS/diabetes_predictor_py/blob/main/LICENSE.md) for more information.

## References

Dua, D., & Graff, C. (2017). Pima Indians Diabetes Database. UCI Machine Learning Repository. Retrieved from <https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database/data>.
