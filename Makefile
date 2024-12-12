.PHONY: clean

all: results/figures

#download the data
data/raw: scripts/download_data.py 
	python scripts/download_data.py \
		--url="https://www.kaggle.com/api/v1/datasets/download/uciml/pima-indians-diabetes-database" \
		--write-to=data/raw

#validate the data 
data/processed: scripts/data_validation_schema.py 
	python scripts/data_validation_schema.py \
		--data-to=data/processed

#EDA
results/figures: scripts/eda_deepchecks.py
	python scripts/eda_deepchecks.py \
		--validated-data=data/processed/df.csv \
		--data-to=data/processed \
		--plot-to=results/figures

data/processed: scripts/eda_deepchecks.py data/processed/df.csv 
	python scripts/eda_deepchecks.py \
		--validated-data=data/processed/df.csv \
		--data-to=data/processed \
		--plot-to=results/figures

./data/processed/: python scripts/split_dataset.py
	python scripts/split_dataset.py \
		--train-file ./data/processed/train_df.csv \
		--test-file ./data/processed/test_df.csv \
		--output-dir ./data/processed/

clean:
	rm -rf data/raw
	rm -rf data/processed
	rm -rf results/figures \
		results/figures \ 
		data/processed
