import React, { useState, useEffect, useRef } from 'react';
import { useLanguage } from '../contexts/LanguageContext';

const ChatWidget = () => {
  const { language } = useLanguage();
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId] = useState(`session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`);
  const messagesEndRef = useRef(null);

  const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleToggleChat = () => {
    console.log('Chat toggle clicked, current isOpen:', isOpen);
    setIsOpen(!isOpen);
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');
    setMessages(prev => [...prev, { type: 'user', text: userMessage }]);
    setIsLoading(true);

    try {
      const response = await fetch(`${BACKEND_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: userMessage,
          session_id: sessionId,
          language: language
        }),
      });

      if (!response.ok) throw new Error('Erreur lors de l\'envoi du message');

      const data = await response.json();
      setMessages(prev => [...prev, { type: 'bot', text: data.response }]);
    } catch (error) {
      console.error('Erreur chat:', error);
      setMessages(prev => [...prev, { 
        type: 'bot', 
        text: language === 'fr' 
          ? 'Désolé, une erreur s\'est produite. Veuillez réessayer.' 
          : 'Sorry, an error occurred. Please try again.'
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div style={{ position: 'fixed', bottom: '24px', right: '24px', zIndex: 9999 }}>
      {/* Bouton flottant */}
      {!isOpen && (
        <button
          onClick={handleToggleChat}
          style={{
            background: 'linear-gradient(to right, #c89a3f, #d4af37)',
            color: 'white',
            borderRadius: '50%',
            padding: '16px',
            border: 'none',
            boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
            cursor: 'pointer',
            transition: 'all 0.3s'
          }}
          aria-label={language === 'fr' ? 'Ouvrir le chat' : 'Open chat'}
        >
          <svg
            style={{ width: '24px', height: '24px' }}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
            />
          </svg>
        </button>
      )}

      {/* Fenêtre de chat */}
      {isOpen && (
        <div style={{
          width: '384px',
          height: '600px',
          backgroundColor: 'white',
          borderRadius: '8px',
          boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
          display: 'flex',
          flexDirection: 'column',
          border: '1px solid #e5e7eb'
        }}>
          {/* En-tête */}
          <div style={{
            background: 'linear-gradient(to right, #c89a3f, #d4af37)',
            color: 'white',
            padding: '16px',
            borderTopLeftRadius: '8px',
            borderTopRightRadius: '8px',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <div style={{ width: '12px', height: '12px', backgroundColor: '#4ade80', borderRadius: '50%' }} />
              <h3 style={{ fontWeight: 600, margin: 0 }}>
                {language === 'fr' ? 'Assistant Tradalife' : 'Tradalife Assistant'}
              </h3>
            </div>
            <button
              onClick={handleToggleChat}
              style={{
                background: 'rgba(255,255,255,0.2)',
                border: 'none',
                borderRadius: '50%',
                padding: '4px',
                cursor: 'pointer',
                color: 'white'
              }}
            >
              <svg style={{ width: '20px', height: '20px' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Zone de messages */}
          <div style={{ flex: 1, overflowY: 'auto', padding: '16px', backgroundColor: '#f9fafb' }}>
            {messages.length === 0 && (
              <div style={{ textAlign: 'center', color: '#6b7280', paddingTop: '32px', paddingBottom: '32px' }}>
                <p style={{ fontSize: '14px' }}>
                  {language === 'fr' 
                    ? 'Bonjour! Comment puis-je vous aider aujourd\'hui?' 
                    : 'Hello! How can I help you today?'}
                </p>
              </div>
            )}
            
            {messages.map((message, index) => (
              <div
                key={index}
                style={{
                  display: 'flex',
                  justifyContent: message.type === 'user' ? 'flex-end' : 'flex-start',
                  marginBottom: '16px'
                }}
              >
                <div
                  style={{
                    maxWidth: '80%',
                    borderRadius: '8px',
                    padding: '12px',
                    background: message.type === 'user' 
                      ? 'linear-gradient(to right, #c89a3f, #d4af37)'
                      : 'white',
                    color: message.type === 'user' ? 'white' : '#1f2937',
                    border: message.type === 'bot' ? '1px solid #e5e7eb' : 'none'
                  }}
                >
                  <p style={{ fontSize: '14px', margin: 0, whiteSpace: 'pre-wrap' }}>{message.text}</p>
                </div>
              </div>
            ))}
            
            {isLoading && (
              <div style={{ display: 'flex', justifyContent: 'flex-start' }}>
                <div style={{ background: 'white', border: '1px solid #e5e7eb', borderRadius: '8px', padding: '12px' }}>
                  <div style={{ display: 'flex', gap: '8px' }}>
                    <div style={{ width: '8px', height: '8px', backgroundColor: '#9ca3af', borderRadius: '50%' }} />
                    <div style={{ width: '8px', height: '8px', backgroundColor: '#9ca3af', borderRadius: '50%' }} />
                    <div style={{ width: '8px', height: '8px', backgroundColor: '#9ca3af', borderRadius: '50%' }} />
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>

          {/* Zone de saisie */}
          <div style={{ padding: '16px', borderTop: '1px solid #e5e7eb', backgroundColor: 'white', borderBottomLeftRadius: '8px', borderBottomRightRadius: '8px' }}>
            <div style={{ display: 'flex', gap: '8px' }}>
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder={language === 'fr' ? 'Tapez votre message...' : 'Type your message...'}
                disabled={isLoading}
                style={{
                  flex: 1,
                  border: '1px solid #d1d5db',
                  borderRadius: '8px',
                  padding: '8px 16px',
                  outline: 'none'
                }}
              />
              <button
                onClick={handleSendMessage}
                disabled={isLoading || !inputMessage.trim()}
                style={{
                  background: 'linear-gradient(to right, #c89a3f, #d4af37)',
                  color: 'white',
                  borderRadius: '8px',
                  padding: '8px 16px',
                  border: 'none',
                  cursor: isLoading || !inputMessage.trim() ? 'not-allowed' : 'pointer',
                  opacity: isLoading || !inputMessage.trim() ? 0.5 : 1
                }}
              >
                <svg style={{ width: '20px', height: '20px' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatWidget;
