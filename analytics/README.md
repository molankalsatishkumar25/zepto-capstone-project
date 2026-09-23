# Module 2 - Titanic Analytics

## 1. Objective

This module performs exploratory data analysis, data cleaning, visualization, classification, class-imbalance analysis, Random Forest tuning, and fare regression using the Titanic dataset.

The notebook for this module is:

`01_eda.ipynb`

## 2. Dataset

The Titanic dataset was loaded using:

`sns.load_dataset("titanic")`

The dataset was immediately saved as:

`titanic.csv`

Original dataset shape:

- Rows: 891
- Columns: 15
## 3. Missing-Value Analysis and Cleaning

Missing values were evaluated using the LMS-defined thresholds:

- Under 5%: drop rows
- 5% to 30%: impute
- High missingness: drop the column or create a missing category with justification

### Missing values found

| Column | Missing Values | Missing % | Action |
|---|---:|---:|---|
| age | 177 | 19.87% | Median imputation |
| embarked | 2 | 0.22% | Drop rows |
| deck | 688 | 77.22% | Drop column |
| embark_town | 2 | 0.22% | Drop rows |

### Cleaning decisions

- `age` was median-imputed because its missingness was between 5% and 30%.
- `embarked` and `embark_town` had very small amounts of missing data, so the affected rows were dropped.
- `deck` had very high missingness and was therefore removed.
- After cleaning, the dataset contained 889 rows and 14 columns.
- No missing values remained after cleaning.
## 4. Univariate Analysis

The analysis includes distributions and summary statistics for important numerical variables.

The following were examined:

- Age histogram and boxplot
- Fare histogram and boxplot
- Fare mean
- Fare median
- Fare mode
- Fare skewness
- IQR-based outlier analysis

The notebook contains the detailed numerical outputs and visualizations.

## 5. Bivariate Analysis

Survival patterns were examined across:

- Sex
- Passenger class
- Sex and passenger class together

These comparisons were used to understand how passenger characteristics were associated with survival.

## 6. Correlation Analysis

The required six numerical columns were used for the correlation analysis:

- `survived`
- `pclass`
- `age`
- `sibsp`
- `parch`
- `fare`

The analysis intentionally excludes `adult_male` and `alone`.

### Strongest correlations

1. `pclass` and `fare`: approximately **-0.548**
2. `sibsp` and `parch`: approximately **0.415**

The correlation heatmap is included in the notebook.
## 7. Multivariate Analysis

Multiple multivariate visualizations were created to examine relationships among survival, passenger class, sex, age, and fare.

Each visualization includes an interpretation in the notebook describing the observed pattern and its relevance to Titanic survival.

## 8. Exploratory Standardization

Standardization was explored for:

- `age`
- `fare`

The standardized columns were created for exploratory analysis only.

The notebook verifies the standardized values and their mean and standard deviation.
## 9. Train/Test Split and Preprocessing

The classification workflow uses a stratified train/test split.

Preprocessing is fitted using the training data before being applied to the test data to avoid data leakage.

The final preprocessing and estimator are stored together in a single scikit-learn pipeline.
## 10. Classification Models

The following classification models were evaluated:

- Logistic Regression
- Decision Tree
- Random Forest
- Random Forest with class weighting
- Random Forest with SMOTE
- Tuned Random Forest

Evaluation metrics include:

- Accuracy
- Precision
- Recall
- F1 score
- ROC-AUC
- Confusion matrix

### Classification Results

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.8090 | 0.7833 | 0.6912 | 0.7344 | 0.8610 |
| Decision Tree | 0.7697 | 0.6901 | 0.7206 | 0.7050 | 0.7541 |
| Random Forest Baseline | 0.8202 | 0.7812 | 0.7353 | 0.7576 | 0.8179 |
| Random Forest Balanced | 0.8034 | 0.7391 | 0.7500 | 0.7445 | 0.8229 |
| Random Forest SMOTE | 0.7921 | 0.7460 | 0.6912 | 0.7176 | 0.8250 |
| Random Forest Tuned | 0.7978 | 0.7667 | 0.6765 | 0.7188 | 0.8265 |
## 11. Class Imbalance Analysis

Random Forest performance was compared using:

- Baseline Random Forest
- `class_weight="balanced"`
- SMOTE applied only to the training data

The comparison uses:

- Accuracy
- Precision
- Recall
- F1 score
- ROC-AUC

The notebook contains the corresponding model evaluation outputs.
## 12. Random Forest Hyperparameter Tuning

`GridSearchCV` was used to tune the Random Forest.

The search covered:

- `n_estimators`
- `max_depth`
- `max_features`

Out-of-bag (OOB) scoring was also used.

The tuned model results are included in the classification comparison table.
## 13. Fare Regression

A regression model was developed to predict `fare` using the other available features.

### Regression Results

| Metric | Result |
|---|---:|
| MAE | 17.2892 |
| RMSE | 28.9728 |
| R² | 0.4575 |
| Adjusted R² | 0.3476 |

The regression test set contained 179 observations.

A residual plot was also created.

### Residual Analysis

The residuals showed a changing spread as predicted fare increased. This indicates evidence of heteroscedasticity in the regression residuals.
## 14. Final Classification Comparison

The classification models were compared using the required evaluation metrics.

The baseline Random Forest achieved the highest accuracy (0.8202) and highest F1 score (0.7576) among the evaluated models.

Logistic Regression produced the highest ROC-AUC among the listed models at 0.8610.

The balanced Random Forest produced the highest recall among the Random Forest imbalance variants at 0.7500.

Based on the overall accuracy and F1 results, the baseline Random Forest was selected for the final classification pipeline.
## 15. Saved Complete Pipeline

The complete preprocessing and classification estimator pipeline was saved using `joblib`.

Saved file:

`../models/titanic_survival_pipeline.joblib`

The saved pipeline was successfully reloaded and used to generate predictions on raw test data.

Validation confirmed:

- Pipeline type: `Pipeline`
- Reloaded prediction count: 178
- Saved pipeline file exists successfully
## 16. Files in This Module

```text
analytics/
├── 01_eda.ipynb
├── titanic.csv
└── README.md

models/
└── titanic_survival_pipeline.joblib
## 17. How to Run

From the project root:

1. Activate the Python virtual environment.
2. Open `analytics/01_eda.ipynb`.
3. Run the notebook cells from top to bottom.
4. The notebook creates/uses `titanic.csv`.
5. The completed classification pipeline is saved under `models/`.

## 18. Reproducibility

The notebook contains the complete workflow for:

- Dataset loading
- Dataset preservation
- Missing-value analysis
- Data cleaning
- Exploratory analysis
- Visualization
- Correlation analysis
- Standardization
- Train/test splitting
- Preprocessing
- Classification
- Class-imbalance comparison
- Random Forest tuning
- Fare regression
- Model evaluation
- Pipeline saving and reloading

