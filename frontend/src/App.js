import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import ResultsDashboard from './components/ResultsDashboard';
import './App.css';

function App() {
    const [analysisResult, setAnalysisResult] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleAnalysisStart = () => {
        setIsLoading(true);
        setError(null);
        setAnalysisResult(null);
    };

    const handleAnalysisComplete = (result) => {
        setAnalysisResult(result);
        setIsLoading(false);
    };
    
    const handleAnalysisError = (err) => {
        const errorMessage = err.response?.data?.detail || err.message || 'An unknown error occurred.';
        setError(errorMessage);
        setIsLoading(false);
    };

    return (
        <div className="App">
            <header className="App-header">
                <h1>AI Career Redirection Mentor</h1>
            </header>
            <main>
                <FileUpload
                    onAnalysisStart={handleAnalysisStart}
                    onAnalysisComplete={handleAnalysisComplete}
                    onAnalysisError={handleAnalysisError}
                />
                {isLoading && <div className="loader">Analyzing Your Profile... This may take a moment.</div>}
                {error && <div className="error">Error: {error}</div>}
                {analysisResult && <ResultsDashboard data={analysisResult} />}
            </main>
        </div>
    );
}

export default App;