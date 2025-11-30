import { useState } from "react";

interface PredictionItem {
  label: string;
  probability: number;
}

interface PredictionResponse {
  top: PredictionItem[];
  all: PredictionItem[];
}

export default function App() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0];
    if (f) {
      setFile(f);
      setPreview(URL.createObjectURL(f));
      setResult(null);
      setError(null);
    }
  };

  const predict = async () => {
    if (!file) {
      setError("Selecione uma imagem primeiro.");
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    const form = new FormData();
    form.append("file", file);

    try {
      const resp = await fetch("http://localhost:8000/predict?topk=5", {
        method: "POST",
        body: form,
      });

      if (!resp.ok) {
        throw new Error(await resp.text());
      }

      const data = await resp.json();
      setResult(data);
    } catch (err: any) {
      setError("Erro ao processar: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center py-10 px-4">
      <h1 className="text-4xl font-bold mb-6 text-blue-700">Retina Analyzer</h1>

      {/* Upload */}
      <div className="bg-white shadow-xl rounded-lg p-6 w-full max-w-xl">
        <label className="block text-sm font-medium mb-2">Selecione uma imagem</label>
        <input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          className="mb-4"
        />

        {preview && (
          <div className="mb-4">
            <img
              src={preview}
              alt="Preview"
              className="w-full rounded shadow"
            />
          </div>
        )}

        <button
          onClick={predict}
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-lg transition disabled:opacity-50"
        >
          {loading ? "Processando..." : "Analisar Imagem"}
        </button>

        {error && <p className="text-red-600 mt-4">{error}</p>}
      </div>

      {/* Resultados */}
      {result && (
        <div className="bg-white shadow-xl rounded-lg p-6 mt-8 w-full max-w-xl">
          <h2 className="text-2xl font-semibold mb-4">Top Previsões</h2>

          {result.top.map((item, idx) => (
            <div key={idx} className="mb-4">
              <div className="flex justify-between mb-1">
                <span className="font-medium">{item.label}</span>
                <span>{(item.probability * 100).toFixed(2)}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div
                  className="bg-blue-600 h-3 rounded-full"
                  style={{ width: `${item.probability * 100}%` }}
                ></div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
