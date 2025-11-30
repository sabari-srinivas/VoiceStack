"""
Quick test script to verify the pipeline setup
"""

import sys
import os
import torch

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')
    sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None


def check_dependencies():
    """Check if all required packages are installed"""
    print("=" * 70)
    print("🔍 Checking Dependencies")
    print("=" * 70)
    
    required_packages = [
        ('torch', 'PyTorch'),
        ('transformers', 'Transformers'),
        ('librosa', 'Librosa'),
        ('soundfile', 'SoundFile'),
        ('numpy', 'NumPy'),
    ]
    
    missing = []
    
    for package, name in required_packages:
        try:
            __import__(package)
            print(f"✅ {name:20} - Installed")
        except ImportError:
            print(f"❌ {name:20} - Missing")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print(f"   Install with: pip install {' '.join(missing)}")
        return False
    
    print("\n✅ All dependencies installed!")
    return True


def check_cuda():
    """Check CUDA availability"""
    print("\n" + "=" * 70)
    print("🎮 Checking CUDA/GPU Support")
    print("=" * 70)
    
    if torch.cuda.is_available():
        print(f"✅ CUDA Available")
        print(f"   Device: {torch.cuda.get_device_name(0)}")
        print(f"   CUDA Version: {torch.version.cuda}")
        print(f"   GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
        return True
    else:
        print("⚠️  CUDA not available - will use CPU")
        print("   Note: Processing will be slower on CPU")
        return False


def show_supported_languages():
    """Display supported languages"""
    try:
        from config import SUPPORTED_LANGUAGES
        
        print("\n" + "=" * 70)
        print("🌏 Supported Indic Languages")
        print("=" * 70)
        
        print(f"\n{'Code':<6} {'Language':<15} {'Script':<15} {'Status'}")
        print("-" * 70)
        
        for code, info in SUPPORTED_LANGUAGES.items():
            print(f"{code:<6} {info['name']:<15} {info['script']:<15} ✅ Ready")
        
        print(f"\nTotal: {len(SUPPORTED_LANGUAGES)} languages supported")
        
    except Exception as e:
        print(f"❌ Error loading config: {e}")


def show_quick_start():
    """Show quick start guide"""
    print("\n" + "=" * 70)
    print("🚀 Quick Start Guide")
    print("=" * 70)
    
    print("""
1. Install dependencies (if not already done):
   pip install -r requirements.txt

2. Basic usage:
   
   from pipeline import IndicSpeechToEnglishPipeline
   
   # Initialize for Hindi
   pipeline = IndicSpeechToEnglishPipeline(language_code='hi')
   
   # Process audio
   result = pipeline.process('your_audio.wav', output_dir='outputs')
   
   # Get English translation
   print(result['english_text'])

3. Run examples:
   python example_usage.py

4. See README.md for detailed documentation
""")


def main():
    """Run all checks"""
    print("\n" + "=" * 70)
    print("🎯 Indic Speech-to-English Translation Pipeline")
    print("   Setup Verification")
    print("=" * 70)
    
    # Check dependencies
    deps_ok = check_dependencies()
    
    if not deps_ok:
        print("\n❌ Please install missing dependencies first:")
        print("   pip install -r requirements.txt")
        return
    
    # Check CUDA
    check_cuda()
    
    # Show supported languages
    show_supported_languages()
    
    # Show quick start
    show_quick_start()
    
    print("\n" + "=" * 70)
    print("✅ Setup verification complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
