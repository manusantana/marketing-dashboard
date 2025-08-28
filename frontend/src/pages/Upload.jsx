import { useState } from "react";

export default function Upload() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file); // 👈 nombre del parámetro debe ser "file"

    try {
      setStatus("Subiendo...");
      const res = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,   // 👈 no pongas headers, el navegador los añade
      });

      if (!res.ok) throw new Error("Error en la subida");
      const data = await res.json();
      setStatus("✅ " + data.message);
    } catch (err) {
      setStatus("❌ Error subiendo archivo");
      console.error(err);
    }
  };

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Subir archivo Excel</h2>

      <input
        type="file"
        accept=".xlsx"
        onChange={(e) => setFile(e.target.files[0])}
        className="mb-4"
      />

      <button
        onClick={handleUpload}
        className="px-4 py-2 bg-indigo-600 text-white rounded"
      >
        Subir
      </button>

      {status && <p className="mt-4">{status}</p>}
    </div>
  );
}
