import { useState } from "react";
import client from "../api/client";

export default function Upload() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);

    try {
      await client.post("/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      setStatus("✅ Archivo subido con éxito");
    } catch (err) {
      setStatus("❌ Error al subir archivo");
    }
  };

  return (
    <div className="p-6">
      <h2 className="text-xl font-bold mb-4">Subir Excel/CSV</h2>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button
        onClick={handleUpload}
        className="bg-indigo-600 text-white px-4 py-2 ml-2 rounded"
      >
        Subir
      </button>
      {status && <p className="mt-4">{status}</p>}
    </div>
  );
}