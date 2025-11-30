# 🚀 Quick Start Guide

## Installation

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- PyTorch (Deep Learning framework)
- Transformers (HuggingFace models)
- Audio processing libraries (librosa, soundfile)
- Other utilities

**Note**: First run will download ~2-3GB of models from HuggingFace.

### Step 2: Verify Setup
```bash
python test_setup.py
```

This checks:
- ✅ All dependencies installed
- ✅ CUDA/GPU availability
- ✅ Supported languages list

---

## Basic Usage

### Option 1: Command Line (Easiest)

```bash
# Process Hindi audio
python demo.py --audio your_audio.wav --lang hi

# Process Tamil audio
python demo.py --audio tamil_speech.mp3 --lang ta

# Use CPU instead of GPU
python demo.py --audio audio.wav --lang hi --device cpu

# Batch process multiple files
python demo.py --audio file1.wav file2.wav file3.wav --lang hi
```

### Option 2: Python Script

```python
from pipeline import IndicSpeechToEnglishPipeline

# Initialize for Hindi
pipeline = IndicSpeechToEnglishPipeline(language_code='hi')

# Process audio
result = pipeline.process('hindi_audio.wav', output_dir='outputs')

# Get results
print("Indic Text:", result['indic_text'])
print("English:", result['english_text'])
```

---

## Supported Languages

| Code | Language  | Code | Language  |
|------|-----------|------|-----------|
| `hi` | Hindi     | `ta` | Tamil     |
| `te` | Telugu    | `ml` | Malayalam |
| `kn` | Kannada   | `mr` | Marathi   |
| `gu` | Gujarati  | `bn` | Bengali   |
| `or` | Odia      | `pa` | Punjabi   |

---

## Output Files

After processing, you'll get:

```
outputs/
├── audio_20251129_094835_result.json    # Complete results
├── audio_20251129_094835_indic.txt      # Transcribed Indic text
└── audio_20251129_094835_english.txt    # English translation
```

---

## Common Commands

```bash
# View help
python demo.py --help

# Run examples
python example_usage.py

# Test setup
python test_setup.py
```

---

## Troubleshooting

### "Missing packages" error
```bash
pip install -r requirements.txt
```

### Out of memory
- Use `--device cpu` instead of GPU
- Process shorter audio files
- Reduce batch size in config.py

### Slow processing
- Ensure GPU is being used (check with test_setup.py)
- First run downloads models (one-time, ~2-3GB)
- Subsequent runs are much faster

---

## Next Steps

1. ✅ Install dependencies
2. ✅ Test with your audio file
3. 📖 Read [README.md](README.md) for detailed documentation
4. 🔧 Customize settings in [config.py](config.py)
5. 💡 Check [example_usage.py](example_usage.py) for advanced usage

---

## Need Help?

- Check [README.md](README.md) for full documentation
- Review [example_usage.py](example_usage.py) for code examples
- Verify setup with `python test_setup.py`

---

**Happy Translating! 🎉**
