import { useEffect, useState } from 'react';
import FileSelector from './FileSelector';
import { useBackend } from './hooks/useBackend';

export default function App() {
  const [selectorStatus, setSelectorStatus] = useState('');
  const [file, setFile] = useState(null);
  const [imageSrc, setImageSrc] = useState(null);
  const backend = useBackend();

  const processImage = () => {
    console.log("Processing image:", file);
    if (!file || !backend) return;
    backend.process_image(file, (result) => {
      console.log("Image processed:", result);
      setImageSrc(`wysebee://openfile/?file=${result}`);
    });
  }

  useEffect(() => {
    if (!backend) return;
    backend.sendFile.connect((file, size) => {
      console.log("received file:", file, "size:", size);
      setSelectorStatus(`Selected ${file} (${Math.round(size / 1024)} KB)`);
      setFile(file);
      setImageSrc(`wysebee://openfile/?file=${file}`);
    })
  }, [backend]);

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      {!selectorStatus && <FileSelector selectorStatus={selectorStatus} />}
      {selectorStatus && imageSrc && (
        <div style={{ marginTop: "1rem" }}>
          <img
            src={imageSrc}
            alt="Selected"
            style={{ maxWidth: "100%", maxHeight: "500px", border: "1px solid #ccc" }}
          />
          <button
            onClick={processImage}
            className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 disabled:opacity-50"
          >
            Process
          </button>
        </div>
      )}
    </div>
  )
}