.PHONY: clean

all: reports/diabetes_analysis.html reports/diabetes_analysis.pdf

# Download the data
data/raw/diabetes.csv: scripts/download_data.py
	python scripts/download_data.py \
		--url="https://www.kaggle.com/api/v1/datasets/download/uciml/pima-indians-diabetes-database" \
		--write-to=data/raw

# Validate and preprocess the data
data/processed/df.csv: scripts/data_validation_schema.py data/raw/diabetes.csv
	python scripts/data_validation_schema.py \
		--raw-data=data/raw/diabetes.csv \
		--data-to=data/processed

# Perform EDA and generate plots
results/figures/feature_histograms.png results/figures/correlation_heat_map.png results/figures/pairwise_scatterplot.png: scripts/eda_deepchecks.py data/processed/df.csv
	python scripts/eda_deepchecks.py \
		--validated-data=data/processed/df.csv \
		--data-to=data/processed \
		--plot-to=results/figures

# Split the dataset into features and labels
data/processed/X_train.csv data/processed/y_train.csv data/processed/X_test.csv data/processed/y_test.csv: scripts/split_dataset.py data/processed/df.csv
	python scripts/split_dataset.py \
		--train-file ./data/processed/train_df.csv \
		--test-file ./data/processed/test_df.csv \
		--output-dir ./data/processed/

# Fit logistic regression model and save results
results/tables/mean_cv_score.csv results/tables/best_params.csv: scripts/preprocessing_model_fitting.py data/processed/X_train.csv data/processed/y_train.csv
	python scripts/preprocessing_model_fitting.py \
	     --processed-dir ./data/processed/ \
	     --results-dir ./results

# Test the model and save results
results/tables/coeff_table.csv results/tables/pred_results_1_df.csv results/tables/accuracy_df.csv results/tables/value_counts_df.csv results/tables/fp_fn_df.csv results/figures/predic_chart.png: scripts/testing_script.py data/processed/X_train.csv data/processed/X_test.csv data/processed/y_test.csv results/models/random_fit.pkl
	python scripts/testing_script.py \
	     --x-train-data='./data/processed/X_train.csv' \
	     --pipeline-from=results/models/random_fit.pkl \
	     --x-test-data='./data/processed/X_test.csv' \
	     --y-test-data='./data/processed/y_test.csv' \
	     --results-to='./results/tables' \
	     --plot-to='./results/figures'

# Render HTML report
reports/diabetes_analysis.html: reports/diabetes_analysis.qmd \
     results/figures/feature_histograms.png \
     results/figures/correlation_heat_map.png \
     results/figures/pairwise_scatterplot.png \
     results/tables/mean_cv_score.csv \
     results/tables/best_params.csv \
     results/tables/coeff_table.csv \
     results/tables/pred_results_1_df.csv \
     results/tables/accuracy_df.csv \
     results/tables/value_counts_df.csv \
     results/tables/fp_fn_df.csv
	quarto render reports/diabetes_analysis.qmd --to html

# Render PDF report
reports/diabetes_analysis.pdf: reports/diabetes_analysis.qmd \
     results/figures/feature_histograms.png \
     results/figures/correlation_heat_map.png \
     results/figures/pairwise_scatterplot.png \
     results/tables/mean_cv_score.csv \
     results/tables/best_params.csv \
     results/tables/coeff_table.csv \
     results/tables/pred_results_1_df.csv \
     results/tables/accuracy_df.csv \
     results/tables/value_counts_df.csv \
     results/tables/fp_fn_df.csv
	quarto render reports/diabetes_analysis.qmd --to pdf

# Clean up generated files
clean:
	rm -rf data/raw/* data/processed/* results/figures/* 
	rm -rf reports/diabetes_analysis.html \
		reports/diabetes_analysis.pdf