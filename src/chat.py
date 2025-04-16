from huggingface_hub import InferenceClient
from config import BASE_MODEL, MY_MODEL, HF_TOKEN
import pandas as pd
import os
from src.rag_engine import RAGEngine, SchoolDocument

class SchoolChatbot:
    """
    This class is extra scaffolding around a model. Modify this class to specify how the model recieves prompts and generates responses.

    Example usage:
        chatbot = SchoolChatbot()
        response = chatbot.get_response("What schools offer Spanish programs?")
    """

    def __init__(self, school_csv='BPS.csv', programs_csv='BPS-special-programs.csv'):
        """
        Initialize the chatbot with a HF model ID
        """
        model_id = MY_MODEL if MY_MODEL else BASE_MODEL # define MY_MODEL in config.py if you create a new model in the HuggingFace Hub
        self.client = InferenceClient(model=model_id, token=HF_TOKEN)
        self.school_csv = school_csv
        self.programs_csv = programs_csv
        
        # Initialize the RAG engine
        self.rag_engine = RAGEngine()
        
        # Set up the RAG index
        self._setup_rag()

    def _setup_rag(self):
        """
        Set up the RAG engine by either loading a pre-built index or building a new one.
        """
        index_dir = 'models'
        index_path = os.path.join(index_dir, 'school_rag')
        
        # Check if index files exist
        if (os.path.exists(f"{index_path}_documents.pkl") and 
            os.path.exists(f"{index_path}_embeddings.pkl") and 
            os.path.exists(f"{index_path}_faiss.index")):
            # Load existing index
            try:
                self.rag_engine.load_index(index_path)
                print("Loaded existing RAG index.")
                return
            except Exception as e:
                print(f"Error loading index: {e}. Building new index...")
        
        # Build new index
        os.makedirs(index_dir, exist_ok=True)
        self.rag_engine.process_school_data(self.school_csv, self.programs_csv)
        self.rag_engine.build_index(index_path)
        print("Built and saved new RAG index.")

    @staticmethod
    def load_age_cutoffs(filepath='age_cutoffs_2025.txt'):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return "# AGE_CUTOFFS\n<Error: age cutoff file not found>"
        
    @staticmethod
    def format_school_data(
        school_csv='BPS.csv',
        programs_csv='BPS-special-programs.csv',
    ):
        """
        Merges main school data with special program indicators and formats it for in-context prompting.

        Args:
            school_csv (str): Path to the main school data CSV.
            programs_csv (str): Path to the special programs CSV.
            max_schools (int or None): Max number of schools to include.

        Returns:
            str: Formatted string for # SCHOOL_DATA section.
        """
        try:
            # Load both datasets
            schools_df = pd.read_csv(school_csv)
            programs_df = pd.read_csv(programs_csv)

            # Merge on School Name
            merged_df = pd.merge(schools_df, programs_df, on="School Name", how="left")

            # Use more concise formatting
            school_lines = []
            for _, row in merged_df.iterrows():
                # Collect all programs marked "Yes"
                programs_offered = [col for col in programs_df.columns[1:] if row.get(col, "") == "Yes"]
                programs_str = "Y" if programs_offered else "N"

                school_lines.append(
                    f'- {row["School Name"]}: {row["Grades Served"]}, {row["School Type"]}, {programs_str}'
                )    
            school_lines = list(set(school_lines))  # Remove duplicates
            return "# SCHOOL_DATA\n" + "\n".join(school_lines)

        except Exception as e:
            return f"# SCHOOL_DATA\n<Error loading or merging data: {e}>"

        
    def format_prompt(self, user_input):
        """
        Format the user's input into a proper prompt using RAG to retrieve relevant context.
        
        Args:
            user_input (str): The user's question about Boston schools

        Returns:
            str: A formatted prompt ready for the model
        """
        system_message = """You are a helpful and accurate school enrollment assistant for Boston Public Schools (BPS).
        You can provide information about school options, locations, programs, and other details
        to help families make informed decisions about their children's education.
        
        Provide clear, fact-based, and non-misleading information using the data provided below.
        Focus on answering only the user's specific question using the relevant school information.
        
        When answering questions about specific schools, neighborhoods, or programs, prioritize information 
        from the RETRIEVED_SCHOOLS section, which contains the most relevant schools for the user's query.

        DO NOT make up or hallucinate any school information.

        If the retrieved schools don't match what the user is looking for, acknowledge this limitation
        and suggest they contact BPS directly at (617) 635-9010 for more information.
        """

        age_cutoffs_section = SchoolChatbot.load_age_cutoffs()

        transportation_section = """# TRANSPORTATION_ELIGIBILITY
        - K0–K1: Bus eligible if >0.75 miles from school
        - K2–5: Bus eligible if >1 mile
        - Grades 6–8: Bus eligible if >1.5 miles
        - Grades 9–12: MBTA pass provided
        """
        
        # Instead of including all school data, retrieve relevant schools using RAG
        retrieved_docs = self.rag_engine.retrieve(user_input, top_k=3)
        retrieved_context = self.rag_engine.format_retrieved_context(retrieved_docs)
        
        # Comment out the full dataset reference to reduce token usage
        # school_data_section = SchoolChatbot.format_school_data(
        #     school_csv=self.school_csv,
        #     programs_csv=self.programs_csv,
        # )

        examples_section = """# EXAMPLES
            User: My child is turning 5 on August 15 and we live in 02124. What grade can they enter, and what schools are available?
            Assistant: Since your child turns 5 before September 1, they are eligible for K2. Based on your zip code (02124), eligible schools may include Joseph Lee K-8, Mildred Avenue, and TechBoston Academy.
            """

        # Combine all sections into the final prompt
        # f"{school_data_section}\n"  # Comment out the full dataset section
        prompt = (
            f"<|system|>\n{system_message}\n"
            f"{age_cutoffs_section}\n"
            f"{transportation_section}\n"
            f"{retrieved_context}\n"
            f"{examples_section}\n"
            f"<|user|>\n{user_input}\n<|assistant|>\n"
        )

        print(prompt)
        return prompt
    

        
    def get_response(self, user_input):
        """
        Generate responses to user questions using RAG and the language model.
        
        Args:
            user_input (str): The user's question about Boston schools

        Returns:
            str: The chatbot's response
        """
        prompt = self.format_prompt(user_input)
        
        # Generate response using the model
        response = self.client.text_generation(
            prompt,
            max_new_tokens=512,
            temperature=0.7,
            do_sample=True,
            repetition_penalty=1.1
        )
        
        return response

