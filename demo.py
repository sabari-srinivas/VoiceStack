"""
Simple Demo Script for Indic Speech-to-English Translation

This script provides a command-line interface for easy testing.
"""

import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description='Indic Speech-to-English Translation Pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process Hindi audio
  python demo.py --audio hindi_speech.wav --lang hi
  
  # Process Tamil audio with custom output directory
  python demo.py --audio tamil_speech.wav --lang ta --output results/
  
  # Process on CPU (no GPU)
  python demo.py --audio audio.wav --lang hi --device cpu
  
  # Batch process multiple files
  python demo.py --audio file1.wav file2.wav file3.wav --lang hi

Supported Languages:
  hi - Hindi        ta - Tamil       te - Telugu
  ml - Malayalam    kn - Kannada     mr - Marathi
  gu - Gujarati     bn - Bengali     or - Odia
  pa - Punjabi
        """
    )
    
    parser.add_argument(
        '--audio', '-a',
        nargs='+',
        required=True,
        help='Path(s) to audio file(s) (WAV, MP3, FLAC, etc.)'
    )
    
    parser.add_argument(
        '--lang', '-l',
        required=True,
        choices=['hi', 'ta', 'te', 'ml', 'kn', 'mr', 'gu', 'bn', 'or', 'pa'],
        help='Language code of the audio'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='outputs',
        help='Output directory for results (default: outputs/)'
    )
    
    parser.add_argument(
        '--device', '-d',
        default='cuda',
        choices=['cuda', 'cpu'],
        help='Device to use for processing (default: cuda)'
    )
    
    parser.add_argument(
        '--no-save-intermediate',
        action='store_true',
        help='Don\'t save intermediate ASR output'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Minimal output'
    )
    
    args = parser.parse_args()
    
    # Import here to avoid slow imports when just showing help
    try:
        from pipeline import IndicSpeechToEnglishPipeline
    except ImportError as e:
        print(f"❌ Error: {e}")
        print("\n💡 Please install dependencies first:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Validate audio files
    audio_files = []
    for audio_path in args.audio:
        path = Path(audio_path)
        if not path.exists():
            print(f"❌ Error: Audio file not found: {audio_path}")
            sys.exit(1)
        audio_files.append(str(path))
    
    if not args.quiet:
        print("\n" + "=" * 70)
        print("🎯 Indic Speech-to-English Translation")
        print("=" * 70)
        print(f"   Language: {args.lang}")
        print(f"   Device: {args.device}")
        print(f"   Files: {len(audio_files)}")
        print("=" * 70)
    
    try:
        # Initialize pipeline
        pipeline = IndicSpeechToEnglishPipeline(
            language_code=args.lang,
            device=args.device
        )
        
        # Process files
        if len(audio_files) == 1:
            # Single file
            result = pipeline.process(
                audio_path=audio_files[0],
                output_dir=args.output,
                save_intermediate=not args.no_save_intermediate,
                verbose=not args.quiet
            )
            
            if not args.quiet:
                print("\n" + "=" * 70)
                print("📄 Results")
                print("=" * 70)
                print(f"\n🔤 Original ({result['language']['script']}):")
                print(f"   {result['indic_text'][:200]}...")
                print(f"\n🌐 English Translation:")
                print(f"   {result['english_text'][:200]}...")
                print(f"\n⏱️  Processing Time: {result['processing_time']['total']}s")
            else:
                print(result['english_text'])
        
        else:
            # Batch processing
            results = pipeline.process_batch(
                audio_paths=audio_files,
                output_dir=args.output
            )
            
            if not args.quiet:
                print("\n" + "=" * 70)
                print("📊 Batch Processing Summary")
                print("=" * 70)
                
                for i, result in enumerate(results, 1):
                    if 'error' in result:
                        print(f"\n[{i}] ❌ {Path(result['audio_path']).name}")
                        print(f"    Error: {result['error']}")
                    else:
                        print(f"\n[{i}] ✅ {Path(result['audio_path']).name}")
                        print(f"    Time: {result['processing_time']['total']}s")
                        print(f"    Translation: {result['english_text'][:100]}...")
        
        if not args.quiet:
            print("\n" + "=" * 70)
            print(f"✅ Complete! Results saved to: {args.output}/")
            print("=" * 70)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if not args.quiet:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
