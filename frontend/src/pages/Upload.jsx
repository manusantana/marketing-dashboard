import { useState } from "react";

export default function Upload() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");
  const [mode, setMode] = useState("append");
  const [lastBatchId, setLastBatchId] = useState(null);

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file); // 👈 nombre del parámetro debe ser "file"

    try {
      setStatus("Subiendo...");
      const res = await fetch(`http://localhost:8000/upload?mode=${mode}`, {
        method: "POST",
        body: formData, // 👈 no pongas headers, el navegador los añade
      });

      if (!res.ok) throw new Error("Error en la subida");
      const data = await res.json();
      setStatus("✅ " + data.message);
      setLastBatchId(data.batch_id);
    } catch (err) {
      setStatus("❌ Error subiendo archivo");
      console.error(err);
    }
  };

  const handleUndo = async () => {
    if (!lastBatchId) return;
    try {
      setStatus("Deshaciendo último upload...");
      const res = await fetch(`http://localhost:8000/upload/${lastBatchId}`, {
        method: "DELETE",
      });
      if (!res.ok) throw new Error("Error deshaciendo upload");
      setStatus("✅ Último upload revertido");
      setLastBatchId(null);
    } catch (err) {
      setStatus("❌ Error deshaciendo upload");
      console.error(err);
    }
  };

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Subir archivo Excel</h2>

      <input
        type="file"
        accept=".xlsx,.xls,.csv"
        onChange={(e) => setFile(e.target.files[0])}
        className="mb-4"
      />

      <div className="mb-4">
        <label className="mr-2 font-semibold">Modo:</label>
        <select
          value={mode}
          onChange={(e) => setMode(e.target.value)}
          className="border rounded px-2 py-1"
        >
          <option value="append">Append</option>
          <option value="replace">Replace</option>
        </select>
      </div>

      <div className="space-x-2">
        <button
          onClick={handleUpload}
          className="px-4 py-2 bg-indigo-600 text-white rounded"
        >
          Subir
        </button>
        <button
          onClick={handleUndo}
          disabled={!lastBatchId}
          className="px-4 py-2 bg-gray-400 text-white rounded disabled:opacity-50"
        >
          Deshacer último upload
        </button>
      </div>

      {status && <p className="mt-4">{status}</p>}
    </div>
  );
}
