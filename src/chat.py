from huggingface_hub import InferenceClient
from config import BASE_MODEL, MY_MODEL, HF_TOKEN
import pandas as pd

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
        max_schools=None
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

            # Merge on School Name (ensure consistency in casing/whitespace if needed)
            merged_df = pd.merge(schools_df, programs_df, on="School Name", how="left")

            # Optionally limit number of rows
            if max_schools:
                merged_df = merged_df.head(max_schools)

            school_lines = []
            for _, row in merged_df.iterrows():
                # Collect all programs marked "Yes"
                programs_offered = [col for col in programs_df.columns[1:] if row.get(col, "") == "Yes"]
                programs_str = ", ".join(programs_offered) if programs_offered else "None"

                school_lines.append(
                    f'- "{row["School Name"]}":\n'
                    f'    Address: {row["Address"]}\n'
                    f'    Grades: {row["Grades Served"]}\n'
                    f'    Type: {row["School Type"]}\n'
                    f'    Contact: {row["Email Address"]}, {row["Phone Number"]}\n'
                    f'    Programs: {programs_str}'
                )

            return "# SCHOOL_DATA\n" + "\n".join(school_lines)

        except Exception as e:
            return f"# SCHOOL_DATA\n<Error loading or merging data: {e}>"

        
    def format_prompt(self, user_input):
        """
        TODO: Implement this method to format the user's input into a proper prompt.
        
        This method should:
        1. Add any necessary system context or instructions
        2. Format the user's input appropriately
        3. Add any special tokens or formatting the model expects

        Args:
            user_input (str): The user's question about Boston schools

        Returns:
            str: A formatted prompt ready for the model
        
        Example prompt format:
            "You are a helpful assistant that specializes in Boston schools...
             User: {user_input}
             Assistant:"
        """
        system_message = """You are a helpful and accurate school enrollment assistant for Boston Public Schools (BPS).
        You can provide information about school options, locations, programs, and other details
        to help families make informed decisions about their children's education, and use the information below.
        Provide clear, fact-based, and non-misleading information using official rules and requirements. If uncertain, 
        politely advise users to consult the official Boston Public Schools (BPS) website or contact BPS directly at (617) 635-9010.
        """

        age_cutoffs_section = SchoolChatbot.load_age_cutoffs()

        transportation_section = """# TRANSPORTATION_ELIGIBILITY
        - K0–K1: Bus eligible if >0.75 miles from school
        - K2–5: Bus eligible if >1 mile
        - Grades 6–8: Bus eligible if >1.5 miles
        - Grades 9–12: MBTA pass provided
        """

        school_data_section = SchoolChatbot.format_school_data(
            school_csv=self.school_csv,
            programs_csv=self.programs_csv,
            max_schools=30
        )

        examples_section = """# EXAMPLES
            User: My child is turning 5 on August 15 and we live in 02124. What grade can they enter, and what schools are available?
            Assistant: Since your child turns 5 before September 1, they are eligible for K2. Based on your zip code (02124), eligible schools may include Joseph Lee K-8, Mildred Avenue, and TechBoston Academy.

            User: My daughter is 4 but her birthday is in October. Can she attend K1?
            Assistant: Children must be 4 years old on or before September 1 to attend K1. Since your daughter’s birthday is in October, she would not be eligible this year.

            User: What school options are available in 02118?
            Assistant: Families in 02118 may be eligible for schools like Hurley K-8, Blackstone Innovation School, and O'Bryant Exam School, depending on the child’s grade level and test eligibility.
            """

        # Combine all sections into the final prompt
        prompt = (
            f"<|system|>\n{system_message}\n"
            f"{age_cutoffs_section}\n"
            f"{transportation_section}\n"
            f"{school_data_section}\n"
            f"{examples_section}\n"
            f"<|user|>\n{user_input}\n<|assistant|>\n"
        )

        return prompt
    

        
    def get_response(self, user_input):
        """
        TODO: Implement this method to generate responses to user questions.
        
        This method should:
        1. Use format_prompt() to prepare the input
        2. Generate a response using the model
        3. Clean up and return the response

        Args:
            user_input (str): The user's question about Boston schools

        Returns:
            str: The chatbot's response

        Implementation tips:
        - Use self.format_prompt() to format the user's input
        - Use self.client to generate responses
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

