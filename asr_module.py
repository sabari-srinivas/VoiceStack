"""
Automatic Speech Recognition (ASR) Module
Converts Indic language audio to native script text using AI4Bharat IndicConformer
"""

import torch
import torchaudio
import librosa
import soundfile as sf
import numpy as np
from transformers import AutoModel
from typing import Optional, Union, Tuple
import warnings
warnings.filterwarnings('ignore')


class IndicASR:
    """
    Automatic Speech Recognition for Indic languages using IndicConformer models
    """
    
    def __init__(
        self,
        model_name: str,
        device: Optional[str] = None,
        sampling_rate: int = 16000
    ):
        """
        Initialize the ASR model
        
        Args:
            model_name: HuggingFace model identifier
            device: Device to run inference on ('cuda', 'cpu', or None for auto)
            sampling_rate: Target sampling rate for audio
        """
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.sampling_rate = sampling_rate
        self.model_name = model_name
        
        print(f"Loading ASR model: {model_name}")
        print(f"Using device: {self.device}")
        
        try:
            # Load IndicConformer model
            self.model = AutoModel.from_pretrained(
                model_name,
                trust_remote_code=True
            )
            self.model.to(self.device)
            self.model.eval()
            
            print("ASR model loaded successfully!")
            
        except Exception as e:
            raise RuntimeError(f"Failed to load ASR model: {str(e)}")
    
    def load_audio(
        self,
        audio_path: str,
        target_sr: Optional[int] = None
    ) -> Tuple[np.ndarray, int]:
        """
        Load and preprocess audio file
        
        Args:
            audio_path: Path to audio file
            target_sr: Target sampling rate (uses model's default if None)
            
        Returns:
            Tuple of (audio_array, sampling_rate)
        """
        target_sr = target_sr or self.sampling_rate
        
        try:
            # Load audio using librosa for better compatibility
            audio, sr = librosa.load(audio_path, sr=target_sr, mono=True)
            
            # Trim silence from beginning and end
            audio, _ = librosa.effects.trim(audio, top_db=20)
            
            # Normalize audio with better method
            audio = librosa.util.normalize(audio)
            
            # Apply pre-emphasis filter to boost high frequencies (improves speech recognition)
            audio = np.append(audio[0], audio[1:] - 0.97 * audio[:-1])
            
            print(f"📂 Loaded audio: {audio_path}")
            print(f"   Duration: {len(audio) / sr:.2f}s, Sample rate: {sr}Hz")
            
            return audio, sr
            
        except Exception as e:
            print(f"Librosa load failed: {str(e)}")
            try:
                # Fallback to soundfile directly
                print("Attempting fallback to soundfile...")
                audio, sr = sf.read(audio_path)
                # Convert to float32 and mono if needed
                if len(audio.shape) > 1:
                    audio = np.mean(audio, axis=1)
                audio = audio.astype(np.float32)
                
                # Resample if needed
                if sr != target_sr:
                    audio = librosa.resample(audio, orig_sr=sr, target_sr=target_sr)
                    sr = target_sr
                    
                print(f"Fallback successful. Loaded audio: {audio_path}")
                return audio, sr
            except Exception as e2:
                import traceback
                traceback.print_exc()
                raise RuntimeError(f"Failed to load audio file: {repr(e)} | Fallback error: {repr(e2)}")
    
    def transcribe(
        self,
        audio_input: Union[str, np.ndarray],
        sampling_rate: Optional[int] = None,
        language_code: str = "hi",
        decoding_type: str = "ctc"
    ) -> str:
        """
        Transcribe audio to Indic text using IndicConformer
        
        Args:
            audio_input: Path to audio file or numpy array
            sampling_rate: Sampling rate if audio_input is array
            language_code: Language code (e.g., 'hi', 'ta', 'te')
            decoding_type: Decoding method ('ctc' or 'rnnt')
            
        Returns:
            Transcribed text in native Indic script
        """
        # Load audio if path is provided
        if isinstance(audio_input, str):
            audio, sr = self.load_audio(audio_input)
        else:
            audio = audio_input
            sr = sampling_rate or self.sampling_rate
        
        # Ensure correct sampling rate
        if sr != self.sampling_rate:
            audio = librosa.resample(
                audio,
                orig_sr=sr,
                target_sr=self.sampling_rate
            )
            sr = self.sampling_rate
        
        print(f"Transcribing audio with language: {language_code}...")
        
        try:
            # Convert to torch tensor and add batch dimension
            wav_tensor = torch.from_numpy(audio).float()
            
            # Ensure mono audio
            if len(wav_tensor.shape) > 1:
                wav_tensor = torch.mean(wav_tensor, dim=0, keepdim=True)
            else:
                wav_tensor = wav_tensor.unsqueeze(0)
            
            # Move to device
            wav_tensor = wav_tensor.to(self.device)
            
            # Perform ASR using IndicConformer's custom method
            with torch.no_grad():
                transcription = self.model(wav_tensor, language_code, decoding_type)
            
            print(f"Transcription complete!")
            print(f"   Text length: {len(transcription)} characters")
            
            return transcription
            
        except Exception as e:
            raise RuntimeError(f"Transcription failed: {str(e)}")
    
    def transcribe_batch(
        self,
        audio_paths: list,
        chunk_length_s: int = 30
    ) -> list:
        """
        Transcribe multiple audio files
        
        Args:
            audio_paths: List of paths to audio files
            chunk_length_s: Length of chunks for processing
            
        Returns:
            List of transcriptions
        """
        transcriptions = []
        
        for i, path in enumerate(audio_paths, 1):
            print(f"\n📝 Processing file {i}/{len(audio_paths)}: {path}")
            transcription = self.transcribe(path, chunk_length_s=chunk_length_s)
            transcriptions.append(transcription)
        
        return transcriptions
    
    def __repr__(self):
        return f"IndicASR(model={self.model_name}, device={self.device})"
