"""
Neural Machine Translation (NMT) Module
Translates Indic text to English using Facebook NLLB
"""

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from typing import List, Optional, Union
import warnings
warnings.filterwarnings('ignore')


class IndicTranslator:
    """
    Neural Machine Translation for Indic languages to English using NLLB
    """
    
    def __init__(
        self,
        model_name: str = "facebook/nllb-200-1.3B",
        device: Optional[str] = None,
        max_length: int = 512
    ):
        """
        Initialize the NMT model
        
        Args:
            model_name: HuggingFace model identifier
            device: Device to run inference on ('cuda', 'cpu', or None for auto)
            max_length: Maximum sequence length for translation
        """
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.max_length = max_length
        self.model_name = model_name
        
        print(f"Loading NMT model: {model_name}")
        print(f"Using device: {self.device}")
        
        try:
            print("Step 1: Loading tokenizer...")
            # Load NLLB tokenizer (no trust_remote_code needed)
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            print("Step 2: Tokenizer loaded successfully!")
            
            print("Step 3: Loading model...")
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            print("Step 4: Model loaded successfully!")
            
            print("Step 5: Moving to device...")
            self.model.to(self.device)
            self.model.eval()
            
            print("NMT model loaded successfully!")
            
        except Exception as e:
            print(f"ERROR: Failed to load NMT model")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            import traceback
            traceback.print_exc()
            raise RuntimeError(f"Failed to load NMT model: {str(e)}")
    
    def translate(
        self,
        text: Union[str, List[str]],
        source_lang: str,
        target_lang: str = "eng_Latn",
        num_beams: int = 5,
        num_return_sequences: int = 1,
        temperature: float = 1.0
    ) -> Union[str, List[str]]:
        """
        Translate Indic text to English
        
        Args:
            text: Input text or list of texts in Indic language
            source_lang: Source language code (e.g., 'hin_Deva' for Hindi)
            target_lang: Target language code (default: 'eng_Latn' for English)
            num_beams: Number of beams for beam search
            num_return_sequences: Number of translations to return
            temperature: Sampling temperature
            
        Returns:
            Translated text or list of texts
        """
        # Handle single string input
        single_input = isinstance(text, str)
        if single_input:
            text = [text]
        
        print(f"Translating {len(text)} text(s) from {source_lang} to {target_lang}...")
        
        try:
            translations = []
            
            # Process in batches
            batch_size = 4
            for i in range(0, len(text), batch_size):
                batch = text[i:i + batch_size]
                
                # Set source language for NLLB tokenizer
                self.tokenizer.src_lang = source_lang
                
                # Prepare input
                inputs = self.tokenizer(
                    batch,
                    return_tensors="pt",
                    padding=True,
                    truncation=True,
                    max_length=self.max_length
                )
                
                # Move to device
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
                
                # Generate translation with improved parameters
                with torch.no_grad():
                    generated_tokens = self.model.generate(
                        **inputs,
                        forced_bos_token_id=self.tokenizer.convert_tokens_to_ids(target_lang),
                        num_beams=8,  # Increased from 5 for better quality
                        num_return_sequences=num_return_sequences,
                        max_length=self.max_length,
                        min_length=1,
                        length_penalty=1.0,  # Balanced length penalty
                        early_stopping=True,  # Stop when all beams finish
                        no_repeat_ngram_size=3,  # Prevent repetition
                        temperature=temperature,
                        do_sample=False
                    )
                
                # Decode translations
                batch_translations = self.tokenizer.batch_decode(
                    generated_tokens,
                    skip_special_tokens=True
                )
                
                translations.extend(batch_translations)
                
                if len(text) > batch_size:
                    progress = min((i + batch_size) / len(text) * 100, 100)
                    print(f"   Progress: {progress:.1f}%")
            
            print(f"Translation complete!")
            
            # Return single string if input was single string
            if single_input:
                return translations[0]
            return translations
            
        except Exception as e:
            raise RuntimeError(f"Translation failed: {str(e)}")
    def translate_sentences(
        self,
        text: str,
        source_lang: str,
        sentence_split: bool = True
    ) -> str:
        """
        Translate text with sentence-level processing for better quality
        
        Args:
            text: Input text in Indic language
            source_lang: Source language code
            sentence_split: Whether to split into sentences
            
        Returns:
            Translated English text
        """
        if not sentence_split or len(text.split()) < 20:
            return self.translate(text, source_lang)
        
        # Simple sentence splitting (can be improved with language-specific tools)
        sentences = self._split_sentences(text)
        
        print(f"Translating {len(sentences)} sentences...")
        
        # Translate each sentence
        translations = self.translate(sentences, source_lang)
        
        # Combine translations
        return " ".join(translations)
    
    def _split_sentences(self, text: str) -> List[str]:
        """
        Simple sentence splitter (basic implementation)
        
        Args:
            text: Input text
            
        Returns:
            List of sentences
        """
        # Basic splitting on common punctuation
        import re
        
        # Split on sentence boundaries
        sentences = re.split(r'[।॥|!?]+', text)
        
        # Clean and filter empty sentences
        sentences = [s.strip() for s in sentences if s.strip()]
        
        return sentences
    
    def batch_translate(
        self,
        texts: List[str],
        source_lang: str,
        batch_size: int = 4
    ) -> List[str]:
        """
        Translate multiple texts efficiently
        
        Args:
            texts: List of input texts
            source_lang: Source language code
            batch_size: Batch size for processing
            
        Returns:
            List of translations
        """
        all_translations = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            translations = self.translate(batch, source_lang)
            all_translations.extend(translations)
        
        return all_translations
    
    def __repr__(self):
        return f"IndicTranslator(model={self.model_name}, device={self.device})"
