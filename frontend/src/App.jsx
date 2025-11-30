import { useState, useEffect } from 'react'
import { Mic, Languages, Loader2, CheckCircle, XCircle, Info } from 'lucide-react'
import AudioRecorder from './components/AudioRecorder'

import LanguageSelector from './components/LanguageSelector'
import ResultDisplay from './components/ResultDisplay'
import { translateAudio, getLanguages } from './api'
import './App.css'

function App() {

    const [selectedLanguage, setSelectedLanguage] = useState('hi')
    const [languages, setLanguages] = useState([])
    const [isProcessing, setIsProcessing] = useState(false)
    const [result, setResult] = useState(null)
    const [error, setError] = useState(null)

    // Load languages on mount
    useEffect(() => {
        loadLanguages()
    }, [])

    const loadLanguages = async () => {
        try {
            const data = await getLanguages()
            setLanguages(data.languages)
        } catch (err) {
            console.error('Failed to load languages:', err)
            setError('Failed to load languages. Please refresh the page.')
        }
    }

    const handleAudioSubmit = async (audioBlob, filename = 'recording.wav') => {
        setIsProcessing(true)
        setError(null)
        setResult(null)

        try {
            const data = await translateAudio(audioBlob, selectedLanguage, filename)
            setResult(data)
        } catch (err) {
            console.error('Translation error:', err)
            setError(err.message || 'Failed to process audio. Please try again.')
        } finally {
            setIsProcessing(false)
        }
    }

    return (
        <div className="app">
            {/* Header */}
            <header className="header">
                <div className="header-content">
                    <div className="logo-section">
                        <div className="logo-icon">
                            <Languages size={32} />
                        </div>
                        <div>
                            <h1 className="title">Indic Speech Translator</h1>
                            <p className="subtitle">Convert Indic speech to English instantly</p>
                        </div>
                    </div>

                    <div className="info-badge">
                        <Info size={16} />
                        <span>10 Languages Supported</span>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="main-content">
                <div className="container">

                    {/* Language Selector */}
                    <div className="section fade-in">
                        <LanguageSelector
                            languages={languages}
                            selectedLanguage={selectedLanguage}
                            onLanguageChange={setSelectedLanguage}
                        />
                    </div>



                    {/* Audio Input */}
                    <div className="section fade-in">
                        <AudioRecorder
                            onAudioReady={handleAudioSubmit}
                            disabled={isProcessing}
                        />
                    </div>

                    {/* Processing Indicator */}
                    {isProcessing && (
                        <div className="section fade-in">
                            <div className="processing-card">
                                <Loader2 className="spin" size={32} />
                                <h3>Processing Audio...</h3>
                                <p>This may take a few moments. Please wait.</p>
                                <div className="progress-bar">
                                    <div className="progress-fill"></div>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Error Display */}
                    {error && (
                        <div className="section fade-in">
                            <div className="error-card">
                                <XCircle size={24} />
                                <h3>Error</h3>
                                <p>{error}</p>
                            </div>
                        </div>
                    )}

                    {/* Result Display */}
                    {result && !isProcessing && (
                        <div className="section fade-in">
                            <ResultDisplay result={result} />
                        </div>
                    )}


                </div>
            </main>

            {/* Footer */}
            <footer className="footer">
                <p>Powered by AI4Bharat • IndicConformer + NLLB</p>
            </footer>
        </div>
    )
}

export default App
