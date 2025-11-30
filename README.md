# 🗣️ Indic Speech-to-English Translation Pipeline

A complete two-stage pipeline for converting spoken Indic languages into English text using state-of-the-art AI4Bharat models.

## 🎯 Overview

This pipeline combines:
1. **ASR (Automatic Speech Recognition)**: Converts Indic language audio → Native Indic script text using **IndicConformer**
2. **NMT (Neural Machine Translation)**: Translates Indic text → English using **IndicTrans2**

## ✨ Features

- 🌏 **10 Indic Languages Supported**: Hindi, Tamil, Telugu, Malayalam, Kannada, Marathi, Gujarati, Bengali, Odia, Punjabi
- 🚀 **GPU Acceleration**: Automatic CUDA support for faster processing
- 📦 **Batch Processing**: Process multiple audio files efficiently
- 💾 **Flexible Output**: Save results in JSON, TXT, or custom formats
- 🎵 **Audio Format Support**: WAV, MP3, FLAC, OGG, and more
- ⚡ **Chunked Processing**: Handle long audio files seamlessly
- 📊 **Detailed Metrics**: Processing time tracking for each stage

## 📋 Supported Languages

| Code | Language   | Script      | ASR Model                                    |
|------|------------|-------------|----------------------------------------------|
| `hi` | Hindi      | Devanagari  | ai4bharat/indicconformer_stt_hi_hybrid_v2   |
| `ta` | Tamil      | Tamil       | ai4bharat/indicconformer_stt_ta_hybrid_v2   |
| `te` | Telugu     | Telugu      | ai4bharat/indicconformer_stt_te_hybrid_v2   |
| `ml` | Malayalam  | Malayalam   | ai4bharat/indicconformer_stt_ml_hybrid_v2   |
| `kn` | Kannada    | Kannada     | ai4bharat/indicconformer_stt_kn_hybrid_v2   |
| `mr` | Marathi    | Devanagari  | ai4bharat/indicconformer_stt_mr_hybrid_v2   |
| `gu` | Gujarati   | Gujarati    | ai4bharat/indicconformer_stt_gu_hybrid_v2   |
| `bn` | Bengali    | Bengali     | ai4bharat/indicconformer_stt_bn_hybrid_v2   |
| `or` | Odia       | Odia        | ai4bharat/indicconformer_stt_or_hybrid_v2   |
| `pa` | Punjabi    | Gurmukhi    | ai4bharat/indicconformer_stt_pa_hybrid_v2   |

**NMT Model**: `ai4bharat/indictrans2-indic-en-1B` (shared across all languages)

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- CUDA-capable GPU (recommended for faster processing)
- 8GB+ RAM (16GB+ recommended)

### Setup

1. **Clone or download this repository**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Verify installation**:
```bash
python pipeline.py
```

This should display the list of supported languages.

## 📖 Quick Start

### Basic Usage

```python
from pipeline import IndicSpeechToEnglishPipeline

# Initialize pipeline for Hindi
pipeline = IndicSpeechToEnglishPipeline(
    language_code='hi',  # Hindi
    device='cuda'        # Use 'cpu' if no GPU
)

# Process audio file
result = pipeline.process(
    audio_path='hindi_audio.wav',
    output_dir='outputs',
    save_intermediate=True
)

# Access results
print("Indic Text:", result['indic_text'])
print("English Translation:", result['english_text'])
print("Processing Time:", result['processing_time']['total'], "seconds")
```

### Batch Processing

```python
# Process multiple files
audio_files = [
    'audio1.wav',
    'audio2.wav',
    'audio3.wav'
]

results = pipeline.process_batch(
    audio_paths=audio_files,
    output_dir='outputs/batch'
)
```

### Different Languages

```python
# Tamil
tamil_pipeline = IndicSpeechToEnglishPipeline(language_code='ta')
result = tamil_pipeline.process('tamil_audio.wav')

# Bengali
bengali_pipeline = IndicSpeechToEnglishPipeline(language_code='bn')
result = bengali_pipeline.process('bengali_audio.wav')
```

## 📁 Project Structure

```
Voice/
├── pipeline.py           # Main pipeline orchestrator
├── asr_module.py         # ASR (Speech-to-Text) module
├── nmt_module.py         # NMT (Translation) module
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── example_usage.py      # Usage examples
└── README.md            # This file
```

## 🔧 Configuration

Edit `config.py` to customize:

```python
# ASR settings
ASR_MODEL_CONFIG = {
    "sampling_rate": 16000,
    "chunk_length_s": 30,
    "batch_size": 8,
}

# NMT settings
NMT_MODEL_CONFIG = {
    "model_name": "ai4bharat/indictrans2-indic-en-1B",
    "batch_size": 4,
    "max_length": 256,
}
```

