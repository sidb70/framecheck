// pages/index.js
import { useState } from 'react';
import axios from 'axios';

export default function Home() {
  const [videoUrl, setVideoUrl] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const extractVideoId = (url) => {
    try {
      const urlParams = new URLSearchParams(new URL(url).search);
      return urlParams.get('v');
    } catch (error) {
      console.error('Error extracting video ID:', error);
      setError('Invalid YouTube URL');
      return null;
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Extract video ID from the YouTube URL
    const videoId = extractVideoId(videoUrl);
    console.log('videoId:', videoId);

    if (!videoId) {
      // Show error message to the user
      return;
    }

    try {
      // Set loading to true before making the request
      setLoading(true);
      setError('');

      // Make GET request with the extracted video ID
      const response = await axios.get(`http://www.framecheck.tech/api/video/${videoId}`);

      // Set loading to false after receiving the response
      setLoading(false);
      setResults(response.data);
    } catch (error) {
      console.error('Error fetching data:', error);

      // Set loading to false and display an error message
      setLoading(false);
      setError('Error fetching data. Please try again.');
    }
  };

  // Reset results when the input changes
  const handleInputChange = (e) => {
    setVideoUrl(e.target.value);
    setResults([]); // Clear previous results
    setError(''); // Clear the error when the user makes changes
  };

  return (
    <div className="container">
      <h1>YouTube Fact Check</h1>
      <form onSubmit={handleSubmit}>
        <label>
          YouTube Video URL:
          <input
            type="text"
            value={videoUrl}
            onChange={handleInputChange}
          />
        </label>
        {error && <p className="error-message">{error}</p>}
        <button type="submit">Submit</button>
      </form>
      {loading && (
        <div className="loading">
          <p>Analyzing video (this can take some time)</p>
          <div className="spinner">
            <div className="dot1"></div>
            <div className="dot2"></div>
            <div className="dot3"></div>
          </div>
        </div>
      )}
      {results.length > 0 && (
        <div className="results">
          <h2>Results:</h2>
          <ul>
            {results.map((result, index) => (
              <li key={index}>
                <strong>Claim:</strong> {result.claim}<br />
                <strong>Truth Value:</strong> {result.truth_value}<br />
                <strong>Explanation:</strong> {result.explanation}
                <hr />
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
