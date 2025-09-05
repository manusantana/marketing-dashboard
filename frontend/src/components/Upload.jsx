// frontend/src/components/Upload.jsx
import React, { useState } from "react";

export default function Upload() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState({ type: "", text: "" });
  const [history, setHistory] = useState([]);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async (mode = "append") => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`http://localhost:8000/upload/?mode=${mode}`, {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setStatus({
        type: "success",
        text: `${data.message} (batch_id: ${data.batch_id})`,
      });
      fetchHistory();
    } catch (err) {
      console.error(err);
      setStatus({ type: "error", text: "No se pudo subir el archivo" });
    }

    setTimeout(() => setStatus({ type: "", text: "" }), 3000);
  };

  const fetchHistory = async () => {
    const res = await fetch("http://localhost:8000/upload/history");
    const data = await res.json();
    setHistory(data);
  };

  const handleUndo = async (batchId) => {
    try {
      await fetch(`http://localhost:8000/upload/${batchId}`, { method: "DELETE" });
      setStatus({
        type: "success",
        text: `Batch ${batchId} eliminado correctamente`,
      });
      fetchHistory();
    } catch (err) {
      console.error(err);
      setStatus({
        type: "error",
        text: "No se pudo deshacer la subida",
      });
    }

    setTimeout(() => setStatus({ type: "", text: "" }), 3000);
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Upload de archivo</h2>
      <input type="file" onChange={handleFileChange} className="mb-2" />
      <div className="flex gap-2 mb-4">
        <button onClick={() => handleUpload("append")} className="btn-primary">
          Subir (Append)
        </button>
        <button onClick={() => handleUpload("replace")} className="btn-danger">
          Subir (Replace)
        </button>
      </div>
      {status.text && (
        <p className={status.type === "success" ? "text-green-600" : "text-red-600"}>
          {status.text}
        </p>
      )}

      <h3 className="text-lg font-semibold mt-6 mb-2">Historial de uploads</h3>
      <button onClick={fetchHistory} className="btn-secondary mb-2">
        Refrescar
      </button>
      <table className="table">
        <thead>
          <tr>
            <th>Batch ID</th>
            <th>Archivo</th>
            <th>Modo</th>
            <th>Filas</th>
            <th>Fecha</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {history.map((h) => (
            <tr key={h.batch_id}>
              <td>{h.batch_id}</td>
              <td>{h.filename}</td>
              <td>{h.mode}</td>
              <td>{h.rows}</td>
              <td>{new Date(h.created_at).toLocaleString()}</td>
              <td>
                <button
                  onClick={() => handleUndo(h.batch_id)}
                  className="btn-danger"
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
