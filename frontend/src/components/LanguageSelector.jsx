import { Globe } from 'lucide-react'
import './LanguageSelector.css'

function LanguageSelector({ languages, selectedLanguage, onLanguageChange }) {
    return (
        <div className="language-selector">
            <div className="selector-header">
                <Globe size={20} />
                <h3>Select Language</h3>
            </div>

            <div className="language-grid">
                {languages.map((lang) => (
                    <button
                        key={lang.code}
                        className={`language-btn ${selectedLanguage === lang.code ? 'active' : ''}`}
                        onClick={() => onLanguageChange(lang.code)}
                    >
                        <div className="lang-name">{lang.name}</div>
                        <div className="lang-script">{lang.script}</div>
                    </button>
                ))}
            </div>

            {languages.length === 0 && (
                <div className="loading-languages">
                    <p>Loading languages...</p>
                </div>
            )}
        </div>
    )
}

export default LanguageSelector
