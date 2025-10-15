# Disease Prediction System using Random Forest

This project implements a machine learning-based disease prediction system that predicts diseases based on symptoms and provides information about severity, precautions, and descriptions.

## Features

- **Disease Prediction**: Predicts diseases based on input symptoms with confidence scores
- **Multiple Predictions**: Returns top 3 most likely diseases
- **Severity Assessment**: Provides severity levels (Mild, Moderate, Severe, Critical)
- **Precautions**: Lists recommended precautions for each disease
- **Disease Descriptions**: Provides detailed descriptions of diseases
- **Symptom Search**: Search and explore available symptoms
- **Interactive Interface**: User-friendly command-line interface

## Project Structure

```
chatbot/
├── dataset/
│   ├── dataset.csv                  # Main dataset with diseases and symptoms
│   ├── symptom_Description.csv      # Disease descriptions
│   ├── symptom_precaution.csv       # Disease precautions
│   └── Symptom-severity.csv         # Symptom severity weights
├── trainmodel.py                    # Model training script
├── ai.py                            # Prediction system and interface
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install pandas numpy scikit-learn
```

## Usage

### Step 1: Train the Model

First, train the Random Forest model using the provided datasets:

```bash
python trainmodel.py
```

This will:
- Load and preprocess all datasets
- Train a Random Forest classifier with 200 estimators
- Evaluate the model on test data
- Save the trained model as `random_forest_model.pkl`
- Save model data as `model_data.pkl`
- Display training/testing accuracy and feature importance

### Step 2: Use the Prediction System

After training, use the interactive prediction system:

```bash
python ai.py
```

The system provides several options:
1. **Predict disease from symptoms**: Enter symptoms to get disease predictions
2. **Search symptoms**: Find available symptoms in the database
3. **Get disease information**: Look up information about a specific disease
4. **Show top important symptoms**: View the most important symptoms for prediction
5. **Exit**: Close the application

### Example Usage

#### Predicting a Disease

Input symptoms (comma-separated):
```
itching, skin_rash, nodal_skin_eruptions
```

Output:
```
1. FUNGAL INFECTION
   Confidence: 95.5%
   Severity: Moderate (Score: 2.0)
   Description: A fungal infection is an invasion of the skin or nails by a fungus...
   Precautions:
      1. bath twice
      2. use detol or neem in bathing water
      3. keep infected area dry
      4. use clean cloths
```

## Model Details

### Algorithm
- **Model**: Random Forest Classifier
- **Estimators**: 200 trees
- **Max Depth**: 20
- **Criterion**: Gini impurity

### Features
- Binary encoding of symptoms (presence/absence)
- Total unique symptoms: ~130+
- Total diseases: 40+

### Performance
- Training Accuracy: ~99%
- Testing Accuracy: ~98%

## Dataset Information

### dataset.csv
- Contains diseases with up to 17 associated symptoms
- Each row represents a disease-symptom combination

### symptom_Description.csv
- Provides detailed descriptions for each disease

### symptom_precaution.csv
- Lists 4 precautions for each disease

### Symptom-severity.csv
- Assigns severity weights to each symptom (1-5 scale)
- Used to calculate overall disease severity

## Severity Levels

- **Mild**: Score < 2
- **Moderate**: Score 2-3
- **Severe**: Score 3-4
- **Critical**: Score 4+

## Sample Diseases Covered

- Fungal infection
- Allergy
- GERD (Gastroesophageal reflux disease)
- Diabetes
- Hypertension
- Migraine
- AIDS
- Malaria
- Tuberculosis
- Pneumonia
- And many more...

## Notes

- Symptom names should use underscores (e.g., `skin_rash` instead of `skin rash`)
- The system is case-insensitive for symptom matching
- Multiple symptoms improve prediction accuracy
- This system is for educational purposes and should not replace professional medical diagnosis

## Future Enhancements

- Web-based interface
- More advanced ML models (XGBoost, Neural Networks)
- Real-time symptom tracking
- Integration with medical databases
- Multi-language support

## License

This project is for educational purposes.

## Disclaimer

⚠️ **Important**: This system is designed for educational and informational purposes only. It should NOT be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider for medical concerns.
"# medicalchatbot" 
