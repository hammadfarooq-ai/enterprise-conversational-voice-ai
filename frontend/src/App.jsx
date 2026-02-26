import { useState } from "react";
import { endCall, startCall } from "./api";

function newCallId() {
  return `call-${Date.now()}`;
}

export default function App() {
  const [leadPhone, setLeadPhone] = useState("+15550001111");
  const [campaignName, setCampaignName] = useState("default-campaign");
  const [activeCallId, setActiveCallId] = useState("");
  const [logLines, setLogLines] = useState([]);
  const [loading, setLoading] = useState(false);

  function addLog(line) {
    setLogLines((prev) => [`${new Date().toISOString()} ${line}`, ...prev].slice(0, 50));
  }

  async function onStart() {
    setLoading(true);
    try {
      const callId = newCallId();
      const res = await startCall({
        call_id: callId,
        lead_phone: leadPhone,
        campaign_name: campaignName,
        metadata: { source: "dashboard" }
      });
      setActiveCallId(res.call_id);
      addLog(`Call started: ${res.call_id}`);
    } catch (err) {
      addLog(`Start failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  }

  async function onEnd() {
    if (!activeCallId) return;
    setLoading(true);
    try {
      const res = await endCall({
        call_id: activeCallId,
        disposition: "completed"
      });
      addLog(`Call ended: ${res.call_id}`);
      setActiveCallId("");
    } catch (err) {
      addLog(`End failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <h1>Conversational Voice AI</h1>
      <p className="subtitle">Outbound calling control panel</p>

      <div className="card">
        <label>Lead Phone</label>
        <input value={leadPhone} onChange={(e) => setLeadPhone(e.target.value)} />

        <label>Campaign Name</label>
        <input value={campaignName} onChange={(e) => setCampaignName(e.target.value)} />

        <div className="row">
          <button disabled={loading || !!activeCallId} onClick={onStart}>
            Start Outbound Call
          </button>
          <button disabled={loading || !activeCallId} className="danger" onClick={onEnd}>
            End Call
          </button>
        </div>
      </div>

      <div className="card">
        <h2>Active Call</h2>
        <p>{activeCallId || "No active call"}</p>
      </div>

      <div className="card">
        <h2>Event Log</h2>
        <div className="log">
          {logLines.length === 0 ? <p>No events yet.</p> : logLines.map((line) => <p key={line}>{line}</p>)}
        </div>
      </div>
    </div>
  );
}
