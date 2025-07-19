import React, { useState } from "react";
import axios from "axios";

function App() {
  const [prompt, setPrompt] = useState("");
  const [sql, setSql] = useState("");
  const [table, setTable] = useState([]);
  const [columns, setColumns] = useState([]);
  const [chart, setChart] = useState(null);
  const [file, setFile] = useState(null);

  const uploadFile = async () => {
    const formData = new FormData();
    formData.append("file", file);
    await axios.post("http://localhost:5000/upload", formData);
  };

  const handlePrompt = async () => {
    const res = await axios.post("http://localhost:5000/prompt", { prompt });
    setSql(res.data.sql);
    setTable(res.data.table);
    setColumns(res.data.columns);
    setChart(res.data.chart);
  };

  return (
    <div className="p-4 max-w-screen-lg mx-auto">
      <h1 className="text-3xl font-bold mb-4">EQ Data Insight Generator</h1>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={uploadFile} className="ml-2 px-3 py-1 bg-blue-500 text-white">Upload</button>
      <div className="mt-4">
        <textarea value={prompt} onChange={(e) => setPrompt(e.target.value)} rows={3} className="w-full border p-2" placeholder="Ask a question..." />
        <button onClick={handlePrompt} className="mt-2 px-4 py-2 bg-green-600 text-white">Generate</button>
      </div>
      <div className="mt-4">
        <p><strong>Generated SQL:</strong> {sql}</p>
        {chart && <img src={`data:image/png;base64,${chart}`} alt="chart" />}
        {table.length > 0 && (
          <table className="mt-4 border border-collapse w-full">
            <thead>
              <tr>{columns.map((col) => <th className="border p-1" key={col}>{col}</th>)}</tr>
            </thead>
            <tbody>
              {table.map((row, i) => (
                <tr key={i}>{columns.map((col) => <td className="border p-1" key={col}>{row[col]}</td>)}</tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default App;
