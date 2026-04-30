import React, { useState, useEffect } from 'react';

interface DiaryEntry {
  id: string;
  date: string;
  timestamp: string;
  original_filename: string;
  file_type: string;
  file_size: number;
  file_path: string;
  created_at: string;
}

const Diary: React.FC = () => {
  const [entries, setEntries] = useState<DiaryEntry[]>([]);
  const [dates, setDates] = useState<string[]>([]);
  const [selectedDate, setSelectedDate] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  // Fetch entries
  const fetchEntries = async (date?: string) => {
    setLoading(true);
    try {
      const url = date ? `http://localhost:8000/api/diary?date=${date}` : 'http://localhost:8000/api/diary';
      const response = await fetch(url);
      const data = await response.json();
      if (data.success) {
        setEntries(data.entries);
        setDates(data.dates);
      }
    } catch (error) {
      console.error('Error fetching entries:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEntries(selectedDate || undefined);
  }, [selectedDate]);

  // Handle file upload
  const handleUpload = async () => {
    if (!selectedFile) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', selectedFile);
    
    // Detect file type
    let fileType = 'other';
    if (selectedFile.type.startsWith('image/')) fileType = 'image';
    else if (selectedFile.type.startsWith('video/')) fileType = 'video';
    else if (selectedFile.type.startsWith('audio/')) fileType = 'audio';
    else if (selectedFile.type === 'application/pdf') fileType = 'pdf';
    else if (selectedFile.type.startsWith('text/') || selectedFile.name.endsWith('.txt')) fileType = 'text';
    
    formData.append('file_type', fileType);

    try {
      const response = await fetch('http://localhost:8000/api/diary/upload', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      if (data.success) {
        alert('✅ Entry uploaded successfully!');
        setSelectedFile(null);
        // Clear file input
        const fileInput = document.getElementById('file-input') as HTMLInputElement;
        if (fileInput) fileInput.value = '';
        fetchEntries(selectedDate || undefined);
      } else {
        alert('❌ Upload failed');
      }
    } catch (error) {
      console.error('Upload error:', error);
      alert('❌ Upload failed');
    } finally {
      setUploading(false);
    }
  };

  // Handle delete
  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this entry?')) return;
    
    try {
      const response = await fetch(`http://localhost:8000/api/diary/${id}`, {
        method: 'DELETE',
      });
      const data = await response.json();
      if (data.success) {
        fetchEntries(selectedDate || undefined);
      } else {
        alert('❌ Delete failed');
      }
    } catch (error) {
      console.error('Delete error:', error);
      alert('❌ Delete failed');
    }
  };

  // Handle file download/view
  const handleViewFile = async (entryId: string, filename: string) => {
    window.open(`http://localhost:8000/api/diary/file/${entryId}`, '_blank');
  };

  // Format file size
  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  // Get emoji for file type
  const getFileEmoji = (type: string) => {
    const emojis: Record<string, string> = {
      image: '🖼️',
      video: '🎥',
      audio: '🎵',
      pdf: '📄',
      text: '📝',
      other: '📎'
    };
    return emojis[type] || emojis.other;
  };

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800 dark:text-white mb-2">
          📔 Digital Diary
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Your personal memory vault — store text, images, videos, audio, and PDFs
        </p>
      </div>

      {/* Upload Section */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-white">
          📤 Upload New Entry
        </h2>
        <div className="flex gap-4 items-end">
          <div className="flex-1">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Choose File
            </label>
            <input
              id="file-input"
              type="file"
              onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              accept="image/*,video/*,audio/*,.pdf,.txt"
            />
          </div>
          <button
            onClick={handleUpload}
            disabled={!selectedFile || uploading}
            className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition"
          >
            {uploading ? 'Uploading...' : 'Upload'}
          </button>
        </div>
        {selectedFile && (
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
            Selected: {selectedFile.name} ({formatFileSize(selectedFile.size)})
          </p>
        )}
      </div>

      {/* Date Filter */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-white">
          📅 Filter by Date
        </h2>
        <div className="flex gap-4">
          <select
            value={selectedDate}
            onChange={(e) => setSelectedDate(e.target.value)}
            className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
          >
            <option value="">All Dates</option>
            {dates.map(date => (
              <option key={date} value={date}>{date}</option>
            ))}
          </select>
          {selectedDate && (
            <button
              onClick={() => setSelectedDate('')}
              className="px-4 py-2 bg-gray-500 text-white rounded-md hover:bg-gray-600 transition"
            >
              Clear
            </button>
          )}
        </div>
      </div>

      {/* Entries List */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-white">
          📋 Diary Entries ({entries.length})
        </h2>
        
        {loading ? (
          <div className="text-center py-8 text-gray-500">Loading...</div>
        ) : entries.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            No entries found. Upload your first memory! 📔
          </div>
        ) : (
          <div className="space-y-3">
            {entries.map((entry) => (
              <div
                key={entry.id}
                className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:shadow-md transition"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-2xl">{getFileEmoji(entry.file_type)}</span>
                      <h3 className="font-semibold text-gray-800 dark:text-white">
                        {entry.original_filename}
                      </h3>
                      <span className="text-xs px-2 py-1 bg-gray-200 dark:bg-gray-600 rounded-full">
                        {entry.file_type}
                      </span>
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400 space-y-1">
                      <p>📅 Date: {entry.date}</p>
                      <p>📏 Size: {formatFileSize(entry.file_size)}</p>
                      <p>🕐 Uploaded: {new Date(entry.created_at).toLocaleString()}</p>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={() => handleViewFile(entry.id, entry.original_filename)}
                      className="px-3 py-1 bg-green-600 text-white rounded-md hover:bg-green-700 text-sm"
                    >
                      View
                    </button>
                    <button
                      onClick={() => handleDelete(entry.id)}
                      className="px-3 py-1 bg-red-600 text-white rounded-md hover:bg-red-700 text-sm"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Diary;
