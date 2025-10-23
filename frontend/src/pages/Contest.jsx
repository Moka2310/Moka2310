import React, { useState, useEffect } from 'react';
import { Trophy, TrendingUp, Calendar } from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';
import { t } from '../translations';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const Contest = () => {
  const { language } = useLanguage();
  const [participants, setParticipants] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadParticipants();
  }, []);

  const loadParticipants = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/trading-contest/participants`);
      const data = await response.json();
      setParticipants(data);
    } catch (error) {
      console.error('Error loading participants:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString(language === 'fr' ? 'fr-FR' : 'en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const getRankColor = (rank) => {
    if (rank === 1) return 'text-yellow-400';
    if (rank === 2) return 'text-gray-300';
    if (rank === 3) return 'text-orange-400';
    return 'text-white';
  };

  const getRankBadge = (rank) => {
    if (rank === 1) return '🥇';
    if (rank === 2) return '🥈';
    if (rank === 3) return '🥉';
    return `#${rank}`;
  };

  return (
    <div className="min-h-screen bg-[#1E1540] pt-24 pb-16 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-block bg-gradient-to-r from-yellow-400 to-orange-500 text-white text-xs font-bold px-4 py-1.5 rounded-full mb-4">
            <Trophy className="w-4 h-4 inline mr-1" />
            {language === 'fr' ? 'CONCOURS EN COURS' : 'ONGOING CONTEST'}
          </div>
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-400">
              {t(language, 'contest.title')}
            </span>
          </h1>
          <p className="text-white/70 text-lg max-w-2xl mx-auto">
            {t(language, 'contest.subtitle')}
          </p>
        </div>

        {/* Loading State */}
        {loading ? (
          <div className="text-center text-white/60 py-12">
            <div className="inline-block w-12 h-12 border-4 border-pink-500/30 border-t-pink-500 rounded-full animate-spin mb-4"></div>
            <p>{language === 'fr' ? 'Chargement...' : 'Loading...'}</p>
          </div>
        ) : participants.length === 0 ? (
          /* No Participants */
          <div className="text-center text-white/60 py-12">
            <Trophy className="w-16 h-16 mx-auto mb-4 text-white/30" />
            <p className="text-lg">{t(language, 'contest.noParticipants')}</p>
          </div>
        ) : (
          /* Contest Table */
          <div className="bg-gradient-to-br from-[#2B1F5C] to-[#1E1540] rounded-3xl p-6 md:p-8 border border-purple-500/30 overflow-hidden">
            {/* Desktop Table */}
            <div className="hidden md:block overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-purple-500/30">
                    <th className="text-left text-white/80 font-semibold py-4 px-4">
                      {t(language, 'contest.table.rank')}
                    </th>
                    <th className="text-left text-white/80 font-semibold py-4 px-4">
                      {t(language, 'contest.table.name')}
                    </th>
                    <th className="text-center text-white/80 font-semibold py-4 px-4">
                      {t(language, 'contest.table.totalTrades')}
                    </th>
                    <th className="text-center text-white/80 font-semibold py-4 px-4">
                      {t(language, 'contest.table.winningTrades')}
                    </th>
                    <th className="text-center text-white/80 font-semibold py-4 px-4">
                      {t(language, 'contest.table.winRate')}
                    </th>
                    <th className="text-center text-white/80 font-semibold py-4 px-4">
                      {t(language, 'contest.table.date')}
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {participants.map((participant, index) => (
                    <tr 
                      key={participant.id}
                      className={`border-b border-purple-500/10 hover:bg-purple-500/5 transition-colors ${
                        index < 3 ? 'bg-purple-500/5' : ''
                      }`}
                    >
                      <td className="py-4 px-4">
                        <div className={`text-2xl font-bold ${getRankColor(participant.rank)}`}>
                          {getRankBadge(participant.rank)}
                        </div>
                      </td>
                      <td className="py-4 px-4">
                        <div className="flex items-center gap-3">
                          <div className="w-10 h-10 bg-gradient-to-br from-pink-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold">
                            {participant.firstName.charAt(0)}{participant.lastName.charAt(0)}
                          </div>
                          <div>
                            <div className="text-white font-semibold">
                              {participant.firstName} {participant.lastName}
                            </div>
                          </div>
                        </div>
                      </td>
                      <td className="py-4 px-4 text-center text-white font-medium">
                        {participant.totalTrades}
                      </td>
                      <td className="py-4 px-4 text-center text-green-400 font-medium">
                        {participant.winningTrades}
                      </td>
                      <td className="py-4 px-4 text-center">
                        <div className="inline-flex items-center gap-2 bg-green-500/20 px-3 py-1 rounded-full">
                          <TrendingUp className="w-4 h-4 text-green-400" />
                          <span className="text-green-400 font-bold">{participant.winRate}%</span>
                        </div>
                      </td>
                      <td className="py-4 px-4 text-center text-white/60 text-sm">
                        <Calendar className="w-4 h-4 inline mr-1" />
                        {formatDate(participant.date)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Mobile Cards */}
            <div className="md:hidden space-y-4">
              {participants.map((participant, index) => (
                <div 
                  key={participant.id}
                  className={`bg-purple-500/10 rounded-xl p-4 border ${
                    index < 3 ? 'border-yellow-500/30 bg-yellow-500/5' : 'border-purple-500/20'
                  }`}
                >
                  <div className="flex items-center justify-between mb-3">
                    <div className={`text-3xl font-bold ${getRankColor(participant.rank)}`}>
                      {getRankBadge(participant.rank)}
                    </div>
                    <div className="inline-flex items-center gap-2 bg-green-500/20 px-3 py-1 rounded-full">
                      <TrendingUp className="w-4 h-4 text-green-400" />
                      <span className="text-green-400 font-bold">{participant.winRate}%</span>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-3 mb-3">
                    <div className="w-12 h-12 bg-gradient-to-br from-pink-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-lg">
                      {participant.firstName.charAt(0)}{participant.lastName.charAt(0)}
                    </div>
                    <div>
                      <div className="text-white font-semibold text-lg">
                        {participant.firstName} {participant.lastName}
                      </div>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-3 text-sm">
                    <div>
                      <div className="text-white/60 mb-1">{t(language, 'contest.table.totalTrades')}</div>
                      <div className="text-white font-semibold">{participant.totalTrades}</div>
                    </div>
                    <div>
                      <div className="text-white/60 mb-1">{t(language, 'contest.table.winningTrades')}</div>
                      <div className="text-green-400 font-semibold">{participant.winningTrades}</div>
                    </div>
                    <div className="col-span-2">
                      <div className="text-white/60 mb-1">{t(language, 'contest.table.date')}</div>
                      <div className="text-white/80 text-sm">
                        <Calendar className="w-3 h-3 inline mr-1" />
                        {formatDate(participant.date)}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Contest;
