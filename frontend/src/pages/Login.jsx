import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { useAuth } from '../contexts/AuthContext';
import { useLanguage } from '../contexts/LanguageContext';
import { t } from '../translations';
import { toast } from '../hooks/use-toast';

const Login = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login, register } = useAuth();
  const { language } = useLanguage();
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await login(formData.email, formData.password);
      toast({
        title: t(language, 'auth.login.success'),
        description: language === 'fr' ? 'Bienvenue sur Tradalife' : 'Welcome to Tradalife'
      });

      // Redirect to return URL or dashboard
      const returnTo = location.state?.returnTo || '/dashboard';
      navigate(returnTo, { state: location.state });
    } catch (error) {
      toast({
        title: t(language, 'common.error'),
        description: error.message,
        variant: 'destructive'
      });
    }
  };

  return (
    <div className="min-h-screen bg-[#1E1540] pt-28 pb-20 px-4 flex items-center justify-center">
      <div className="max-w-md w-full">
        <div className="bg-gradient-to-b from-[#2B1F5C] to-[#1E1540] rounded-3xl p-8 border border-purple-500/30 shadow-2xl">
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold mb-2">
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-400">
                {t(language, 'auth.login.title')}
              </span>
            </h1>
            <p className="text-white/70">
              {t(language, 'auth.login.subtitle')}
            </p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-white/80 mb-2 text-sm">{t(language, 'auth.login.email')}</label>
              <Input
                type="email"
                required
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                className="bg-white/10 border-purple-500/30 text-white placeholder:text-white/50 focus:border-pink-500"
                placeholder={language === 'fr' ? 'votre@email.com' : 'your@email.com'}
              />
            </div>

            <div>
              <label className="block text-white/80 mb-2 text-sm">{t(language, 'auth.login.password')}</label>
              <Input
                type="password"
                required
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                className="bg-white/10 border-purple-500/30 text-white placeholder:text-white/50 focus:border-pink-500"
                placeholder="••••••••"
              />
            </div>

            <Button
              type="submit"
              className="w-full bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white py-6 rounded-full font-semibold text-lg"
            >
              {t(language, 'auth.login.button')}
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Login;