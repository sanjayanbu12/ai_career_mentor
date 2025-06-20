import React, { useState } from 'react';
import axios from 'axios';

const FileUpload = ({ onAnalysisStart, onAnalysisComplete, onAnalysisError }) => {
    const [files, setFiles] = useState({
        resume: null,
        coding_results: null,
        interview_feedback: null,
        performance_data: null,
    });

    const handleFileChange = (e) => {
        setFiles({
            ...files,
            [e.target.name]: e.target.files[0],
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        onAnalysisStart();

        const formData = new FormData();
        for (const key in files) {
            if (files[key]) {
                formData.append(key, files[key]);
            } else {
                onAnalysisError(new Error(`Please upload all required files. Missing: ${key}`));
                return;
            }
        }

        try {
            const response = await axios.post(`${process.env.REACT_APP_API_URL}/analyze`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            onAnalysisComplete(response.data);
        } catch (error) {
            onAnalysisError(error);
        }
    };

    return (
        <div className="file-upload-container">
            <h2>Upload Your Career Documents</h2>
            <p>Provide your resume, past rejection feedback, and performance data to get started.</p>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label>Resume (PDF/DOCX/TXT)</label>
                    <input type="file" name="resume" onChange={handleFileChange} required />
                </div>
                <div className="form-group">
                    <label>Coding Test Results (CSV/TXT)</label>
                    <input type="file" name="coding_results" onChange={handleFileChange} required />
                </div>
                <div className="form-group">
                    <label>Interview Feedback (TXT)</label>
                    <input type="file" name="interview_feedback" onChange={handleFileChange} required />
                </div>
                <div className="form-group">
                    <label>Performance Data (e.g., Hackathon Ranks) (CSV/TXT)</label>
                    <input type="file" name="performance_data" onChange={handleFileChange} required />
                </div>
                <button type="submit">Analyze My Profile</button>
            </form>
        </div>
    );
};

export default FileUpload;