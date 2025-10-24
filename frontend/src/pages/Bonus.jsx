import React, { useState, useEffect } from 'react';
import { ChevronLeft, ChevronRight, Gift, ExternalLink, ArrowUp } from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';
import { t } from '../translations';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const Bonus = () => {
  const { language } = useLanguage();
  const [announcements, setAnnouncements] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [loading, setLoading] = useState(true);
  const [showScrollTop, setShowScrollTop] = useState(false);

  useEffect(() => {
    loadAnnouncements();
    
    // Show scroll to top button when scrolling
    const handleScroll = () => {
      setShowScrollTop(window.scrollY > 300);
    };
    
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const loadAnnouncements = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/bonus-announcements/all`);
      const data = await response.json();
      setAnnouncements(data);
    } catch (error) {
      console.error('Error loading announcements:', error);
    } finally {
      setLoading(false);
    }
  };

  const nextSlide = () => {
    setCurrentIndex((prev) => (prev + 1) % announcements.length);
  };

  const prevSlide = () => {
    setCurrentIndex((prev) => (prev - 1 + announcements.length) % announcements.length);
  };

  const goToSlide = (index) => {
    setCurrentIndex(index);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-[#0A0118] via-[#1a0b2e] to-[#16213E] flex items-center justify-center">
        <div className="text-white text-xl">{t(language, 'common.loading')}</div>
      </div>
    );
  }

  if (announcements.length === 0) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-[#0A0118] via-[#1a0b2e] to-[#16213E] pt-32 px-4">
        <div className="max-w-6xl mx-auto text-center">
          <Gift className="w-20 h-20 text-pink-400 mx-auto mb-6" />
          <h1 className="text-4xl font-bold text-white mb-4">
            {t(language, 'bonus.title')}
          </h1>
          <p className="text-white/70 text-lg">
            {t(language, 'bonus.noAnnouncements')}
          </p>
        </div>
      </div>
    );
  }

  const currentAnnouncement = announcements[currentIndex];
  const title = language === 'fr' ? currentAnnouncement.titleFr : currentAnnouncement.titleEn;
  const description = language === 'fr' ? currentAnnouncement.descriptionFr : currentAnnouncement.descriptionEn;

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#0A0118] via-[#1a0b2e] to-[#16213E] pt-32 px-4 pb-20">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Gift className="w-12 h-12 text-pink-400" />
            <h1 className="text-5xl font-bold bg-gradient-to-r from-pink-400 to-purple-600 bg-clip-text text-transparent">
              {t(language, 'bonus.title')}
            </h1>
          </div>
          <p className="text-white/70 text-lg">
            {t(language, 'bonus.subtitle')}
          </p>
        </div>

        {/* Carousel */}
        <div className="relative">
          {/* Main Card */}
          <div className="bg-gradient-to-br from-[#2B1F5C]/50 to-[#1E1540]/50 rounded-3xl border border-purple-500/30 overflow-hidden backdrop-blur-sm">
            {/* Image */}
            <div className="relative h-96 overflow-hidden">
              <img
                src={currentAnnouncement.imageUrl}
                alt={title}
                className="w-full h-full object-cover"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
            </div>

            {/* Content */}
            <div className="p-8">
              <h2 className="text-3xl font-bold text-white mb-4">{title}</h2>
              {description && (
                <p className="text-white/80 text-lg mb-6 leading-relaxed">
                  {description}
                </p>
              )}
              
              {currentAnnouncement.linkUrl && (
                <a
                  href={currentAnnouncement.linkUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 bg-gradient-to-r from-pink-500 to-purple-600 text-white px-6 py-3 rounded-xl font-semibold hover:from-pink-600 hover:to-purple-700 transition-all"
                >
                  {t(language, 'bonus.learnMore')}
                  <ExternalLink className="w-5 h-5" />
                </a>
              )}
            </div>
          </div>

          {/* Navigation Arrows */}
          {announcements.length > 1 && (
            <>
              <button
                onClick={prevSlide}
                className="absolute left-4 top-1/2 -translate-y-1/2 bg-white/10 backdrop-blur-sm hover:bg-white/20 text-white p-3 rounded-full transition-all"
              >
                <ChevronLeft className="w-6 h-6" />
              </button>
              <button
                onClick={nextSlide}
                className="absolute right-4 top-1/2 -translate-y-1/2 bg-white/10 backdrop-blur-sm hover:bg-white/20 text-white p-3 rounded-full transition-all"
              >
                <ChevronRight className="w-6 h-6" />
              </button>
            </>
          )}

          {/* Dots Indicator */}
          {announcements.length > 1 && (
            <div className="flex justify-center gap-2 mt-6">
              {announcements.map((_, index) => (
                <button
                  key={index}
                  onClick={() => goToSlide(index)}
                  className={`h-2 rounded-full transition-all ${
                    index === currentIndex
                      ? 'w-8 bg-gradient-to-r from-pink-500 to-purple-600'
                      : 'w-2 bg-white/30 hover:bg-white/50'
                  }`}
                />
              ))}
            </div>
          )}
        </div>

        {/* Grid View of All Announcements */}
        {announcements.length > 1 && (
          <div className="mt-16">
            <h3 className="text-2xl font-bold text-white mb-8 text-center">
              {t(language, 'bonus.allAnnouncements')}
            </h3>
            <div className="grid md:grid-cols-3 gap-6">
              {announcements.map((announcement, index) => {
                const itemTitle = language === 'fr' ? announcement.titleFr : announcement.titleEn;
                return (
                  <button
                    key={announcement.id}
                    onClick={() => goToSlide(index)}
                    className={`bg-gradient-to-br from-[#2B1F5C]/30 to-[#1E1540]/30 rounded-2xl border overflow-hidden transition-all hover:scale-105 ${
                      index === currentIndex
                        ? 'border-pink-500 shadow-lg shadow-pink-500/20'
                        : 'border-purple-500/20'
                    }`}
                  >
                    <div className="h-48 overflow-hidden">
                      <img
                        src={announcement.imageUrl}
                        alt={itemTitle}
                        className="w-full h-full object-cover"
                      />
                    </div>
                    <div className="p-4">
                      <h4 className="text-white font-semibold text-lg line-clamp-2">
                        {itemTitle}
                      </h4>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Bonus;