## 📊 Output Format

### JSON Output (`*_result.json`)
```json
{
  "audio_path": "audio.wav",
  "language": {
    "code": "hi",
    "name": "Hindi",
    "script": "Devanagari"
  },
  "indic_text": "मूल हिंदी पाठ...",
  "english_text": "Translated English text...",
  "processing_time": {
    "asr": 2.34,
    "nmt": 0.56,
    "total": 2.90
  },
  "timestamp": "2025-11-29T09:48:35"
}
```

### Text Files
- `*_indic.txt`: Transcribed text in native script
- `*_english.txt`: Final English translation

## 🎛️ Advanced Usage

### Custom Device Selection
```python
# Use specific GPU
pipeline = IndicSpeechToEnglishPipeline(
    language_code='hi',
    device='cuda:0'  # Specific GPU
)

# Force CPU
pipeline = IndicSpeechToEnglishPipeline(
    language_code='hi',
    device='cpu'
)
```

### Lazy Model Loading
```python
# Initialize without loading models
pipeline = IndicSpeechToEnglishPipeline(
    language_code='hi',
    load_models=False
)

# Load models when needed
pipeline.load_models()
```

### Direct Module Usage

#### ASR Only
```python
from asr_module import IndicASR

asr = IndicASR(
    model_name='ai4bharat/indicconformer_stt_hi_hybrid_v2',
    device='cuda'
)

text = asr.transcribe('audio.wav')
print(text)
```

#### NMT Only
```python
from nmt_module import IndicTranslator

translator = IndicTranslator(
    model_name='ai4bharat/indictrans2-indic-en-1B',
    device='cuda'
)

english = translator.translate(
    text='हिंदी पाठ',
    source_lang='hin_Deva'
)
print(english)
```

## 🔍 Examples

See `example_usage.py` for comprehensive examples:
- Single file processing
- Batch processing
- Multiple languages
- Custom output handling
- Lazy loading

Run examples:
```bash
python example_usage.py
```

## ⚡ Performance Tips

1. **Use GPU**: Processing is 10-50x faster with CUDA
2. **Batch Processing**: Process multiple files together for efficiency
3. **Chunk Length**: Adjust `chunk_length_s` in config for memory/speed tradeoff
4. **Model Caching**: Models are cached after first download

## 🐛 Troubleshooting

### Out of Memory
- Reduce `batch_size` in config
- Reduce `chunk_length_s` for ASR
- Use CPU instead of GPU
- Process files one at a time

### Slow Processing
- Ensure CUDA is properly installed
- Check `device='cuda'` is set
- Reduce audio file size/duration
- Use batch processing for multiple files

### Model Download Issues
- Check internet connection
- Models are downloaded from HuggingFace Hub
- First run will download ~2-3GB of models
- Models are cached in `~/.cache/huggingface/`

## 📚 Model Information

### ASR Models (IndicConformer)
- **Architecture**: Conformer-based CTC
- **Training Data**: AI4Bharat's Indic speech datasets
- **Size**: ~600M parameters per language
- **Input**: 16kHz mono audio
- **Output**: Native Indic script text

### NMT Model (IndicTrans2)
- **Architecture**: Transformer-based Seq2Seq
- **Training Data**: FLORES-200, Samanantar, BPCC
- **Size**: 1B parameters
- **Input**: Indic text with language tags
- **Output**: English text

## 🙏 Credits

This pipeline uses models from [AI4Bharat](https://ai4bharat.org/):
- **IndicConformer**: [Paper](https://arxiv.org/abs/2301.01926)
- **IndicTrans2**: [Paper](https://arxiv.org/abs/2305.16307)

## 📄 License

This project is provided as-is for educational and research purposes. Please refer to AI4Bharat's model licenses for commercial use.

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional language support
- Better sentence segmentation
- Real-time streaming support
- Web interface
- API server

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review `example_usage.py`
3. Check AI4Bharat documentation
4. Open an issue with error details

## 🎓 Citation

If you use this pipeline in research, please cite the AI4Bharat models:

```bibtex
@article{javed2023indicconformer,
  title={IndicConformer: A Conformer-based ASR Framework for Indian Languages},
  author={Javed, Tahir and others},
  journal={arXiv preprint arXiv:2301.01926},
  year={2023}
}

@article{gala2023indictrans2,
  title={IndicTrans2: Towards High-Quality and Accessible Machine Translation Models for all 22 Scheduled Indian Languages},
  author={Gala, Jay and others},
  journal={arXiv preprint arXiv:2305.16307},
  year={2023}
}
```

---

**Made with ❤️ for Indic Language Processing**
