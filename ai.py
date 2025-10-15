import pickle
import numpy as np
import warnings
warnings.filterwarnings('ignore')

class DiseasePredictionSystem:
    """
    Disease Prediction System using trained Random Forest model
    """
    
    def __init__(self):
        """Load the trained model and data"""
        print("Loading model and data...")
        
        # Load the trained model
        with open('random_forest_model.pkl', 'rb') as f:
            self.model = pickle.load(f)
        
        # Load the model data
        with open('model_data.pkl', 'rb') as f:
            model_data = pickle.load(f)
        
        self.all_symptoms = model_data['all_symptoms']
        self.symptom_severity_dict = model_data['symptom_severity_dict']
        self.description_dict = model_data['description_dict']
        self.precaution_dict = model_data['precaution_dict']
        self.disease_severity_dict = model_data['disease_severity_dict']
        self.feature_importance = model_data['feature_importance']
        
        print("Model loaded successfully!")
        print(f"Total symptoms in database: {len(self.all_symptoms)}")
        print(f"Total diseases: {len(self.description_dict)}")
    
    def get_all_symptoms(self):
        """Return list of all available symptoms"""
        return self.all_symptoms
    
    def search_symptoms(self, query):
        """
        Search for symptoms matching the query
        
        Parameters:
        query: Search string
        
        Returns:
        List of matching symptoms
        """
        query = query.lower()
        matching_symptoms = [s for s in self.all_symptoms if query in s.lower()]
        return matching_symptoms
    
    def predict_disease(self, symptoms_list, top_n=3):
        """
        Predict disease based on input symptoms
        
        Parameters:
        symptoms_list: List of symptoms (strings)
        top_n: Number of top predictions to return
        
        Returns:
        List of dictionaries with disease predictions and information
        """
        # Create feature vector
        feature_vector = [0] * len(self.all_symptoms)
        matched_symptoms = []
        unmatched_symptoms = []
        
        for symptom in symptoms_list:
            symptom = symptom.strip().lower().replace(' ', '_')
            matched = False
            
            # Find matching symptom
            for idx, existing_symptom in enumerate(self.all_symptoms):
                if existing_symptom.lower() == symptom:
                    feature_vector[idx] = 1
                    matched_symptoms.append(existing_symptom)
                    matched = True
                    break
            
            if not matched:
                unmatched_symptoms.append(symptom)
        
        # Check if any symptoms were matched
        if sum(feature_vector) == 0:
            return {
                'error': 'No matching symptoms found',
                'matched_symptoms': matched_symptoms,
                'unmatched_symptoms': unmatched_symptoms
            }
        
        # Predict probabilities
        prediction_proba = self.model.predict_proba([feature_vector])[0]
        
        # Get top N predictions
        top_indices = np.argsort(prediction_proba)[::-1][:top_n]
        classes = self.model.classes_
        
        results = []
        for idx in top_indices:
            disease = classes[idx]
            confidence = prediction_proba[idx] * 100
            
            # Get disease information
            disease_info = {
                'disease': disease,
                'confidence': round(confidence, 2),
                'description': self.description_dict.get(disease, 'No description available'),
                'precautions': self.precaution_dict.get(disease, []),
                'severity_score': self.disease_severity_dict.get(disease, 0),
                'severity_level': self._get_severity_level(self.disease_severity_dict.get(disease, 0))
            }
            results.append(disease_info)
        
        return {
            'predictions': results,
            'matched_symptoms': matched_symptoms,
            'unmatched_symptoms': unmatched_symptoms,
            'total_symptoms_provided': len(symptoms_list)
        }
    
    def _get_severity_level(self, severity_score):
        """Convert severity score to severity level"""
        if severity_score < 2:
            return "Mild"
        elif severity_score < 3:
            return "Moderate"
        elif severity_score < 4:
            return "Severe"
        else:
            return "Critical"
    
    def get_symptom_severity(self, symptom):
        """Get severity weight of a symptom"""
        symptom = symptom.strip().lower().replace(' ', '_')
        for s in self.all_symptoms:
            if s.lower() == symptom:
                return self.symptom_severity_dict.get(s, 0)
        return None
    
    def get_disease_info(self, disease_name):
        """Get complete information about a disease"""
        return {
            'disease': disease_name,
            'description': self.description_dict.get(disease_name, 'Not found'),
            'precautions': self.precaution_dict.get(disease_name, []),
            'severity_score': self.disease_severity_dict.get(disease_name, 0),
            'severity_level': self._get_severity_level(self.disease_severity_dict.get(disease_name, 0))
        }
    
    def get_top_important_symptoms(self, n=20):
        """Get top N most important symptoms"""
        return self.feature_importance.head(n)
    
    def extract_symptoms_from_message(self, message):
        """
        Extract symptoms from a natural language message
        
        Parameters:
        message: The user's message
        
        Returns:
        List of extracted symptoms
        """
        # First, try comma-separated parsing
        parts = [s.strip() for s in message.split(',') if s.strip()]
        if len(parts) > 1:
            return parts
        
        # Otherwise, find words that match known symptoms
        words = message.lower().split()
        matched = []
        symptom_names = [s.lower().replace('_', ' ') for s in self.all_symptoms]
        for word in words:
            if word in symptom_names:
                matched.append(word.replace(' ', '_'))
        return matched


