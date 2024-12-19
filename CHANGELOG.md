## CHANGELOG FOR GROUP 15

Please see all feedback from TA through Milestone grading and peer review consolidated below. 
Commit links as evidence of improvements and some description have also been included.

### Analysis and Code Related

1. Abstract & Summary: Does not clearly state the question being asked (-0.25). Does not discuss importance and limitations of findings (-0.25).
https://github.com/UBC-MDS/diabetes_predictor_py/pull/89/commits/6d90b864082ff2b6fddea9ca6cec9c214e3e7402

2. Introduction: Did not clearly identify the question being asked, or the question was not clear in some way. Did not clearly identify and describe the dataset that was used to answer the question. This should be done at least at a high-level in the introduction.
https://github.com/UBC-MDS/diabetes_predictor_py/pull/89/commits/6d90b864082ff2b6fddea9ca6cec9c214e3e7402

3. Introduction: Did not clearly identify the question being asked, or the question was not clear in some way (-1). Did not clearly identify and describe the dataset that was used to answer the question. This should be done at least at a high-level in the introduction (-1). Did not reference the data set when referring to it (-0.25).
https://github.com/UBC-MDS/diabetes_predictor_py/pull/89/commits/6d90b864082ff2b6fddea9ca6cec9c214e3e7402

4. Methods & Results: Important methodology descriptions missing (e.g., did not explain in narrative what metric was being used for model parameter optimization). t=The first question that came into my head and could be further specified in the report is : "is this a balanced dataset?", how many patients were recorded in each category? this needs to be stated in the method section as it's important info about the dataset. (-1)
https://github.com/UBC-MDS/diabetes_predictor_py/commit/725fc5ff057fd685290c0bf7104eb66198cec805

5. Methods & Results: The data should be reproducibly downloaded from it's source using code in the analysis code document, and a copy saved in the data directory (and ideally in the data/raw subdirectory). (-1) 
Amended in an earlier Milestone
https://github.com/UBC-MDS/diabetes_predictor_py/blob/b51334551073b80786aa1339960580e45465d34b/scripts/download_data.py

6. Methods & Results: the method and results should be listed seperately in 2 different sections, not merged as one.
https://github.com/UBC-MDS/diabetes_predictor_py/commit/371a970375246d4e546198c8e8cb90711980b6a5

7. EDA: Missing figure or table legends/descriptions. (-1)
https://github.com/UBC-MDS/diabetes_predictor_py/blob/1a705b08226680570fc3a69c30b76157eb03cc7d/reports/diabetes_analysis.qmd

8. Discussion: Key findings from the project are not presented. (-1)
https://github.com/UBC-MDS/diabetes_predictor_py/blob/1a705b08226680570fc3a69c30b76157eb03cc7d/reports/diabetes_analysis.qmd

9. There were many spelling or grammatical errors. They did not impact the understanding of the document. (-0.5)
https://github.com/UBC-MDS/diabetes_predictor_py/blob/530cfcb738c1e8a19c0958be6664f0f472e6f604/reports/diabetes_analysis.html

10. It would be better to use a confusion matrix to show the results instead of prediction probabilities. The prediction probabilities plot can be confusing for general audience. / Consider presenting the model results using a confusion matrix or a logistic regression curve for better clarity.
https://github.com/UBC-MDS/diabetes_predictor_py/blob/7994a29ba2be714390120beb7700eb567d6f84e8/scripts/evaluate_predictor.py

11. Consider adding PR curve and ROC curve for a more detailed evaluation of the results.
https://github.com/UBC-MDS/diabetes_predictor_py/blob/7994a29ba2be714390120beb7700eb567d6f84e8/scripts/evaluate_predictor.py

12. The pairwise scatter plots extend beyond the page in the PDF. Additionally, each individual plot in the pairwise comparisons is too small, making it difficult to read the axes.
https://github.com/UBC-MDS/diabetes_predictor_py/blob/530cfcb738c1e8a19c0958be6664f0f472e6f604/reports/diabetes_analysis.pdf

13. Many of the references are missing their DOI link / Some references in the documentation are missing DOI information.
https://github.com/UBC-MDS/diabetes_predictor_py/pull/89/commits/6d90b864082ff2b6fddea9ca6cec9c214e3e7402

14. Discuss the range of C used for hyperparameter optimization, and explain the rationale behind your chosen range.
https://github.com/UBC-MDS/diabetes_predictor_py/commit/371a970375246d4e546198c8e8cb90711980b6a5

15. Some libraries loaded in individual scripts are not utilized within the code. Removing these unused libraries can streamline the scripts, reduce potential confusion, and improve code efficiency.
https://github.com/UBC-MDS/diabetes_predictor_py/commit/bb540cc50eca77e4d7ad4ac13973c538c2f00020

16. The text references a heatmap, but the corresponding figure is absent from the report.
Note: text was fixed and it is no longer referring the table as heatmap.
https://github.com/UBC-MDS/diabetes_predictor_py/blob/530cfcb738c1e8a19c0958be6664f0f472e6f604/reports/diabetes_analysis.qmd

