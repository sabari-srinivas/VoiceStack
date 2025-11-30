import { useState, useRef } from 'react'
import { Upload, File, X } from 'lucide-react'
import './FileUpload.css'

function FileUpload({ onFileSelect, disabled }) {
    const [selectedFile, setSelectedFile] = useState(null)
    const [isDragging, setIsDragging] = useState(false)
    const fileInputRef = useRef(null)

    const handleFileChange = (e) => {
        const file = e.target.files[0]
        if (file) {
            validateAndSetFile(file)
        }
    }

    const validateAndSetFile = (file) => {
        // Check file type
        const validTypes = ['audio/wav', 'audio/mpeg', 'audio/mp3', 'audio/flac', 'audio/ogg', 'audio/webm']
        const fileExtension = file.name.split('.').pop().toLowerCase()
        const validExtensions = ['wav', 'mp3', 'flac', 'ogg', 'webm', 'm4a']

        if (!validTypes.includes(file.type) && !validExtensions.includes(fileExtension)) {
            alert('Please select a valid audio file (WAV, MP3, FLAC, OGG, WebM)')
            return
        }

        // Check file size (max 50MB)
        if (file.size > 50 * 1024 * 1024) {
            alert('File size must be less than 50MB')
            return
        }

        setSelectedFile(file)
    }

    const handleDragOver = (e) => {
        e.preventDefault()
        setIsDragging(true)
    }

    const handleDragLeave = (e) => {
        e.preventDefault()
        setIsDragging(false)
    }

    const handleDrop = (e) => {
        e.preventDefault()
        setIsDragging(false)

        const file = e.dataTransfer.files[0]
        if (file) {
            validateAndSetFile(file)
        }
    }

    const handleRemoveFile = () => {
        setSelectedFile(null)
        if (fileInputRef.current) {
            fileInputRef.current.value = ''
        }
    }

    const handleSubmit = () => {
        if (selectedFile) {
            onFileSelect(selectedFile, selectedFile.name)
            handleRemoveFile()
        }
    }

    const formatFileSize = (bytes) => {
        if (bytes === 0) return '0 Bytes'
        const k = 1024
        const sizes = ['Bytes', 'KB', 'MB', 'GB']
        const i = Math.floor(Math.log(bytes) / Math.log(k))
        return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
    }

    return (
        <div className="file-upload">
            <div
                className={`upload-area ${isDragging ? 'dragging' : ''} ${selectedFile ? 'has-file' : ''}`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                onClick={() => !selectedFile && fileInputRef.current?.click()}
            >
                <input
                    ref={fileInputRef}
                    type="file"
                    accept="audio/*,.wav,.mp3,.flac,.ogg,.webm,.m4a"
                    onChange={handleFileChange}
                    style={{ display: 'none' }}
                    disabled={disabled}
                />

                {!selectedFile ? (
                    <>
                        <Upload size={48} className="upload-icon" />
                        <h3>Drop your audio file here</h3>
                        <p>or click to browse</p>
                        <div className="supported-formats">
                            <span>Supported: WAV, MP3, FLAC, OGG, WebM</span>
                            <span>Max size: 50MB</span>
                        </div>
                    </>
                ) : (
                    <div className="file-preview">
                        <div className="file-info">
                            <File size={32} className="file-icon" />
                            <div className="file-details">
                                <h4>{selectedFile.name}</h4>
                                <p>{formatFileSize(selectedFile.size)}</p>
                            </div>
                            <button
                                className="remove-btn"
                                onClick={(e) => {
                                    e.stopPropagation()
                                    handleRemoveFile()
                                }}
                                disabled={disabled}
                            >
                                <X size={20} />
                            </button>
                        </div>

                        <button
                            className="submit-btn"
                            onClick={(e) => {
                                e.stopPropagation()
                                handleSubmit()
                            }}
                            disabled={disabled}
                        >
                            Translate Audio
                        </button>
                    </div>
                )}
            </div>
        </div>
    )
}

export default FileUpload
