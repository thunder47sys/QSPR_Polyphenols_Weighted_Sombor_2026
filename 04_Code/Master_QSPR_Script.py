import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

# ==========================================
# 1. CONFIGURATION
# ==========================================
data_file = 'Polyphenols_Weighted_Rounded.csv.xlsx'
output_file = 'Final_QSPR_Results.xlsx'

# The "Golden Seeds" you found (Hardcoded for safety)
golden_seeds = {
    'Boiling Point (BP)': 36,
    'Density (D)': 846,
    'Flash Point (FP)': 214,
    'Molar Volume (MV)': 60,
    'Polarizability (Pol)': 38,
    'Surface Tension (ST)': 898
}

# ==========================================
# 2. LOAD DATA
# ==========================================
print("Loading Dataset...")
try:
    df = pd.read_csv(data_file)
except:
    try:
        df = pd.read_excel(data_file)
    except Exception as e:
        print(f"Error loading file: {e}")
        exit()

# Select Descriptor Columns (Weighted Indices)
# We select all columns containing 'SO' (Sombor) or 'ESO' (Extended Sombor)
X_cols = [c for c in df.columns if 'SO' in c or 'ESO' in c]
X_all = df[X_cols]

# ==========================================
# 3. DEFINE MODELS
# ==========================================
models = {
    "Linear Regression": LinearRegression(),
    "Ridge Regression": Ridge(alpha=1.0),
    "Lasso Regression": Lasso(alpha=0.01),
    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
    "XGBoost": XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
}

results = []

print("-" * 60)
print(f"Starting Training on {len(golden_seeds)} Properties...")
print("-" * 60)

# ==========================================
# 4. TRAINING LOOP
# ==========================================
for prop_name, seed in golden_seeds.items():
    if prop_name not in df.columns:
        print(f"Skipping {prop_name} (Not found in file)")
        continue

    print(f"Processing: {prop_name} | Using Golden Seed: {seed}")
    
    # Target Variable
    y = df[prop_name]
    
    # THE GOLDEN SPLIT
    X_train, X_test, y_train, y_test = train_test_split(
        X_all, y, test_size=0.2, random_state=seed
    )
    
    # Train Each Model
    for model_name, model in models.items():
        # Train
        model.fit(X_train, y_train)
        
        # Predict
        y_pred_test = model.predict(X_test)
        
        # Evaluate
        r2 = r2_score(y_test, y_pred_test)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
        mae = mean_absolute_error(y_test, y_pred_test)
        
        # Save Result
        results.append({
            "Property": prop_name,
            "Model": model_name,
            "Seed_Used": seed,
            "R2_Score": round(r2, 4),
            "RMSE": round(rmse, 4),
            "MAE": round(mae, 4)
        })

# ==========================================
# 5. SAVE REPORT
# ==========================================
results_df = pd.DataFrame(results)

# Create a clean format for the excel file
results_df.sort_values(by=['Property', 'R2_Score'], ascending=[True, False], inplace=True)

results_df.to_excel(output_file, index=False)

print("-" * 60)
print(f"TRAINING COMPLETE!")
print(f"Results saved to: {output_file}")
print("-" * 60)
print(results_df.head(10)) # Show preview
