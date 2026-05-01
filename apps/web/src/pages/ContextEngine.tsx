import React, { useState, useEffect } from 'react';
import { MapPin, Plus, Trash2, Search, X } from 'lucide-react';
import { getContexts, addContext, deleteContext, getCategories, Context } from '../api/contextApi';

export const ContextEngine: React.FC = () => {
  const [contexts, setContexts] = useState<Context[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [searchKeyword, setSearchKeyword] = useState('');
  const [showAddModal, setShowAddModal] = useState(false);
  const [loading, setLoading] = useState(true);
  
  // Form state
  const [formKey, setFormKey] = useState('');
  const [formValue, setFormValue] = useState('');
  const [formCategory, setFormCategory] = useState('market_price');
  const [formLocation, setFormLocation] = useState('Sakhipur');

  useEffect(() => {
    loadContexts();
    loadCategories();
  }, []);

  useEffect(() => {
    loadContexts();
  }, [selectedCategory, searchKeyword]);

  const loadContexts = async () => {
    setLoading(true);
    try {
      const data = await getContexts(selectedCategory || undefined, searchKeyword || undefined);
      setContexts(data);
    } catch (err) {
      console.error('Failed to load contexts:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadCategories = async () => {
    try {
      const data = await getCategories();
      setCategories(data);
    } catch (err) {
      console.error('Failed to load categories:', err);
    }
  };

  const handleAddContext = async () => {
    if (!formKey || !formValue) return;
    try {
      await addContext(formKey, formValue, formCategory, formLocation);
      setShowAddModal(false);
      resetForm();
      loadContexts();
      loadCategories();
    } catch (err) {
      console.error('Failed to add context:', err);
    }
  };

  const handleDeleteContext = async (id: string) => {
    if (confirm('Delete this context? This cannot be undone.')) {
      await deleteContext(id);
      loadContexts();
    }
  };

  const resetForm = () => {
    setFormKey('');
    setFormValue('');
    setFormCategory('market_price');
    setFormLocation('Sakhipur');
    setEditingContext(null);
  };

  const categoryColors: Record<string, string> = {
    market_price: 'bg-green-600/30 text-green-300',
    labour: 'bg-blue-600/30 text-blue-300',
    transport: 'bg-yellow-600/30 text-yellow-300',
    general: 'bg-gray-600/30 text-gray-300',
    construction: 'bg-orange-600/30 text-orange-300'
  };

  const categoryIcons: Record<string, string> = {
    market_price: '🏪',
    labour: '👷',
    transport: '🚗',
    general: '📝',
    construction: '🏗️'
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2 flex items-center gap-2">
          <MapPin className="w-8 h-8 text-green-400" /> Local Context Engine
        </h1>
        <p className="text-gray-400">
          Bangladesh/Sakhipur specific knowledge — prices, places, culture, labour rates
        </p>
      </div>

      {/* Actions Bar */}
      <div className="flex flex-wrap gap-4 mb-6">
        <button
          onClick={() => setShowAddModal(true)}
          className="bg-green-600 hover:bg-green-700 px-4 py-2 rounded-lg flex items-center gap-2"
        >
          <Plus className="w-4 h-4" /> Add New Context
        </button>
        
        <div className="flex-1 max-w-md">
          <div className="relative">
            <Search className="w-4 h-4 absolute left-3 top-3 text-gray-400" />
            <input
              type="text"
              placeholder="Search contexts..."
              value={searchKeyword}
              onChange={(e) => setSearchKeyword(e.target.value)}
              className="w-full bg-gray-800 border border-gray-700 rounded-lg pl-10 pr-4 py-2"
            />
          </div>
        </div>
        
        <select
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
          className="bg-gray-800 border border-gray-700 rounded-lg px-4 py-2"
        >
          <option value="">All Categories</option>
          {categories.map(cat => (
            <option key={cat} value={cat}>{cat}</option>
          ))}
        </select>
      </div>

      {/* Contexts List */}
      {loading ? (
        <div className="text-center py-12 text-gray-400">Loading contexts...</div>
      ) : contexts.length === 0 ? (
        <div className="text-center py-12 text-gray-400">
          No contexts found. Click "Add New Context" to get started.
        </div>
      ) : (
        <div className="space-y-3">
          {contexts.map((ctx) => (
            <div key={ctx.id} className="bg-gray-800 rounded-lg p-4 border border-gray-700 hover:border-green-500/50 transition-all">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="text-2xl">{categoryIcons[ctx.category] || '📌'}</span>
                    <h3 className="text-lg font-semibold">{ctx.key}</h3>
                    <span className={`text-xs px-2 py-1 rounded-full ${categoryColors[ctx.category] || 'bg-gray-600/30'}`}>
                      {ctx.category}
                    </span>
                  </div>
                  <p className="text-green-400 font-mono mb-2">{ctx.value}</p>
                  <div className="flex items-center gap-4 text-xs text-gray-500">
                    <span>📍 {ctx.location}</span>
                    <span>📅 {new Date(ctx.created_at).toLocaleDateString()}</span>
                    <span>🔗 source: {ctx.source}</span>
                  </div>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => handleDeleteContext(ctx.id)}
                    className="p-2 hover:bg-red-600/20 rounded-lg transition-all text-red-400"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          ))}
          
          <div className="mt-4 text-center text-sm text-gray-500">
            Total: {contexts.length} contexts
          </div>
        </div>
      )}

      {/* Add Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50">
          <div className="bg-gray-800 rounded-xl p-6 w-full max-w-md border border-gray-700">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold">Add New Context</h2>
              <button onClick={() => { setShowAddModal(false); resetForm(); }} className="text-gray-400 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm text-gray-400 mb-1">Key (e.g., "Partex timber")</label>
                <input
                  type="text"
                  value={formKey}
                  onChange={(e) => setFormKey(e.target.value)}
                  className="w-full bg-gray-900 border border-gray-700 rounded-lg p-2"
                  placeholder="Enter context key"
                />
              </div>
              
              <div>
                <label className="block text-sm text-gray-400 mb-1">Value (e.g., "৳1,200 per cft")</label>
                <input
                  type="text"
                  value={formValue}
                  onChange={(e) => setFormValue(e.target.value)}
                  className="w-full bg-gray-900 border border-gray-700 rounded-lg p-2"
                  placeholder="Enter context value"
                />
              </div>
              
              <div>
                <label className="block text-sm text-gray-400 mb-1">Category</label>
                <select
                  value={formCategory}
                  onChange={(e) => setFormCategory(e.target.value)}
                  className="w-full bg-gray-900 border border-gray-700 rounded-lg p-2"
                >
                  <option value="market_price">Market Price</option>
                  <option value="labour">Labour</option>
                  <option value="transport">Transport</option>
                  <option value="construction">Construction</option>
                  <option value="general">General</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm text-gray-400 mb-1">Location</label>
                <input
                  type="text"
                  value={formLocation}
                  onChange={(e) => setFormLocation(e.target.value)}
                  className="w-full bg-gray-900 border border-gray-700 rounded-lg p-2"
                  placeholder="e.g., Sakhipur, Partex"
                />
              </div>
              
              <button
                onClick={handleAddContext}
                className="w-full bg-green-600 hover:bg-green-700 py-2 rounded-lg font-semibold"
              >
                Save Context
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
