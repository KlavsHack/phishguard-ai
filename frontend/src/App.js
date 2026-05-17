import './App.css';
import { useState } from 'react';

function App() {

  const [url, setUrl] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const [recentUrls, setRecentUrls] = useState(
    JSON.parse(localStorage.getItem("recentUrls")) || []
  );

  const checkPhishing = async () => {

    if (!url) return;

    setLoading(true);

    try {

      const response = await fetch('http://127.0.0.1:8000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });

      const data = await response.json();

      let updatedUrls = [
        url,
        ...recentUrls.filter(item => item !== url)
      ];

      if (updatedUrls.length > 5) {
        updatedUrls = updatedUrls.slice(0, 5);
      }

      setRecentUrls(updatedUrls);

      localStorage.setItem(
        "recentUrls",
        JSON.stringify(updatedUrls)
      );

      setResult(data);

    } catch (error) {

      console.log(error);
      alert("Backend not running");

    }

    setLoading(false);
  };

  return (

    <div className="container">

      <div className="card">

        <div className="top-bar">

          <div>

            <h1>PHISHGUARD AI</h1>

            <p className="subtitle">
              Intelligent Real-Time Phishing Detection Platform
            </p>

          </div>

          <div className="live-box">

            <h3>⚡ Live Threats</h3>

            <p>12,847 Detected Today</p>

          </div>

        </div>

        <div className="search-section">

          <input
            type="text"
            placeholder="https://example.com"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />

          <button onClick={checkPhishing}>

            {loading ? 'SCANNING...' : 'SCAN WEBSITE'}

          </button>

        </div>

        {loading && (

          <div className="loading-section">

            <div className="loader"></div>

            <div className="scan-logs">

              <p>✔ Initializing AI Engine...</p>
              <p>✔ Checking SSL Security...</p>
              <p>✔ Running URL Analysis...</p>
              <p>✔ Detecting Threat Intelligence...</p>
              <p>✔ Generating ML Prediction...</p>

            </div>

          </div>

        )}

        {result && (

          <div className="dashboard">

            <div className="result-header">

              <div>

                <h2>
                  {result.prediction === 'Phishing'
                    ? '⚠️ PHISHING DETECTED'
                    : '✅ SAFE WEBSITE'}
                </h2>

                <p className="small-text">
                  AI Security Analysis Completed
                </p>

              </div>

              <div className="score-circle">

                {result.confidence}%

              </div>

            </div>

            <div className="stats-grid">

              <div className="stat-box">

                <h3>SSL Security</h3>

                <p>
                  {url.startsWith('https')
                    ? 'Secure HTTPS'
                    : 'Unsecure HTTP'}
                </p>

              </div>

              <div className="stat-box">

                <h3>Risk Level</h3>

                <p>
                  {result.confidence > 70
                    ? 'LOW'
                    : result.confidence > 40
                    ? 'MEDIUM'
                    : 'HIGH'}
                </p>

              </div>

              <div className="stat-box">

                <h3>Domain Trust</h3>

                <p>
                  {result.prediction === 'Phishing'
                    ? 'Suspicious'
                    : 'Trusted'}
                </p>

              </div>

            </div>

            <div className="meter-section">

              <div className="meter-title">

                Threat Confidence Meter

              </div>

              <div className="meter">

                <div
                  className="meter-fill"
                  style={{ width: `${result.confidence}%` }}
                ></div>

              </div>

            </div>

            <div className="analysis-grid">

              <div className="analysis-box">

                <h3>Threat Intelligence</h3>

                <ul>

                  <li>✔ URL structure analyzed</li>
                  <li>✔ ML prediction generated</li>
                  <li>✔ Suspicious patterns checked</li>
                  <li>✔ Domain validation completed</li>
                  <li>✔ Security scoring completed</li>

                </ul>

              </div>

              <div className="analysis-box">

                <h3>Detected Features</h3>

                <ul>

                  {result.features &&
                    Object.entries(result.features).map(([key, value]) => (

                      <li key={key}>
                        {key}: {value.toString()}
                      </li>

                    ))}

                </ul>

              </div>

            </div>

          </div>

        )}

        {recentUrls.length > 0 && (

          <div className="recent-section">

            <h3>Recent Scanned URLs</h3>

            <div className="recent-list">

              {recentUrls.map((item, index) => (

                <div
                  key={index}
                  className="recent-item"
                  onClick={() => setUrl(item)}
                >
                  {item}
                </div>

              ))}

            </div>

          </div>

        )}

        <p className="footer">
          Developed using Machine Learning & Cybersecurity Techniques
        </p>

      </div>

    </div>

  );
}

export default App;