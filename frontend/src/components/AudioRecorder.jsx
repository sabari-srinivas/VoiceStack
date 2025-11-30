import { useState, useRef } from 'react'
import { Mic, Square, Play, Trash2 } from 'lucide-react'
import './AudioRecorder.css'

function AudioRecorder({ onAudioReady, disabled }) {
    const [isRecording, setIsRecording] = useState(false)
    const [audioURL, setAudioURL] = useState(null)
    const [audioBlob, setAudioBlob] = useState(null)
    const [recordingTime, setRecordingTime] = useState(0)

    const mediaRecorderRef = useRef(null)
    const chunksRef = useRef([])
    const timerRef = useRef(null)

    const convertToWav = async (audioBlob) => {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)()
        const arrayBuffer = await audioBlob.arrayBuffer()
        const audioBuffer = await audioContext.decodeAudioData(arrayBuffer)

        // Convert to WAV
        const wavBuffer = audioBufferToWav(audioBuffer)
        return new Blob([wavBuffer], { type: 'audio/wav' })
    }

    const audioBufferToWav = (audioBuffer) => {
        const numChannels = 1 // Mono
        const sampleRate = audioBuffer.sampleRate
        const format = 1 // PCM
        const bitDepth = 16

        const channelData = audioBuffer.getChannelData(0)
        const samples = new Int16Array(channelData.length)

        // Convert float32 to int16
        for (let i = 0; i < channelData.length; i++) {
            const s = Math.max(-1, Math.min(1, channelData[i]))
            samples[i] = s < 0 ? s * 0x8000 : s * 0x7FFF
        }

        const buffer = new ArrayBuffer(44 + samples.length * 2)
        const view = new DataView(buffer)

        // WAV header
        const writeString = (offset, string) => {
            for (let i = 0; i < string.length; i++) {
                view.setUint8(offset + i, string.charCodeAt(i))
            }
        }

        writeString(0, 'RIFF')
        view.setUint32(4, 36 + samples.length * 2, true)
        writeString(8, 'WAVE')
        writeString(12, 'fmt ')
        view.setUint32(16, 16, true)
        view.setUint16(20, format, true)
        view.setUint16(22, numChannels, true)
        view.setUint32(24, sampleRate, true)
        view.setUint32(28, sampleRate * numChannels * bitDepth / 8, true)
        view.setUint16(32, numChannels * bitDepth / 8, true)
        view.setUint16(34, bitDepth, true)
        writeString(36, 'data')
        view.setUint32(40, samples.length * 2, true)

        // Write samples
        const offset = 44
        for (let i = 0; i < samples.length; i++) {
            view.setInt16(offset + i * 2, samples[i], true)
        }

        return buffer
    }

    const startRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true })

            const mediaRecorder = new MediaRecorder(stream)
            mediaRecorderRef.current = mediaRecorder
            chunksRef.current = []

            mediaRecorder.ondataavailable = (e) => {
                if (e.data.size > 0) {
                    chunksRef.current.push(e.data)
                }
            }

            mediaRecorder.onstop = async () => {
                const webmBlob = new Blob(chunksRef.current, { type: 'audio/webm' })

                // Convert to WAV
                const wavBlob = await convertToWav(webmBlob)
                const url = URL.createObjectURL(wavBlob)
                setAudioURL(url)
                setAudioBlob(wavBlob)

                // Stop all tracks
                stream.getTracks().forEach(track => track.stop())
            }

            mediaRecorder.start()
            setIsRecording(true)
            setRecordingTime(0)

            // Start timer
            timerRef.current = setInterval(() => {
                setRecordingTime(prev => prev + 1)
            }, 1000)

        } catch (error) {
            console.error('Error accessing microphone:', error)
            alert('Could not access microphone. Please grant permission.')
        }
    }

    const stopRecording = () => {
        if (mediaRecorderRef.current && isRecording) {
            mediaRecorderRef.current.stop()
            setIsRecording(false)

            if (timerRef.current) {
                clearInterval(timerRef.current)
            }
        }
    }

    const clearRecording = () => {
        setAudioURL(null)
        setAudioBlob(null)
        setRecordingTime(0)
    }

    const handleSubmit = () => {
        if (audioBlob) {
            onAudioReady(audioBlob, `recording_${Date.now()}.wav`)
            clearRecording()
        }
    }

    const formatTime = (seconds) => {
        const mins = Math.floor(seconds / 60)
        const secs = seconds % 60
        return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
    }

    return (
        <div className="audio-recorder">
            <div className="recorder-card">

                {/* Recording Indicator */}
                {isRecording && (
                    <div className="recording-indicator">
                        <div className="pulse-dot"></div>
                        <span>Recording... {formatTime(recordingTime)}</span>
                    </div>
                )}

                {/* Controls */}
                <div className="recorder-controls">
                    {!isRecording && !audioURL && (
                        <button
                            className="record-btn"
                            onClick={startRecording}
                            disabled={disabled}
                        >
                            <Mic size={32} />
                            <span>Start Recording</span>
                        </button>
                    )}

                    {isRecording && (
                        <button
                            className="stop-btn"
                            onClick={stopRecording}
                        >
                            <Square size={32} />
                            <span>Stop Recording</span>
                        </button>
                    )}

                    {audioURL && !isRecording && (
                        <div className="playback-controls">
                            <audio src={audioURL} controls className="audio-player" />

                            <div className="action-buttons">
                                <button
                                    className="btn-secondary"
                                    onClick={clearRecording}
                                    disabled={disabled}
                                >
                                    <Trash2 size={20} />
                                    <span>Clear</span>
                                </button>

                                <button
                                    className="btn-primary"
                                    onClick={handleSubmit}
                                    disabled={disabled}
                                >
                                    <Play size={20} />
                                    <span>Translate</span>
                                </button>
                            </div>
                        </div>
                    )}
                </div>

                {/* Instructions */}
                {!isRecording && !audioURL && (
                    <p className="recorder-hint">
                        Click the microphone to start recording your voice
                    </p>
                )}
            </div>
        </div>
    )
}

export default AudioRecorder
