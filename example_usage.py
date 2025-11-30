"""
Example Usage of Indic Speech-to-English Translation Pipeline

This script demonstrates how to use the pipeline for various scenarios.
"""

import os
from pathlib import Path
from pipeline import IndicSpeechToEnglishPipeline, list_supported_languages


def example_single_file():
    """Example: Process a single audio file"""
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Single File Processing")
    print("=" * 70)
    
    # Initialize pipeline for Hindi
    pipeline = IndicSpeechToEnglishPipeline(
        language_code='hi',  # Hindi
        device='cuda'  # Use 'cpu' if no GPU available
    )
    
    # Process audio file
    audio_file = "path/to/your/hindi_audio.wav"
    
    # Check if file exists (for demo purposes)
    if not os.path.exists(audio_file):
        print(f"\n⚠️  Demo file not found: {audio_file}")
        print("   Please provide a valid audio file path")
        return
    
    result = pipeline.process(
        audio_path=audio_file,
        output_dir="outputs",
        save_intermediate=True
    )
    
    # Access results
    print("\n📊 Results:")
    print(f"   Indic Text: {result['indic_text'][:100]}...")
    print(f"   English Text: {result['english_text'][:100]}...")
    print(f"   Processing Time: {result['processing_time']['total']}s")


def example_batch_processing():
    """Example: Process multiple audio files"""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Batch Processing")
    print("=" * 70)
    
    # Initialize pipeline for Tamil
    pipeline = IndicSpeechToEnglishPipeline(
        language_code='ta',  # Tamil
        device='cuda'
    )
    
    # List of audio files
    audio_files = [
        "path/to/tamil_audio1.wav",
        "path/to/tamil_audio2.wav",
        "path/to/tamil_audio3.wav"
    ]
    
    # Filter existing files
    existing_files = [f for f in audio_files if os.path.exists(f)]
    
    if not existing_files:
        print("\n⚠️  No demo files found")
        print("   Please provide valid audio file paths")
        return
    
    # Process all files
    results = pipeline.process_batch(
        audio_paths=existing_files,
        output_dir="outputs/batch"
    )
    
    # Summary
    print("\n📊 Batch Processing Summary:")
    for i, result in enumerate(results, 1):
        if 'error' in result:
            print(f"   [{i}] ❌ Error: {result['error']}")
        else:
            print(f"   [{i}] ✅ Success - {result['processing_time']['total']}s")


def example_different_languages():
    """Example: Process files in different languages"""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Multiple Languages")
    print("=" * 70)
    
    # Define files with their languages
    files_with_languages = [
        ("path/to/hindi_audio.wav", "hi"),
        ("path/to/tamil_audio.wav", "ta"),
        ("path/to/bengali_audio.wav", "bn"),
    ]
    
    results = []
    
    for audio_file, lang_code in files_with_languages:
        if not os.path.exists(audio_file):
            print(f"\n⚠️  File not found: {audio_file}")
            continue
        
        # Create pipeline for specific language
        pipeline = IndicSpeechToEnglishPipeline(
            language_code=lang_code,
            device='cuda'
        )
        
        # Process file
        result = pipeline.process(
            audio_path=audio_file,
            output_dir=f"outputs/{lang_code}"
        )
        
        results.append(result)
    
    print(f"\n✅ Processed {len(results)} files in different languages")


def example_custom_output():
    """Example: Custom output handling"""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Custom Output Handling")
    print("=" * 70)
    
    pipeline = IndicSpeechToEnglishPipeline(
        language_code='mr',  # Marathi
        device='cuda'
    )
    
    audio_file = "path/to/marathi_audio.wav"
    
    if not os.path.exists(audio_file):
        print(f"\n⚠️  Demo file not found: {audio_file}")
        return
    
    # Process without saving to disk
    result = pipeline.process(
        audio_path=audio_file,
        output_dir=None,  # Don't save to disk
        save_intermediate=False
    )
    
    # Custom processing of results
    print("\n📝 Custom Output:")
    print(f"   Language: {result['language']['name']}")
    print(f"   Original ({result['language']['script']}): {result['indic_text']}")
    print(f"   Translation: {result['english_text']}")
    
    # Save in custom format
    output_file = "custom_output.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Language: {result['language']['name']}\n")
        f.write(f"Script: {result['language']['script']}\n")
        f.write(f"\nOriginal Text:\n{result['indic_text']}\n")
        f.write(f"\nEnglish Translation:\n{result['english_text']}\n")
    
    print(f"\n💾 Saved custom output to: {output_file}")


def example_lazy_loading():
    """Example: Lazy model loading for faster initialization"""
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Lazy Model Loading")
    print("=" * 70)
    
    # Initialize without loading models
    pipeline = IndicSpeechToEnglishPipeline(
        language_code='gu',  # Gujarati
        load_models=False  # Don't load models yet
    )
    
    print("✅ Pipeline initialized (models not loaded)")
    
    # Load models only when needed
    print("\n🔄 Loading models now...")
    pipeline.load_models()
    
    # Now ready to process
    print("✅ Ready to process audio files")


def main():
    """Run all examples"""
    print("\n" + "=" * 70)
    print("🎯 Indic Speech-to-English Translation Pipeline Examples")
    print("=" * 70)
    
    # Show supported languages
    list_supported_languages()
    
    # Note: These examples use placeholder paths
    # Replace with actual audio file paths to run
    
    print("\n" + "=" * 70)
    print("📝 USAGE NOTES:")
    print("=" * 70)
    print("""
    1. Replace placeholder paths with actual audio files
    2. Supported formats: WAV, MP3, FLAC, OGG, etc.
    3. Audio will be automatically resampled to 16kHz
    4. Use 'cuda' device for GPU acceleration (much faster)
    5. Use 'cpu' device if no GPU is available
    
    Quick Start:
    ------------
    from pipeline import IndicSpeechToEnglishPipeline
    
    # Initialize for your language
    pipeline = IndicSpeechToEnglishPipeline(language_code='hi')
    
    # Process audio
    result = pipeline.process('your_audio.wav', output_dir='outputs')
    
    # Get English translation
    english_text = result['english_text']
    print(english_text)
    """)
    
    # Uncomment to run specific examples:
    # example_single_file()
    # example_batch_processing()
    # example_different_languages()
    # example_custom_output()
    # example_lazy_loading()


if __name__ == "__main__":
    main()
