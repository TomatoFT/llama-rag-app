import React, { useCallback, useState } from 'react';
import { Upload, File, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';

interface FileUploadProps {
  onUploadSuccess: () => void;
  apiBaseUrl: string;
}

export const FileUpload: React.FC<FileUploadProps> = ({ onUploadSuccess, apiBaseUrl }) => {
  const [uploading, setUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'success' | 'error'>('idle');
  const [uploadedFile, setUploadedFile] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileUpload = useCallback(async (file: File) => {
    if (!file.type.includes('pdf')) {
      setError('Please upload a PDF file');
      setUploadStatus('error');
      return;
    }

    setUploading(true);
    setError(null);
    setUploadStatus('idle');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${apiBaseUrl}/upload`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Upload failed: ${response.statusText}`);
      }

      setUploadedFile(file.name);
      setUploadStatus('success');
      onUploadSuccess();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed');
      setUploadStatus('error');
    } finally {
      setUploading(false);
    }
  }, [apiBaseUrl, onUploadSuccess]);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      handleFileUpload(files[0]);
    }
  }, [handleFileUpload]);

  const handleFileSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      handleFileUpload(files[0]);
    }
  }, [handleFileUpload]);

  return (
    <div className="w-full max-w-2xl mx-auto">
      <div
        className={`border-2 border-dashed rounded-xl p-8 text-center transition-all duration-200 ${
          uploading
            ? 'border-blue-300 bg-blue-50'
            : uploadStatus === 'success'
            ? 'border-green-300 bg-green-50'
            : uploadStatus === 'error'
            ? 'border-red-300 bg-red-50'
            : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50'
        }`}
        onDrop={handleDrop}
        onDragOver={(e) => e.preventDefault()}
      >
        <input
          type="file"
          accept=".pdf"
          onChange={handleFileSelect}
          className="hidden"
          id="file-upload"
          disabled={uploading}
        />
        
        <div className="flex flex-col items-center space-y-4">
          {uploading ? (
            <Loader2 className="h-12 w-12 text-blue-500 animate-spin" />
          ) : uploadStatus === 'success' ? (
            <CheckCircle className="h-12 w-12 text-green-500" />
          ) : uploadStatus === 'error' ? (
            <AlertCircle className="h-12 w-12 text-red-500" />
          ) : (
            <Upload className="h-12 w-12 text-gray-400" />
          )}
          
          <div>
            {uploading ? (
              <p className="text-blue-600 font-medium">Uploading document...</p>
            ) : uploadStatus === 'success' ? (
              <div>
                <p className="text-green-600 font-medium">Document uploaded successfully!</p>
                <p className="text-sm text-gray-600 mt-1 flex items-center justify-center gap-1">
                  <File className="h-4 w-4" />
                  {uploadedFile}
                </p>
              </div>
            ) : uploadStatus === 'error' ? (
              <div>
                <p className="text-red-600 font-medium">Upload failed</p>
                <p className="text-sm text-red-500 mt-1">{error}</p>
              </div>
            ) : (
              <div>
                <p className="text-lg font-medium text-gray-700">Upload your PDF document</p>
                <p className="text-gray-500 mt-2">Drag and drop or click to select</p>
              </div>
            )}
          </div>
          
          {!uploading && uploadStatus !== 'success' && (
            <label
              htmlFor="file-upload"
              className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors cursor-pointer"
            >
              <Upload className="h-4 w-4 mr-2" />
              Choose File
            </label>
          )}
        </div>
      </div>
    </div>
  );
};