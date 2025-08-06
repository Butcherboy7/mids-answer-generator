import os
import re
import html
from datetime import datetime
import tempfile
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Preformatted
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

class PDFCompiler:
    """Compiles generated answers into a professional PDF document"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
    
    def _setup_custom_styles(self):
        """Setup clean, professional paragraph styles for the PDF"""
        
        # Clean title style with appealing color
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Title'],
            fontSize=28,
            spaceAfter=40,
            spaceBefore=20,
            alignment=TA_CENTER,
            textColor=colors.Color(0.1, 0.2, 0.4),  # Professional dark blue
            fontName='Helvetica-Bold'
        )
        
        # Subtitle style for cover page
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Normal'],
            fontSize=14,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.grey,
            fontName='Helvetica'
        )
        
        # Question style - bold, clean, well-spaced with appealing color
        self.question_style = ParagraphStyle(
            'QuestionStyle',
            parent=self.styles['Normal'],
            fontSize=13,
            spaceAfter=15,
            spaceBefore=25,
            textColor=colors.Color(0.2, 0.2, 0.4),  # Dark blue-gray for questions
            fontName='Helvetica-Bold',
            leftIndent=0,
            rightIndent=0,
            borderWidth=0,
            borderPadding=8,
            backColor=colors.Color(0.98, 0.98, 1.0)  # Very subtle background
        )
        
        # Main answer style - clean, readable with improved font
        self.answer_style = ParagraphStyle(
            'AnswerStyle',
            parent=self.styles['Normal'],
            fontSize=11,  # Slightly smaller for better fitting
            spaceAfter=12,
            spaceBefore=8,
            alignment=TA_JUSTIFY,  # Justified for professional look
            leftIndent=20,
            rightIndent=20,
            leading=16,  # Better line spacing
            textColor=colors.Color(0.1, 0.1, 0.1),  # Very dark gray instead of pure black
            fontName='Helvetica'
        )
        
        # Code style for technical content
        self.code_style = ParagraphStyle(
            'CodeStyle',
            parent=self.styles['Code'],
            fontSize=10,
            spaceAfter=12,
            spaceBefore=8,
            leftIndent=25,
            rightIndent=25,
            leading=13,
            textColor=colors.black,
            fontName='Courier',
            backColor=colors.lightgrey,
            borderWidth=1,
            borderColor=colors.grey,
            borderPadding=8
        )
        
        # List item style
        self.list_style = ParagraphStyle(
            'ListStyle',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=4,
            leftIndent=25,
            rightIndent=15,
            leading=15,
            textColor=colors.black,
            fontName='Helvetica'
        )
        
        # Bold heading style for sections within answers
        self.section_heading_style = ParagraphStyle(
            'SectionHeading',
            parent=self.styles['Normal'],
            fontSize=13,  # Better hierarchy
            spaceAfter=10,
            spaceBefore=15,
            textColor=colors.Color(0.2, 0.4, 0.6),  # Professional blue
            fontName='Helvetica-Bold',
            leftIndent=5,
            borderWidth=0,
            borderPadding=5
        )
        
        # Main heading style for titles and table of contents
        self.heading_style = ParagraphStyle(
            'MainHeading',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=20,
            spaceBefore=15,
            textColor=colors.black,
            fontName='Helvetica-Bold',
            alignment=TA_CENTER
        )
        
        # Subheading style for sections
        self.subheading_style = ParagraphStyle(
            'SubHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=10,
            textColor=colors.black,
            fontName='Helvetica-Bold'
        )
        
        # Code block style with better contrast and readability
        self.code_style = ParagraphStyle(
            'CodeStyle',
            parent=self.styles['Code'],
            fontSize=9,  # Slightly larger for better readability
            spaceAfter=6,
            spaceBefore=6,
            leftIndent=12,
            rightIndent=12,
            fontName='Courier-Bold',  # Bold for better contrast
            textColor=colors.black,   # Black text for better contrast
            backColor=colors.lightgrey,  # Light gray background
            borderColor=colors.grey,   # Darker border
            borderWidth=1,
            borderPadding=8,
            leading=12  # More spacing between lines
        )
        
        # Mathematical formula style
        self.math_style = ParagraphStyle(
            'MathStyle',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=8,
            spaceBefore=8,
            alignment=TA_CENTER,
            fontName='Courier',
            textColor=colors.darkgreen,
            leftIndent=30,
            rightIndent=30
        )
        
        # List item style
        self.list_style = ParagraphStyle(
            'ListStyle',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=4,
            spaceBefore=2,
            leftIndent=25,
            bulletIndent=10,
            textColor=colors.black,
            fontName='Helvetica'
        )
    
    def compile_answers_pdf(self, answers: list, subject: str, mode: str, custom_prompt: str = "") -> str:
        """Compile all answers into a professional PDF document"""
        
        # Store subject for formatting decisions
        self.current_subject = subject
        
        try:
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"answers_{subject.lower().replace(' ', '_')}_{timestamp}.pdf"
            filepath = os.path.join("data", filename)
            
            # Create PDF document
            doc = SimpleDocTemplate(
                filepath,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Build content
            story = []
            
            # Add cover page
            story.extend(self._create_cover_page(subject, mode, len(answers), custom_prompt))
            story.append(PageBreak())
            
            # Add answers section directly (simplified)
            story.extend(self._create_answers_section(answers))
            
            # Build PDF
            doc.build(story)
            
            return filepath
            
        except Exception as e:
            raise Exception(f"Error compiling PDF: {str(e)}")
    
    def _create_cover_page(self, subject: str, mode: str, question_count: int, custom_prompt: str) -> list:
        """Create a professional cover page"""
        
        story = []
        
        # Title
        story.append(Spacer(1, 2*inch))
        story.append(Paragraph("🎓 College Answer Generator", self.title_style))
        story.append(Spacer(1, 0.5*inch))
        
        # Subtitle
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=self.styles['Normal'],
            fontSize=18,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        story.append(Paragraph(f"Comprehensive Answers for {subject}", subtitle_style))
        story.append(Spacer(1, 1*inch))
        
        # Details table
        details = [
            ["Subject:", subject],
            ["Answer Mode:", mode],
            ["Total Questions:", str(question_count)],
            ["Generated On:", datetime.now().strftime("%B %d, %Y at %I:%M %p")],
        ]
        
        if custom_prompt.strip():
            details.append(["Custom Instructions:", "Yes"])
        
        details_table = Table(details, colWidths=[2*inch, 3*inch])
        details_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
        ]))
        
        story.append(details_table)
        story.append(Spacer(1, 1*inch))
        
        # Mode description
        mode_description = ""
        if mode == "Understand Mode":
            mode_description = "Detailed explanations with analogies, examples, and comprehensive understanding focus."
        else:
            mode_description = "Concise, exam-focused answers with key points and formal academic language."
        
        desc_style = ParagraphStyle(
            'Description',
            parent=self.styles['Normal'],
            fontSize=11,
            alignment=TA_CENTER,
            textColor=colors.grey,
            fontStyle='italic'
        )
        story.append(Paragraph(mode_description, desc_style))
        
        return story
    
    def _create_table_of_contents(self, answers: list) -> list:
        """Create table of contents"""
        
        story = []
        
        story.append(Paragraph("Table of Contents", self.heading_style))
        story.append(Spacer(1, 20))
        
        toc_data = [["Question", "Page"]]
        
        for i, answer in enumerate(answers):
            question_preview = answer['question'][:60] + "..." if len(answer['question']) > 60 else answer['question']
            # Simplified page calculation (approximate)
            page_num = 3 + (i * 2)  # Starting after cover and TOC, roughly 2 pages per answer
            toc_data.append([f"Q{i+1}: {question_preview}", str(page_num)])
        
        toc_table = Table(toc_data, colWidths=[4.5*inch, 1*inch])
        toc_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(toc_table)
        
        return story
    
    def _create_answers_section(self, answers: list) -> list:
        """Create the main answers section"""
        
        story = []
        
        for i, answer_data in enumerate(answers):
            # Question header
            story.append(Paragraph(f"Question {i+1}", self.heading_style))
            story.append(Spacer(1, 12))
            
            # Question text
            question_text = self._clean_text_for_pdf(answer_data['question'])
            story.append(Paragraph(f"<b>Q{i+1}:</b> {question_text}", self.question_style))
            story.append(Spacer(1, 16))
            
            # Answer text
            story.append(Paragraph("<b>Answer:</b>", self.subheading_style))
            
            # Process and format the answer
            formatted_answer = self._format_answer_text(answer_data['answer'])
            for paragraph in formatted_answer:
                story.append(paragraph)
                story.append(Spacer(1, 6))
            
            # Add separator between questions
            if i < len(answers) - 1:
                story.append(Spacer(1, 20))
                story.append(PageBreak())
        
        return story
    
    def _format_answer_text(self, answer_text: str) -> list:
        """Smart formatting with proper structure and readability"""
        
        paragraphs = []
        
        # Preprocess text while preserving structure
        answer_text = self._smart_text_preprocessing(answer_text)
        
        # Split into sections and paragraphs
        sections = answer_text.split('\n\n')
        
        for section in sections:
            section = section.strip()
            if not section:
                continue
            
            # Detect and format different content types
            if self._is_code_section(section):
                # Format code blocks for programming subjects
                paragraphs.extend(self._format_smart_code_block(section))
                
            elif self._is_heading_section(section):
                # Format headings with proper styling
                paragraphs.append(self._format_heading(section))
                
            elif self._is_list_section(section):
                # Format lists with proper bullets and spacing
                paragraphs.extend(self._format_smart_list(section))
                
            else:
                # Regular paragraph with enhanced formatting
                paragraphs.extend(self._format_regular_paragraph(section))
            
            # Add proper spacing between sections
            paragraphs.append(Spacer(1, 12))
        
        return paragraphs
    
    def _is_code_block(self, text: str, subject: str = "") -> bool:
        """Check if text should be formatted as code block - subject-aware"""
        
        # Only use code blocks for programming/computer science subjects
        programming_subjects = ['computer science', 'programming', 'software', 'coding', 'algorithm', 'data structure']
        is_programming_subject = any(prog in subject.lower() for prog in programming_subjects)
        
        # For non-programming subjects, never format as code block
        if not is_programming_subject:
            return False
        
        # For programming subjects, check for actual code patterns
        return (text.startswith('```') or 
                ('def ' in text and '(' in text and ')' in text) or
                ('function ' in text and '(' in text and ')' in text) or
                ('class ' in text and ('{' in text or ':' in text)) or
                ('import ' in text and len(text.split('\n')) > 1))
    
    def _is_section_heading(self, text: str) -> bool:
        """Check if text is a section heading"""
        return bool(text.startswith('#') or 
                   (text.startswith('**') and text.endswith('**') and len(text) < 100) or
                   (text.endswith(':') and len(text.split()) < 5))
    
    def _is_list_item(self, text: str) -> bool:
        """Check if text is a list item"""
        return bool(text.startswith('•') or 
                   text.startswith('-') or 
                   text.startswith('*') or
                   re.match(r'^\d+\.', text))
    
    def _preprocess_text(self, text: str) -> str:
        """Preprocess text to handle special characters and encoding issues"""
        
        # Handle common special characters and symbols
        replacements = {
            '"': '"', '"': '"',  # Smart quotes
            ''': "'", ''': "'",  # Smart apostrophes
            '—': '-', '–': '-',  # Em and en dashes
            '…': '...',          # Ellipsis
            '©': '(c)',          # Copyright
            '®': '(R)',          # Registered trademark
            '™': '(TM)',         # Trademark
            '°': ' degrees',     # Degree symbol
            '±': '+/-',          # Plus-minus
            '≤': '<=',           # Less than or equal
            '≥': '>=',           # Greater than or equal
            '≠': '!=',           # Not equal
            '∞': 'infinity',     # Infinity
            'α': 'alpha', 'β': 'beta', 'γ': 'gamma', 'δ': 'delta',
            'π': 'pi', 'θ': 'theta', 'λ': 'lambda', 'μ': 'mu',
            'σ': 'sigma', 'φ': 'phi', 'ω': 'omega'
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        return text
    
    def _format_code_block(self, code_text: str) -> list:
        """Format code blocks with enhanced styling and line wrapping for long lines"""
        
        elements = []
        
        # Remove code block markers
        code_text = re.sub(r'^```[\w]*\s*', '', code_text)
        code_text = re.sub(r'```\s*$', '', code_text)
        
        # Split into lines for better formatting
        lines = code_text.split('\n')
        
        # Add spacing before code block
        elements.append(Spacer(1, 8))
        
        # Create a table for code block with background
        code_lines = []
        for line in lines:
            if line.strip():
                # Break long lines to prevent overflow
                wrapped_lines = self._wrap_long_code_line(line)
                for wrapped_line in wrapped_lines:
                    formatted_line = self._format_code_line(wrapped_line)
                    code_lines.append([formatted_line])
        
        if code_lines:
            # Create table with background for code block
            from reportlab.platypus import Table, TableStyle
            code_table = Table(code_lines, colWidths=[5.5*inch])  # Slightly narrower for better fit
            # Choose appealing colors based on subject with better contrast
            if hasattr(self, 'current_subject') and 'computer' in self.current_subject.lower():
                bg_color = colors.Color(0.95, 0.97, 0.99)  # Very light blue-gray
                text_color = colors.Color(0.2, 0.3, 0.5)   # Dark blue-gray
                border_color = colors.Color(0.4, 0.5, 0.7)  # Medium blue
            else:
                bg_color = colors.Color(0.97, 0.97, 0.97)  # Very light gray
                text_color = colors.Color(0.2, 0.2, 0.2)   # Dark gray
                border_color = colors.Color(0.5, 0.5, 0.5)  # Medium gray
                
            code_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), bg_color),
                ('FONTNAME', (0, 0), (-1, -1), 'Courier'),  # Regular weight for better readability
                ('FONTSIZE', (0, 0), (-1, -1), 9),  # Optimal size for code
                ('TEXTCOLOR', (0, 0), (-1, -1), text_color),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('BOX', (0, 0), (-1, -1), 1.5, border_color),  # Slightly thicker border
                ('GRID', (0, 0), (-1, -1), 0.5, border_color),  # Add subtle grid lines
            ]))
            elements.append(code_table)
        
        # Add spacing after code block
        elements.append(Spacer(1, 8))
        return elements
    
    def _format_code_line(self, line: str) -> str:
        """Format individual code lines with minimal escaping"""
        
        # Minimal escaping - only escape ampersands that aren't part of entities
        # Don't escape < and > in code as they're common in programming
        line = line.replace('&', '&amp;')
        
        return line
    
    def _wrap_long_code_line(self, line: str, max_length: int = 65) -> list:
        """Wrap long code lines to prevent overflow in PDF with better line breaking"""
        
        # Reduce max length for better fitting in PDF
        if len(line) <= max_length:
            return [line]
        
        wrapped_lines = []
        current_line = line.rstrip()
        
        while len(current_line) > max_length:
            # Find a good break point (prefer spaces, then operators)
            break_point = max_length
            
            # Look for natural break points going backwards from max_length
            for i in range(min(max_length, len(current_line)-1), max(0, max_length - 30), -1):
                if i < len(current_line) and current_line[i] in [' ', ',', ';', ')', '}', ']', '.', '=', '+', '-']:
                    break_point = i + 1
                    break
            
            # If no good break point found, check for word boundaries
            if break_point == max_length:
                for i in range(min(max_length, len(current_line)-1), max(0, max_length - 15), -1):
                    if i < len(current_line) and current_line[i] == ' ':
                        break_point = i + 1
                        break
            
            # Force break if still too long
            if break_point == max_length and len(current_line) > max_length:
                break_point = max_length - 3  # Leave room for continuation marker
            
            # Add the wrapped line
            wrapped_part = current_line[:break_point].rstrip()
            wrapped_lines.append(wrapped_part)
            
            # Prepare the next line with proper indentation
            remaining = current_line[break_point:].lstrip()
            if remaining:
                # Add indentation for continuation, but don't exceed reasonable indentation
                indent = "  "  # Simpler indentation
                current_line = indent + remaining
            else:
                break
        
        # Add the remaining part
        if current_line.strip():
            wrapped_lines.append(current_line)
        
        return wrapped_lines
    
    def _format_math_formula(self, formula_text: str) -> list:
        """Format mathematical formulas - simplified to avoid parser errors"""
        
        elements = []
        
        # Clean up LaTeX markers
        formula_text = re.sub(r'\$+', '', formula_text)
        formula_text = formula_text.strip()
        
        # Convert common LaTeX symbols to readable text - no complex HTML
        latex_replacements = {
            r'\\frac\{([^}]+)\}\{([^}]+)\}': r'(\1)/(\2)',
            r'\\sqrt\{([^}]+)\}': r'sqrt(\1)',
            r'\\sum': 'Σ',
            r'\\int': '∫',
            r'\\alpha': 'α',
            r'\\beta': 'β',
            r'\\gamma': 'γ',
            r'\\delta': 'δ',
            r'\\pi': 'π',
            r'\\theta': 'θ',
            r'\\lambda': 'λ',
            r'\\mu': 'μ',
            r'\\sigma': 'σ',
            r'\\phi': 'φ',
            r'\\omega': 'ω',
            r'\\leq': '≤',
            r'\\geq': '≥',
            r'\\neq': '≠',
            r'\\infty': '∞',
            r'\^([0-9]+)': r'^(\1)',
            r'_([0-9]+)': r'_(\1)'
        }
        
        for pattern, replacement in latex_replacements.items():
            formula_text = re.sub(pattern, replacement, formula_text)
        
        # Safe escaping without complex font tags
        formula_text = formula_text.replace('<', '&lt;').replace('>', '&gt;').replace('&', '&amp;')
        
        elements.append(Spacer(1, 6))
        elements.append(Paragraph(f"<i>{formula_text}</i>", self.math_style))
        elements.append(Spacer(1, 6))
        
        return elements
    
    def _format_list_item(self, item_text: str) -> Paragraph:
        """Format list items with proper bullets and indentation"""
        
        # Clean up the item text
        clean_item = item_text.lstrip('•-*').strip()
        if re.match(r'^\d+\.', item_text):
            clean_item = re.sub(r'^\d+\.\s*', '', item_text)
        
        # Enhanced formatting for list items
        formatted_text = self._enhance_text_formatting(clean_item)
        
        return Paragraph(f"• {formatted_text}", self.list_style)
    
    def _enhance_text_formatting(self, text: str) -> str:
        """Ultra-safe text formatting without HTML tags"""
        
        # Remove ALL HTML tags completely to prevent any parsing issues
        text = re.sub(r'<[^>]+>', '', text)
        
        # Clean up HTML entities
        text = text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
        text = text.replace('&quot;', '"').replace('&nbsp;', ' ')
        
        # Remove markdown formatting entirely for safety
        text = re.sub(r'^#+\s*', '', text)             # Remove heading hashtags
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # Remove bold markup
        text = re.sub(r'__([^_]+)__', r'\1', text)      # Remove bold markup  
        text = re.sub(r'\*([^*]+)\*', r'\1', text)      # Remove italic markup
        text = re.sub(r'_([^_]+)_', r'\1', text)        # Remove italic markup
        text = re.sub(r'`([^`]+)`', r'[\1]', text)      # Convert code to brackets
        
        # Clean up spaces and problematic characters
        text = re.sub(r'\s+', ' ', text).strip()
        text = text.replace('<br>', ' ').replace('<br/>', ' ')
        
        return text
    
    def _simple_text_cleanup(self, text: str) -> str:
        """Simple text cleanup without complex formatting"""
        
        # Replace common problematic characters
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        text = text.replace('–', '-').replace('—', '-')
        
        # Remove any HTML-like tags completely
        text = re.sub(r'<[^>]+>', '', text)
        
        # Clean up excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        return text.strip()
    
    def _is_simple_heading(self, text: str) -> bool:
        """Check if text is a simple heading (ends with colon, short length)"""
        return (text.endswith(':') and len(text) < 80 and '\n' not in text)
    
    def _format_simple_list_item(self, text: str) -> Paragraph:
        """Format list item with simple bullet point"""
        
        # Remove existing bullets and clean up
        clean_text = text.lstrip('•-*').strip()
        if clean_text.startswith(('1.', '2.', '3.', '4.', '5.')):
            # Keep numbered lists as is
            return Paragraph(clean_text, self.list_style)
        else:
            # Add simple bullet
            return Paragraph(f"• {clean_text}", self.list_style)
    
    def _smart_text_preprocessing(self, text: str) -> str:
        """Intelligent text preprocessing that preserves structure"""
        
        # Fix common encoding issues
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        text = text.replace('–', '-').replace('—', '-')
        
        # Clean up excessive whitespace while preserving structure
        text = re.sub(r' +', ' ', text)  # Multiple spaces to single
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)  # Multiple newlines to double
        
        return text.strip()
    
    def _is_code_section(self, text: str) -> bool:
        """Detect code sections for programming subjects"""
        if not (hasattr(self, 'current_subject') and 
                any(prog in self.current_subject.lower() for prog in ['computer', 'programming', 'software'])):
            return False
        
        # Look for code patterns
        code_indicators = [
            r'def\s+\w+\(', r'function\s+\w+\(', r'class\s+\w+', 
            r'import\s+\w+', r'#include', r'<\w+>', r'{\s*\w+',
            r'console\.log', r'print\(', r'SELECT\s+', r'if\s*\(',
            r'for\s*\(', r'while\s*\('
        ]
        
        return any(re.search(pattern, text, re.IGNORECASE) for pattern in code_indicators)
    
    def _is_heading_section(self, text: str) -> bool:
        """Detect headings and important section titles"""
        return (text.endswith(':') and len(text) < 100 and '\n' not in text) or \
               text.isupper() or \
               text.startswith('####') or \
               text.startswith('###') or \
               text.startswith('##') or \
               text.startswith('#') or \
               (text.startswith(('DEFINITION', 'EXPLANATION', 'EXAMPLE', 'ANSWER', 'SOLUTION')))
    
    def _is_list_section(self, text: str) -> bool:
        """Detect list sections"""
        lines = text.split('\n')
        return len(lines) > 1 and any(line.strip().startswith(('-', '•', '*')) or 
                                     re.match(r'^\d+\.', line.strip()) for line in lines)
    
    def _format_smart_code_block(self, text: str) -> list:
        """Format code blocks with proper styling and background"""
        elements = []
        
        lines = text.split('\n')
        code_lines = []
        
        for line in lines:
            if line.strip():
                # Clean and wrap long lines
                clean_line = line.replace('\t', '    ')  # Convert tabs to spaces
                if len(clean_line) > 80:
                    # Wrap long lines
                    chunks = [clean_line[i:i+80] for i in range(0, len(clean_line), 80)]
                    code_lines.extend([[chunk] for chunk in chunks])
                else:
                    code_lines.append([clean_line])
        
        if code_lines:
            from reportlab.platypus import Table, TableStyle
            code_table = Table(code_lines, colWidths=[6*inch])
            
            # Subject-aware coloring
            if 'computer' in self.current_subject.lower():
                bg_color = colors.lightblue  # Light blue
                text_color = colors.darkblue  # Dark blue
                border_color = colors.blue
            else:
                bg_color = colors.lightgrey  # Light gray
                text_color = colors.black
                border_color = colors.grey
            
            code_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), bg_color),
                ('FONTNAME', (0, 0), (-1, -1), 'Courier-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TEXTCOLOR', (0, 0), (-1, -1), text_color),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 12),
                ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('BOX', (0, 0), (-1, -1), 1, border_color),
            ]))
            
            elements.append(Spacer(1, 6))
            elements.append(code_table)
            elements.append(Spacer(1, 6))
        
        return elements
    
    def _format_heading(self, text: str) -> Paragraph:
        """Format headings with safe styling"""
        # Remove markdown heading symbols and clean up
        clean_text = re.sub(r'^#+\s*', '', text)  # Remove # symbols
        clean_text = clean_text.replace(':', '').strip()
        clean_text = self._enhance_text_formatting(clean_text)
        return Paragraph(clean_text, self.section_heading_style)
    
    def _format_smart_list(self, text: str) -> list:
        """Format lists with proper bullets and indentation"""
        elements = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Format different list types
            if re.match(r'^\d+\.', line):
                # Numbered list
                elements.append(Paragraph(line, self.list_style))
            elif line.startswith(('-', '•', '*')):
                # Bullet list
                clean_line = line.lstrip('-•*').strip()
                formatted_line = self._enhance_text_formatting(clean_line)
                elements.append(Paragraph(f"• {formatted_line}", self.list_style))
            else:
                # Regular line in list context
                formatted_line = self._enhance_text_formatting(line)
                elements.append(Paragraph(f"• {formatted_line}", self.list_style))
            
            elements.append(Spacer(1, 4))
        
        return elements
    
    def _format_regular_paragraph(self, text: str) -> list:
        """Format regular paragraphs with proper line spacing"""
        elements = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line:
                formatted_line = self._enhance_text_formatting(line)
                elements.append(Paragraph(formatted_line, self.answer_style))
                elements.append(Spacer(1, 6))
        
        return elements
    
    def _is_math_formula(self, text: str) -> bool:
        """Check if text contains mathematical formulas"""
        math_indicators = [
            r'\$', r'\\frac', r'\\sqrt', r'\\sum', r'\\int',
            r'\\alpha', r'\\beta', r'\\gamma', r'\\delta', r'\\pi',
            r'\\theta', r'\\lambda', r'\\mu', r'\\sigma', r'\\phi', r'\\omega',
            r'\^[0-9]', r'_[0-9]', 'equation:', 'formula:'
        ]
        
        return any(re.search(pattern, text, re.IGNORECASE) for pattern in math_indicators)
    
    def _escape_and_enhance_html(self, text: str) -> str:
        """Escape HTML while preserving enhancement tags with proper formatting"""
        
        # Handle special characters that cause parsing issues
        problematic_chars = {
            '<': '&lt;',
            '>': '&gt;',
            '&': '&amp;',
            '"': '&quot;',
        }
        
        # First escape problematic characters
        for char, escape in problematic_chars.items():
            text = text.replace(char, escape)
        
        # Then safely restore our specific formatting tags
        safe_replacements = {
            '&lt;b&gt;': '<b>',
            '&lt;/b&gt;': '</b>',
            '&lt;i&gt;': '<i>',
            '&lt;/i&gt;': '</i>',
        }
        
        for escaped, safe in safe_replacements.items():
            text = text.replace(escaped, safe)
        
        # Remove any malformed font tags that cause parser errors
        text = re.sub(r'&lt;font[^&]*&gt;([^&]*)&lt;/font&gt;', r'\1', text)
        
        return text
    
    def _clean_text_for_pdf(self, text: str) -> str:
        """Clean and format text for PDF generation with professional styling"""
        
        # Remove any existing HTML/XML tags to avoid conflicts
        text = re.sub(r'<[^>]+>', '', text)
        
        # Escape HTML entities
        import html
        text = html.escape(text)
        
        # Apply clean, professional formatting
        # Bold for important terms and headings
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)  # Bold
        text = re.sub(r'\*(.*?)\*(?!\*)', r'<i>\1</i>', text)  # Italic
        
        # Clean bullet points
        text = re.sub(r'^[\-\*]\s+', '• ', text, flags=re.MULTILINE)
        
        # Clean numbered lists
        text = re.sub(r'^(\d+)\.\s+', r'\1. ', text, flags=re.MULTILINE)
        
        # Make key terms bold (common academic terms)
        key_terms = [
            'Definition:', 'Answer:', 'Solution:', 'Explanation:', 'Example:', 
            'Note:', 'Important:', 'Key Points:', 'Summary:', 'Conclusion:',
            'Types:', 'Steps:', 'Process:', 'Method:', 'Algorithm:', 'Formula:'
        ]
        
        for term in key_terms:
            text = re.sub(f'({re.escape(term)})', r'<b>\1</b>', text, flags=re.IGNORECASE)
        
        # Clean up multiple spaces and line breaks
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Balance HTML tags
        text = self._balance_html_tags(text)
        
        return text
    
    def _balance_html_tags(self, text: str) -> str:
        """Ensure HTML tags are properly balanced to prevent parser errors"""
        
        # Stack to track open tags
        tag_stack = []
        result = ""
        i = 0
        
        while i < len(text):
            if text[i] == '<':
                # Find the end of the tag
                tag_end = text.find('>', i)
                if tag_end != -1:
                    tag = text[i:tag_end+1]
                    
                    if tag.startswith('</'):
                        # Closing tag
                        tag_name = tag[2:-1]
                        if tag_stack and tag_stack[-1] == tag_name:
                            tag_stack.pop()
                            result += tag
                        # Ignore unmatched closing tags
                    elif not tag.endswith('/>'):
                        # Opening tag
                        tag_name = tag[1:-1]
                        if tag_name in ['b', 'i', 'u']:  # Only allow safe tags
                            tag_stack.append(tag_name)
                            result += tag
                    
                    i = tag_end + 1
                else:
                    # Malformed tag, skip the '<'
                    result += '&lt;'
                    i += 1
            else:
                result += text[i]
                i += 1
        
        # Close any remaining open tags
        while tag_stack:
            tag_name = tag_stack.pop()
            result += f'</{tag_name}>'
        
        return result
    
    def _clean_nested_tags(self, text: str) -> str:
        """Clean nested HTML tags to prevent parser errors"""
        
        # Remove font tags that are inside other formatting tags
        text = re.sub(r'<([bi])>([^<]*)<font[^>]*>([^<]*)</font>([^<]*)</\1>', r'<\1>\2\3\4</\1>', text)
        text = re.sub(r'<font[^>]*>([^<]*)<([bi])>([^<]*)</\2>([^<]*)</font>', r'<\2>\1\3\4</\2>', text)
        
        # Remove any remaining problematic font tags
        text = re.sub(r'<font[^>]*color="[^"]*">([^<]*)</font>', r'\1', text)
        
        return text
