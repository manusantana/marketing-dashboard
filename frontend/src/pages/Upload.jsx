import { useState } from "react";

export default function Upload() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");
  const [mode, setMode] = useState("append");
  const [lastBatchId, setLastBatchId] = useState(null);

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      setStatus("Subiendo...");
      const res = await fetch(`http://localhost:8000/upload?mode=${mode}`, {
        method: "POST",
        body: formData,
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
    <div className="p-6 space-y-4">
      <h2 className="text-2xl font-bold">Subir archivo Excel</h2>
      <div className="card space-y-4">
        <input
          type="file"
          accept=".xlsx,.xls,.csv"
          onChange={(e) => setFile(e.target.files[0])}
          className="mb-4"
        />

        <div>
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

        <div className="flex gap-2">
          <button onClick={handleUpload} className="btn-primary">
            Subir
          </button>
          <button
            onClick={handleUndo}
            disabled={!lastBatchId}
            className="btn-secondary disabled:opacity-50"
          >
            Deshacer último upload
          </button>
        </div>
      </div>
      {status && <p>{status}</p>}
    </div>
  );
}
