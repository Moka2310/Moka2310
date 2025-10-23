import React, { useState, useEffect } from 'react';
import { Button } from './ui/button';
import { Textarea } from './ui/textarea';
import { toast } from '../hooks/use-toast';
import { useLanguage } from '../contexts/LanguageContext';
import { t } from '../translations';
import { 
  BarChart3, 
  Trophy, 
  UserCheck, 
  ExternalLink, 
  Plus, 
  Trash2, 
  Edit2,
  Save,
  X
} from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

// Onglet Statistiques
const StatsTab = ({ language }) => {
  return (
    <div className="bg-gradient-to-br from-[#2B1F5C] to-[#1E1540] rounded-3xl p-6 md:p-8 border border-purple-500/30">
      <div className="flex items-center gap-3 mb-6">
        <BarChart3 className="w-8 h-8 text-pink-400" />
        <h2 className="text-2xl font-bold text-white">
          {t(language, 'admin.analytics.title')}
        </h2>
      </div>

      <div className="bg-blue-500/10 border border-blue-500/30 rounded-xl p-6 mb-6">
        <p className="text-white/80 mb-4">
          {t(language, 'admin.analytics.info')}
        </p>
        
        <Button
          onClick={() => window.open('https://analytics.google.com', '_blank')}
          className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white"
        >
          <ExternalLink className="w-4 h-4 mr-2" />
          {t(language, 'admin.analytics.openGA')}
        </Button>
      </div>

      <div className="bg-white/5 rounded-xl p-6">
        <h3 className="text-white font-semibold mb-3">
          📊 {language === 'fr' ? 'Métriques Disponibles' : 'Available Metrics'}
        </h3>
        <ul className="text-white/70 space-y-2 text-sm">
          <li>✅ {language === 'fr' ? 'Visiteurs uniques' : 'Unique visitors'}</li>
          <li>✅ {language === 'fr' ? 'Pays d\'origine' : 'Countries of origin'}</li>
          <li>✅ {language === 'fr' ? 'Pages visitées' : 'Pages visited'}</li>
          <li>✅ {language === 'fr' ? 'Durée de session' : 'Session duration'}</li>
          <li>✅ {language === 'fr' ? 'Sources de trafic' : 'Traffic sources'}</li>
        </ul>
        <p className="text-yellow-400 text-xs mt-4">
          ⏱️ {language === 'fr' 
            ? 'Les données apparaissent après 24-48h' 
            : 'Data appears after 24-48h'}
        </p>
      </div>
    </div>
  );
};

