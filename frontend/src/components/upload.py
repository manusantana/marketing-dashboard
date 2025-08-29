// frontend/src/components/Upload.jsx
import React, { useState } from "react";

export default function Upload() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [history, setHistory] = useState([]);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async (mode = "append") => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch(`http://localhost:8000/upload/?mode=${mode}`, {
      method: "POST",
      body: formData,
    });
    const data = await res.json();
    setMessage(data.message + " (batch_id: " + data.batch_id + ")");
    fetchHistory(); // refresca historial
  };

  const fetchHistory = async () => {
    const res = await fetch("http://localhost:8000/upload/history");
    const data = await res.json();
    setHistory(data);
  };

  const handleUndo = async (batchId) => {
    await fetch(`http://localhost:8000/upload/${batchId}`, { method: "DELETE" });
    setMessage(`Batch ${batchId} eliminado correctamente`);
    fetchHistory();
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Upload de archivo</h2>
      <input type="file" onChange={handleFileChange} className="mb-2" />
      <div className="space-x-2 mb-4">
        <button
          onClick={() => handleUpload("append")}
          className="px-4 py-2 bg-blue-500 text-white rounded"
        >
          Subir (Append)
        </button>
        <button
          onClick={() => handleUpload("replace")}
          className="px-4 py-2 bg-red-500 text-white rounded"
        >
          Subir (Replace)
        </button>
      </div>
      {message && <p className="mb-4 text-green-600">{message}</p>}

      <h3 className="text-lg font-semibold mt-6 mb-2">Historial de uploads</h3>
      <button
        onClick={fetchHistory}
        className="mb-2 px-3 py-1 bg-gray-300 rounded"
      >
        Refrescar
      </button>
      <table className="table-auto border-collapse border border-gray-300 w-full text-sm">
        <thead>
          <tr className="bg-gray-100">
            <th className="border px-2 py-1">Batch ID</th>
            <th className="border px-2 py-1">Archivo</th>
            <th className="border px-2 py-1">Modo</th>
            <th className="border px-2 py-1">Filas</th>
            <th className="border px-2 py-1">Fecha</th>
            <th className="border px-2 py-1">Acciones</th>
          </tr>
        </thead>
        <tbody>
          {history.map((h) => (
            <tr key={h.batch_id}>
              <td className="border px-2 py-1">{h.batch_id}</td>
              <td className="border px-2 py-1">{h.filename}</td>
              <td className="border px-2 py-1">{h.mode}</td>
              <td className="border px-2 py-1">{h.rows}</td>
              <td className="border px-2 py-1">
                {new Date(h.created_at).toLocaleString()}
              </td>
              <td className="border px-2 py-1">
                <button
                  onClick={() => handleUndo(h.batch_id)}
                  className="px-2 py-1 bg-red-400 text-white rounded"
                >
                  Deshacer
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
