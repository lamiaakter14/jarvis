/**
 * Digital Diary Page for Jarvis OS
 * Allows users to write daily journals with file attachments
 */

import React, { useState, useEffect } from 'react';
import {
  Calendar,
  Search,
  Upload,
  Image,
  Video,
  Music,
  FileText,
  Trash2,
  Edit2,
  Save,
  X,
  Smile,
  Tag,
  Clock,
  ChevronLeft,
  ChevronRight,
  BarChart3,
  FolderOpen
} from 'lucide-react';
import { diaryApi, DiaryEntry, DiaryStats } from '../api/diaryApi';

const Diary: React.FC = () => {
  const [selectedDate, setSelectedDate] = useState<string>(
    new Date().toISOString().split('T')[0]
  );
  const [entries, setEntries] = useState<DiaryEntry[]>([]);
  const [currentEntry, setCurrentEntry] = useState<DiaryEntry | null>(null);
  const [content, setContent] = useState('');
  const [tags, setTags] = useState<string>('');
  const [mood, setMood] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [isEditing, setIsEditing] = useState(false);
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState<DiaryStats | null>(null);
  const [viewMode, setViewMode] = useState<'daily' | 'list' | 'search'>('daily');

  const moods = ['😊 Happy', '😢 Sad', '🤔 Thinking', '💪 Energetic', '😴 Tired', '🎉 Excited', '😌 Peaceful'];

  useEffect(() => {
    loadEntries();
    loadStats();
  }, []);

  useEffect(() => {
    if (viewMode === 'daily' && selectedDate) {
      loadEntryForDate(selectedDate);
    }
  }, [selectedDate, viewMode]);

  const loadEntries = async () => {
    try {
      const allEntries = await diaryApi.getAllEntries(100);
      setEntries(allEntries);
    } catch (error) {
      console.error('Failed to load entries:', error);
    }
  };

  const loadStats = async () => {
    try {
      const statsData = await diaryApi.getStats();
      setStats(statsData);
    } catch (error) {
      console.error('Failed to load stats:', error);
    }
  };

  const loadEntryForDate = async (date: string) => {
    setLoading(true);
    try {
      const entry = await diaryApi.getEntryByDate(date);
      setCurrentEntry(entry);
      setContent(entry.content);
      setTags(entry.tags.join(', '));
      setMood(entry.mood || '');
      setIsEditing(false);
    } catch (error: any) {
      if (error.message.includes('404')) {
        setCurrentEntry(null);
        setContent('');
        setTags('');
        setMood('');
        setIsEditing(true);
      } else {
        console.error('Error loading entry:', error);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    if (!content.trim()) {
      alert('Please write something in your diary entry');
      return;
    }

    setLoading(true);
    try {
      const tagsArray = tags.split(',').map(t => t.trim()).filter(t => t);
      
      if (selectedFiles.length > 0) {
        await diaryApi.createEntryWithAttachments(
          selectedDate,
          content,
          selectedFiles,
          tagsArray,
          mood || undefined
        );
      } else {
        await diaryApi.createOrUpdateEntry(
          selectedDate,
          content,
          tagsArray,
          mood || undefined
        );
      }
      
      await loadEntryForDate(selectedDate);
      await loadEntries();
      await loadStats();
      setSelectedFiles([]);
      setIsEditing(false);
    } catch (error) {
      console.error('Failed to save entry:', error);
      alert('Failed to save diary entry');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!currentEntry) return;
    
    if (window.confirm(`Are you sure you want to delete the entry for ${selectedDate}?`)) {
      setLoading(true);
      try {
        await diaryApi.deleteEntry(selectedDate);
        setCurrentEntry(null);
        setContent('');
        setTags('');
        setMood('');
        setIsEditing(true);
        await loadEntries();
        await loadStats();
      } catch (error) {
        console.error('Failed to delete entry:', error);
        alert('Failed to delete entry');
      } finally {
        setLoading(false);
      }
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      await loadEntries();
      setViewMode('list');
      return;
    }
    
    setLoading(true);
    try {
      const results = await diaryApi.searchEntries(searchQuery);
      setEntries(results.results);
      setViewMode('search');
    } catch (error) {
      console.error('Search failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const getFileIcon = (type: string) => {
    switch (type) {
      case 'image': return <Image className="w-4 h-4" />;
      case 'video': return <Video className="w-4 h-4" />;
      case 'audio': return <Music className="w-4 h-4" />;
      default: return <FileText className="w-4 h-4" />;
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-pink-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
            Digital Diary
          </h1>
          <p className="text-gray-600 mt-2">Your personal memory keeper</p>
        </div>

        {/* Stats Bar */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <div className="bg-white rounded-lg shadow-md p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-500 text-sm">Total Entries</p>
                  <p className="text-2xl font-bold text-purple-600">{stats.total_entries}</p>
                </div>
                <FolderOpen className="w-8 h-8 text-purple-300" />
              </div>
            </div>
            <div className="bg-white rounded-lg shadow-md p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-500 text-sm">Attachments</p>
                  <p className="text-2xl font-bold text-pink-600">{stats.total_attachments}</p>
                </div>
                <Upload className="w-8 h-8 text-pink-300" />
              </div>
            </div>
            <div className="bg-white rounded-lg shadow-md p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-500 text-sm">Storage Used</p>
                  <p className="text-2xl font-bold text-blue-600">{stats.total_size_mb} MB</p>
                </div>
                <BarChart3 className="w-8 h-8 text-blue-300" />
              </div>
            </div>
            <div className="bg-white rounded-lg shadow-md p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-500 text-sm">Last Entry</p>
                  <p className="text-sm font-medium text-gray-700">
                    {entries[0]?.date || 'No entries'}
                  </p>
                </div>
                <Clock className="w-8 h-8 text-gray-300" />
              </div>
            </div>
          </div>
        )}

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Sidebar */}
          <div className="lg:col-span-1 space-y-4">
            {/* Date Picker */}
            <div className="bg-white rounded-lg shadow-md p-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Calendar className="inline-block w-4 h-4 mr-2" />
                Select Date
              </label>
              <input
                type="date"
                value={selectedDate}
                onChange={(e) => {
                  setSelectedDate(e.target.value);
                  setViewMode('daily');
                }}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              />
            </div>

            {/* Search */}
            <div className="bg-white rounded-lg shadow-md p-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Search className="inline-block w-4 h-4 mr-2" />
                Search Entries
              </label>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                  placeholder="Search by content or tags..."
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                />
                <button
                  onClick={handleSearch}
                  className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition"
                >
                  Go
                </button>
              </div>
            </div>

            {/* Recent Entries */}
            <div className="bg-white rounded-lg shadow-md p-4">
              <h3 className="font-semibold text-gray-700 mb-3">Recent Entries</h3>
              <div className="space-y-2 max-h-96 overflow-y-auto">
                {entries.slice(0, 10).map((entry) => (
                  <button
                    key={entry.id}
                    onClick={() => {
                      setSelectedDate(entry.date);
                      setViewMode('daily');
                    }}
                    className="w-full text-left p-3 rounded-lg hover:bg-purple-50 transition"
                  >
                    <div className="font-medium text-gray-800">{entry.date}</div>
                    <div className="text-sm text-gray-500 truncate">
                      {entry.content.substring(0, 50)}...
                    </div>
                    {entry.tags.length > 0 && (
                      <div className="flex gap-1 mt-1">
                        {entry.tags.slice(0, 2).map(tag => (
                          <span key={tag} className="text-xs bg-gray-100 px-2 py-0.5 rounded">
                            #{tag}
                          </span>
                        ))}
                      </div>
                    )}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Editor/Viewer */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex justify-between items-center mb-4">
                <div>
                  <h2 className="text-2xl font-semibold text-gray-800">
                    {viewMode === 'daily' ? selectedDate : viewMode === 'search' ? 'Search Results' : 'All Entries'}
                  </h2>
                  {currentEntry && !isEditing && (
                    <p className="text-sm text-gray-500 mt-1">
                      Last updated: {new Date(currentEntry.updated_at).toLocaleString()}
                    </p>
                  )}
                </div>
                {viewMode === 'daily' && (
                  <div className="flex gap-2">
                    {currentEntry && !isEditing && (
                      <>
                        <button
                          onClick={() => setIsEditing(true)}
                          className="px-3 py-1 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition flex items-center gap-1"
                        >
                          <Edit2 className="w-4 h-4" />
                          Edit
                        </button>
                        <button
                          onClick={handleDelete}
                          className="px-3 py-1 bg-red-600 text-white rounded-lg hover:bg-red-700 transition flex items-center gap-1"
                        >
                          <Trash2 className="w-4 h-4" />
                          Delete
                        </button>
                      </>
                    )}
                    {(!currentEntry || isEditing) && (
                      <button
                        onClick={handleSave}
                        disabled={loading}
                        className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition flex items-center gap-2 disabled:opacity-50"
                      >
                        <Save className="w-4 h-4" />
                        {loading ? 'Saving...' : 'Save Entry'}
                      </button>
                    )}
                  </div>
                )}
              </div>

              {viewMode === 'daily' ? (
                <div className="space-y-4">
                  {/* Mood Selector */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      <Smile className="inline-block w-4 h-4 mr-1" />
                      How are you feeling?
                    </label>
                    <select
                      value={mood}
                      onChange={(e) => setMood(e.target.value)}
                      disabled={!isEditing && !(!currentEntry)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 disabled:bg-gray-100"
                    >
                      <option value="">Select mood...</option>
                      {moods.map(m => (
                        <option key={m} value={m}>{m}</option>
                      ))}
                    </select>
                  </div>

                  {/* Tags */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      <Tag className="inline-block w-4 h-4 mr-1" />
                      Tags (comma separated)
                    </label>
                    <input
                      type="text"
                      value={tags}
                      onChange={(e) => setTags(e.target.value)}
                      disabled={!isEditing && !(!currentEntry)}
                      placeholder="personal, work, ideas, etc."
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 disabled:bg-gray-100"
                    />
                  </div>

                  {/* Content */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Diary Entry
                    </label>
                    <textarea
                      value={content}
                      onChange={(e) => setContent(e.target.value)}
                      disabled={!isEditing && !(!currentEntry)}
                      rows={12}
                      placeholder="Write your thoughts here..."
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 disabled:bg-gray-100 font-mono"
                    />
                  </div>

                  {/* File Upload */}
                  {(isEditing || !currentEntry) && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        <Upload className="inline-block w-4 h-4 mr-1" />
                        Attachments (Images, Videos, Audio, PDFs)
                      </label>
                      <input
                        type="file"
                        multiple
                        onChange={(e) => {
                          if (e.target.files) {
                            setSelectedFiles(Array.from(e.target.files));
                          }
                        }}
                        accept="image/*,video/*,audio/*,.pdf"
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                      />
                      {selectedFiles.length > 0 && (
                        <div className="mt-2 space-y-1">
                          {selectedFiles.map((file, idx) => (
                            <div key={idx} className="text-sm text-gray-600">
                              📎 {file.name} ({(file.size / 1024).toFixed(1)} KB)
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  )}

                  {/* Existing Attachments */}
                  {currentEntry && currentEntry.attachments.length > 0 && (
                    <div>
                      <h4 className="font-medium text-gray-700 mb-2">Attachments</h4>
                      <div className="space-y-2">
                        {currentEntry.attachments.map((att, idx) => (
                          <div key={idx} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                            <div className="flex items-center gap-2">
                              {getFileIcon(att.type)}
                              <span className="text-sm">{att.filename}</span>
                              <span className="text-xs text-gray-500">
                                ({formatFileSize(att.size)})
                              </span>
                            </div>
                            <a
                              href={`/${att.path}`}
                              target="_blank"
                              className="text-blue-600 hover:text-blue-800 text-sm"
                            >
                              View
                            </a>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <div className="space-y-4 max-h-[600px] overflow-y-auto">
                  {entries.length === 0 ? (
                    <p className="text-gray-500 text-center py-8">
                      No entries found. Try a different search or write your first diary entry!
                    </p>
                  ) : (
                    entries.map((entry) => (
                      <div
                        key={entry.id}
                        className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition cursor-pointer"
                        onClick={() => {
                          setSelectedDate(entry.date);
                          setViewMode('daily');
                        }}
                      >
                        <div className="flex justify-between items-start mb-2">
                          <h3 className="font-semibold text-lg text-purple-700">{entry.date}</h3>
                          {entry.mood && (
                            <span className="text-sm bg-purple-100 px-2 py-1 rounded">
                              {entry.mood}
                            </span>
                          )}
                        </div>
                        <p className="text-gray-700 mb-2">{entry.content.substring(0, 200)}...</p>
                        {entry.tags.length > 0 && (
                          <div className="flex gap-1 mt-2">
                            {entry.tags.map(tag => (
                              <span key={tag} className="text-xs bg-gray-100 px-2 py-0.5 rounded">
                                #{tag}
                              </span>
                            ))}
                          </div>
                        )}
                        {entry.attachments.length > 0 && (
                          <div className="flex gap-2 mt-2 text-xs text-gray-500">
                            <Upload className="w-3 h-3" />
                            {entry.attachments.length} attachment(s)
                          </div>
                        )}
                      </div>
                    ))
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Diary;