17. The figure 1 in the report is formatted into two columns but I believe it would be better if it was a 3 by 3 figure.
https://github.com/UBC-MDS/diabetes_predictor_py/blob/1a705b08226680570fc3a69c30b76157eb03cc7d/scripts/eda_deepchecks.py

18. In Table 1 of the analysis report, the coefficients are displayed with varying decimal places. Consider standardizing the number of decimal places for clarity and consistency.
https://github.com/UBC-MDS/diabetes_predictor_py/blob/1a705b08226680570fc3a69c30b76157eb03cc7d/reports/diabetes_analysis.qmd

19. Certain numbers in the analysis report appear to be hard-coded. It is recommended to replace these with inline Python code.
_NOTE: this was one of the peer review feedback received. However, proofreader has walked through the entire report and noticed that the only numbers remain hard coded are those cited from research report from introduction or any factual ranges related to data validation. All results related to analysis was properly transformed and linked. Providing the final report edit commit as reference._ 
https://github.com/UBC-MDS/diabetes_predictor_py/commit/b14df6ce4f7e35fcb79ed94c6f1a060d111e43f6


### Process Related

1. The Dockefile could be simplified. For instance, multiple RUN instructions could be merged into one. (-1)
https://github.com/UBC-MDS/diabetes_predictor_py/pull/81/commits/5e37027e0bd5ab0fcb753ea19e1b3827c4a7656f

2. the instructions for how to set up environment is missing a step to change into the cloned repository directory after cloning it. user will not be able to recreate the virtual environment if the "cd ..." part is missing (-0.5)
_NOTE: already incorporated in earlier milestone. See a final commit link for final result._
https://github.com/UBC-MDS/diabetes_predictor_py/blob/8f48f6b8df8812069e1933829a3ed2c35812d9bb/README.md

3. `environment.yml`: versions are missing from environment files(s) for some R or Python packages (-1) 
_NOTE: already incorporated in earlier milestone. See a final commit link for final result._
https://github.com/UBC-MDS/diabetes_predictor_py/blob/019af1f5cd2dd1a33f9d79a0e1f90ad23c5f96fd/environment.yml

4. `environment.yml`: Programming language and/or package versions are pinned using >= instead of =. This means that each time the environment is built in the future, the most recent version of the programming language and/or package will be installed in the environment. This will lead to the environment not being able to be reproducibly built in the future. (-1)
_NOTE: already incorporated in earlier milestone. See a final commit link for final result._
https://github.com/UBC-MDS/diabetes_predictor_py/blob/019af1f5cd2dd1a33f9d79a0e1f90ad23c5f96fd/environment.yml

5. Reproducibility Miletone 1: I cannot find the "Python [conda env:diabetes-predictor" selection for kernel after following your instructions. (-1)
_NOTE: no longer applicable and already fixed in Docker._

6. Reproducibility Milestone 2:  instructions is a bit confusing if I am a complete new user to docker "Once the container is running, access the server by opening the link shown in the terminal (e.g., http://127.0.0.1:8888/lab?token={your_token})" => essentially including an image (-0.5)
https://github.com/UBC-MDS/diabetes_predictor_py/pull/89/commits/ce885de6a3ca455b469ffe1ac7ac0f238f258214

7. Workflow: branch name is not meaningful: kuo4230-patch-1 (-0.5)
_NOTE: no longer applicable_

8. Github issues communication: GitHub issues were rarely used for project communication. (-4)
_NOTE: fixed since Milestone 2_

### Structure Related

1. the index.html should not be living in the root directory, it belongs to the analysis folder (-0.5)
https://github.com/UBC-MDS/diabetes_predictor_py/commit/fc9a16ddf22a873da8ff6579575252ff33225899

2. `CONTRIBUTING.md`: the links are broken for "Project's license", "UBC-MDS Code of Conduct" (-1)
https://github.com/UBC-MDS/diabetes_predictor_py/commit/fabaabc17cb665b2e9b9d6a5ebf2a1d849431870

3. The some of the processed data files are simply call df.csv and test_df.csv. I cannot tell what data is in the file. A more descriptive or meaningful name would be nice.
_NOTE: this involves changes in multiple scripts so instead of pointing to the scripts, I am pointing to the commits where showcase generated files with new meaningful names_
https://github.com/UBC-MDS/diabetes_predictor_py/commit/7994a29ba2be714390120beb7700eb567d6f84e8

4. The "Option 1" header in the README is unnecessary since there is no corresponding "Option 2." Consider removing it to avoid confusion.
https://github.com/UBC-MDS/diabetes_predictor_py/commit/8b24aa91a8736e30125f31578ad36b9b80a6f53e

5. There are two validation_errors.log files—one in the report folder and another in the root directory. One of these files may be redundant.
https://github.com/UBC-MDS/diabetes_predictor_py/commit/8822725913e2c7ef473471c22abeaf31201699c5