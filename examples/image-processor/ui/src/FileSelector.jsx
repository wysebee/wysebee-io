import { useRef } from 'react';
import { useBackend } from './hooks/useBackend';

export default function FileSelector({selectorStatus}) {
  const inputRef = useRef(null);
  const backend = useBackend();

  const handleOpenFileDialog = (e) => {
    e.preventDefault();
    if (backend) {
      backend.openFileDialog();
    }
  };

  return (
    <div className="max-w-xl mx-auto mt-10 p-6 border-2 border-dashed rounded-2xl border-blue-300 bg-white text-center">
      <div
        className="p-10 cursor-pointer transition hover:bg-blue-50"
        onClick={() => inputRef.current.click()}
        onDragOver={(e) => e.preventDefault()}
      >
        <p className="text-lg font-medium text-gray-700">Drag & drop files here</p>
        <p className="text-sm text-gray-500">or click to select files</p>
        <input
          type="file"
          multiple
          hidden
          ref={inputRef}
          onClick={handleOpenFileDialog}
        />
      </div>
      {selectorStatus && (
        <p className="my-4 text-sm text-gray-700">{selectorStatus}</p>
      )}
    </div>
  );
}