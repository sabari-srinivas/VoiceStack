# 📑 Project Index

Welcome to the **Indic Speech-to-English Translation Pipeline**!

This index helps you navigate the project and find what you need quickly.

---

## 🚀 Getting Started (Start Here!)

1. **[QUICKSTART.md](QUICKSTART.md)** ⭐
   - Fastest way to get up and running
   - Installation in 2 steps
   - Basic usage examples
   - **Read this first!**

2. **[test_setup.py](test_setup.py)**
   - Verify your installation
   - Check dependencies
   - Test GPU availability
   - Run: `python test_setup.py`

3. **[demo.py](demo.py)**
   - Command-line interface
   - Process audio files easily
   - Run: `python demo.py --help`

---

## 📚 Documentation

### For Users

- **[README.md](README.md)** - Complete documentation
  - Full feature list
  - Detailed installation guide
  - API reference
  - Troubleshooting guide
  - Performance tips

- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Project overview
  - What this pipeline does
  - Key features
  - Use cases
  - Technical specifications

- **[architecture.py](architecture.py)** - Visual architecture
  - Pipeline flow diagram
  - Supported languages table
  - Performance metrics
  - Run: `python architecture.py`

### For Developers

- **[example_usage.py](example_usage.py)** - Code examples
  - Single file processing
  - Batch processing
  - Multiple languages
  - Custom output handling
  - Advanced usage patterns

---

## 💻 Core Code

### Main Pipeline

- **[pipeline.py](pipeline.py)** - Main orchestrator
  - `IndicSpeechToEnglishPipeline` class
  - Combines ASR + NMT
  - Batch processing
  - Result saving

### Modules

- **[asr_module.py](asr_module.py)** - Speech-to-Text
  - `IndicASR` class
  - Audio preprocessing
  - IndicConformer models
  - Chunked processing

- **[nmt_module.py](nmt_module.py)** - Translation
  - `IndicTranslator` class
  - IndicTrans2 model
  - Sentence-level translation
  - Batch translation

### Configuration

- **[config.py](config.py)** - Settings
  - Model configurations
  - Supported languages
  - Audio settings
  - Output formats

---

## 🛠️ Utilities

- **[requirements.txt](requirements.txt)** - Dependencies
  - All required packages
  - Install: `pip install -r requirements.txt`

- **[.gitignore](.gitignore)** - Git ignore rules
  - Excludes models, outputs, cache

---

## 📖 How to Use This Project

### Scenario 1: Quick Test
```
1. Read QUICKSTART.md
2. Run: pip install -r requirements.txt
3. Run: python demo.py --audio your_audio.wav --lang hi
```

### Scenario 2: Integrate into Your Code
```
1. Read example_usage.py
2. Copy relevant code
3. Customize for your needs
```

### Scenario 3: Understand the Architecture
```
1. Read PROJECT_SUMMARY.md
2. Run: python architecture.py
3. Read README.md for details
```

### Scenario 4: Troubleshooting
```
1. Run: python test_setup.py
2. Check README.md troubleshooting section
3. Review example_usage.py for correct usage
```

---

## 🎯 File Purpose Quick Reference

| File | Purpose | When to Use |
|------|---------|-------------|
| **QUICKSTART.md** | Quick start guide | First time setup |
| **README.md** | Full documentation | Detailed reference |
| **PROJECT_SUMMARY.md** | Project overview | Understanding the project |
| **demo.py** | CLI tool | Quick testing |
| **example_usage.py** | Code examples | Learning the API |
| **test_setup.py** | Setup verification | Checking installation |
| **architecture.py** | Visual diagram | Understanding flow |
| **pipeline.py** | Main code | Using the pipeline |
| **asr_module.py** | ASR component | Speech-to-text only |
| **nmt_module.py** | NMT component | Translation only |
| **config.py** | Settings | Customization |
| **requirements.txt** | Dependencies | Installation |

---

## 🌟 Common Tasks

### Install the Pipeline
```bash
pip install -r requirements.txt
python test_setup.py
```

### Process a Single Audio File
```bash
python demo.py --audio audio.wav --lang hi
```

### Process Multiple Files
```bash
python demo.py --audio file1.wav file2.wav file3.wav --lang ta
```

### Use in Python Code
```python
from pipeline import IndicSpeechToEnglishPipeline
pipeline = IndicSpeechToEnglishPipeline(language_code='hi')
result = pipeline.process('audio.wav')
```

### Check Supported Languages
```python
from pipeline import list_supported_languages
list_supported_languages()
```

### Use ASR Only
```python
from asr_module import IndicASR
asr = IndicASR(model_name='ai4bharat/indicconformer_stt_hi_hybrid_v2')
text = asr.transcribe('audio.wav')
```

### Use NMT Only
```python
from nmt_module import IndicTranslator
translator = IndicTranslator()
english = translator.translate('हिंदी पाठ', source_lang='hin_Deva')
```

---

## 🆘 Need Help?

1. **Installation issues?** → Run `test_setup.py`
2. **Usage questions?** → Read `QUICKSTART.md`
3. **Code examples?** → Check `example_usage.py`
4. **Understanding pipeline?** → Read `PROJECT_SUMMARY.md`
5. **Detailed docs?** → See `README.md`
6. **Architecture?** → Run `architecture.py`

---

## 📊 Project Statistics

- **Total Files**: 13
- **Code Files**: 7 (Python)
- **Documentation**: 4 (Markdown)
- **Total Lines**: ~1,500+
- **Supported Languages**: 10
- **AI Models**: 11 (10 ASR + 1 NMT)

---

## 🎓 Learning Path

### Beginner
1. QUICKSTART.md
2. demo.py (try it out)
3. PROJECT_SUMMARY.md

### Intermediate
1. README.md
2. example_usage.py
3. config.py

### Advanced
1. pipeline.py
2. asr_module.py
3. nmt_module.py

---

## 🔗 Quick Links

- **Start Here**: [QUICKSTART.md](QUICKSTART.md)
- **Full Docs**: [README.md](README.md)
- **Examples**: [example_usage.py](example_usage.py)
- **Test Setup**: Run `python test_setup.py`
- **CLI Tool**: Run `python demo.py --help`

---

**Happy Translating! 🎉**

*For questions or issues, refer to the troubleshooting section in README.md*
