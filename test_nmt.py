import sys
import os
# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("Starting NMT Test (NLLB)...")

try:
    from nmt_module import IndicTranslator
    
    print("Imported IndicTranslator successfully.")
    
    print("Initializing model...")
    translator = IndicTranslator(
        model_name="facebook/nllb-200-distilled-600M",
        device="cpu"
    )
    
    print("Model initialized successfully.")
    
    print("Testing translation...")
    text = "नमस्ते दुनिया"
    result = translator.translate(text, source_lang="hin_Deva")
    print(f"Translation result: {result}")
    
    print("Test Complete!")

except Exception as e:
    print(f"ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
