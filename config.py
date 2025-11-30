"""
Configuration file for Indic Speech-to-English Translation Pipeline
"""

# Model configurations
ASR_MODEL_CONFIG = {
    "model_name": "ai4bharat/indicconformer_stt_hi_hybrid_v2",  # Hindi ASR model
    "sampling_rate": 16000,
    "chunk_length_s": 30,
    "batch_size": 8,
}

NMT_MODEL_CONFIG = {
    "model_name": "facebook/nllb-200-1.3B",  # NLLB-1.3B - Better quality than 600M
    "batch_size": 4,
    "max_length": 512,  # Increased from 256 for longer sentences
}

# Supported Indic languages mapping
# Using AI4Bharat IndicConformer Multilingual model
SUPPORTED_LANGUAGES = {
    "hi": {
        "name": "Hindi",
        "asr_model": "ai4bharat/indic-conformer-600m-multilingual",
        "flores_code": "hin_Deva",
        "script": "Devanagari"
    },
    "ta": {
        "name": "Tamil",
        "asr_model": "ai4bharat/indic-conformer-600m-multilingual",
        "flores_code": "tam_Taml",
        "script": "Tamil"
    },
    "te": {
        "name": "Telugu",
        "asr_model": "ai4bharat/indic-conformer-600m-multilingual",
        "flores_code": "tel_Telu",
        "script": "Telugu"
    },
    "ml": {
        "name": "Malayalam",
        "asr_model": "ai4bharat/indic-conformer-600m-multilingual",
        "flores_code": "mal_Mlym",
        "script": "Malayalam"
    },
    "kn": {
        "name": "Kannada",
        "asr_model": "ai4bharat/indic-conformer-600m-multilingual",
        "flores_code": "kan_Knda",
        "script": "Kannada"
    },
    "mr": {
        "name": "Marathi",
        "asr_model": "ai4bharat/indic-conformer-600m-multilingual",
        "flores_code": "mar_Deva",
        "script": "Devanagari"
    },
    "gu": {
        "name": "Gujarati",
        "asr_model": "ai4bharat/indic-conformer-600m-multilingual",
        "flores_code": "guj_Gujr",
        "script": "Gujarati"
    },
    "bn": {
        "name": "Bengali",
        "asr_model": "ai4bharat/indic-conformer-600m-multilingual",
        "flores_code": "ben_Beng",
        "script": "Bengali"
    },
    "or": {
        "name": "Odia",
        "asr_model": "ai4bharat/indic-conformer-600m-multilingual",
        "flores_code": "ory_Orya",
        "script": "Odia"
    },
    "pa": {
        "name": "Punjabi",
        "asr_model": "ai4bharat/indic-conformer-600m-multilingual",
        "flores_code": "pan_Guru",
        "script": "Gurmukhi"
    }
}

# Audio processing settings
AUDIO_CONFIG = {
    "target_sample_rate": 16000,
    "mono": True,
    "normalize": True,
}

# Output settings
OUTPUT_CONFIG = {
    "save_intermediate": True,  # Save ASR output
    "output_format": "json",  # json, txt, or both
    "verbose": True,
}
