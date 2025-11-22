import React, { useState } from "react";

function App() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [currentPage, setCurrentPage] = useState(0);
  const pageSize = 10;

  const [mode, setMode] = useState("list"); // "list" | "call"
  const [selectedCustomer, setSelectedCustomer] = useState(null);
  const [callPhone, setCallPhone] = useState("");
  const [callScript, setCallScript] = useState("");
  const [callLoading, setCallLoading] = useState(false);
  const [callError, setCallError] = useState("");

  const handleRun = async () => {
    setLoading(true);
    setError("");
    setResults([]);
    setCurrentPage(0);
    setMode("list");

    try {
      const res = await fetch("http://127.0.0.1:8000/api/topk/", {
        method: "GET",
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

  const handlePrev = () => setCurrentPage((p) => Math.max(0, p - 1));
  const handleNext = () =>
    setCurrentPage((p) => Math.min(totalPages - 1, p + 1));

  const handlePhoneClick = async (row) => {
    setMode("call");
    setSelectedCustomer(row);
    setCallPhone(row.phone_number || "");
    setCallScript("");
    setCallError("");
    setCallLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/call_script/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ customer_id: row.customer_id }),
      });

      if (!res.ok) {
        throw new Error(`Request failed: ${res.status}`);
      }

      const data = await res.json();
      setCallPhone(data.phone_number || row.phone_number || "");
      setCallScript(data.call_script || "");
    } catch (err) {
      setCallError(err.message || "Failed to generate call script");
    } finally {
      setCallLoading(false);
    }
  };

  const handleEmailClick = (row) => {
    console.log("Email click for:", row.customer_id, row.email_id);
    // will be used later
  };

  const handleBackToList = () => {
    setMode("list");
    setCallError("");
  };

  // const handleConfirmCall = () => {
  //   console.log("TODO: trigger telephony API with:", {
  //     customer: selectedCustomer,
  //     phone: callPhone,
  //     script: callScript,
  //   });
  //   alert("In final version, this will trigger a real call via telephony API.");
  // };

  const handleConfirmCall = async () => {
    alert("Button clicked");

    console.log("Sending to backend:", {
      phone: callPhone,
      script: callScript,
    });

    try {
      const res = await fetch("http://127.0.0.1:8000/api/trigger-call/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ phone: callPhone, script: callScript }),
      });

      console.log("Response status:", res.status);
      const text = await res.text();
      console.log("Raw response text:", text);

      alert("Got response. Check console for details.");
    } catch (err) {
      console.error("Network or JS error:", err);
      alert("Something went wrong calling backend");
    }
  };

  // ---------------- RENDER ----------------

  if (mode === "call" && selectedCustomer) {
    return (
      <div style={{ padding: "24px", fontFamily: "system-ui, sans-serif" }}>
        <button onClick={handleBackToList} style={{ marginBottom: 12 }}>
          ◀ Back to list
        </button>
        <h2>Call Preview</h2>
        <p style={{ color: "#555" }}>
          Review the phone number and AI-generated script before triggering the
          call.
        </p>

        <div style={{ marginBottom: 12 }}>
          <label style={{ display: "block", marginBottom: 4 }}>
            Customer ID: <b>{selectedCustomer.customer_id}</b>
          </label>
          <label style={{ display: "block", marginBottom: 4 }}>
            Phone number:
          </label>
          <input
            type="text"
            value={callPhone}
            onChange={(e) => setCallPhone(e.target.value)}
            style={{ width: "300px", padding: "6px" }}
          />
        </div>

        {callLoading && <p>Generating script...</p>}
        {callError && <p style={{ color: "red" }}>Error: {callError}</p>}

        <div style={{ marginTop: 12 }}>
          <label style={{ display: "block", marginBottom: 4 }}>
            Call script (editable):
          </label>
          <textarea
            value={callScript}
            onChange={(e) => setCallScript(e.target.value)}
            rows={10}
            style={{ width: "100%", padding: "8px", fontFamily: "inherit" }}
          />
        </div>

        <button
          onClick={handleConfirmCall}
          style={{ marginTop: 16, padding: "8px 16px" }}
          disabled={callLoading}
        >
          Confirm &amp; Trigger Call
        </button>
      </div>
    );
  }

  // LIST VIEW
  return (
    <div style={{ padding: "24px", fontFamily: "system-ui, sans-serif" }}>
      <h1 style={{ marginBottom: 4 }}>Customer Churn Action Center</h1>
      <p style={{ maxWidth: 700, marginBottom: 16, color: "#444" }}>
        This dashboard surfaces high-risk customers for a D2C skincare brand.
        Click <b>Run</b> to score the latest data, then use the phone and email
        actions to reach out and prevent churn.
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
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              marginTop: 8,
            }}
          >
            <h3 style={{ margin: 0 }}>
              Top 10% High-Risk Customers{" "}
              <span style={{ fontSize: 12, color: "#666" }}>
                (showing {pageStart + 1}–
                {Math.min(pageEnd, results.length)} of {results.length})
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
