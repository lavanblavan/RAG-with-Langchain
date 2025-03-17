import React, { useState } from 'react';

const QuestionAnswering = () => {
    const [question, setQuestion] = useState(''); // State to store the question
    const [answer, setAnswer] = useState(''); // State to store the answer
    const [isLoading, setIsLoading] = useState(false); // State to handle loading
    const [error, setError] = useState(null); // State to handle errors

    const handleAsk = async () => {
        if (!question) {
            alert("Please enter a question.");
            return;
        }

        setIsLoading(true); // Set loading to true
        setError(null); // Clear any previous errors
        setAnswer(''); // Clear previous answer

        try {
            // Send a POST request to the backend
            const response = await fetch("http://127.0.0.1:8000/ask", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ question }), // Send the question in the request body
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json(); // Parse the JSON response
            setAnswer(`Answer: ${data.answer}`); // Set the answer state
        } catch (error) {
            setError(error.message); // Set the error state
            console.error("Error fetching answer:", error);
        } finally {
            setIsLoading(false); // Set loading to false
        }
    };

    return (
        <div style={{ margin: '20px', fontFamily: 'Arial, sans-serif' }}>
            <h1 style={{ color: '#333' }}>Ask a Question</h1>
            <input
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)} // Update the question state
                placeholder="Enter your question"
                style={{ width: '300px', padding: '10px', fontSize: '16px' }}
            />
            <button
                onClick={handleAsk}
                disabled={isLoading} // Disable the button while loading
                style={{
                    padding: '10px 20px',
                    fontSize: '16px',
                    cursor: 'pointer',
                    backgroundColor: isLoading ? '#ccc' : '#007bff',
                    color: '#fff',
                    border: 'none',
                    borderRadius: '5px',
                    marginLeft: '10px',
                }}
            >
                {isLoading ? "Asking..." : "Ask"} {/* Change button text based on loading state */}
            </button>
            {error && (
                <div style={{ color: 'red', marginTop: '10px' }}>
                    Error: {error} {/* Display error message */}
                </div>
            )}
            <div id="answer" style={{ marginTop: '20px', fontSize: '18px', color: '#555' }}>
                {answer} {/* Display the answer */}
            </div>
        </div>
    );
};

export default QuestionAnswering;