import os
from google import genai
from google.genai import types
import streamlit as st

class AIGenerator:
    """Handles AI-powered answer generation using Google Gemini"""
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY", "")
        if not api_key:
            st.error("GEMINI_API_KEY environment variable not found. Please set your API key.")
            st.stop()
        
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.5-flash"
    
    def generate_answer(self, question: str, subject: str, mode: str, 
                       custom_prompt: str = "", reference_content: str = "") -> str:
        """Generate an answer for a given question using AI"""
        
        try:
            # Construct the prompt based on mode and subject
            prompt = self._construct_prompt(
                question=question,
                subject=subject,
                mode=mode,
                custom_prompt=custom_prompt,
                reference_content=reference_content
            )
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            return response.text or "Unable to generate answer for this question."
            
        except Exception as e:
            st.error(f"Error generating answer: {str(e)}")
            return f"Error generating answer: {str(e)}"
    
    def _construct_prompt(self, question: str, subject: str, mode: str, 
                         custom_prompt: str = "", reference_content: str = "") -> str:
        """Construct a sophisticated prompt for the AI model"""
        
        # Base instruction for 8-mark college-level answers
        base_instruction = f"""
You are an expert academic assistant specializing in {subject}. 
Generate a comprehensive answer for the following college-level question worth 8 marks.

The answer should be:
- Well-structured with clear headings and subheadings
- Include key terms in **bold** and important concepts in *italics*
- Use bullet points and numbered lists where appropriate
- Maintain academic rigor and accuracy
- Be approximately 400-600 words for an 8-mark question
"""
        
        # Mode-specific instructions
        if mode == "Understand Mode":
            mode_instruction = """
ANSWER GENERATION MODE: UNDERSTAND MODE
- Provide detailed explanations with analogies and real-world examples
- Use simpler language where appropriate for foundational understanding
- Include step-by-step breakdowns of complex concepts
- Add background context and theoretical foundations
- Use illustrative examples to clarify difficult points
- Focus on building comprehensive understanding
"""
        else:  # Exam Mode
            mode_instruction = """
ANSWER GENERATION MODE: EXAM MODE
- Provide concise, highly focused answers with direct key points
- Use formal academic language appropriate for examinations
- Minimize verbose examples or extensive background explanations
- Structure answers for maximum marks in minimum words
- Include only the most relevant information for exam success
- Format for quick review and memorization
"""
        
        # Subject-specific guidelines
        subject_guidelines = self._get_subject_guidelines(subject)
        
        # Reference content section
        reference_section = ""
        if reference_content.strip():
            reference_section = f"""
REFERENCE MATERIAL:
Use the following college notes as additional context when relevant:
{reference_content[:1500]}...

"""
        
        # Custom prompt section
        custom_section = ""
        if custom_prompt.strip():
            custom_section = f"""
ADDITIONAL INSTRUCTIONS:
{custom_prompt}

"""
        
        # Construct final prompt
        final_prompt = f"""
{base_instruction}

{mode_instruction}

{subject_guidelines}

{reference_section}

{custom_section}

QUESTION TO ANSWER:
{question}

Please provide a comprehensive, well-formatted answer following all the above guidelines.
"""
        
        return final_prompt
    
    def _get_subject_guidelines(self, subject: str) -> str:
        """Get subject-specific guidelines for answer generation"""
        
        guidelines = {
            "Mathematics": """
SUBJECT-SPECIFIC GUIDELINES FOR MATHEMATICS:
- Include step-by-step mathematical derivations
- Show all calculation steps clearly
- Use proper mathematical notation and symbols
- Include diagrams or geometric explanations where relevant
- Provide alternative solution methods when applicable
- Verify answers with examples or proofs
""",
            "Physics": """
SUBJECT-SPECIFIC GUIDELINES FOR PHYSICS:
- Include relevant physical laws and principles
- Show mathematical derivations and unit analysis
- Explain physical intuition behind concepts
- Include real-world applications and examples
- Draw diagrams for physical systems when helpful
- Connect theory to experimental observations
""",
            "Computer Science": """
SUBJECT-SPECIFIC GUIDELINES FOR COMPUTER SCIENCE:
- Include code examples and algorithms where relevant
- Explain time and space complexity
- Provide practical implementation details
- Include system design considerations
- Explain both theoretical and practical aspects
- Use proper technical terminology
""",
            "History": """
SUBJECT-SPECIFIC GUIDELINES FOR HISTORY:
- Provide chronological context and timelines
- Include specific dates, names, and locations
- Explain cause-and-effect relationships
- Consider multiple perspectives and interpretations
- Include primary source references when relevant
- Connect events to broader historical patterns
""",
            "Literature": """
SUBJECT-SPECIFIC GUIDELINES FOR LITERATURE:
- Include textual evidence and quotations
- Analyze literary devices and techniques
- Consider historical and cultural context
- Discuss themes, characters, and symbolism
- Include critical perspectives and interpretations
- Connect to broader literary movements
""",
            "Chemistry": """
SUBJECT-SPECIFIC GUIDELINES FOR CHEMISTRY:
- Include chemical equations and reactions
- Explain molecular structures and bonding
- Provide step-by-step reaction mechanisms
- Include experimental procedures and observations
- Discuss practical applications and real-world relevance
- Use proper chemical nomenclature
""",
            "Biology": """
SUBJECT-SPECIFIC GUIDELINES FOR BIOLOGY:
- Include biological processes and mechanisms
- Explain structure-function relationships
- Provide examples from different organisms
- Include evolutionary and ecological perspectives
- Discuss experimental evidence and methods
- Connect molecular to organismal levels
""",
            "Economics": """
SUBJECT-SPECIFIC GUIDELINES FOR ECONOMICS:
- Include economic models and graphs
- Explain market mechanisms and behaviors
- Provide real-world economic examples
- Discuss policy implications
- Include quantitative analysis where relevant
- Consider multiple economic perspectives
""",
            "Psychology": """
SUBJECT-SPECIFIC GUIDELINES FOR PSYCHOLOGY:
- Include psychological theories and research
- Explain cognitive and behavioral processes
- Provide experimental evidence and studies
- Discuss practical applications
- Consider individual and cultural differences
- Include ethical considerations
""",
            "Engineering": """
SUBJECT-SPECIFIC GUIDELINES FOR ENGINEERING:
- Include technical specifications and calculations
- Explain design principles and constraints
- Provide practical implementation details
- Discuss safety and efficiency considerations
- Include system analysis and optimization
- Connect theory to real-world applications
"""
        }
        
        return guidelines.get(subject, """
GENERAL ACADEMIC GUIDELINES:
- Maintain academic rigor and scholarly approach
- Include relevant theories and concepts
- Provide evidence-based explanations
- Consider practical applications
- Use appropriate academic terminology
""")
