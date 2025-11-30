"""
Gemini API Service
Refines translated text into structured prototype prompts
"""

import google.generativeai as genai
from typing import Optional

class GeminiRefiner:
    """
    Service to refine translated text using Gemini API
    """
    
    def __init__(self, api_key: str):
        """
        Initialize Gemini API
        
        Args:
            api_key: Google Gemini API key
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        print("Gemini API initialized successfully!")
    
    def refine_to_prototype_prompt(self, text: str) -> str:
        """
        Refine translated text into a structured prototype prompt
        
        Args:
            text: The translated English text
            
        Returns:
            Refined prototype prompt
        """
        prompt_template = f"""You are an expert at transforming rough, unstructured ideas into clear, actionable prompts for building interactive prototypes and demos. Your goal is to help people rapidly visualize and test their concepts.

Given this free-form idea: "{text}"

Analyze and transform it into a structured prototype prompt by:

**1. CLARIFY THE CORE CONCEPT**
- Identify the main problem being solved or need being addressed
- Extract the key user action or workflow
- Determine the primary value proposition

**2. DEFINE THE PROTOTYPE SCOPE**
- What's the minimal viable version that demonstrates the core idea?
- What can be mocked or simplified for demo purposes?
- What's essential vs. nice-to-have for initial validation?

**3. STRUCTURE THE TECHNICAL REQUIREMENTS**
- Interface type: Web app, mobile mockup, dashboard, interactive visualization, tool, game, etc.
- Key features: List 3-5 core interactions or capabilities
- Data needs: What information needs to be displayed, captured, or processed?
- User flow: Describe the step-by-step experience in 3-5 stages

**4. SPECIFY DESIGN CONSIDERATIONS**
- Visual style: Modern, minimal, playful, professional, etc.
- Color scheme: Based on the concept's tone and audience
- Layout: Desktop-first, mobile-first, or responsive
- Key UI elements: Forms, buttons, cards, charts, maps, etc.

**5. IDENTIFY INTERACTIVITY**
- What should users be able to click, input, or manipulate?
- What real-time feedback or updates should occur?
- What state changes or transitions are important?

**OUTPUT FORMAT:**

Create a [TYPE] prototype for [CONCEPT NAME].

**Purpose**: [1-2 sentence description of what this demo proves/shows]

**Core Functionality**:
- [Feature 1 with brief description]
- [Feature 2 with brief description]
- [Feature 3 with brief description]

**User Flow**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Design Requirements**:
- Style: [visual direction]
- Key components: [list important UI elements]
- Interactions: [describe main interactive elements]

**Technical Notes**:
- [Any specific libraries, data structures, or approaches to use]
- [What to mock vs. what to make functional]

**Success Criteria**: This prototype successfully demonstrates [X] when a user can [Y].

**GUIDELINES**:
- Aim for something buildable in a single session
- Prioritize "show, don't tell" - interactive beats static
- Include realistic sample data or content suggestions
- Specify what should be functional vs. placeholder
- Keep scope tight enough to finish, broad enough to be meaningful

Begin your response directly with "Create a [TYPE] prototype..." without any preamble or explanation of your process.
"""
        
        try:
            print("Sending to Gemini API for refinement...")
            response = self.model.generate_content(prompt_template)
            refined_prompt = response.text
            print("Gemini refinement complete!")
            return refined_prompt
        except Exception as e:
            print(f"Error calling Gemini API: {str(e)}")
            raise RuntimeError(f"Gemini API error: {str(e)}")
