# testing_script.py
# author: Inder Khera
# date: 2024-12-03

import click
import os
import altair as alt
import numpy as np
import pandas as pd
import pickle
from sklearn import set_config
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.compose import make_column_transformer, make_column_selector
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import fbeta_score, make_scorer
@click.command()
@click.option('--x-train-data', type=str, help="Path to X_train data")
@click.option('--x-test-data', type=str, help="Path to X_train data")
@click.option('--y-test-data', type=str, help="Path to X_train data")
@click.option('--pipeline-from', type=str, help="Path to directory where the fit pipeline object lives")
@click.option('--results-to', type=str, help="Path to directory where the table will be written to")
@click.option('--plot-to', type=str, help="Path to directory where the plot will be written to")
def main(x_train_data, x_test_data, y_test_data, pipeline_from, results_to, plot_to):

    
    #read in csv files for training and testing model
    X_train = pd.read_csv(x_train_data)
    X_test = pd.read_csv(x_test_data)
    y_test= pd.read_csv(y_test_data)

    # read in random_fit model (pipeline object)
    with open(pipeline_from, 'rb') as f:
        random_fit = pickle.load(f)

    mean_scores = pd.DataFrame(random_fit.cv_results_).sort_values(
        "rank_test_score").head(3)[["mean_test_score",
                                "mean_train_score"]]
    
    mean_scores.to_csv(os.path.join(results_to, "mean_scores.csv"), index=False)

    # Best model from the search object
    best_model = random_fit.best_estimator_

    # Retrieve the coefficients and feature names
    coefficients = best_model.named_steps['logisticregression'].coef_.flatten()
    features = X_train.columns 
    
    # Create a DataFrame to display the feature names and corresponding coefficients
    coeff_df = pd.DataFrame({
        'Features': features,
        'Coefficients': coefficients
    })

    # Sort by 'Coefficients' in descending order to see the most important features first
    coeff_df_sorted = coeff_df.sort_values(by = 'Coefficients', ascending = False)

    coeff_table = coeff_df_sorted.style.format(
        precision = 3
        ).background_gradient(
            axis = None
            )
    # Save the sorted coefficients to a CSV file
    coeff_df_sorted.to_csv(os.path.join(results_to, "coeff_table.csv"))
    coeff_table.to_html(os.path.join(results_to, 'coeff_table.html'))

    # Make predictions using the best model
    y_pred = best_model.predict(X_test)
    y_test = y_test.squeeze()
    
    y_pred_prob = best_model.predict_proba(X_test)
    pred_bool = (y_test == y_pred)
    pred_results_1 = np.vstack([y_test, y_pred, pred_bool, y_pred_prob[:, 1]])
    pred_results_1_df = pd.DataFrame(pred_results_1.T, 
                                 columns = ['y_test', 'y_pred', 'pred_bool', 'y_pred_prob_1'])
    pred_results_1_df['pred_bool'] = pred_results_1_df['pred_bool'] == 1
    pred_results_1_df.head()

    pred_results_1_df.to_csv(os.path.join(results_to, "pred_results_1_df.csv"), index=False)

    # Compute accuracy
    accuracy = best_model.score(X_test, y_test)

    accuracy_df = pd.DataFrame({'accuracy': [accuracy]})
    accuracy_df.to_csv(os.path.join(results_to, "accuracy_df.csv"), index=False)

    # Calculate the number of correct predictions and misclassifications
    value_counts = pred_results_1_df['pred_bool'].value_counts()

    value_counts_df = pd.DataFrame({
        'correct predictions': [value_counts.get(True, 0)], 
        'misclassifications': [value_counts.get(False, 0)]
        })
    value_counts_df.to_csv(os.path.join(results_to, "value_counts_df.csv"), index=False)

    # Calculate the number of false positives (FPs) and false negatives (FNs)
    fp = len(pred_results_1_df[(pred_results_1_df['y_test'] == 0) & (pred_results_1_df['y_pred'] == 1)])
    fn = len(pred_results_1_df[(pred_results_1_df['y_test'] == 1) & (pred_results_1_df['y_pred'] == 0)])

    fp_fn_df = pd.DataFrame({
        'false positives': [fp], 
        'false negatives': [fn]
        })
    
    fp_fn_df.to_csv(os.path.join(results_to, "fp_fn_df.csv"), index=False)

    predic_chart = alt.Chart(pred_results_1_df, title = 'Test Set Prediction Accuracy').mark_tick().encode(
        x = alt.X('y_pred_prob_1').title('Positive Class Prediction Prob'),
        y = alt.Y('pred_bool').title('Pred. Accuracy'),
        color = alt.Color('y_test:N').title('Outcome')
        )
    predic_chart.save(os.path.join(plot_to, 'predic_chart.png'),
                            scale_factor=2.0)

if __name__ == '__main__':
    main()