# After getting HuggingFace token and logging in:
# Run: huggingface-cli login

# Then use this configuration:

ASR_MODEL_CONFIG = {
    "model_name": "openai/whisper-small",  # Whisper supports all Indic languages
    "sampling_rate": 16000,
    "chunk_length_s": 30,
    "batch_size": 8,
}

NMT_MODEL_CONFIG = {
    "model_name": "ai4bharat/indictrans2-indic-en-1B",  # Requires HuggingFace login
    "batch_size": 4,
    "max_length": 256,
}

# Note: IndicConformer models are not publicly available on HuggingFace
# Whisper is an excellent alternative that supports all Indic languages
