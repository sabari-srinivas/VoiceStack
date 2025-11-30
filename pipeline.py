"""
Indic Speech-to-English Translation Pipeline
Two-stage pipeline: ASR (Speech-to-Text) + NMT (Text-to-English)
"""

import os
import json
import time
from pathlib import Path
from typing import Optional, Dict, Union, List
from datetime import datetime

from asr_module import IndicASR
from nmt_module import IndicTranslator
from config import (
    SUPPORTED_LANGUAGES,
    ASR_MODEL_CONFIG,
    NMT_MODEL_CONFIG,
    OUTPUT_CONFIG
)


class IndicSpeechToEnglishPipeline:
    """
    Complete pipeline for converting Indic speech to English text
    """
    
    def __init__(
        self,
        language_code: str,
        device: Optional[str] = None,
        load_models: bool = True
    ):
        """
        Initialize the pipeline
        
        Args:
            language_code: Language code (e.g., 'hi' for Hindi, 'ta' for Tamil)
            device: Device to run models on ('cuda', 'cpu', or None for auto)
            load_models: Whether to load models immediately
        """
        if language_code not in SUPPORTED_LANGUAGES:
            raise ValueError(
                f"Unsupported language: {language_code}. "
                f"Supported languages: {list(SUPPORTED_LANGUAGES.keys())}"
            )
        
        self.language_code = language_code
        self.language_info = SUPPORTED_LANGUAGES[language_code]
        self.device = device
        
        print("=" * 70)
        print(f"Initializing Indic Speech-to-English Pipeline")
        print(f"   Language: {self.language_info['name']} ({language_code})")
        print(f"   Script: {self.language_info['script']}")
        print("=" * 70)
        
        self.asr_model = None
        self.nmt_model = None
        
        if load_models:
            self.load_models()
    
    def load_models(self):
        """Load ASR and NMT models"""
        print("\nLoading models...")
        
        # Load ASR model
        print("\n[1/2] Loading ASR Model")
        self.asr_model = IndicASR(
            model_name=self.language_info['asr_model'],
            device=self.device,
            sampling_rate=ASR_MODEL_CONFIG['sampling_rate']
        )
        
        # Load NMT model
        print("\n[2/2] Loading NMT Model")
        self.nmt_model = IndicTranslator(
            model_name=NMT_MODEL_CONFIG['model_name'],
            device=self.device,
            max_length=NMT_MODEL_CONFIG['max_length']
        )
        
        print("\nAll models loaded successfully!")
    
    def process(
        self,
        audio_path: str,
        output_dir: Optional[str] = None,
        save_intermediate: bool = True,
        verbose: bool = True
    ) -> Dict[str, str]:
        """
        Process audio file through the complete pipeline
        
        Args:
            audio_path: Path to input audio file
            output_dir: Directory to save outputs (optional)
            save_intermediate: Whether to save ASR output
            verbose: Whether to print detailed progress
            
        Returns:
            Dictionary containing:
                - audio_path: Input audio file path
                - indic_text: Transcribed Indic text (ASR output)
                - english_text: Translated English text (NMT output)
                - language: Language information
                - processing_time: Total processing time
        """
        if not self.asr_model or not self.nmt_model:
            raise RuntimeError("Models not loaded. Call load_models() first.")
        
        start_time = time.time()
        
        print("\n" + "=" * 70)
        print(f"Starting Pipeline Processing")
        print(f"   Input: {audio_path}")
        print("=" * 70)
        
        # Stage 1: ASR (Speech to Indic Text)
        print("\n" + "─" * 70)
        print("STAGE 1: Automatic Speech Recognition (ASR)")
        print("─" * 70)
        
        asr_start = time.time()
        indic_text = self.asr_model.transcribe(
            audio_path,
            language_code=self.language_code
        )
        asr_time = time.time() - asr_start
        
        if verbose:
            print(f"\nTranscribed Text ({self.language_info['script']}):")
            print(f"   {indic_text[:200]}{'...' if len(indic_text) > 200 else ''}")
            print(f"\nASR Time: {asr_time:.2f}s")
        
        # Stage 2: NMT (Indic Text to English)
        print("\n" + "─" * 70)
        print("STAGE 2: Neural Machine Translation (NMT)")
        print("─" * 70)
        
        nmt_start = time.time()
        english_text = self.nmt_model.translate_sentences(
            indic_text,
            source_lang=self.language_info['flores_code']
        )
        nmt_time = time.time() - nmt_start
        
        if verbose:
            print(f"\nTranslated Text (English):")
            print(f"   {english_text[:200]}{'...' if len(english_text) > 200 else ''}")
            print(f"\nNMT Time: {nmt_time:.2f}s")
        
        total_time = time.time() - start_time
        
        # Prepare result
        result = {
            "audio_path": audio_path,
            "language": {
                "code": self.language_code,
                "name": self.language_info['name'],
                "script": self.language_info['script']
            },
            "indic_text": indic_text,
            "english_text": english_text,
            "processing_time": {
                "asr": round(asr_time, 2),
                "nmt": round(nmt_time, 2),
                "total": round(total_time, 2)
            },
            "timestamp": datetime.now().isoformat()
        }
        
        # Save outputs if directory specified
        if output_dir:
            self._save_outputs(result, output_dir, save_intermediate)
        
        print("\n" + "=" * 70)
        print("Pipeline Processing Complete!")
        print(f"   Total Time: {total_time:.2f}s")
        print("=" * 70)
        
        return result
    
    def process_batch(
        self,
        audio_paths: List[str],
        output_dir: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """
        Process multiple audio files
        
        Args:
            audio_paths: List of audio file paths
            output_dir: Directory to save outputs
            
        Returns:
            List of result dictionaries
        """
        results = []
        
        print(f"\nProcessing {len(audio_paths)} audio files...")
        
        for i, audio_path in enumerate(audio_paths, 1):
            print(f"\n{'=' * 70}")
            print(f"Processing file {i}/{len(audio_paths)}")
            print(f"{'=' * 70}")
            
            try:
                result = self.process(audio_path, output_dir)
                results.append(result)
            except Exception as e:
                print(f"Error processing {audio_path}: {str(e)}")
                results.append({
                    "audio_path": audio_path,
                    "error": str(e)
                })
        
        return results
    
    def _save_outputs(
        self,
        result: Dict,
        output_dir: str,
        save_intermediate: bool
    ):
        """Save processing results to files"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate base filename from audio file
        audio_name = Path(result['audio_path']).stem
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"{audio_name}_{timestamp}"
        
        # Save complete result as JSON
        json_path = output_path / f"{base_name}_result.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\nSaved JSON result: {json_path}")
        
        # Save intermediate ASR output if requested
        if save_intermediate:
            indic_path = output_path / f"{base_name}_indic.txt"
            with open(indic_path, 'w', encoding='utf-8') as f:
                f.write(result['indic_text'])
            print(f"Saved Indic text: {indic_path}")
        
        # Save final English translation
        english_path = output_path / f"{base_name}_english.txt"
        with open(english_path, 'w', encoding='utf-8') as f:
            f.write(result['english_text'])
        print(f"Saved English text: {english_path}")
    
    def __repr__(self):
        return (
            f"IndicSpeechToEnglishPipeline("
            f"language={self.language_info['name']}, "
            f"device={self.device})"
        )


def list_supported_languages():
    """Print all supported languages"""
    print("\nSupported Indic Languages:")
    print("=" * 70)
    for code, info in SUPPORTED_LANGUAGES.items():
        print(f"  [{code}] {info['name']:15} - Script: {info['script']}")
    print("=" * 70)


if __name__ == "__main__":
    # Example usage
    list_supported_languages()
