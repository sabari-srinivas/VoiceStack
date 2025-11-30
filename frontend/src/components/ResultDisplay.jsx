import { CheckCircle, Copy, Download, Clock } from 'lucide-react'
import { useState } from 'react'
import './ResultDisplay.css'

function ResultDisplay({ result }) {
    const [copied, setCopied] = useState(false)

    const handleCopy = (text) => {
        navigator.clipboard.writeText(text)
        setCopied(true)
        setTimeout(() => setCopied(false), 2000)
    }

    const handleDownload = () => {
        const content = `
Speech Processing Result
================================

Language: ${result.language.name} (${result.language.script})
Filename: ${result.filename}
Timestamp: ${new Date(result.timestamp).toLocaleString()}

Transcription (${result.language.script}):
${result.transcription}

${result.language.code !== 'en' && result.translation ? `English Translation:
${result.translation}

` : ''}${result.refined_prompt ? `Refined Prompt:
${result.refined_prompt}

` : ''}Processing Time:
- ASR: ${result.processing_time.asr}s
- NMT: ${result.processing_time.nmt}s
- Total: ${result.processing_time.total}s
    `.trim()

        const blob = new Blob([content], { type: 'text/plain' })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `transcription_${Date.now()}.txt`
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
        URL.revokeObjectURL(url)
    }

    return (
        <div className="result-display fade-in">
            {/* Success Header */}
            <div className="result-header">
                <CheckCircle size={32} className="success-icon" />
                <div>
                    <h2>Processing Complete!</h2>
                    <p>Your audio has been successfully processed</p>
                </div>
            </div>

            {/* Language Info */}
            <div className="language-info">
                <div className="info-item">
                    <span className="info-label">Language:</span>
                    <span className="info-value">{result.language.name}</span>
                </div>
                <div className="info-item">
                    <span className="info-label">Script:</span>
                    <span className="info-value">{result.language.script}</span>
                </div>
                <div className="info-item">
                    <Clock size={16} />
                    <span className="info-value">{result.processing_time.total}s</span>
                </div>
            </div>

            {/* Two Column Layout */}
            <div className="results-grid">
                {/* Left Column: Transcription & Translation (if not English) */}
                <div className="left-column">
                    {/* Transcription */}
                    <div className="result-section">
                        <div className="section-header">
                            <h3>{result.language.code === 'en' ? 'Transcription' : 'Original Transcription'}</h3>
                            <span className="script-badge">{result.language.script}</span>
                        </div>
                        <div className="text-content transcription">
                            {result.transcription}
                        </div>
                        <button
                            className="copy-btn"
                            onClick={() => handleCopy(result.transcription)}
                        >
                            <Copy size={16} />
                            <span>{copied ? 'Copied!' : 'Copy'}</span>
                        </button>
                    </div>

                    {/* Translation - Only show for non-English languages */}
                    {result.language.code !== 'en' && result.translation && (
                        <div className="result-section highlight">
                            <div className="section-header">
                                <h3>English Translation</h3>
                                <span className="script-badge">English</span>
                            </div>
                            <div className="text-content translation">
                                {result.translation}
                            </div>
                            <button
                                className="copy-btn"
                                onClick={() => handleCopy(result.translation)}
                            >
                                <Copy size={16} />
                                <span>{copied ? 'Copied!' : 'Copy'}</span>
                            </button>
                        </div>
                    )}

                    {/* Processing Stats */}
                    <div className="stats-grid">
                        <div className="stat-card">
                            <div className="stat-label">ASR Time</div>
                            <div className="stat-value">{result.processing_time.asr}s</div>
                        </div>
                        <div className="stat-card">
                            <div className="stat-label">NMT Time</div>
                            <div className="stat-value">{result.processing_time.nmt}s</div>
                        </div>
                        <div className="stat-card">
                            <div className="stat-label">Total Time</div>
                            <div className="stat-value">{result.processing_time.total}s</div>
                        </div>
                    </div>
                </div>

                {/* Right Column: Refined Prompt */}
                {result.refined_prompt && (
                    <div className="right-column">
                        <div className="result-section refined-prompt">
                            <div className="section-header">
                                <h3>✨ Refined Prompt</h3>
                                <span className="script-badge gemini-badge">Gemini 2.0</span>
                            </div>
                            <div className="text-content refined-text">
                                {result.refined_prompt}
                            </div>
                            <button
                                className="copy-btn"
                                onClick={() => handleCopy(result.refined_prompt)}
                            >
                                <Copy size={16} />
                                <span>{copied ? 'Copied!' : 'Copy'}</span>
                            </button>
                        </div>
                    </div>
                )}
            </div>

            {/* Download Button */}
            <button className="download-btn" onClick={handleDownload}>
                <Download size={20} />
                <span>Download Results</span>
            </button>
        </div>
    )
}

export default ResultDisplay
