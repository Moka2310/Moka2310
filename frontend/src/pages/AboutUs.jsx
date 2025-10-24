import React from 'react';
import { Users, Award, TrendingUp, Shield } from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';
import { t } from '../translations';

const AboutUs = () => {
  const { language } = useLanguage();

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#0A0118] via-[#1a0b2e] to-[#16213E] pt-32 px-4 pb-20">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-pink-400 to-purple-600 bg-clip-text text-transparent mb-4">
            {t(language, 'aboutUs.title')}
          </h1>
          <p className="text-white/70 text-lg">
            {t(language, 'aboutUs.subtitle')}
          </p>
        </div>

        {/* Main Content Card */}
        <div className="bg-gradient-to-br from-[#2B1F5C] to-[#1E1540] rounded-3xl border border-purple-500/30 overflow-hidden mb-12">
          {/* Image Section */}
          <div className="relative h-96 overflow-hidden">
            <img
              src="https://images.unsplash.com/photo-1559136555-9303baea8ebd?w=1200&h=600&fit=crop"
              alt={t(language, 'aboutUs.title')}
              className="w-full h-full object-cover"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-[#2B1F5C] via-[#2B1F5C]/50 to-transparent" />
            
            {/* Overlay Logo/Icon */}
            <div className="absolute bottom-8 left-8">
              <div className="bg-gradient-to-r from-pink-500 to-purple-600 p-4 rounded-2xl">
                <Users className="w-12 h-12 text-white" />
              </div>
            </div>
          </div>

          {/* Text Content */}
          <div className="p-8 md:p-12">
            <div className="prose prose-invert max-w-none">
              <p className="text-white/90 text-lg leading-relaxed mb-6">
                {t(language, 'aboutUs.description')}
              </p>
              
              <p className="text-white/80 text-lg leading-relaxed mb-6">
                {t(language, 'aboutUs.mission')}
              </p>

              <p className="text-white/80 text-lg leading-relaxed">
                {t(language, 'aboutUs.vision')}
              </p>
            </div>
          </div>
        </div>

        {/* Stats/Features Grid */}
        <div className="grid md:grid-cols-3 gap-6">
          <div className="bg-gradient-to-br from-blue-500/20 to-purple-500/20 rounded-2xl border border-blue-500/30 p-6 backdrop-blur-sm">
            <div className="bg-blue-500/20 w-14 h-14 rounded-xl flex items-center justify-center mb-4">
              <Award className="w-7 h-7 text-blue-400" />
            </div>
            <h3 className="text-xl font-bold text-white mb-2">
              {t(language, 'aboutUs.feature1Title')}
            </h3>
            <p className="text-white/70">
              {t(language, 'aboutUs.feature1Desc')}
            </p>
          </div>

          <div className="bg-gradient-to-br from-pink-500/20 to-purple-500/20 rounded-2xl border border-pink-500/30 p-6 backdrop-blur-sm">
            <div className="bg-pink-500/20 w-14 h-14 rounded-xl flex items-center justify-center mb-4">
              <TrendingUp className="w-7 h-7 text-pink-400" />
            </div>
            <h3 className="text-xl font-bold text-white mb-2">
              {t(language, 'aboutUs.feature2Title')}
            </h3>
            <p className="text-white/70">
              {t(language, 'aboutUs.feature2Desc')}
            </p>
          </div>

          <div className="bg-gradient-to-br from-green-500/20 to-emerald-500/20 rounded-2xl border border-green-500/30 p-6 backdrop-blur-sm">
            <div className="bg-green-500/20 w-14 h-14 rounded-xl flex items-center justify-center mb-4">
              <Shield className="w-7 h-7 text-green-400" />
            </div>
            <h3 className="text-xl font-bold text-white mb-2">
              {t(language, 'aboutUs.feature3Title')}
            </h3>
            <p className="text-white/70">
              {t(language, 'aboutUs.feature3Desc')}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AboutUs;
