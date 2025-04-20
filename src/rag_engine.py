import pandas as pd
import numpy as np
import faiss
import os
from typing import List, Dict, Tuple, Any, Optional
from sentence_transformers import SentenceTransformer
import pickle
import re

class SchoolDocument:
    """
    Represents a document containing information about a school,
    which can be used for retrieval and context building.
    """
    def __init__(self, 
                 school_name: str, 
                 content: str, 
                 metadata: Optional[Dict[str, Any]] = None):
        self.school_name = school_name
        self.content = content
        self.metadata = metadata or {}
    
    def __str__(self):
        return f"{self.school_name}: {self.content}"

class RAGEngine:
    """
    Retrieval-Augmented Generation engine for the Boston School Chatbot.
    This class handles the embedding, indexing, and retrieval of school information
    to provide context-relevant responses.
    """
    
    def __init__(self, embedding_model: str = "all-MiniLM-L6-v2"):
        """
        Initialize the RAG engine with a sentence transformer model for embeddings.
        
        Args:
            embedding_model: The HuggingFace model ID to use for embeddings
        """
        self.embedding_model = SentenceTransformer(embedding_model)
        self.documents = []
        self.embeddings = None
        self.faiss_index = None
        self.index_built = False
        
    def process_school_data(self, 
                           school_csv: str = 'BPS.csv',
                           programs_csv: str = 'BPS-special-programs.csv') -> List[SchoolDocument]:
        """
        Process school data from CSV files and create document objects.
        
        Args:
            school_csv: Path to the school data CSV
            programs_csv: Path to the special programs CSV
            
        Returns:
            List of SchoolDocument objects
        """
        # Load both datasets
        schools_df = pd.read_csv(school_csv)
        programs_df = pd.read_csv(programs_csv)
        
        # Merge on School Name
        merged_df = pd.merge(schools_df, programs_df, on="School Name", how="left")
        
        # Create documents for each school
        documents = []
        
        for _, row in merged_df.iterrows():
            school_name = row["School Name"]
            
            # Extract address components to identify the neighborhood
            address = row["Address"] if "Address" in row else ""
            zip_code = ""
            neighborhood = ""
            
            if address:
                # Extract zip code from address
                zip_match = re.search(r'MA\s+(\d{5})', address)
                if zip_match:
                    zip_code = zip_match.group(1)
                
                # Extract neighborhood from address
                neighborhood_match = re.search(r'([A-Za-z\s]+),\s+MA', address)
                if neighborhood_match:
                    neighborhood = neighborhood_match.group(1).strip()
            
            # Collect all programs marked "Yes"
            programs_offered = []
            for col in programs_df.columns[1:]:
                if row.get(col) == "Yes":
                    programs_offered.append(col)
            
            # Create the content string
            content = f"{school_name} is a {row.get('School Type', 'N/A')} school serving grades {row.get('Grades Served', 'N/A')}."
            
            if address:
                content += f" Located at {address}."
            
            if programs_offered:
                # Format program names to be more readable
                readable_programs = [p.replace('_', ' ').title() for p in programs_offered]
                content += f" Special programs include: {', '.join(readable_programs)}."
            
            # Create metadata
            metadata = {
                "grades": row.get("Grades Served", ""),
                "type": row.get("School Type", ""),
                "address": address,
                "zip_code": zip_code,
                "neighborhood": neighborhood,
                "programs": programs_offered,
                "phone": row.get("Phone Number", "") if "Phone Number" in row else "",
                "email": row.get("Email Address", "") if "Email Address" in row else ""
            }
            
            # Create document
            doc = SchoolDocument(school_name, content, metadata)
            documents.append(doc)
        
        self.documents = documents
        return documents
    
    def build_index(self, save_path: Optional[str] = None) -> None:
        """
        Build the FAISS index for fast similarity search.
        
        Args:
            save_path: Optional path to save the index and documents
        """
        if not self.documents:
            raise ValueError("No documents to index. Call process_school_data first.")
        
        # Create text chunks for embedding
        texts = [doc.content for doc in self.documents]
        
        # Generate embeddings
        embeddings = self.embedding_model.encode(texts)
        self.embeddings = embeddings.astype('float32')
        
        # Build the FAISS index
        dimension = self.embeddings.shape[1]
        self.faiss_index = faiss.IndexFlatL2(dimension)
        self.faiss_index.add(self.embeddings)
        self.index_built = True
        
        # Save if a path is provided
        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(f"{save_path}_documents.pkl", "wb") as f:
                pickle.dump(self.documents, f)
            with open(f"{save_path}_embeddings.pkl", "wb") as f:
                pickle.dump(self.embeddings, f)
            faiss.write_index(self.faiss_index, f"{save_path}_faiss.index")
    
    def load_index(self, load_path: str) -> None:
        """
        Load a previously built index from disk.
        
        Args:
            load_path: Path prefix for the saved files
        """
        with open(f"{load_path}_documents.pkl", "rb") as f:
            self.documents = pickle.load(f)
        with open(f"{load_path}_embeddings.pkl", "rb") as f:
            self.embeddings = pickle.load(f)
        self.faiss_index = faiss.read_index(f"{load_path}_faiss.index")
        self.index_built = True
    
    def retrieve(self, query: str, top_k: int = 3) -> List[SchoolDocument]:
        """
        Retrieve the most relevant documents for a given query.
        
        Args:
            query: The user's query
            top_k: Number of documents to retrieve
            
        Returns:
            List of the most relevant school documents
        """
        if not self.index_built:
            raise ValueError("Index not built. Call build_index first.")
        
        # Encode the query
        query_embedding = self.embedding_model.encode([query])
        query_embedding = query_embedding.astype('float32')
        
        # Search the index
        distances, indices = self.faiss_index.search(query_embedding, top_k)
        
        # Return the relevant documents
        relevant_docs = [self.documents[idx] for idx in indices[0]]
        return relevant_docs
    
    def format_retrieved_context(self, docs: List[SchoolDocument]) -> str:
        """
        Format retrieved documents into a context string for the model.
        
        Args:
            docs: List of retrieved school documents
            
        Returns:
            Formatted context string
        """
        context = "# RETRIEVED_SCHOOLS\n"
        for i, doc in enumerate(docs, 1):
            context += f"{i}. {doc.content}\n"
            
            # Add metadata details that might be helpful
            if doc.metadata.get("phone"):
                context += f"   Phone: {doc.metadata['phone']}\n"
            if doc.metadata.get("email"):
                context += f"   Email: {doc.metadata['email']}\n"
            
        return context 