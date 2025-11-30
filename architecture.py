"""
Pipeline Architecture Visualization

This module provides a text-based visualization of the pipeline architecture.
"""

import sys
import os

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None


def print_architecture():
    """Print the pipeline architecture diagram"""
    
    diagram = """
╔══════════════════════════════════════════════════════════════════════════╗
║                 INDIC SPEECH-TO-ENGLISH TRANSLATION PIPELINE              ║
╚══════════════════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────────────────┐
│                              INPUT AUDIO FILE                             │
│                    (WAV, MP3, FLAC, OGG, etc.)                           │
└────────────────────────────────┬─────────────────────────────────────────┘
                                 │
                                 ▼
        ┌────────────────────────────────────────────────┐
        │         Audio Preprocessing                     │
        │  • Resample to 16kHz                           │
        │  • Convert to mono                             │
        │  • Normalize audio                             │
        └────────────────┬───────────────────────────────┘
                         │
                         ▼
╔════════════════════════════════════════════════════════════════════════╗
║                    STAGE 1: ASR (Speech-to-Text)                        ║
╠════════════════════════════════════════════════════════════════════════╣
║  Model: AI4Bharat IndicConformer (~600M parameters)                    ║
║  Architecture: Conformer-based CTC                                     ║
║  Input: 16kHz mono audio                                               ║
║  Output: Native Indic script text                                      ║
║                                                                         ║
║  Process:                                                               ║
║  1. Split audio into 30-second chunks                                  ║
║  2. Extract acoustic features                                          ║
║  3. CTC decoding to text                                               ║
║  4. Combine chunks                                                     ║
╚════════════════════════════════════════════════════════════════════════╝
                         │
                         ▼
        ┌────────────────────────────────────────────────┐
        │      Intermediate Output (Optional Save)        │
        │                                                 │
        │  Example (Hindi):                              │
        │  "यह एक परीक्षण वाक्य है"                      │
        │                                                 │
        │  Example (Tamil):                              │
        │  "இது ஒரு சோதனை வாக்கியம்"                    │
        └────────────────┬───────────────────────────────┘
                         │
                         ▼
╔════════════════════════════════════════════════════════════════════════╗
║                  STAGE 2: NMT (Text-to-English)                         ║
╠════════════════════════════════════════════════════════════════════════╣
║  Model: AI4Bharat IndicTrans2-Indic-En-1B (1B parameters)              ║
║  Architecture: Transformer Seq2Seq                                     ║
║  Input: Indic text with language tags                                  ║
║  Output: English text                                                  ║
║                                                                         ║
║  Process:                                                               ║
║  1. Add language-specific tags (e.g., hin_Deva)                       ║
║  2. Tokenize with SentencePiece                                        ║
║  3. Encoder-Decoder translation                                        ║
║  4. Beam search decoding (5 beams)                                     ║
║  5. Post-processing and cleanup                                        ║
╚════════════════════════════════════════════════════════════════════════╝
                         │
                         ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                         FINAL ENGLISH OUTPUT                              │
│                                                                           │
│  Example: "This is a test sentence"                                     │
│                                                                           │
│  Saved as:                                                               │
│  • JSON (complete results with metadata)                                │
│  • TXT (plain English text)                                             │
│  • TXT (intermediate Indic text, optional)                              │
└──────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════
                          SUPPORTED LANGUAGES (10)
═══════════════════════════════════════════════════════════════════════════

┌─────────────┬──────────────┬─────────────────┬──────────────────────────┐
│ Language    │ Code         │ Script          │ ASR Model                │
├─────────────┼──────────────┼─────────────────┼──────────────────────────┤
│ Hindi       │ hi           │ Devanagari      │ indicconformer_hi        │
│ Tamil       │ ta           │ Tamil           │ indicconformer_ta        │
│ Telugu      │ te           │ Telugu          │ indicconformer_te        │
│ Malayalam   │ ml           │ Malayalam       │ indicconformer_ml        │
│ Kannada     │ kn           │ Kannada         │ indicconformer_kn        │
│ Marathi     │ mr           │ Devanagari      │ indicconformer_mr        │
│ Gujarati    │ gu           │ Gujarati        │ indicconformer_gu        │
│ Bengali     │ bn           │ Bengali         │ indicconformer_bn        │
│ Odia        │ or           │ Odia            │ indicconformer_or        │
│ Punjabi     │ pa           │ Gurmukhi        │ indicconformer_pa        │
└─────────────┴──────────────┴─────────────────┴──────────────────────────┘

Note: All languages use the same NMT model (IndicTrans2-Indic-En-1B)


═══════════════════════════════════════════════════════════════════════════
                           PERFORMANCE METRICS
═══════════════════════════════════════════════════════════════════════════

Typical Processing Times (GPU - NVIDIA RTX 3060):
┌────────────────────┬──────────────┬──────────────┬──────────────┐
│ Audio Duration     │ ASR Time     │ NMT Time     │ Total Time   │
├────────────────────┼──────────────┼──────────────┼──────────────┤
│ 10 seconds         │ ~1-2s        │ ~0.3s        │ ~1.5-2.5s    │
│ 30 seconds         │ ~2-4s        │ ~0.5s        │ ~2.5-4.5s    │
│ 1 minute           │ ~4-8s        │ ~0.8s        │ ~5-9s        │
│ 5 minutes          │ ~20-40s      │ ~2s          │ ~22-42s      │
└────────────────────┴──────────────┴──────────────┴──────────────┘

CPU Processing: 10-50x slower than GPU


═══════════════════════════════════════════════════════════════════════════
                            SYSTEM REQUIREMENTS
═══════════════════════════════════════════════════════════════════════════

Minimum:
  • Python 3.8+
  • 8GB RAM
  • 10GB disk space (for models)
  • CPU: Any modern processor

Recommended:
  • Python 3.10+
  • 16GB+ RAM
  • CUDA-capable GPU (4GB+ VRAM)
  • SSD storage


═══════════════════════════════════════════════════════════════════════════
                              DATA FLOW
═══════════════════════════════════════════════════════════════════════════

Audio File → Preprocessing → ASR Model → Indic Text → NMT Model → English
    ↓            ↓              ↓            ↓           ↓           ↓
  WAV/MP3    16kHz Mono    Conformer    Devanagari  Transformer  Output
  Any SR      Normalized      CTC        Tamil etc    Seq2Seq     Files
"""
    
    print(diagram)


if __name__ == "__main__":
    print_architecture()