// Onglet Gestion du Concours
const ContestTab = ({ language }) => {
  const [participants, setParticipants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    totalTrades: '',
    winningTrades: '',
    date: new Date().toISOString().split('T')[0]
  });

  useEffect(() => {
    loadParticipants();
  }, []);

  const loadParticipants = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/trading-contest/admin/all`, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('tradalife_token')}` }
      });
      const data = await response.json();
      setParticipants(data);
    } catch (error) {
      console.error('Error loading participants:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const url = editingId 
        ? `${BACKEND_URL}/api/trading-contest/admin/update/${editingId}`
        : `${BACKEND_URL}/api/trading-contest/admin/add`;
      
      const method = editingId ? 'PUT' : 'POST';
      
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('tradalife_token')}`
        },
        body: JSON.stringify({
          ...formData,
          totalTrades: parseInt(formData.totalTrades),
          winningTrades: parseInt(formData.winningTrades),
          date: new Date(formData.date).toISOString()
        })
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Erreur');
      }

      toast({
        title: '✅ ' + (editingId 
          ? t(language, 'admin.contestManagement.updateSuccess')
          : t(language, 'admin.contestManagement.addSuccess'))
      });

      setFormData({
        firstName: '',
        lastName: '',
        totalTrades: '',
        winningTrades: '',
        date: new Date().toISOString().split('T')[0]
      });
      setShowAddForm(false);
      setEditingId(null);
      loadParticipants();
    } catch (error) {
      toast({
        title: '❌ Erreur',
        description: error.message,
        variant: 'destructive'
      });
    }
  };

  const handleEdit = (participant) => {
    setFormData({
      firstName: participant.firstName,
      lastName: participant.lastName,
      totalTrades: participant.totalTrades.toString(),
      winningTrades: participant.winningTrades.toString(),
      date: new Date(participant.date).toISOString().split('T')[0]
    });
    setEditingId(participant.id);
    setShowAddForm(true);
  };

  const handleDelete = async (id) => {
    if (!confirm(language === 'fr' ? 'Supprimer ce participant?' : 'Delete this participant?')) {
      return;
    }

    try {
      const response = await fetch(`${BACKEND_URL}/api/trading-contest/admin/delete/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${localStorage.getItem('tradalife_token')}` }
      });

      if (!response.ok) throw new Error('Erreur de suppression');

      toast({
        title: '✅ ' + t(language, 'admin.contestManagement.deleteSuccess')
      });
      loadParticipants();
    } catch (error) {
      toast({
        title: '❌ Erreur',
        description: error.message,
        variant: 'destructive'
      });
    }
  };

  const cancelEdit = () => {
    setFormData({
      firstName: '',
      lastName: '',
      totalTrades: '',
      winningTrades: '',
      date: new Date().toISOString().split('T')[0]
    });
    setEditingId(null);
    setShowAddForm(false);
  };

  return (
    <div className="bg-gradient-to-br from-[#2B1F5C] to-[#1E1540] rounded-3xl p-6 md:p-8 border border-purple-500/30">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <Trophy className="w-8 h-8 text-yellow-400" />
          <h2 className="text-2xl font-bold text-white">
            {t(language, 'admin.contestManagement.title')}
          </h2>
        </div>
        
        {!showAddForm && (
          <Button
            onClick={() => setShowAddForm(true)}
            className="bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700"
          >
            <Plus className="w-4 h-4 mr-2" />
            {t(language, 'admin.contestManagement.addParticipant')}
          </Button>
        )}
      </div>

      {/* Formulaire d'ajout/modification */}
      {showAddForm && (
        <div className="bg-purple-500/10 border border-purple-500/30 rounded-xl p-6 mb-6">
          <h3 className="text-white font-semibold mb-4">
            {editingId 
              ? t(language, 'admin.contestManagement.edit')
              : t(language, 'admin.contestManagement.addParticipant')}
          </h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <label className="text-white/80 text-sm block mb-2">
                  {t(language, 'admin.contestManagement.firstName')} *
                </label>
                <input
                  type="text"
                  required
                  value={formData.firstName}
                  onChange={(e) => setFormData({...formData, firstName: e.target.value})}
                  className="w-full bg-white/10 border border-purple-500/30 rounded-lg px-4 py-2 text-white"
                />
              </div>
              <div>
                <label className="text-white/80 text-sm block mb-2">
                  {t(language, 'admin.contestManagement.lastName')} *
                </label>
                <input
                  type="text"
                  required
                  value={formData.lastName}
                  onChange={(e) => setFormData({...formData, lastName: e.target.value})}
                  className="w-full bg-white/10 border border-purple-500/30 rounded-lg px-4 py-2 text-white"
                />
              </div>
            </div>

            <div className="grid md:grid-cols-3 gap-4">
              <div>
                <label className="text-white/80 text-sm block mb-2">
                  {t(language, 'admin.contestManagement.totalTrades')} *
                </label>
                <input
                  type="number"
                  required
                  min="0"
                  value={formData.totalTrades}
                  onChange={(e) => setFormData({...formData, totalTrades: e.target.value})}
                  className="w-full bg-white/10 border border-purple-500/30 rounded-lg px-4 py-2 text-white"
                />
              </div>
              <div>
                <label className="text-white/80 text-sm block mb-2">
                  {t(language, 'admin.contestManagement.winningTrades')} *
                </label>
                <input
                  type="number"
                  required
                  min="0"
                  value={formData.winningTrades}
                  onChange={(e) => setFormData({...formData, winningTrades: e.target.value})}
                  className="w-full bg-white/10 border border-purple-500/30 rounded-lg px-4 py-2 text-white"
                />
              </div>
              <div>
                <label className="text-white/80 text-sm block mb-2">
                  {t(language, 'admin.contestManagement.date')} *
                </label>
                <input
                  type="date"
                  required
                  value={formData.date}
                  onChange={(e) => setFormData({...formData, date: e.target.value})}
                  className="w-full bg-white/10 border border-purple-500/30 rounded-lg px-4 py-2 text-white"
                />
              </div>
            </div>

            <div className="flex gap-3">
              <Button type="submit" className="bg-gradient-to-r from-green-500 to-emerald-600">
                <Save className="w-4 h-4 mr-2" />
                {t(language, 'admin.contestManagement.save')}
              </Button>
              <Button type="button" onClick={cancelEdit} variant="outline" className="text-white border-white/30">
                <X className="w-4 h-4 mr-2" />
                {t(language, 'admin.contestManagement.cancel')}
              </Button>
            </div>
          </form>
        </div>
      )}

      {/* Liste des participants */}
      {loading ? (
        <div className="text-center text-white/60 py-8">Chargement...</div>
      ) : participants.length === 0 ? (
        <div className="text-center text-white/60 py-8">
          {t(language, 'admin.contestManagement.noParticipants')}
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-purple-500/30">
                <th className="text-left text-white/80 py-3 px-4">#</th>
                <th className="text-left text-white/80 py-3 px-4">Nom</th>
                <th className="text-center text-white/80 py-3 px-4">Total</th>
                <th className="text-center text-white/80 py-3 px-4">Gagnants</th>
                <th className="text-center text-white/80 py-3 px-4">%</th>
                <th className="text-center text-white/80 py-3 px-4">Actions</th>
              </tr>
            </thead>
            <tbody>
              {participants.map((p) => (
                <tr key={p.id} className="border-b border-purple-500/10 hover:bg-purple-500/5">
                  <td className="py-3 px-4">
                    <span className="text-yellow-400 font-bold">#{p.rank}</span>
                  </td>
                  <td className="py-3 px-4 text-white">
                    {p.firstName} {p.lastName}
                  </td>
                  <td className="py-3 px-4 text-center text-white">{p.totalTrades}</td>
                  <td className="py-3 px-4 text-center text-green-400">{p.winningTrades}</td>
                  <td className="py-3 px-4 text-center">
                    <span className="text-green-400 font-bold">{p.winRate}%</span>
                  </td>
                  <td className="py-3 px-4">
                    <div className="flex items-center justify-center gap-2">
                      <Button
                        onClick={() => handleEdit(p)}
                        size="sm"
                        className="bg-blue-500 hover:bg-blue-600"
                      >
                        <Edit2 className="w-3 h-3" />
                      </Button>
                      <Button
                        onClick={() => handleDelete(p.id)}
                        size="sm"
                        variant="destructive"
                      >
                        <Trash2 className="w-3 h-3" />
                      </Button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export { StatsTab, ContestTab };
