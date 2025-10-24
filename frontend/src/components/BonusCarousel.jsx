import React, { useState, useEffect } from 'react';
import { ChevronLeft, ChevronRight, Gift, ExternalLink } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useLanguage } from '../contexts/LanguageContext';
import { t } from '../translations';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const BonusCarousel = () => {
  const { language } = useLanguage();
  const navigate = useNavigate();
  const [announcements, setAnnouncements] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAnnouncements();
    // Auto-slide every 5 seconds
    const interval = setInterval(() => {
      if (announcements.length > 1) {
        setCurrentIndex((prev) => (prev + 1) % announcements.length);
      }
    }, 5000);
    return () => clearInterval(interval);
  }, [announcements.length]);

  const loadAnnouncements = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/bonus-announcements/all`);
      const data = await response.json();
      setAnnouncements(data.slice(0, 3)); // Limite à 3 pour la page d'accueil
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

  if (loading || announcements.length === 0) {
    return null;
  }

  const currentAnnouncement = announcements[currentIndex];
  const title = language === 'fr' ? currentAnnouncement.titleFr : currentAnnouncement.titleEn;
  const description = language === 'fr' ? currentAnnouncement.descriptionFr : currentAnnouncement.descriptionEn;

  return (
    <section className="py-20 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Section Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Gift className="w-10 h-10 text-pink-400" />
            <h2 className="text-4xl font-bold text-white">
              {t(language, 'bonus.title')}
            </h2>
          </div>
          <p className="text-white/70 text-lg">
            {t(language, 'bonus.homeSubtitle')}
          </p>
        </div>

        {/* Carousel Container */}
        <div className="relative">
          <div className="bg-gradient-to-br from-[#2B1F5C]/50 to-[#1E1540]/50 rounded-3xl border border-purple-500/30 overflow-hidden backdrop-blur-sm">
            <div className="grid md:grid-cols-2 gap-0">
              {/* Image Side */}
              <div className="relative h-96 md:h-auto overflow-hidden">
                <img
                  src={currentAnnouncement.imageUrl}
                  alt={title}
                  className="w-full h-full object-cover"
                />
                <div className="absolute inset-0 bg-gradient-to-r from-transparent to-[#2B1F5C]/50" />
              </div>

              {/* Content Side */}
              <div className="p-8 md:p-12 flex flex-col justify-center">
                <h3 className="text-3xl font-bold text-white mb-4">{title}</h3>
                {description && (
                  <p className="text-white/80 text-lg mb-6 leading-relaxed line-clamp-4">
                    {description}
                  </p>
                )}
                
                <div className="flex gap-4">
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
                  
                  <button
                    onClick={() => navigate('/bonus')}
                    className="inline-flex items-center gap-2 bg-white/10 backdrop-blur-sm text-white px-6 py-3 rounded-xl font-semibold hover:bg-white/20 transition-all border border-white/20"
                  >
                    {t(language, 'bonus.viewAll')}
                  </button>
                </div>

                {/* Dots Indicator */}
                {announcements.length > 1 && (
                  <div className="flex gap-2 mt-8">
                    {announcements.map((_, index) => (
                      <button
                        key={index}
                        onClick={() => setCurrentIndex(index)}
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
            </div>
          </div>

          {/* Navigation Arrows */}
          {announcements.length > 1 && (
            <>
              <button
                onClick={prevSlide}
                className="absolute left-4 top-1/2 -translate-y-1/2 bg-white/10 backdrop-blur-sm hover:bg-white/20 text-white p-3 rounded-full transition-all z-10"
              >
                <ChevronLeft className="w-6 h-6" />
              </button>
              <button
                onClick={nextSlide}
                className="absolute right-4 top-1/2 -translate-y-1/2 bg-white/10 backdrop-blur-sm hover:bg-white/20 text-white p-3 rounded-full transition-all z-10"
              >
                <ChevronRight className="w-6 h-6" />
              </button>
            </>
          )}
        </div>
      </div>
    </section>
  );
};

export default BonusCarousel;
