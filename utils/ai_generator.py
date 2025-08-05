import os
import time
import asyncio
from typing import List, Dict
import google.generativeai as genai
import streamlit as st

class AIGenerator:
    """Handles AI-powered answer generation using Google Gemini"""
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY", "")
        if not api_key:
            st.error("GEMINI_API_KEY environment variable not found. Please set your API key.")
            st.stop()
        
        genai.configure(api_key=api_key)
        self.model = "gemini-1.5-flash"
        self.rate_limit_delay = 1.0  # Delay between requests (seconds)
        self.batch_size = 5  # Process questions in batches
        self.request_count = 0  # Track API requests
        self.max_requests_per_session = 60  # Conservative limit per session
    
    def generate_answer(self, question: str, subject: str, mode: str, 
                       custom_prompt: str = "", reference_content: str = "") -> str:
        """Generate an answer for a given question using AI with rate limiting"""
        
        # Construct the prompt based on mode and subject
        prompt = self._construct_prompt(
            question=question,
            subject=subject,
            mode=mode,
            custom_prompt=custom_prompt,
            reference_content=reference_content
        )
        
        try:
            # Check if we're approaching request limits
            if self.request_count >= self.max_requests_per_session:
                return f"Session request limit reached ({self.max_requests_per_session}). Please restart the app to continue."
            
            # Add rate limiting delay
            time.sleep(self.rate_limit_delay)
            
            # Track request
            self.request_count += 1
            
            model = genai.GenerativeModel(self.model)
            response = model.generate_content(prompt)
            
            return response.text or "Unable to generate answer for this question."
            
        except Exception as e:
            # Handle rate limiting and other API errors
            if "rate limit" in str(e).lower() or "quota" in str(e).lower():
                st.warning(f"API rate limit reached. Waiting 5 seconds before retry...")
                time.sleep(5)
                # Retry once
                try:
                    model = genai.GenerativeModel(self.model)
                    response = model.generate_content(prompt)
                    return response.text or "Unable to generate answer for this question."
                except Exception as retry_e:
                    return f"API limit exceeded. Please try again later. Error: {str(retry_e)}"
            else:
                st.error(f"Error generating answer: {str(e)}")
                return f"Error generating answer: {str(e)}"
    
    def generate_multi_question_answer(self, questions_batch: List[Dict], subject: str, mode: str,
                                      custom_prompt: str = "", reference_content: str = "") -> List[Dict]:
        """Generate answers for multiple questions in a single API call"""
        
        # Remove debug output for cleaner interface
        
        # Check if we're approaching request limits
        if self.request_count >= self.max_requests_per_session:
            return [{"question": q["question"], "answer": f"Session request limit reached ({self.max_requests_per_session}). Please restart the app to continue.", "question_number": q["question_number"]} for q in questions_batch]
        
        # Construct multi-question prompt
        multi_prompt = self._construct_multi_question_prompt(
            questions_batch=questions_batch,
            subject=subject,
            mode=mode,
            custom_prompt=custom_prompt,
            reference_content=reference_content
        )
        
        # Implement robust retry mechanism for API errors
        max_retries = 3
        base_delay = 2
        
        for attempt in range(max_retries):
            try:
                # Add rate limiting delay
                if attempt > 0:
                    # Exponential backoff for retries
                    delay = base_delay * (2 ** attempt)
                    st.info(f"Retrying API call (attempt {attempt + 1}/{max_retries}) after {delay} seconds...")
                    time.sleep(delay)
                else:
                    time.sleep(self.rate_limit_delay)
                
                # Track request
                self.request_count += 1
                
                model = genai.GenerativeModel(self.model)
                response = model.generate_content(multi_prompt)
                
                response_text = response.text or "Unable to generate answers for these questions."
                
                # Parse the response to extract individual answers
                parsed_answers = self._parse_multi_question_response(response_text, questions_batch)
                
                return parsed_answers
                
            except Exception as e:
                error_msg = str(e).lower()
                
                # Debug logging for Streamlit
                import streamlit as st
                st.write(f"API Error Debug: {str(e)}")
                
                # Check for specific error types
                if "500" in error_msg or "internal" in error_msg:
                    if attempt < max_retries - 1:
                        st.warning(f"Google API server error (500). Retrying in {base_delay * (2 ** attempt)} seconds...")
                        continue
                    else:
                        st.error("Google API is temporarily unavailable. Please try again in a few minutes.")
                        error_response = "Google's AI service is temporarily unavailable due to server issues. Please try generating answers again in a few minutes."
                        
                elif "rate limit" in error_msg or "quota" in error_msg:
                    if attempt < max_retries - 1:
                        st.warning(f"API rate limit reached. Waiting longer before retry...")
                        time.sleep(10)  # Longer delay for rate limits
                        continue
                    else:
                        error_response = "API rate limit exceeded. Please wait a few minutes before trying again."
                        
                elif "authentication" in error_msg or "api key" in error_msg:
                    st.error("API key issue detected. Please check your Gemini API key.")
                    error_response = "API authentication failed. Please verify your Gemini API key is valid and has sufficient quota."
                    
                else:
                    if attempt < max_retries - 1:
                        st.warning(f"API error: {str(e)}. Retrying...")
                        continue
                    else:
                        error_response = f"API error after {max_retries} attempts: {str(e)}"
                
                # Return error responses for all questions in batch
                return [{"question": q["question"], "answer": error_response, "question_number": q["question_number"]} for q in questions_batch]
        
        # Fallback return (should not reach here)
        return [{"question": q["question"], "answer": "Unable to generate answer due to unexpected error.", "question_number": q["question_number"]} for q in questions_batch]
    
    def _construct_prompt(self, question: str, subject: str, mode: str, 
                         custom_prompt: str = "", reference_content: str = "") -> str:
        """Construct a sophisticated prompt for the AI model"""
        
        # Base instruction for 8-mark college-level answers with enhanced formatting
        base_instruction = f"""
You are an expert academic assistant specializing in {subject}. 
Generate a comprehensive answer for the following college-level question worth 8 marks.

ENHANCED FORMATTING REQUIREMENTS:
- Well-structured with clear headings using **bold** or # markdown
- Include key terms in **bold** and important concepts in *italics*
- For code: Use ```language blocks for multi-line code and `backticks` for inline code
- For math: Use LaTeX notation like $x^2$ for inline math and $$equation$$ for display math
- Use proper special characters: α β γ δ π θ λ μ σ φ ω ∞ ≤ ≥ ≠ ± ° © ® ™
- Format lists with bullet points (•) and numbered lists appropriately
- Use proper citations and references with formal academic style
- Maintain academic rigor and accuracy throughout
- Be approximately 400-600 words for an 8-mark question
- Ensure all content renders properly in PDF format with special characters
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
- Include step-by-step mathematical derivations with LaTeX: $\\frac{dy}{dx}$, $\\int_a^b f(x)dx$
- Show calculation steps with proper mathematical notation: α, β, π, ∞, ≤, ≥, ≠, ±
- Use display math for complex formulas: $$\\sum_{i=1}^{n} x_i = \\frac{n(n+1)}{2}$$
- Include geometric explanations with coordinate references like (x₁, y₁)
- Provide alternative solution methods with clear step numbering
- Verify answers with worked examples and mathematical proofs
- Use proper mathematical symbols and Greek letters throughout
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
- Include code examples with proper syntax highlighting using ```javascript, ```python, ```java, etc.
- Explain time and space complexity with mathematical notation like O(n²), Ω(log n)
- Provide practical implementation details with inline code `functions()` and `variables`
- Include system design considerations with architectural diagrams in text
- Use technical terminology like APIs, algorithms, data structures, OOP, etc.
- Show code snippets for algorithms, functions, and key programming concepts
- Format technical specifications and requirements clearly
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
- Include chemical equations: H₂SO₄ + 2NaOH → Na₂SO₄ + 2H₂O
- Use proper chemical notation with subscripts and superscripts: CO₂, H⁺, Fe³⁺
- Explain molecular structures with bond angles: 109.5°, 120°, 180°
- Include reaction mechanisms with arrow notation: → ⇌ ⟶
- Use proper chemical symbols and formulas throughout
- Include temperature and pressure conditions: 25°C, 1 atm
- Format chemical nomenclature with proper IUPAC naming
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
    
    def _construct_multi_question_prompt(self, questions_batch: List[Dict], subject: str, mode: str,
                                        custom_prompt: str = "", reference_content: str = "") -> str:
        """Construct a prompt for multiple questions in one API call"""
        
        # Base instruction for multiple questions
        base_instruction = f"""
