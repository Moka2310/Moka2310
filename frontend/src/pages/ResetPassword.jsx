import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams, Link } from 'react-router-dom';
import { Lock, Check, ArrowLeft } from 'lucide-react';

const ResetPassword = () => {
  const [searchParams] = useSearchParams();
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const token = searchParams.get('token');
  const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

  useEffect(() => {
    if (!token) {
      setError('Token manquant. Veuillez utiliser le lien envoyé par email.');
    }
  }, [token]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    // Validation
    if (password.length < 6) {
      setError('Le mot de passe doit contenir au moins 6 caractères');
      return;
    }

    if (password !== confirmPassword) {
      setError('Les mots de passe ne correspondent pas');
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(`${BACKEND_URL}/api/auth/reset-password`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          token,
          newPassword: password,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setSuccess(true);
        setTimeout(() => navigate('/login'), 3000);
      } else {
        setError(data.detail || 'Erreur lors de la réinitialisation');
      }
    } catch (error) {
      console.error('Erreur:', error);
      setError('Erreur de connexion au serveur');
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-[#1a0a2e] to-[#2B1F5C] flex items-center justify-center px-4">
        <div className="max-w-md w-full bg-gradient-to-br from-purple-900/50 to-pink-900/50 backdrop-blur-lg rounded-3xl p-8 border border-purple-500/30 text-center">
          <div className="mb-6">
            <div className="w-20 h-20 bg-green-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
              <Check className="w-10 h-10 text-green-400" />
            </div>
            <h2 className="text-3xl font-bold text-white mb-4">Mot de passe réinitialisé! ✅</h2>
          </div>
          
          <p className="text-white/80 mb-6">
            Votre mot de passe a été modifié avec succès. Vous allez être redirigé vers la page de connexion...
          </p>
          
          <Link
            to="/login"
            className="inline-flex items-center gap-2 bg-gradient-to-r from-pink-500 to-purple-500 hover:from-pink-600 hover:to-purple-600 text-white px-6 py-3 rounded-xl font-bold transition"
          >
            Se connecter maintenant
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#1a0a2e] to-[#2B1F5C] flex items-center justify-center px-4">
      <div className="max-w-md w-full bg-gradient-to-br from-purple-900/50 to-pink-900/50 backdrop-blur-lg rounded-3xl p-8 border border-purple-500/30">
        <div className="mb-8 text-center">
          <h1 className="text-3xl font-bold text-white mb-2">Nouveau mot de passe</h1>
          <p className="text-white/70">Choisissez un nouveau mot de passe sécurisé pour votre compte.</p>
        </div>

        {error && (
          <div className="bg-red-500/20 border border-red-500/50 rounded-xl p-4 mb-6 text-red-300 text-center">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-white mb-2 font-medium">
              <Lock className="w-4 h-4 inline mr-2" />
              Nouveau mot de passe
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              minLength={6}
              placeholder="Minimum 6 caractères"
              className="w-full bg-white/10 border border-purple-500/30 rounded-xl px-4 py-3 text-white placeholder-white/50 focus:outline-none focus:border-purple-400 transition"
            />
          </div>

          <div>
            <label className="block text-white mb-2 font-medium">
              <Lock className="w-4 h-4 inline mr-2" />
              Confirmer le mot de passe
            </label>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
              minLength={6}
              placeholder="Retapez votre mot de passe"
              className="w-full bg-white/10 border border-purple-500/30 rounded-xl px-4 py-3 text-white placeholder-white/50 focus:outline-none focus:border-purple-400 transition"
            />
          </div>

          <div className="bg-blue-500/10 border border-blue-500/30 rounded-xl p-4">
            <p className="text-blue-300 text-sm">
              💡 <strong>Conseil:</strong> Utilisez un mot de passe d'au moins 8 caractères avec des lettres, chiffres et symboles.
            </p>
          </div>

          <button
            type="submit"
            disabled={loading || !token}
            className="w-full bg-gradient-to-r from-pink-500 via-purple-500 to-violet-600 hover:from-pink-600 hover:via-purple-600 hover:to-violet-700 text-white py-3 rounded-xl font-bold transition shadow-lg disabled:opacity-50"
          >
            {loading ? 'Réinitialisation...' : 'Réinitialiser le mot de passe'}
          </button>
        </form>

        <div className="mt-6 text-center">
          <Link
            to="/login"
            className="inline-flex items-center gap-2 text-purple-400 hover:text-purple-300 transition"
          >
            <ArrowLeft className="w-4 h-4" />
            Retour à la connexion
          </Link>
        </div>
      </div>
    </div>
  );
};

export default ResetPassword;
