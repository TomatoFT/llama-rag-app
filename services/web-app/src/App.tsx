import React, { useState } from 'react';
import { FileText, MessageSquare, Settings, Activity } from 'lucide-react';
import { FileUpload } from './components/FileUpload';
import { ChatInterface } from './components/ChatInterface';
import { StatusIndicator } from './components/StatusIndicator';

function App() {
  const [isDocumentUploaded, setIsDocumentUploaded] = useState(false);
  const [apiBaseUrl, setApiBaseUrl] = useState('http://localhost:8000');
  const [showSettings, setShowSettings] = useState(false);

  const handleUploadSuccess = () => {
    setIsDocumentUploaded(true);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-sm border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-blue-600 rounded-lg">
                <FileText className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">RAG Chatbot</h1>
                <p className="text-sm text-gray-500">Document Q&A Assistant</p>
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              <StatusIndicator apiBaseUrl={apiBaseUrl} />
              <button
                onClick={() => setShowSettings(!showSettings)}
                className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
                title="Settings"
              >
                <Settings className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Settings Panel */}
      {showSettings && (
        <div className="bg-white border-b border-gray-200 px-4 py-3">
          <div className="max-w-7xl mx-auto">
            <div className="flex items-center gap-4">
              <label htmlFor="api-url" className="text-sm font-medium text-gray-700">
                API Base URL:
              </label>
              <input
                id="api-url"
                type="text"
                value={apiBaseUrl}
                onChange={(e) => setApiBaseUrl(e.target.value)}
                className="px-3 py-1 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="http://localhost:8000"
              />
            </div>
          </div>
        </div>
      )}

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {!isDocumentUploaded ? (
          /* Upload Phase */
          <div className="max-w-4xl mx-auto">
            <div className="text-center mb-12">
              <div className="inline-flex p-4 bg-blue-100 rounded-full mb-6">
                <MessageSquare className="h-12 w-12 text-blue-600" />
              </div>
              <h2 className="text-3xl font-bold text-gray-900 mb-4">
                Welcome to RAG Chatbot
              </h2>
              <p className="text-lg text-gray-600 max-w-2xl mx-auto">
                Upload your PDF document to start an intelligent conversation. 
                Our AI will analyze your document and answer questions based on its content.
              </p>
            </div>
            
            <FileUpload 
              onUploadSuccess={handleUploadSuccess}
              apiBaseUrl={apiBaseUrl}
            />
            
            <div className="mt-12 grid md:grid-cols-3 gap-6 text-center">
              <div className="p-6">
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <FileText className="h-6 w-6 text-blue-600" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Upload Documents</h3>
                <p className="text-gray-600 text-sm">
                  Upload PDF documents for AI-powered analysis and questioning
                </p>
              </div>
              
              <div className="p-6">
                <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <MessageSquare className="h-6 w-6 text-green-600" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Ask Questions</h3>
                <p className="text-gray-600 text-sm">
                  Chat naturally with your document using advanced AI understanding
                </p>
              </div>
              
              <div className="p-6">
                <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <Activity className="h-6 w-6 text-purple-600" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Get Insights</h3>
                <p className="text-gray-600 text-sm">
                  Receive detailed answers backed by relevant document sections
                </p>
              </div>
            </div>
          </div>
        ) : (
          /* Chat Phase */
          <div className="h-[calc(100vh-12rem)]">
            <div className="bg-white rounded-2xl shadow-xl border border-gray-200 h-full flex flex-col overflow-hidden">
              <div className="px-6 py-4 border-b border-gray-200 bg-gray-50 rounded-t-2xl">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-3 h-3 bg-green-400 rounded-full"></div>
                    <h3 className="font-semibold text-gray-900">Document Chat</h3>
                  </div>
                  <button
                    onClick={() => setIsDocumentUploaded(false)}
                    className="text-sm text-blue-600 hover:text-blue-700 font-medium"
                  >
                    Upload New Document
                  </button>
                </div>
              </div>
              
              <ChatInterface 
                apiBaseUrl={apiBaseUrl}
                isDocumentUploaded={isDocumentUploaded}
              />
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;