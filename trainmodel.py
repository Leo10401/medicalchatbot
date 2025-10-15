import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle
import warnings
warnings.filterwarnings('ignore')

# Load all datasets
print("Loading datasets...")
df_dataset = pd.read_csv('dataset/dataset.csv')
df_description = pd.read_csv('dataset/symptom_Description.csv')
df_precaution = pd.read_csv('dataset/symptom_precaution.csv')
df_severity = pd.read_csv('dataset/Symptom-severity.csv')

print(f"Dataset shape: {df_dataset.shape}")
print(f"Number of unique diseases: {df_dataset['Disease'].nunique()}")
print(f"Number of unique symptoms: {df_severity.shape[0]}")

# Data Preprocessing
print("\nPreprocessing data...")

# Get all unique symptoms from the dataset
all_symptoms = set()
for col in df_dataset.columns[1:]:  # Skip 'Disease' column
    symptoms = df_dataset[col].dropna().unique()
    for symptom in symptoms:
        # Clean the symptom names (remove leading/trailing spaces)
        symptom_clean = str(symptom).strip()
        if symptom_clean and symptom_clean != 'nan':
            all_symptoms.add(symptom_clean)

all_symptoms = sorted(list(all_symptoms))
print(f"Total unique symptoms found: {len(all_symptoms)}")

# Create a symptom severity dictionary
symptom_severity_dict = dict(zip(df_severity['Symptom'].str.strip(), df_severity['weight']))

# Create feature matrix
# Each row will have binary values for presence/absence of symptoms
X = []
y = []

for index, row in df_dataset.iterrows():
    # Create a feature vector with 0s
    feature_vector = [0] * len(all_symptoms)
    
    # Get the disease
    disease = row['Disease']
    
    # Mark symptoms as 1 if present
    for col in df_dataset.columns[1:]:
        symptom = str(row[col]).strip()
        if symptom and symptom != 'nan' and symptom in all_symptoms:
            symptom_index = all_symptoms.index(symptom)
            feature_vector[symptom_index] = 1
    
    X.append(feature_vector)
    y.append(disease)

# Convert to numpy arrays
X = np.array(X)
y = np.array(y)

print(f"\nFeature matrix shape: {X.shape}")
print(f"Target vector shape: {y.shape}")

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print(f"\nTraining set size: {X_train.shape[0]}")
print(f"Testing set size: {X_test.shape[0]}")

# Train Random Forest Classifier
print("\nTraining Random Forest model...")
rf_classifier = RandomForestClassifier(
    n_estimators=200,
    criterion='gini',
    max_depth=20,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1,
    verbose=1
)

rf_classifier.fit(X_train, y_train)

# Make predictions
print("\nEvaluating model...")
y_pred_train = rf_classifier.predict(X_train)
y_pred_test = rf_classifier.predict(X_test)

# Calculate accuracy
train_accuracy = accuracy_score(y_train, y_pred_train)
test_accuracy = accuracy_score(y_test, y_pred_test)

print(f"\nTraining Accuracy: {train_accuracy * 100:.2f}%")
print(f"Testing Accuracy: {test_accuracy * 100:.2f}%")

# Display classification report
print("\nClassification Report:")
print(classification_report(y_test, y_pred_test, zero_division=0))

# Feature importance
feature_importance = pd.DataFrame({
    'Symptom': all_symptoms,
    'Importance': rf_classifier.feature_importances_
}).sort_values('Importance', ascending=False)

print("\nTop 20 Most Important Symptoms:")
print(feature_importance.head(20))

# Create dictionaries for disease information
print("\nCreating disease information dictionaries...")

# Description dictionary
description_dict = dict(zip(df_description['Disease'], df_description['Description']))

# Precaution dictionary
precaution_dict = {}
for index, row in df_precaution.iterrows():
    disease = row['Disease']
    precautions = [
        row['Precaution_1'],
        row['Precaution_2'],
        row['Precaution_3'],
        row['Precaution_4']
    ]
    # Remove NaN values
    precautions = [p for p in precautions if pd.notna(p)]
    precaution_dict[disease] = precautions

# Calculate disease severity based on symptoms
disease_severity_dict = {}
for disease in df_dataset['Disease'].unique():
    disease_data = df_dataset[df_dataset['Disease'] == disease]
    total_severity = 0
    symptom_count = 0
    
    for col in df_dataset.columns[1:]:
        symptoms = disease_data[col].dropna().unique()
        for symptom in symptoms:
            symptom_clean = str(symptom).strip()
            if symptom_clean in symptom_severity_dict:
                total_severity += symptom_severity_dict[symptom_clean]
                symptom_count += 1
    
    if symptom_count > 0:
        avg_severity = total_severity / symptom_count
        disease_severity_dict[disease] = round(avg_severity, 2)
    else:
        disease_severity_dict[disease] = 0

# Save the model and data
print("\nSaving model and data...")

# Save the trained model
with open('random_forest_model.pkl', 'wb') as f:
    pickle.dump(rf_classifier, f)

# Save all necessary data
model_data = {
    'all_symptoms': all_symptoms,
    'symptom_severity_dict': symptom_severity_dict,
    'description_dict': description_dict,
    'precaution_dict': precaution_dict,
    'disease_severity_dict': disease_severity_dict,
    'feature_importance': feature_importance
}

with open('model_data.pkl', 'wb') as f:
    pickle.dump(model_data, f)

print("\nModel and data saved successfully!")
print("Files created:")
print("  - random_forest_model.pkl")
print("  - model_data.pkl")

# Test prediction function
print("\n" + "="*80)
print("TESTING PREDICTION SYSTEM")
print("="*80)

def predict_disease(symptoms_list):
    """
    Predict disease based on input symptoms
    
    Parameters:
    symptoms_list: List of symptoms (strings)
    
    Returns:
    Dictionary with disease, description, precautions, and severity
    """
    # Create feature vector
    feature_vector = [0] * len(all_symptoms)
    
    for symptom in symptoms_list:
        symptom = symptom.strip().lower().replace(' ', '_')
        # Find matching symptom
        for idx, existing_symptom in enumerate(all_symptoms):
            if existing_symptom.lower() == symptom:
                feature_vector[idx] = 1
                break
    
    # Predict
    prediction = rf_classifier.predict([feature_vector])[0]
    prediction_proba = rf_classifier.predict_proba([feature_vector])[0]
    confidence = max(prediction_proba) * 100
    
    # Get disease information
    result = {
        'disease': prediction,
        'confidence': round(confidence, 2),
        'description': description_dict.get(prediction, 'No description available'),
        'precautions': precaution_dict.get(prediction, []),
        'severity': disease_severity_dict.get(prediction, 0)
    }
    
    return result

# Test with sample symptoms
test_cases = [
    ['itching', 'skin_rash', 'nodal_skin_eruptions'],
    ['continuous_sneezing', 'shivering', 'chills'],
    ['stomach_pain', 'acidity', 'vomiting'],
    ['fatigue', 'weight_loss', 'restlessness', 'lethargy']
]

for i, test_symptoms in enumerate(test_cases, 1):
    print(f"\nTest Case {i}: {test_symptoms}")
    result = predict_disease(test_symptoms)
    print(f"Predicted Disease: {result['disease']}")
    print(f"Confidence: {result['confidence']}%")
    print(f"Severity Score: {result['severity']}")
    print(f"Description: {result['description']}")
    print(f"Precautions: {', '.join(result['precautions'])}")

print("\n" + "="*80)
print("Training and testing completed successfully!")
print("="*80)
