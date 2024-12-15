import pandas as pd
import os

def save_coefficients_table(best_model, X_train, results_to):
    """
    Extracts coefficients from a logistic regression model, creates a DataFrame
    with feature names and coefficients, and saves it as a CSV file.
    """
    # Check if X_train is a pandas DataFrame
    if not isinstance(X_train, pd.DataFrame):
        raise TypeError("X_train should be a pandas DataFrame")
    
    # Check if the model has been trained and has 'coef_'
    if not hasattr(best_model.named_steps['logisticregression'], 'coef_'):
        raise ValueError("Model is not trained. Please train the model before extracting coefficients.")
    
    coefficients = best_model.named_steps['logisticregression'].coef_.flatten()
    
    # Creating DataFrame with features and coefficients
    coeff_df = pd.DataFrame({
        'Features': X_train.columns,
        'Coefficients': coefficients
    })
    
    # Sorting by coefficients (optional)
    coeff_df_sorted = coeff_df.sort_values(by='Coefficients', ascending=False)
    
    # Saving the table as a CSV file
    coeff_df_sorted.to_csv(os.path.join(results_to, "coeff_table.csv"), index=False)
    
    return coeff_df_sorted.style  # Returning the styled DataFrame
