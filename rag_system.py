import pandas as pd
import numpy as np
import pickle
import os
from sentence_transformers import SentenceTransformer
import faiss
from typing import List, Dict, Tuple

class MedicalRAG:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """Initialize RAG system with embedding model"""
        self.embedding_model = SentenceTransformer(model_name)
        self.index = None
        self.documents = []
        self.metadata = []
        
    def load_medical_knowledge(self):
        """Load and process medical datasets into knowledge base"""
        documents = []
        metadata = []
        
        # Load datasets
        try:
            df_dataset = pd.read_csv('dataset/dataset.csv')
            df_description = pd.read_csv('dataset/symptom_Description.csv')
            df_precaution = pd.read_csv('dataset/symptom_precaution.csv')
            df_severity = pd.read_csv('dataset/Symptom-severity.csv')
            
            # Process disease descriptions
            for _, row in df_description.iterrows():
                disease = row['Disease']
                description = row['Description']
                
                doc_text = f"Disease: {disease}\nDescription: {description}"
                documents.append(doc_text)
                metadata.append({
                    'type': 'description',
                    'disease': disease,
                    'content': description
                })
            
            # Process disease symptoms
            for _, row in df_dataset.iterrows():
                disease = row['Disease']
                symptoms = [str(row[col]) for col in df_dataset.columns[1:] 
                           if pd.notna(row[col]) and str(row[col]) != 'nan']
                
                if symptoms:
                    symptoms_text = ', '.join(symptoms)
                    doc_text = f"Disease: {disease}\nSymptoms: {symptoms_text}"
                    documents.append(doc_text)
                    metadata.append({
                        'type': 'symptoms',
                        'disease': disease,
                        'symptoms': symptoms
                    })
            
            # Process precautions
            for _, row in df_precaution.iterrows():
                disease = row['Disease']
                precautions = [str(row[f'Precaution_{i}']) for i in range(1, 5) 
                              if pd.notna(row[f'Precaution_{i}'])]
                
                if precautions:
                    precautions_text = ', '.join(precautions)
                    doc_text = f"Disease: {disease}\nPrecautions: {precautions_text}"
                    documents.append(doc_text)
                    metadata.append({
                        'type': 'precautions',
                        'disease': disease,
                        'precautions': precautions
                    })
            
            # Process symptom severity
            severity_info = []
            for _, row in df_severity.iterrows():
                symptom = row['Symptom']
                weight = row['weight']
                severity_level = 'mild' if weight < 3 else 'moderate' if weight < 5 else 'severe'
                
                doc_text = f"Symptom: {symptom}\nSeverity: {severity_level} (weight: {weight})"
                documents.append(doc_text)
                metadata.append({
                    'type': 'severity',
                    'symptom': symptom,
                    'weight': weight,
                    'severity_level': severity_level
                })
            
            self.documents = documents
            self.metadata = metadata
            
            print(f"Loaded {len(documents)} documents into knowledge base")
            return True
            
        except Exception as e:
            print(f"Error loading medical knowledge: {e}")
            return False
    
    def build_index(self):
        """Build FAISS index from documents"""
        if not self.documents:
            print("No documents loaded. Call load_medical_knowledge() first.")
            return False
        
        print("Generating embeddings...")
        embeddings = self.embedding_model.encode(
            self.documents, 
            show_progress_bar=True,
            convert_to_numpy=True
        )
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        
        # Create FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)  # Inner product = cosine similarity
        self.index.add(embeddings)
        
        print(f"Built FAISS index with {self.index.ntotal} vectors")
        return True
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search for relevant documents"""
        if self.index is None:
            return []
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query], convert_to_numpy=True)
        faiss.normalize_L2(query_embedding)
        
        # Search
        scores, indices = self.index.search(query_embedding, top_k)
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.documents):
                results.append({
                    'document': self.documents[idx],
                    'metadata': self.metadata[idx],
                    'score': float(score)
                })
        
        return results
    
    def get_context_for_query(self, query: str, top_k: int = 5) -> str:
        """Get formatted context for LLM based on query"""
        results = self.search(query, top_k)
        
        if not results:
            return ""
        
        context_parts = ["Here is relevant medical information from the knowledge base:\n"]
        
        for i, result in enumerate(results, 1):
            context_parts.append(f"\n{i}. {result['document']}")
        
        context_parts.append("\n\nPlease use this information to provide an accurate and helpful response.")
        
        return '\n'.join(context_parts)
    
    def save(self, filepath: str = 'rag_system.pkl'):
        """Save RAG system to file"""
        data = {
            'documents': self.documents,
            'metadata': self.metadata,
            'index': faiss.serialize_index(self.index) if self.index else None
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
        
        print(f"RAG system saved to {filepath}")
    
    def load(self, filepath: str = 'rag_system.pkl'):
        """Load RAG system from file"""
        try:
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
            
            self.documents = data['documents']
            self.metadata = data['metadata']
            
            if data['index'] is not None:
                self.index = faiss.deserialize_index(data['index'])
            
            print(f"RAG system loaded from {filepath}")
            return True
        except Exception as e:
            print(f"Error loading RAG system: {e}")
            return False


def initialize_rag_system():
    """Initialize and build RAG system"""
    print("Initializing Medical RAG System...")
    
    rag = MedicalRAG()
    
    # Load knowledge base
    if not rag.load_medical_knowledge():
        print("Failed to load medical knowledge")
        return None
    
    # Build index
    if not rag.build_index():
        print("Failed to build index")
        return None
    
    # Save for later use
    rag.save()
    
    print("RAG system initialized successfully!")
    return rag


if __name__ == '__main__':
    # Initialize RAG system
    rag = initialize_rag_system()
    
    # Test queries
    if rag:
        test_queries = [
            "What are the symptoms of diabetes?",
            "How to prevent heart disease?",
            "What causes fever and headache?"
        ]
        
        print("\n" + "="*80)
        print("Testing RAG System")
        print("="*80)
        
        for query in test_queries:
            print(f"\nQuery: {query}")
            print("-" * 80)
            context = rag.get_context_for_query(query, top_k=3)
            print(context)
            print()
