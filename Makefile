.PHONY: clean all

all: reports/diabetes_analysis.html reports/diabetes_analysis.pdf

# Download the data
data/raw/diabetes.csv: scripts/download_data.py
	python scripts/download_data.py \
		--url="https://www.kaggle.com/api/v1/datasets/download/uciml/pima-indians-diabetes-database" \
		--write-to=data/raw


# Validate and preprocess the data
data/processed/diabetes_validated.csv: scripts/data_validation_schema.py data/raw/diabetes.csv
	python scripts/data_validation_schema.py \
		--raw-data=data/raw/diabetes.csv \
		--data-to=data/processed

# Perform EDA and generate plots
results/figures/feature_histograms.png \
results/figures/correlation_heat_map.png \
results/figures/pairwise_scatterplot.png: scripts/eda_deepchecks.py \
data/processed/diabetes_validated.csv
	python scripts/eda_deepchecks.py \
		--validated-data=data/processed/diabetes_validated.csv \
		--data-to=data/processed \
		--plot-to=results/figures

# Split the dataset into features and labels
data/processed/X_train.csv \
data/processed/y_train.csv \
data/processed/X_test.csv \
data/processed/y_test.csv: scripts/split_dataset.py \
data/processed/diabetes_validated.csv
	python scripts/split_dataset.py \
		--train-file ./data/processed/diabetes_train.csv \
		--test-file ./data/processed/diabetes_test.csv \
		--output-dir ./data/processed/

# Fit logistic regression model and save results
results/models/log_pipe.pkl \
results/models/random_fit.pkl \
results/tables/mean_cv_score.csv \
results/tables/best_params.csv: scripts/preprocessing_model_fitting.py \
data/processed/X_train.csv \
data/processed/y_train.csv
	python scripts/preprocessing_model_fitting.py \
		--processed-dir ./data/processed \
	    --results-dir ./results

# Test the model and save results
results/tables/mean_scores.csv \
results/tables/coeff_table.csv \
results/tables/coeff_table.html \
results/tables/pred_results_1_df.csv \
results/tables/test_scores_df.csv \
results/tables/confusion_matrix_df.csv \
results/tables/value_counts_df.csv \
results/tables/fp_fn_df.csv \
results/figures/confusion_matrix_plot.png \
results/figures/precision_recall_plot.png \
results/figures/roc_curve.png \
results/figures/predict_chart.png: scripts/evaluate_predictor.py \
data/processed/X_train.csv \
data/processed/X_test.csv \
data/processed/y_test.csv \
results/models/random_fit.pkl
	python scripts/evaluate_predictor.py \
		--x-train-data='./data/processed/X_train.csv' \
	    --pipeline-from=results/models/random_fit.pkl \
	    --x-test-data='./data/processed/X_test.csv' \
	    --y-test-data='./data/processed/y_test.csv' \
	    --results-to='./results/tables' \
	    --plot-to='./results/figures'

# Render HTML report
reports/diabetes_analysis.html: reports/diabetes_analysis.qmd \
results/figures/feature_histograms.png \
results/figures/correlation_heatmap.png \
results/figures/pairwise_scatterplot.png \
results/figures/confusion_matrix_plot.png \
results/figures/precision_recall_plot.png \
results/figures/roc_curve.png \
results/figures/predict_chart.png \
results/tables/mean_cv_score.csv \
results/tables/best_params.csv \
results/tables/coeff_table.csv \
results/tables/pred_results_1_df.csv \
results/tables/test_scores_df.csv \
results/tables/confusion_matrix_df.csv \
results/tables/value_counts_df.csv \
results/tables/fp_fn_df.csv
	quarto render reports/diabetes_analysis.qmd --to html

# Render PDF report
reports/diabetes_analysis.pdf: reports/diabetes_analysis.qmd \
results/figures/feature_histograms.png \
results/figures/correlation_heatmap.png \
results/figures/pairwise_scatterplot.png \
results/figures/confusion_matrix_plot.png \
results/figures/precision_recall_plot.png \
results/figures/roc_curve.png \
results/figures/predict_chart.png \
results/tables/mean_cv_score.csv \
results/tables/best_params.csv \
results/tables/coeff_table.csv \
results/tables/pred_results_1_df.csv \
results/tables/test_scores_df.csv \
results/tables/confusion_matrix_df.csv \
results/tables/value_counts_df.csv \
results/tables/fp_fn_df.csv
	quarto render reports/diabetes_analysis.qmd --to pdf

# Clean up generated files
clean:
	rm -f data/raw/diabetes.csv
	rm -f data/processed/diabetes_validated.csv \
		  data/processed/diabetes_train.csv \
		  data/processed/diabetes_test.csv \
	      data/processed/X_train.csv \
	      data/processed/y_train.csv \
	      data/processed/X_test.csv \
	      data/processed/y_test.csv
	rm -f results/figures/feature_histograms.png \
	      results/figures/correlation_heatmap.png \
	      results/figures/pairwise_scatterplot.png \
		  results/figures/confusion_matrix_plot.png \
		  results/figures/precision_recall_plot.png \
		  results/figures/roc_curve.png \
	      results/figures/predict_chart.png
	rm -f results/tables/mean_cv_score.csv \
		  results/tables/mean_scores.csv \
	      results/tables/best_params.csv \
	      results/tables/coeff_table.csv \
		  results/tables/coeff_table.html \
		  results/tables/confusion_matrix_df.csv \
	      results/tables/pred_results_1_df.csv \
	      results/tables/test_scores_df.csv \
	      results/tables/value_counts_df.csv \
	      results/tables/fp_fn_df.csv
	rm -f reports/diabetes_analysis.html \
	      reports/diabetes_analysis.pdf
