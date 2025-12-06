# ML Planning Notes

## Dataset to Use
I will use the PIMA Diabetes Dataset from Kaggle/UCI.

## Goal of the ML Model
Predict the early risk of diabetes using basic medical indicators.

## What I Need to Learn First
- Analyze and understand CSV files
- How to load a dataset into Python?
- What is train-test split?
- What is Logistic Regression?
- What is accuracy score?

## File structure (ML)
ml/
 ├── hello.py
 ├── load_data.py
 ├── analyze_data.py
 └── train_model.py 

## First issue summary:
The PIMA Indans Diabetes dataset was successfully loaded and inspected. It was ensured that all 768 rows and 9 columns contained correct values (non-null) as a result of replacing biologically invalid zero values in certain features like Glucose, BloodPressure, SkinThickness and Insulin with their medians. ".describe()" method assisted me in understanding the overall distribution of the features. Further data analysis showed the clear difference in glucose ditribution based on diabetes outcome. In the class distribution, the graph showed a moderate imbalance (approx 65% diabetic and 34.9% non diabetic). Thankfully the imbalance wasn't too far off but it revealed that accuracy alone wasn't enough, so additional metrics such as precision, recall, F1-score and ROC-AUC will be used during the learning models.