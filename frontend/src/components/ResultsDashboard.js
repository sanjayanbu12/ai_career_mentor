import React from 'react';

const UpskillingPlan = ({ planData }) => {
    let plan;
    try {
        plan = typeof planData === 'string' ? JSON.parse(planData) : planData;
    } catch (e) {
        console.error("Failed to parse upskilling plan:", e);
        return <p>Upskilling plan could not be displayed due to a formatting error.</p>;
    }

    if (!plan || typeof plan !== 'object' || Object.keys(plan).length === 0) {
        return <p>An upskilling plan could not be generated.</p>;
    }

    return (
        <div className="upskilling-plan-structured">
            {Object.entries(plan).map(([careerTitle, careerPlan]) => (
                <div key={careerTitle}>
                    <h4>{careerTitle}</h4>
                    {careerPlan.milestones?.map((milestone, index) => (
                        <div key={index} className="milestone-card" style={{paddingBottom: '1rem', borderBottom: '1px solid #eee', marginBottom: '1rem'}}>
                            <p><strong>Milestone:</strong> {milestone.milestone}</p>
                            <p><em>{milestone.description}</em></p>
                            <strong>Suggested Resources:</strong>
                            <ul>
                                {milestone.resources?.map((resource, r_index) => (
                                    <li key={r_index}>
                                        {/* This handles both string and object resources */}
                                        {typeof resource === 'string' ? resource : (
                                            <a href={resource.link} target="_blank" rel="noopener noreferrer">
                                                {resource.name}
                                            </a>
                                        )}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    ))}
                </div>
            ))}
        </div>
    );
};


const ResultsDashboard = ({ data }) => {
    if (!data) return null;

    return (
        <div className="results-dashboard">
            <div className="dashboard-grid">
                <div className="grid-column">
                    <h2>Diagnosis</h2>
                    <div className="result-section">
                        <h3><span role="img" aria-label="chart">📉</span>Rejection Patterns</h3>
                        {data.rejection_patterns?.rejection_patterns?.length > 0 ? (
                            <ul>
                                {data.rejection_patterns.rejection_patterns.map((pattern, index) => (
                                    <li key={index}><strong>{pattern.pattern}:</strong> <em>{pattern.actionable_insight}</em></li>
                                ))}
                            </ul>
                        ) : (
                            <p>No specific rejection patterns were identified.</p>
                        )}
                    </div>
                    <div className="result-section">
                        <h3><span role="img" aria-label="star">⭐</span>Identified Strengths</h3>
                        {data.strengths?.strengths?.length > 0 ? (
                            <ul>
                                {data.strengths.strengths.map((strength, index) => (
                                    <li key={index}><strong>{strength.strength}:</strong> {strength.evidence}</li>
                                ))}
                            </ul>
                        ) : (
                            <p>Could not identify specific strengths from the documents provided.</p>
                        )}
                    </div>
                </div>

                <div className="grid-column">
                    <h2>Action Plan</h2>
                    <div className="result-section">
                        <h3><span role="img" aria-label="compass">🧭</span>Recommended Career Alternatives</h3>
                        {data.career_alternatives?.career_alternatives?.length > 0 ? (
                            data.career_alternatives.career_alternatives.map((career, index) => (
                                <div key={index} className="career-card">
                                    <h4>{career.title}</h4>
                                    <p>{career.description}</p>
                                </div>
                            ))
                        ) : (
                            <p>No suitable career alternatives were generated.</p>
                        )}
                    </div>
                     <div className="result-section">
                        <h3><span role="img" aria-label="users">👥</span>Potential Support Network</h3>
                        {data.support_matches?.support_matches?.length > 0 ? (
                            data.support_matches.support_matches.map((match, index) => (
                                 <div key={index} className="support-card">
                                    <h4>{match.name} ({match.type})</h4>
                                    <p><strong>Focus:</strong> {Array.isArray(match.focus) ? match.focus.join(', ') : match.focus || 'N/A'}</p>
                                    {/* --- THIS IS THE FINAL CHANGE --- */}
                                    <p><strong>Contact:</strong> <a href={`//${match.contact}`} target="_blank" rel="noopener noreferrer">{match.contact}</a></p>
                                </div>
                            ))
                        ) : (
                            <p>No relevant support network matches were found.</p>
                        )}
                    </div>
                    <div className="result-section upskilling-plan">
                        <h3><span role="img" aria-label="rocket">🚀</span>Suggested Upskilling Plan</h3>
                        <UpskillingPlan planData={data.upskilling_plan?.upskilling_plan} />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ResultsDashboard;