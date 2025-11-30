function ControlPanel({ temperature, setTemperature, responseTime, tokenUsage }) {
  return (
    <div className="control-panel">
      <div className="control-section">
        <label>Temperature: {temperature.toFixed(2)}</label>
        <input
          type="range"
          min="0"
          max="2"
          step="0.1"
          value={temperature}
          onChange={(e) => setTemperature(parseFloat(e.target.value))}
          className="temperature-slider"
        />
      </div>

      <div className="stats-section">
        {responseTime !== null && (
          <div className="stat-item">
            <span className="stat-label">Response Time:</span>
            <span className="stat-value">{responseTime}ms</span>
          </div>
        )}
        {tokenUsage && (
          <>
            <div className="stat-item">
              <span className="stat-label">Prompt Tokens:</span>
              <span className="stat-value">{tokenUsage.prompt_tokens}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Completion Tokens:</span>
              <span className="stat-value">{tokenUsage.completion_tokens}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Total Tokens:</span>
              <span className="stat-value">{tokenUsage.total_tokens}</span>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default ControlPanel;
