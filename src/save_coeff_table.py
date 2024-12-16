import pandas as pd
import os

def save_coefficients_table(best_model, X_train, results_to):
    """
    Extracts coefficients from a logistic regression model, creates a DataFrame
    with feature names and coefficients, and saves it as a CSV file.
    
    Parameters:
    - best_model: sklearn Pipeline with a logistic regression model as a step
    - X_train: pandas DataFrame of training features
    - results_to: Directory path to save the output CSV file
    
    Returns:
    - coeff_df_sorted: pandas DataFrame with sorted coefficients
    """
    # Check if X_train is a pandas DataFrame
    if not isinstance(X_train, pd.DataFrame):
        raise TypeError("X_train should be a pandas DataFrame")
    
    # Ensure the model has a 'logisticregression' step
    if 'logisticregression' not in best_model.named_steps:
        raise ValueError("'logisticregression' step not found in the pipeline.")
    
    logistic_model = best_model.named_steps['logisticregression']
    
    # Ensure the model is trained and has coefficients
    if not hasattr(logistic_model, 'coef_'):
        raise ValueError("Model is not trained or does not have coefficients.")
    
    # Extract coefficients
    coefficients = logistic_model.coef_.flatten()
    
    # Handle feature alignment for transformed data
    if hasattr(best_model, 'named_steps') and 'columntransformer' in best_model.named_steps:
        transformer = best_model.named_steps['columntransformer']
        feature_names = transformer.get_feature_names_out()
    else:
        feature_names = X_train.columns
    
    # Creating DataFrame with features and coefficients
    coeff_df = pd.DataFrame({
        'Features': feature_names,
        'Coefficients': coefficients
    })
    
    # Sorting by absolute value of coefficients for better interpretability
    coeff_df_sorted = coeff_df.reindex(coeff_df['Coefficients'].abs().sort_values(ascending=False).index)
    
    # Saving the table as a CSV file
    output_path = os.path.join(results_to, "coeff_table.csv")
    coeff_df_sorted.to_csv(output_path, index=False)
    print(f"Coefficient table saved to {output_path}")
    
    return coeff_df_sorted
