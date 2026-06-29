import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { Loader2, CheckCircle2, Bot, FileText, Send } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

import ParticleNetwork from './components/ParticleNetwork';
import AICore3D from './components/AICore3D';

function App() {
  const [topic, setTopic] = useState("The impact of Agentic AI on software development in 2024");
  const [isLoading, setIsLoading] = useState(false);
  const [events, setEvents] = useState([]);
  const [article, setArticle] = useState("");
  const endOfMessagesRef = useRef(null);

  const scrollToBottom = () => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [events]);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!topic.trim()) return;

    setIsLoading(true);
    setEvents([]);
    setArticle("");

    try {
      const response = await fetch("http://localhost:8000/api/research", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic }),
      });

      if (!response.body) throw new Error("No response body");

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\n\n');
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const dataStr = line.substring(6);
            try {
              const data = JSON.parse(dataStr);
              
              if (data.agent === 'system' && data.status === 'COMPLETE') {
                setIsLoading(false);
                break;
              }

              if (data.agent === 'system' && data.status.startsWith('ERROR')) {
                setEvents(prev => [...prev, { icon: 'error', text: data.status }]);
                setIsLoading(false);
                break;
              }

              if (data.status) {
                setEvents(prev => [...prev, { 
                  agent: data.agent, 
                  text: data.status 
                }]);
              }

              if (data.data) {
                setArticle(data.data);
              }
            } catch (e) {
              console.error("Error parsing chunk", e, dataStr);
            }
          }
        }
      }
    } catch (error) {
      console.error("Fetch error:", error);
      setEvents(prev => [...prev, { agent: 'system', text: `Error: ${error.message}` }]);
    } finally {
      setIsLoading(false);
    }
  };

  const getIcon = (agent) => {
    if (agent === 'researcher') return <Bot size={20} className="status-icon" />;
    if (agent === 'writer') return <FileText size={20} className="status-icon" />;
    return <CheckCircle2 size={20} className="status-icon" />;
  };

  return (
    <>
      <ParticleNetwork />
      
      <div className="app-container">
        <motion.header 
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          style={{ textAlign: 'center', marginBottom: '2rem' }}
        >
          <AICore3D isThinking={isLoading} />
          <h1>Agentic AI Researcher</h1>
          <p style={{ color: 'var(--text-muted)' }}>Powered by LangGraph & Gemini</p>
        </motion.header>

        <motion.form 
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="search-container" 
          onSubmit={handleSearch}
        >
          <input
            type="text"
            className="search-input"
            placeholder="Enter a topic for the AI agents to research and write about..."
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            disabled={isLoading}
          />
          <motion.button 
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            type="submit" 
            className="search-btn" 
            disabled={isLoading || !topic.trim()}
          >
            {isLoading ? <Loader2 size={20} className="spin" /> : <Send size={20} />}
            {isLoading ? 'Processing...' : 'Generate'}
          </motion.button>
        </motion.form>

        <AnimatePresence>
          {events.length > 0 && (
            <motion.div 
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="glass-panel status-area"
            >
              <AnimatePresence>
                {events.map((event, idx) => (
                  <motion.div 
                    key={idx} 
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.1 }}
                    className="status-item"
                  >
                    {getIcon(event.agent)}
                    <span className="status-text">{event.text}</span>
                  </motion.div>
                ))}
              </AnimatePresence>
              
              {isLoading && (
                <motion.div 
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="status-item pulse"
                >
                  <Loader2 size={20} className="status-icon spin" />
                  <span className="status-text">Agents are thinking...</span>
                </motion.div>
              )}
              <div ref={endOfMessagesRef} />
            </motion.div>
          )}
        </AnimatePresence>

        <AnimatePresence>
          {article && (
            <motion.div 
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, type: "spring" }}
              className="glass-panel content-area"
            >
              <ReactMarkdown>{article}</ReactMarkdown>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </>
  );
}

export default App;
