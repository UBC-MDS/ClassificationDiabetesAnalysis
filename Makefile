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

