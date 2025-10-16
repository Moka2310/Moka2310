import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { useAuth } from '../contexts/AuthContext';
import { toast } from '../hooks/use-toast';

const Login = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login, register } = useAuth();
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: ''
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!isLogin && formData.password !== formData.confirmPassword) {
      toast({
        title: 'Erreur',
        description: 'Les mots de passe ne correspondent pas',
        variant: 'destructive'
      });
      return;
    }

    if (isLogin) {
      login(formData.email, formData.password);
      toast({
        title: 'Connexion réussie !',
        description: 'Bienvenue sur Tradalife'
      });
    } else {
      register(formData.email, formData.password);
      toast({
        title: 'Inscription réussie !',
        description: 'Votre compte a été créé avec succès'
      });
    }

    // Redirect to return URL or dashboard
    const returnTo = location.state?.returnTo || '/dashboard';
    navigate(returnTo, { state: location.state });
  };

  return (
    <div className="min-h-screen bg-[#1E1540] pt-28 pb-20 px-4 flex items-center justify-center">
      <div className="max-w-md w-full">
        <div className="bg-gradient-to-b from-[#2B1F5C] to-[#1E1540] rounded-3xl p-8 border border-purple-500/30 shadow-2xl">
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold mb-2">
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-400">
                {isLogin ? 'Connexion' : 'Inscription'}
              </span>
            </h1>
            <p className="text-white/70">
              {isLogin ? 'Content de vous revoir !' : 'Rejoignez notre communauté'}
            </p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-white/80 mb-2 text-sm">Email</label>
              <Input
                type="email"
                required
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                className="bg-white/10 border-purple-500/30 text-white placeholder:text-white/50 focus:border-pink-500"
                placeholder="votre@email.com"
              />
            </div>

            <div>
              <label className="block text-white/80 mb-2 text-sm">Mot de passe</label>
              <Input
                type="password"
                required
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                className="bg-white/10 border-purple-500/30 text-white placeholder:text-white/50 focus:border-pink-500"
                placeholder="••••••••"
              />
            </div>

            {!isLogin && (
              <div>
                <label className="block text-white/80 mb-2 text-sm">Confirmer le mot de passe</label>
                <Input
                  type="password"
                  required
                  value={formData.confirmPassword}
                  onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
                  className="bg-white/10 border-purple-500/30 text-white placeholder:text-white/50 focus:border-pink-500"
                  placeholder="••••••••"
                />
              </div>
            )}

            <Button
              type="submit"
              className="w-full bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white py-6 rounded-full font-semibold text-lg"
            >
              {isLogin ? 'Se connecter' : "S'inscrire"}
            </Button>
          </form>

          {/* Toggle */}
          <div className="mt-6 text-center">
            <button
              onClick={() => setIsLogin(!isLogin)}
              className="text-pink-400 hover:text-pink-300 transition-colors"
            >
              {isLogin ? "Pas encore de compte ? S'inscrire" : 'Déjà un compte ? Se connecter'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;