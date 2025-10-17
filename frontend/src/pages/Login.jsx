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
  const { login } = useAuth();
  const { language } = useLanguage();
  const [isLogin] = useState(true); // Removed registration functionality
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!isLogin && formData.password !== formData.confirmPassword) {
      toast({
        title: t(language, 'common.error'),
        description: t(language, 'auth.register.passwordMismatch'),
        variant: 'destructive'
      });
      return;
    }

    try {
      if (isLogin) {
        await login(formData.email, formData.password);
        toast({
          title: t(language, 'auth.login.success'),
          description: language === 'fr' ? 'Bienvenue sur Tradalife' : 'Welcome to Tradalife'
        });
      } else {
        await register(formData.email, formData.password);
        toast({
          title: t(language, 'auth.register.success'),
          description: t(language, 'auth.register.success')
        });
      }

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
                {isLogin ? t(language, 'auth.login.title') : t(language, 'auth.register.title')}
              </span>
            </h1>
            <p className="text-white/70">
              {isLogin ? t(language, 'auth.login.subtitle') : t(language, 'auth.register.subtitle')}
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

            {!isLogin && (
              <div>
                <label className="block text-white/80 mb-2 text-sm">{t(language, 'auth.register.confirmPassword')}</label>
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
              {isLogin ? t(language, 'auth.login.button') : t(language, 'auth.register.button')}
            </Button>
          </form>

          {/* Toggle */}
          <div className="mt-6 text-center">
            <button
              onClick={() => setIsLogin(!isLogin)}
              className="text-pink-400 hover:text-pink-300 transition-colors"
            >
              {isLogin 
                ? `${t(language, 'auth.login.noAccount')} ${t(language, 'auth.login.register')}`
                : `${t(language, 'auth.register.hasAccount')} ${t(language, 'auth.register.login')}`
              }
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;