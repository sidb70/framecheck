// pages/index.js
import { useState } from 'react';
import axios from 'axios';

export default function Home() {
  const [videoUrl, setVideoUrl] = useState('');
  const [results, setResults] = useState([]);

  const extractVideoId = (url) => {
    const urlParams = new URLSearchParams(new URL(url).search);
    return urlParams.get('v');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Extract video ID from the YouTube URL
    const videoId = extractVideoId(videoUrl);
    console.log('videoId:', videoId)

    if (!videoId) {
      console.error('Invalid YouTube URL');
      return;
    }

    try {
      // Make GET request with the extracted video ID
      const response = await axios.get(`http://127.0.0.1:8000/video/${videoId}`);
      setResults(response.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <div>
      <h1>Video App</h1>
      <form onSubmit={handleSubmit}>
        <label>
          YouTube Video URL:
          <input
            type="text"
            value={videoUrl}
            onChange={(e) => setVideoUrl(e.target.value)}
          />
        </label>
        <button type="submit">Submit</button>
      </form>
      {results.length > 0 && (
        <div>
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