def main():
    """Main function to demonstrate the prediction system"""
    
    # Initialize the system
    print("="*80)
    print("DISEASE PREDICTION SYSTEM")
    print("="*80)
    print()
    
    predictor = DiseasePredictionSystem()
    
    print("\n" + "="*80)
    print("INTERACTIVE PREDICTION MODE")
    print("="*80)
    
    while True:
        print("\nOptions:")
        print("1. Predict disease from symptoms")
        print("2. Search symptoms")
        print("3. Get disease information")
        print("4. Show top important symptoms")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            print("\nEnter symptoms (comma-separated):")
            print("Example: itching, skin_rash, vomiting")
            symptoms_input = input("Symptoms: ").strip()
            
            if not symptoms_input:
                print("No symptoms entered!")
                continue
            
            symptoms = [s.strip() for s in symptoms_input.split(',')]
            
            print(f"\nAnalyzing {len(symptoms)} symptoms...")
            result = predictor.predict_disease(symptoms, top_n=3)
            
            if 'error' in result:
                print(f"\nError: {result['error']}")
                if result['unmatched_symptoms']:
                    print(f"Unmatched symptoms: {', '.join(result['unmatched_symptoms'])}")
            else:
                print(f"\nMatched symptoms: {', '.join(result['matched_symptoms'])}")
                if result['unmatched_symptoms']:
                    print(f"Unmatched symptoms: {', '.join(result['unmatched_symptoms'])}")
                
                print(f"\n{'='*80}")
                print("TOP PREDICTIONS:")
                print('='*80)
                
                for i, pred in enumerate(result['predictions'], 1):
                    print(f"\n{i}. {pred['disease'].upper()}")
                    print(f"   Confidence: {pred['confidence']}%")
                    print(f"   Severity: {pred['severity_level']} (Score: {pred['severity_score']})")
                    print(f"   Description: {pred['description']}")
                    print(f"   Precautions:")
                    for j, precaution in enumerate(pred['precautions'], 1):
                        print(f"      {j}. {precaution}")
        
        elif choice == '2':
            query = input("\nEnter search term: ").strip()
            if query:
                matching = predictor.search_symptoms(query)
                if matching:
                    print(f"\nFound {len(matching)} matching symptoms:")
                    for symptom in matching[:20]:  # Show first 20
                        print(f"  - {symptom}")
                    if len(matching) > 20:
                        print(f"  ... and {len(matching) - 20} more")
                else:
                    print("No matching symptoms found!")
        
        elif choice == '3':
            disease = input("\nEnter disease name: ").strip()
            if disease:
                info = predictor.get_disease_info(disease)
                print(f"\nDisease: {info['disease']}")
                print(f"Description: {info['description']}")
                print(f"Severity: {info['severity_level']} (Score: {info['severity_score']})")
                print(f"Precautions:")
                for i, precaution in enumerate(info['precautions'], 1):
                    print(f"  {i}. {precaution}")
        
        elif choice == '4':
            print("\nTop 20 Most Important Symptoms:")
            top_symptoms = predictor.get_top_important_symptoms(20)
            for idx, row in top_symptoms.iterrows():
                print(f"  {row['Symptom']}: {row['Importance']:.4f}")
        
        elif choice == '5':
            print("\nThank you for using the Disease Prediction System!")
            break
        
        else:
            print("\nInvalid choice! Please enter 1-5.")


if __name__ == "__main__":
    main()
