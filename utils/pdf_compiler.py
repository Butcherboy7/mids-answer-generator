import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import tempfile
import re

class PDFCompiler:
    """Compiles generated answers into a professional PDF document"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles for the PDF"""
        
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        # Heading style
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.darkblue,
            borderWidth=1,
            borderColor=colors.darkblue,
            borderPadding=5
        )
        
        # Subheading style
        self.subheading_style = ParagraphStyle(
            'CustomSubheading',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=8,
            spaceBefore=12,
            textColor=colors.darkgreen
        )
        
        # Question style
        self.question_style = ParagraphStyle(
            'QuestionStyle',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=8,
            spaceBefore=16,
            textColor=colors.darkred,
            fontName='Helvetica-Bold',
            leftIndent=20,
            rightIndent=20,
            borderWidth=1,
            borderColor=colors.lightgrey,
            borderPadding=10,
            backColor=colors.lightgrey
        )
        
        # Answer style
        self.answer_style = ParagraphStyle(
            'AnswerStyle',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            spaceBefore=8,
            alignment=TA_JUSTIFY,
            leftIndent=20,
            rightIndent=20
        )
    
    def compile_answers_pdf(self, answers: list, subject: str, mode: str, custom_prompt: str = "") -> str:
        """Compile all answers into a professional PDF document"""
        
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
            
            # Add table of contents
            story.extend(self._create_table_of_contents(answers))
            story.append(PageBreak())
            
            # Add answers
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
        """Format answer text with proper styling"""
        
        paragraphs = []
        
        # Split text into paragraphs
        text_paragraphs = answer_text.split('\n\n')
        
        for para in text_paragraphs:
            para = para.strip()
            if not para:
                continue
            
            # Clean and format the text
            formatted_text = self._clean_text_for_pdf(para)
            
            # Apply different styles based on content
            if para.startswith('#') or para.startswith('**') and para.endswith('**'):
                # This looks like a heading
                clean_text = para.replace('#', '').replace('**', '').strip()
                paragraphs.append(Paragraph(clean_text, self.subheading_style))
            else:
                # Regular paragraph
                paragraphs.append(Paragraph(formatted_text, self.answer_style))
        
        return paragraphs
    
    def _clean_text_for_pdf(self, text: str) -> str:
        """Clean and format text for PDF generation with proper HTML tag handling"""
        
        # First, fix any malformed HTML tags by removing all HTML formatting
        # This prevents ReportLab parser errors
        import html
        
        # Remove any existing HTML tags completely to avoid conflicts
        text = re.sub(r'<[^>]+>', '', text)
        
        # Escape HTML entities
        text = html.escape(text)
        
        # Now apply clean ReportLab formatting
        # Replace markdown-style formatting with proper ReportLab tags
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)  # Bold
        text = re.sub(r'\*(.*?)\*(?!\*)', r'<i>\1</i>', text)  # Italic (not part of **)
        
        # Handle bullet points
        text = re.sub(r'^[\-\*]\s+', '• ', text, flags=re.MULTILINE)
        
        # Handle numbered lists
        text = re.sub(r'^(\d+)\.\s+', r'\1. ', text, flags=re.MULTILINE)
        
        # Clean up extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Ensure no unclosed tags by checking for balanced tags
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
