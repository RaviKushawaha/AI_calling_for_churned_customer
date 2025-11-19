import React, { useState } from "react";

function App() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [currentPage, setCurrentPage] = useState(0); // 0-based page index
  const pageSize = 10;

  const handleRun = async () => {
    setLoading(true);
    setError("");
    setResults([]);
    setCurrentPage(0);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/topk/", {
        method: "GET", // allowed in your view now
      });

      if (!res.ok) {
        throw new Error(`Request failed: ${res.status}`);
      }

      const data = await res.json();
      setResults(data.results || []);
    } catch (err) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  const totalPages = Math.ceil(results.length / pageSize);
  const pageStart = currentPage * pageSize;
  const pageEnd = pageStart + pageSize;
  const pageData = results.slice(pageStart, pageEnd);

  const handlePrev = () => {
    setCurrentPage((p) => Math.max(0, p - 1));
  };

  const handleNext = () => {
    setCurrentPage((p) => Math.min(totalPages - 1, p + 1));
  };

  // stubs for future phone/email actions
  const handlePhoneClick = (row) => {
    console.log("Phone click for:", row.customer_id, row.phone_number);
    // later: trigger call API / tel: link
  };

  const handleEmailClick = (row) => {
    console.log("Email click for:", row.customer_id, row.email_id);
    // later: trigger AI-generated email / mailto / backend API
  };

  return (
    <div style={{ padding: "24px", fontFamily: "system-ui, sans-serif" }}>
      <h1 style={{ marginBottom: 4 }}>Customer Churn Action Center</h1>
      <p style={{ maxWidth: 700, marginBottom: 16, color: "#444" }}>
        This dashboard surfaces high-risk customers for a D2C skincare brand
        (Minimalist-like). Click <b>Run</b> to score the latest data, then use
        the phone and email actions to reach out and prevent churn.
      </p>

      <button
        onClick={handleRun}
        disabled={loading}
        style={{
          padding: "8px 18px",
          cursor: loading ? "not-allowed" : "pointer",
          marginBottom: "16px",
        }}
      >
        {loading ? "Running..." : "Run churn scoring"}
      </button>

      {error && <p style={{ color: "red" }}>Error: {error}</p>}

      {results.length === 0 && !loading && !error && (
        <p style={{ marginTop: 8 }}>
          No results yet. Click <b>Run churn scoring</b> to load Top-risk
          customers.
        </p>
      )}

      {results.length > 0 && (
        <>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginTop: 8 }}>
            <h3 style={{ margin: 0 }}>
              Top 10% High-Risk Customers{" "}
              <span style={{ fontSize: 12, color: "#666" }}>
                (showing {pageStart + 1}–{Math.min(pageEnd, results.length)} of {results.length})
              </span>
            </h3>
            <div>
              <button
                onClick={handlePrev}
                disabled={currentPage === 0}
                style={{ marginRight: 8 }}
              >
                ◀ Prev 10
              </button>
              <button
                onClick={handleNext}
                disabled={currentPage >= totalPages - 1}
              >
                Next 10 ▶
              </button>
            </div>
          </div>

          <table
            style={{
              borderCollapse: "collapse",
              width: "100%",
              marginTop: "10px",
              fontSize: 14,
            }}
          >
            <thead>
              <tr>
                <th style={thStyle}>Customer ID</th>
                <th style={thStyle}>Email</th>
                <th style={thStyle}>Phone</th>
                <th style={thStyle}>Avg Order Value</th>
                <th style={thStyle}>Acquisition Channel</th>
                <th style={thStyle}>Days Since Last Purchase</th>
                <th style={thStyle}>Churn Probability</th>
                <th style={thStyle}>Contact</th>
              </tr>
            </thead>
            <tbody>
              {pageData.map((row, idx) => (
                <tr key={idx}>
                  <td style={tdStyle}>{row.customer_id}</td>
                  <td style={tdStyle}>{row.email_id}</td>
                  <td style={tdStyle}>{row.phone_number}</td>
                  <td style={tdStyle}>
                    {row.avg_order_value !== undefined
                      ? row.avg_order_value.toFixed(2)
                      : ""}
                  </td>
                  <td style={tdStyle}>{row.acquisition_channel}</td>
                  <td style={tdStyle}>{row.days_since_last_purchase}</td>
                  <td style={tdStyle}>
                    {row.prob !== undefined ? row.prob.toFixed(3) : ""}
                  </td>
                  <td style={{ ...tdStyle, textAlign: "center" }}>
                    <button
                      style={iconButtonStyle}
                      title="Call customer"
                      onClick={() => handlePhoneClick(row)}
                    >
                      📞
                    </button>
                    <button
                      style={iconButtonStyle}
                      title="Email customer"
                      onClick={() => handleEmailClick(row)}
                    >
                      ✉️
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}
    </div>
  );
}

const thStyle = {
  border: "1px solid #ddd",
  padding: "8px",
  backgroundColor: "#f4f4f4",
  textAlign: "left",
};

const tdStyle = {
  border: "1px solid #eee",
  padding: "8px",
};

const iconButtonStyle = {
  border: "none",
  background: "none",
  cursor: "pointer",
  fontSize: "16px",
  margin: "0 4px",
};

export default App;
