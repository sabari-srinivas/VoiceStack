import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

// Create axios instance with extended timeout for model loading
const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 600000, // 10 minutes timeout for initial model loading
    headers: {
        'Content-Type': 'multipart/form-data',
    },
})

/**
 * Get list of supported languages
 */
export const getLanguages = async () => {
    try {
        const response = await api.get('/languages')
        return response.data
    } catch (error) {
        console.error('Error fetching languages:', error)
        throw new Error('Failed to fetch languages')
    }
}

/**
 * Translate audio to English
 * @param {Blob} audioBlob - Audio file as Blob
 * @param {string} language - Language code
 * @param {string} filename - Original filename
 */
export const translateAudio = async (audioBlob, language, filename = 'audio.wav') => {
    try {
        const formData = new FormData()
        formData.append('audio', audioBlob, filename)
        formData.append('language', language)

        const response = await api.post('/translate', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        })

        return response.data
    } catch (error) {
        console.error('Error translating audio:', error)

        if (error.response) {
            // Server responded with error
            throw new Error(error.response.data.detail || 'Translation failed')
        } else if (error.request) {
            // Request made but no response
            throw new Error('Server not responding. Please ensure the backend is running.')
        } else {
            // Other errors
            throw new Error('Failed to send request')
        }
    }
}

/**
 * Check server health
 */
export const checkHealth = async () => {
    try {
        const response = await api.get('/health')
        return response.data
    } catch (error) {
        console.error('Health check failed:', error)
        return { status: 'unhealthy' }
    }
}

export default api
