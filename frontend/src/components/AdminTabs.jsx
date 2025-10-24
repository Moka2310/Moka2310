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
  X,
  Bot,
  Gift,
  Image as ImageIcon,
  Link as LinkIcon,
  Eye,
  EyeOff
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

// Onglet Membres
const MembersTab = ({ language }) => {
  const [members, setMembers] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadMembers();
    loadStats();
  }, []);

  const loadMembers = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/members/all`, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('tradalife_token')}` }
      });
      const data = await response.json();
      setMembers(data.members);
    } catch (error) {
      console.error('Error loading members:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadStats = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/members/stats`, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('tradalife_token')}` }
      });
      const data = await response.json();
      setStats(data);
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  };

  const filteredMembers = members.filter(m => 
    m.firstName.toLowerCase().includes(searchTerm.toLowerCase()) ||
    m.lastName.toLowerCase().includes(searchTerm.toLowerCase()) ||
    m.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString(language === 'fr' ? 'fr-FR' : 'en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  return (
    <div className="space-y-6">
      {/* Stats Cards */}
      {stats && (
        <div className="grid md:grid-cols-4 gap-4">
          <div className="bg-gradient-to-br from-blue-500/20 to-purple-500/20 rounded-xl p-4 border border-blue-500/30">
            <div className="text-blue-400 text-sm mb-1">{language === 'fr' ? 'Total Membres' : 'Total Members'}</div>
            <div className="text-3xl font-bold text-white">{stats.total_users}</div>
          </div>
          <div className="bg-gradient-to-br from-green-500/20 to-emerald-500/20 rounded-xl p-4 border border-green-500/30">
            <div className="text-green-400 text-sm mb-1">{language === 'fr' ? 'Utilisateurs' : 'Users'}</div>
            <div className="text-3xl font-bold text-white">{stats.regular_users}</div>
          </div>
          <div className="bg-gradient-to-br from-yellow-500/20 to-orange-500/20 rounded-xl p-4 border border-yellow-500/30">
            <div className="text-yellow-400 text-sm mb-1">KYC {language === 'fr' ? 'En attente' : 'Pending'}</div>
            <div className="text-3xl font-bold text-white">{stats.kyc_stats.pending}</div>
          </div>
          <div className="bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-xl p-4 border border-purple-500/30">
            <div className="text-purple-400 text-sm mb-1">Admins</div>
            <div className="text-3xl font-bold text-white">{stats.admins}</div>
          </div>
        </div>
      )}

      {/* Members List */}
      <div className="bg-gradient-to-br from-[#2B1F5C] to-[#1E1540] rounded-3xl p-6 md:p-8 border border-purple-500/30">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-white">
            {language === 'fr' ? 'Liste des Membres' : 'Members List'}
          </h2>
          <div className="text-white/60">
            {filteredMembers.length} {language === 'fr' ? 'membres' : 'members'}
          </div>
        </div>

        {/* Search */}
        <div className="mb-4">
          <input
            type="text"
            placeholder={language === 'fr' ? 'Rechercher par nom ou email...' : 'Search by name or email...'}
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full bg-white/10 border border-purple-500/30 rounded-lg px-4 py-2 text-white placeholder-white/50"
          />
        </div>

        {loading ? (
          <div className="text-center text-white/60 py-8">Chargement...</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-purple-500/30">
                  <th className="text-left text-white/80 py-3 px-4">{language === 'fr' ? 'Nom' : 'Name'}</th>
                  <th className="text-left text-white/80 py-3 px-4">Email</th>
                  <th className="text-center text-white/80 py-3 px-4">KYC</th>
                  <th className="text-center text-white/80 py-3 px-4">{language === 'fr' ? 'Rôle' : 'Role'}</th>
                  <th className="text-center text-white/80 py-3 px-4">{language === 'fr' ? 'Inscription' : 'Registered'}</th>
                </tr>
              </thead>
              <tbody>
                {filteredMembers.map((member) => (
                  <tr key={member.id} className="border-b border-purple-500/10 hover:bg-purple-500/5">
                    <td className="py-3 px-4 text-white">
                      {member.firstName} {member.lastName}
                    </td>
                    <td className="py-3 px-4 text-white/70 text-sm">{member.email}</td>
                    <td className="py-3 px-4 text-center">
                      <span className={`px-2 py-1 rounded-full text-xs ${
                        member.kycStatus === 'approved' ? 'bg-green-500/20 text-green-400' :
                        member.kycStatus === 'pending_review' ? 'bg-yellow-500/20 text-yellow-400' :
                        member.kycStatus === 'rejected' ? 'bg-red-500/20 text-red-400' :
                        'bg-gray-500/20 text-gray-400'
                      }`}>
                        {member.kycStatus === 'approved' ? '✓' : 
                         member.kycStatus === 'pending_review' ? '⏱' :
                         member.kycStatus === 'rejected' ? '✗' : '-'}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-center">
                      <span className={`px-2 py-1 rounded-full text-xs ${
                        member.role === 'admin' ? 'bg-purple-500/20 text-purple-400' : 'bg-blue-500/20 text-blue-400'
                      }`}>
                        {member.role}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-center text-white/60 text-sm">
                      {formatDate(member.createdAt)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

// Onglet Abonnements
const SubscriptionsTab = ({ language }) => {
  const [subscriptions, setSubscriptions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadSubscriptions();
  }, []);

  const loadSubscriptions = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/subscriptions/admin/all`, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('tradalife_token')}` }
      });
      const data = await response.json();
      setSubscriptions(data);
    } catch (error) {
      console.error('Error loading subscriptions:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString(language === 'fr' ? 'fr-FR' : 'en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getPaymentMethodBadge = (method) => {
    if (method === 'stripe') {
      return <span className="bg-blue-500/20 text-blue-400 px-2 py-1 rounded-full text-xs">💳 Stripe</span>;
    } else if (method === 'paypal') {
      return <span className="bg-yellow-500/20 text-yellow-400 px-2 py-1 rounded-full text-xs">🅿️ PayPal</span>;
    }
    return <span className="bg-gray-500/20 text-gray-400 px-2 py-1 rounded-full text-xs">{method}</span>;
  };

  const getStatusBadge = (status) => {
    const statusConfig = {
      active: { color: 'green', text: language === 'fr' ? 'Actif' : 'Active', icon: '✓' },
      canceled: { color: 'red', text: language === 'fr' ? 'Annulé' : 'Canceled', icon: '✗' },
      past_due: { color: 'orange', text: language === 'fr' ? 'En retard' : 'Past Due', icon: '⚠' }
    };
    const config = statusConfig[status] || { color: 'gray', text: status, icon: '?' };
    return (
      <span className={`bg-${config.color}-500/20 text-${config.color}-400 px-2 py-1 rounded-full text-xs`}>
        {config.icon} {config.text}
      </span>
    );
  };

  return (
    <div className="bg-gradient-to-br from-[#2B1F5C] to-[#1E1540] rounded-3xl p-6 md:p-8 border border-purple-500/30">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-white">
          {language === 'fr' ? 'Abonnements' : 'Subscriptions'}
        </h2>
        <div className="text-white/60">
          {subscriptions.length} {language === 'fr' ? 'abonnements' : 'subscriptions'}
        </div>
      </div>

      {loading ? (
        <div className="text-center text-white/60 py-8">Chargement...</div>
      ) : subscriptions.length === 0 ? (
        <div className="text-center text-white/60 py-8">
          {language === 'fr' ? 'Aucun abonnement' : 'No subscriptions'}
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-purple-500/30">
                <th className="text-left text-white/80 py-3 px-4">Email</th>
                <th className="text-center text-white/80 py-3 px-4">{language === 'fr' ? 'Méthode' : 'Method'}</th>
                <th className="text-center text-white/80 py-3 px-4">{language === 'fr' ? 'Statut' : 'Status'}</th>
                <th className="text-center text-white/80 py-3 px-4">{language === 'fr' ? 'Prix' : 'Price'}</th>
                <th className="text-center text-white/80 py-3 px-4">{language === 'fr' ? 'Date' : 'Date'}</th>
              </tr>
            </thead>
            <tbody>
              {subscriptions.map((sub) => (
                <tr key={sub.id} className="border-b border-purple-500/10 hover:bg-purple-500/5">
                  <td className="py-3 px-4 text-white text-sm">{sub.userEmail}</td>
                  <td className="py-3 px-4 text-center">
                    {getPaymentMethodBadge(sub.paymentMethod)}
                  </td>
                  <td className="py-3 px-4 text-center">
                    {getStatusBadge(sub.status)}
                  </td>
                  <td className="py-3 px-4 text-center text-green-400 font-bold">
                    {sub.pricePerMonth}$ CAD
                  </td>
                  <td className="py-3 px-4 text-center text-white/60 text-sm">
                    {formatDate(sub.createdAt)}
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

// Onglet Pré-commandes Bot
const BotPreordersTab = ({ language }) => {
  const [preorders, setPreorders] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadPreorders();
  }, []);

  const loadPreorders = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/bot-preorders/admin/all`, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('tradalife_token')}` }
      });
      const data = await response.json();
      setPreorders(data.preorders);
      setStats(data.stats);
    } catch (error) {
      console.error('Error loading preorders:', error);
      toast({
        title: '❌ Erreur',
        description: 'Impossible de charger les pré-commandes',
        variant: 'destructive'
      });
    } finally {
      setLoading(false);
    }
  };

  const filteredPreorders = preorders.filter(p => 
    p.userEmail.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString(language === 'fr' ? 'fr-FR' : 'en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getStatusBadge = (status) => {
    const statusConfig = {
      paid: { color: 'green', text: language === 'fr' ? 'Payé' : 'Paid', icon: '✓' },
      pending_payment: { color: 'yellow', text: language === 'fr' ? 'En attente' : 'Pending', icon: '⏱' },
      delivered: { color: 'blue', text: language === 'fr' ? 'Livré' : 'Delivered', icon: '📦' },
      canceled: { color: 'red', text: language === 'fr' ? 'Annulé' : 'Canceled', icon: '✗' }
    };
    const config = statusConfig[status] || { color: 'gray', text: status, icon: '?' };
    return (
      <span className={`bg-${config.color}-500/20 text-${config.color}-400 px-2 py-1 rounded-full text-xs font-medium`}>
        {config.icon} {config.text}
      </span>
    );
  };

  const getPaymentMethodBadge = (method) => {
    if (method === 'stripe') {
      return <span className="bg-blue-500/20 text-blue-400 px-2 py-1 rounded-full text-xs">💳 Stripe</span>;
    } else if (method === 'paypal') {
      return <span className="bg-yellow-500/20 text-yellow-400 px-2 py-1 rounded-full text-xs">🅿️ PayPal</span>;
    }
    return <span className="bg-gray-500/20 text-gray-400 px-2 py-1 rounded-full text-xs">{method}</span>;
  };

  return (
    <div className="space-y-6">
      {/* Stats Cards */}
      {stats && (
        <div className="grid md:grid-cols-4 gap-4">
          <div className="bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-xl p-4 border border-purple-500/30">
            <div className="text-purple-400 text-sm mb-1">
              {language === 'fr' ? 'Total Pré-commandes' : 'Total Preorders'}
            </div>
            <div className="text-3xl font-bold text-white">{stats.total}</div>
          </div>
          <div className="bg-gradient-to-br from-green-500/20 to-emerald-500/20 rounded-xl p-4 border border-green-500/30">
            <div className="text-green-400 text-sm mb-1">
              {language === 'fr' ? 'Payées' : 'Paid'}
            </div>
            <div className="text-3xl font-bold text-white">{stats.paid}</div>
          </div>
          <div className="bg-gradient-to-br from-yellow-500/20 to-orange-500/20 rounded-xl p-4 border border-yellow-500/30">
            <div className="text-yellow-400 text-sm mb-1">
              {language === 'fr' ? 'En attente' : 'Pending'}
            </div>
            <div className="text-3xl font-bold text-white">{stats.pending}</div>
          </div>
          <div className="bg-gradient-to-br from-blue-500/20 to-cyan-500/20 rounded-xl p-4 border border-blue-500/30">
            <div className="text-blue-400 text-sm mb-1">
              {language === 'fr' ? 'Revenu Total' : 'Total Revenue'}
            </div>
            <div className="text-3xl font-bold text-white">{stats.revenue.toFixed(2)}$ CAD</div>
          </div>
        </div>
      )}

      {/* Preorders List */}
      <div className="bg-gradient-to-br from-[#2B1F5C] to-[#1E1540] rounded-3xl p-6 md:p-8 border border-purple-500/30">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <Bot className="w-8 h-8 text-pink-400" />
            <h2 className="text-2xl font-bold text-white">
              {language === 'fr' ? 'Pré-commandes Bot' : 'Bot Preorders'}
            </h2>
          </div>
          <div className="text-white/60">
            {filteredPreorders.length} {language === 'fr' ? 'pré-commandes' : 'preorders'}
          </div>
        </div>

        {/* Search */}
        <div className="mb-4">
          <input
            type="text"
            placeholder={language === 'fr' ? 'Rechercher par email...' : 'Search by email...'}
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full bg-white/10 border border-purple-500/30 rounded-lg px-4 py-2 text-white placeholder-white/50"
          />
        </div>

        {loading ? (
          <div className="text-center text-white/60 py-8">
            {language === 'fr' ? 'Chargement...' : 'Loading...'}
          </div>
        ) : filteredPreorders.length === 0 ? (
          <div className="text-center text-white/60 py-8">
            {language === 'fr' ? 'Aucune pré-commande' : 'No preorders'}
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-purple-500/30">
                  <th className="text-left text-white/80 py-3 px-4">Email</th>
                  <th className="text-center text-white/80 py-3 px-4">
                    {language === 'fr' ? 'Méthode' : 'Method'}
                  </th>
                  <th className="text-center text-white/80 py-3 px-4">
                    {language === 'fr' ? 'Statut' : 'Status'}
                  </th>
                  <th className="text-center text-white/80 py-3 px-4">
                    {language === 'fr' ? 'Prix' : 'Price'}
                  </th>
                  <th className="text-center text-white/80 py-3 px-4">
                    {language === 'fr' ? 'Date' : 'Date'}
                  </th>
                </tr>
              </thead>
              <tbody>
                {filteredPreorders.map((preorder) => (
                  <tr key={preorder.id} className="border-b border-purple-500/10 hover:bg-purple-500/5">
                    <td className="py-3 px-4 text-white text-sm">{preorder.userEmail}</td>
                    <td className="py-3 px-4 text-center">
                      {getPaymentMethodBadge(preorder.paymentMethod)}
                    </td>
                    <td className="py-3 px-4 text-center">
                      {getStatusBadge(preorder.status)}
                    </td>
                    <td className="py-3 px-4 text-center text-green-400 font-bold">
                      {preorder.price}$ CAD
                    </td>
                    <td className="py-3 px-4 text-center text-white/60 text-sm">
                      {formatDate(preorder.createdAt)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

// Onglet Gestion des Annonces Bonus
const BonusManagementTab = ({ language }) => {
  const [announcements, setAnnouncements] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [formData, setFormData] = useState({
    titleFr: '',
    titleEn: '',
    descriptionFr: '',
    descriptionEn: '',
    imageUrl: '',
    linkUrl: '',
    order: 0
  });

  useEffect(() => {
    loadAnnouncements();
  }, []);

  const loadAnnouncements = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/bonus-announcements/admin/all`, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('tradalife_token')}` }
      });
      const data = await response.json();
      setAnnouncements(data);
    } catch (error) {
      console.error('Error loading announcements:', error);
      toast({
        title: '❌ Erreur',
        description: 'Impossible de charger les annonces',
        variant: 'destructive'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const url = editingId 
        ? `${BACKEND_URL}/api/bonus-announcements/admin/update/${editingId}`
        : `${BACKEND_URL}/api/bonus-announcements/admin/create`;
      
      const method = editingId ? 'PUT' : 'POST';
      
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('tradalife_token')}`
        },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        toast({
          title: '✅ Succès',
          description: editingId ? 'Annonce mise à jour' : 'Annonce créée',
        });
        resetForm();
        loadAnnouncements();
      } else {
        throw new Error('Failed to save announcement');
      }
    } catch (error) {
      console.error('Error saving announcement:', error);
      toast({
        title: '❌ Erreur',
        description: 'Impossible de sauvegarder l\'annonce',
        variant: 'destructive'
      });
    }
  };

  const handleEdit = (announcement) => {
    setFormData({
      titleFr: announcement.titleFr,
      titleEn: announcement.titleEn,
      descriptionFr: announcement.descriptionFr || '',
      descriptionEn: announcement.descriptionEn || '',
      imageUrl: announcement.imageUrl,
      linkUrl: announcement.linkUrl || '',
      order: announcement.order
    });
    setEditingId(announcement.id);
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Êtes-vous sûr de vouloir supprimer cette annonce?')) return;

    try {
      const response = await fetch(`${BACKEND_URL}/api/bonus-announcements/admin/delete/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${localStorage.getItem('tradalife_token')}` }
      });

      if (response.ok) {
        toast({
          title: '✅ Succès',
          description: 'Annonce supprimée',
        });
        loadAnnouncements();
      }
    } catch (error) {
      console.error('Error deleting announcement:', error);
      toast({
        title: '❌ Erreur',
        description: 'Impossible de supprimer l\'annonce',
        variant: 'destructive'
      });
    }
  };

  const handleToggle = async (id) => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/bonus-announcements/admin/toggle/${id}`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${localStorage.getItem('tradalife_token')}` }
      });

      if (response.ok) {
        toast({
          title: '✅ Succès',
          description: 'Statut mis à jour',
        });
        loadAnnouncements();
      }
    } catch (error) {
      console.error('Error toggling announcement:', error);
      toast({
        title: '❌ Erreur',
        description: 'Impossible de changer le statut',
        variant: 'destructive'
      });
    }
  };

  const resetForm = () => {
    setFormData({
      titleFr: '',
      titleEn: '',
      descriptionFr: '',
      descriptionEn: '',
      imageUrl: '',
      linkUrl: '',
      order: 0
    });
    setEditingId(null);
    setShowForm(false);
  };

  return (
    <div className="space-y-6">
      {/* Header with Add Button */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Gift className="w-8 h-8 text-pink-400" />
          <h2 className="text-2xl font-bold text-white">
            {language === 'fr' ? 'Gestion des Annonces Bonus' : 'Bonus Announcements Management'}
          </h2>
        </div>
        {!showForm && (
          <Button
            onClick={() => setShowForm(true)}
            className="bg-gradient-to-r from-pink-500 to-purple-600"
          >
            <Plus className="w-4 h-4 mr-2" />
            {language === 'fr' ? 'Nouvelle annonce' : 'New announcement'}
          </Button>
        )}
      </div>

      {/* Form */}
      {showForm && (
        <div className="bg-gradient-to-br from-[#2B1F5C] to-[#1E1540] rounded-3xl p-6 border border-purple-500/30">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl font-bold text-white">
              {editingId 
                ? (language === 'fr' ? 'Modifier l\'annonce' : 'Edit announcement')
                : (language === 'fr' ? 'Nouvelle annonce' : 'New announcement')}
            </h3>
            <button onClick={resetForm} className="text-white/60 hover:text-white">
              <X className="w-6 h-6" />
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <label className="text-white/80 text-sm mb-2 block">Titre (FR) *</label>
                <input
                  type="text"
                  required
                  value={formData.titleFr}
                  onChange={(e) => setFormData({...formData, titleFr: e.target.value})}
                  className="w-full bg-white/10 border border-purple-500/30 rounded-lg px-4 py-2 text-white"
                />
              </div>
              <div>
                <label className="text-white/80 text-sm mb-2 block">Title (EN) *</label>
                <input
                  type="text"
                  required
                  value={formData.titleEn}
                  onChange={(e) => setFormData({...formData, titleEn: e.target.value})}
                  className="w-full bg-white/10 border border-purple-500/30 rounded-lg px-4 py-2 text-white"
                />
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <label className="text-white/80 text-sm mb-2 block">Description (FR)</label>
                <Textarea
                  value={formData.descriptionFr}
                  onChange={(e) => setFormData({...formData, descriptionFr: e.target.value})}
                  className="w-full bg-white/10 border border-purple-500/30 rounded-lg px-4 py-2 text-white min-h-[100px]"
                />
              </div>
              <div>
                <label className="text-white/80 text-sm mb-2 block">Description (EN)</label>
                <Textarea
                  value={formData.descriptionEn}
                  onChange={(e) => setFormData({...formData, descriptionEn: e.target.value})}
                  className="w-full bg-white/10 border border-purple-500/30 rounded-lg px-4 py-2 text-white min-h-[100px]"
                />
              </div>
            </div>

            <div>
              <label className="text-white/80 text-sm mb-2 block flex items-center gap-2">
                <ImageIcon className="w-4 h-4" />
                URL de l'image *
              </label>
              <input
                type="url"
                required
                value={formData.imageUrl}
                onChange={(e) => setFormData({...formData, imageUrl: e.target.value})}
                placeholder="https://..."
                className="w-full bg-white/10 border border-purple-500/30 rounded-lg px-4 py-2 text-white"
              />
            </div>

            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <label className="text-white/80 text-sm mb-2 block flex items-center gap-2">
                  <LinkIcon className="w-4 h-4" />
                  Lien (optionnel)
                </label>
                <input
                  type="url"
                  value={formData.linkUrl}
                  onChange={(e) => setFormData({...formData, linkUrl: e.target.value})}
                  placeholder="https://..."
                  className="w-full bg-white/10 border border-purple-500/30 rounded-lg px-4 py-2 text-white"
                />
              </div>
              <div>
                <label className="text-white/80 text-sm mb-2 block">Ordre d'affichage</label>
                <input
                  type="number"
                  value={formData.order}
                  onChange={(e) => setFormData({...formData, order: parseInt(e.target.value)})}
                  className="w-full bg-white/10 border border-purple-500/30 rounded-lg px-4 py-2 text-white"
                />
              </div>
            </div>

            <div className="flex gap-4 justify-end">
              <Button
                type="button"
                onClick={resetForm}
                className="bg-white/10"
              >
                Annuler
              </Button>
              <Button
                type="submit"
                className="bg-gradient-to-r from-pink-500 to-purple-600"
              >
                <Save className="w-4 h-4 mr-2" />
                {editingId ? 'Mettre à jour' : 'Créer'}
              </Button>
            </div>
          </form>
        </div>
      )}

      {/* Announcements List */}
      <div className="bg-gradient-to-br from-[#2B1F5C] to-[#1E1540] rounded-3xl p-6 border border-purple-500/30">
        {loading ? (
          <div className="text-center text-white/60 py-8">Chargement...</div>
        ) : announcements.length === 0 ? (
          <div className="text-center text-white/60 py-8">
            {language === 'fr' ? 'Aucune annonce' : 'No announcements'}
          </div>
        ) : (
          <div className="space-y-4">
            {announcements.map((announcement) => (
              <div
                key={announcement.id}
                className="bg-white/5 rounded-2xl p-4 border border-purple-500/20 hover:border-purple-500/40 transition-all"
              >
                <div className="flex gap-4">
                  {/* Image */}
                  <div className="w-32 h-32 rounded-xl overflow-hidden flex-shrink-0">
                    <img
                      src={announcement.imageUrl}
                      alt={announcement.titleFr}
                      className="w-full h-full object-cover"
                    />
                  </div>

                  {/* Content */}
                  <div className="flex-1">
                    <div className="flex items-start justify-between mb-2">
                      <div>
                        <h4 className="text-white font-semibold text-lg">{announcement.titleFr}</h4>
                        <p className="text-white/60 text-sm">{announcement.titleEn}</p>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                          announcement.isActive 
                            ? 'bg-green-500/20 text-green-400'
                            : 'bg-red-500/20 text-red-400'
                        }`}>
                          {announcement.isActive ? (language === 'fr' ? 'Actif' : 'Active') : (language === 'fr' ? 'Inactif' : 'Inactive')}
                        </span>
                        <span className="px-3 py-1 rounded-full text-xs font-medium bg-blue-500/20 text-blue-400">
                          Ordre: {announcement.order}
                        </span>
                      </div>
                    </div>

                    {announcement.descriptionFr && (
                      <p className="text-white/70 text-sm mb-3 line-clamp-2">
                        {announcement.descriptionFr}
                      </p>
                    )}

                    {announcement.linkUrl && (
                      <a
                        href={announcement.linkUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-pink-400 text-sm flex items-center gap-1 mb-3"
                      >
                        <ExternalLink className="w-4 h-4" />
                        {announcement.linkUrl}
                      </a>
                    )}

                    {/* Actions */}
                    <div className="flex gap-2">
                      <button
                        onClick={() => handleToggle(announcement.id)}
                        className="px-3 py-1 bg-blue-500/20 text-blue-400 rounded-lg text-sm hover:bg-blue-500/30 transition-all flex items-center gap-1"
                      >
                        {announcement.isActive ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                        {announcement.isActive ? (language === 'fr' ? 'Masquer' : 'Hide') : (language === 'fr' ? 'Afficher' : 'Show')}
                      </button>
                      <button
                        onClick={() => handleEdit(announcement)}
                        className="px-3 py-1 bg-yellow-500/20 text-yellow-400 rounded-lg text-sm hover:bg-yellow-500/30 transition-all flex items-center gap-1"
                      >
                        <Edit2 className="w-4 h-4" />
                        {language === 'fr' ? 'Modifier' : 'Edit'}
                      </button>
                      <button
                        onClick={() => handleDelete(announcement.id)}
                        className="px-3 py-1 bg-red-500/20 text-red-400 rounded-lg text-sm hover:bg-red-500/30 transition-all flex items-center gap-1"
                      >
                        <Trash2 className="w-4 h-4" />
                        {language === 'fr' ? 'Supprimer' : 'Delete'}
                      </button>
                    </div>
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

export { StatsTab, ContestTab, MembersTab, SubscriptionsTab, BotPreordersTab, BonusManagementTab };