You are an expert academic assistant specializing in {subject}. 
Generate comprehensive answers for the following {len(questions_batch)} college-level questions, each worth 8 marks.

IMPORTANT FORMATTING INSTRUCTIONS:
- Start each answer with "ANSWER [question_number]:" 
- Each answer should be 400-600 words for an 8-mark question
- Use **bold** for key terms and *italics* for important concepts
- Include bullet points and numbered lists where appropriate
- Maintain academic rigor and accuracy
- Separate each answer clearly with a line break

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
        
        # Questions section
        questions_section = "QUESTIONS TO ANSWER:\n\n"
        for i, q_data in enumerate(questions_batch, 1):
            questions_section += f"QUESTION {q_data['question_number']}: {q_data['question']}\n\n"
        
        # Construct final prompt
        final_prompt = f"""
{base_instruction}

{mode_instruction}

{subject_guidelines}

{reference_section}

{custom_section}

{questions_section}

Please provide comprehensive, well-formatted answers for all questions following the above guidelines.
Remember to start each answer with "ANSWER [question_number]:" and maintain consistent formatting.
"""
        
        return final_prompt
    
    def _parse_multi_question_response(self, response_text: str, questions_batch: List[Dict]) -> List[Dict]:
        """Parse the multi-question response to extract individual answers"""
        
        answers = []
        
        # Split response by answer markers
        import re
        answer_sections = re.split(r'ANSWER\s+(\d+):', response_text, flags=re.IGNORECASE)
        
        # First element is usually empty or contains preamble
        if len(answer_sections) > 1:
            # Process pairs of (question_number, answer_text)
            for i in range(1, len(answer_sections), 2):
                if i + 1 < len(answer_sections):
                    question_num = int(answer_sections[i].strip())
                    answer_text = answer_sections[i + 1].strip()
                    
                    # Find the corresponding question
                    for q_data in questions_batch:
                        if q_data['question_number'] == question_num:
                            answers.append({
                                "question": q_data['question'],
                                "answer": answer_text,
                                "question_number": question_num
                            })
                            break
        
        # If parsing failed, create fallback answers
        if len(answers) != len(questions_batch):
            st.warning("Response parsing incomplete. Using fallback method.")
            # Split by approximate sections
            sections = response_text.split('\n\n')
            for i, q_data in enumerate(questions_batch):
                if i < len(sections):
                    answer_text = sections[i].strip()
                else:
                    answer_text = "Answer extraction failed. Please try regenerating."
                
                # Check if we already have this answer
                existing = [a for a in answers if a['question_number'] == q_data['question_number']]
                if not existing:
                    answers.append({
                        "question": q_data['question'],
                        "answer": answer_text,
                        "question_number": q_data['question_number']
                    })
        
        return answers
