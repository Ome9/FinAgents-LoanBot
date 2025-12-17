import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Download, Upload, User, Bot, CheckCircle2, Loader2, Sparkles } from 'lucide-react';
import { chatAPI } from '../services/api';
import ReactMarkdown from 'react-markdown';
import QuickReplyButtons from './QuickReplyButtons';

const ChatInterface = ({ customerId }) => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [sessionId, setSessionId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [currentStage, setCurrentStage] = useState('sales');
  const [requiresSalarySlip, setRequiresSalarySlip] = useState(false);
  const [conversationComplete, setConversationComplete] = useState(false);
  const [sanctionLetterAvailable, setSanctionLetterAvailable] = useState(false);
  const [salaryAmount, setSalaryAmount] = useState('');
  const [showSalaryInput, setShowSalaryInput] = useState(false);
  const [quickReplies, setQuickReplies] = useState([]);
  
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  useEffect(() => {
    if (customerId) {
      initializeConversation();
    }
  }, [customerId]);

  const initializeConversation = async () => {
    try {
      setIsLoading(true);
      const response = await chatAPI.startConversation(customerId);
      setSessionId(response.session_id);
      setMessages(response.messages);
      setCurrentStage(response.current_stage);
      setQuickReplies(response.quick_replies || []);
    } catch (error) {
      console.error('Error initializing conversation:', error);
      setMessages([
        {
          role: 'assistant',
          content: 'Sorry, I encountered an error starting the conversation. Please try again.',
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');
    
    // Immediately add user message to UI for instant feedback
    const newUserMessage = {
      role: 'user',
      content: userMessage,
    };
    setMessages((prev) => [...prev, newUserMessage]);
    setIsLoading(true);

    try {
      const response = await chatAPI.sendMessage(userMessage, sessionId, customerId);
      
      setSessionId(response.session_id);
      // Update with full messages from backend (includes AI response)
      setMessages(response.messages);
      setCurrentStage(response.current_stage);
      setRequiresSalarySlip(response.requires_salary_slip);
      setConversationComplete(response.conversation_complete);
      setSanctionLetterAvailable(response.sanction_letter_available);
      setQuickReplies(response.quick_replies || []);

      if (response.requires_salary_slip) {
        setShowSalaryInput(true);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: 'Sorry, I encountered an error. Please try again.',
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSalarySlipUpload = async () => {
    if (!salaryAmount || parseFloat(salaryAmount) <= 0) {
      alert('Please enter a valid salary amount');
      return;
    }

    setIsLoading(true);
    setShowSalaryInput(false);

    try {
      const response = await chatAPI.uploadSalarySlip(sessionId, parseFloat(salaryAmount));
      
      setMessages(response.messages);
      setCurrentStage(response.current_stage);
      setRequiresSalarySlip(response.requires_salary_slip);
      setConversationComplete(response.conversation_complete);
      setSanctionLetterAvailable(response.sanction_letter_available);
      setSalaryAmount('');
    } catch (error) {
      console.error('Error uploading salary slip:', error);
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: 'Sorry, there was an error processing your salary information. Please try again.',
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const downloadSanctionLetter = () => {
    if (sessionId) {
      window.open(chatAPI.downloadSanctionLetter(sessionId), '_blank');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const handleQuickReply = async (value) => {
    // Send the quick reply value as a message
    setInputMessage('');
    setQuickReplies([]); // Hide quick replies immediately
    
    const newUserMessage = {
      role: 'user',
      content: value,
    };
    setMessages((prev) => [...prev, newUserMessage]);
    setIsLoading(true);

    try {
      const response = await chatAPI.sendMessage(value, sessionId, customerId);
      
      setSessionId(response.session_id);
      setMessages(response.messages);
      setCurrentStage(response.current_stage);
      setRequiresSalarySlip(response.requires_salary_slip);
      setConversationComplete(response.conversation_complete);
      setSanctionLetterAvailable(response.sanction_letter_available);
      setQuickReplies(response.quick_replies || []);

      if (response.requires_salary_slip) {
        setShowSalaryInput(true);
      }
    } catch (error) {
      console.error('Error with quick reply:', error);
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: 'Sorry, I encountered an error. Please try again.',
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const getStageIcon = (stage) => {
    // Map confirmation stages to their base stages
    const normalizedStage = stage.replace('awaiting_', '').replace('_confirmation', '');
    
    const stages = {
      sales: { label: 'Sales Agent Active', color: 'bg-blue-500', worker: '💼 Sales Agent' },
      verification: { label: 'Verification Agent Active', color: 'bg-purple-500', worker: '✅ Verification Agent' },
      underwriting: { label: 'Underwriting Agent Active', color: 'bg-amber-500', worker: '📊 Underwriting Agent' },
      sanction_letter: { label: 'Document Generator Active', color: 'bg-green-500', worker: '📄 Sanction Letter Agent' },
      end: { label: 'Process Complete', color: 'bg-green-500', worker: '✅ Complete' },
    };
    return stages[normalizedStage] || stages.sales;
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Modern Header with Glassmorphism */}
      <motion.header 
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="bg-white/70 backdrop-blur-xl border-b border-slate-200/50 shadow-sm sticky top-0 z-50"
      >
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center shadow-lg">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  Tata Capital AI Assistant
                </h1>
                <p className="text-sm text-slate-500">Powered by Agentic AI • Perplexity</p>
              </div>
            </div>
            <motion.div 
              layout
              className="flex items-center gap-3 px-4 py-2 rounded-full bg-white/90 border border-slate-200 shadow-sm"
            >
              <motion.div
                animate={{ rotate: currentStage.includes('sales') ? 0 : 360 }}
                transition={{ duration: 0.5 }}
                className={`w-2.5 h-2.5 rounded-full ${getStageIcon(currentStage).color}`}
              />
              <div className="flex flex-col">
                <span className="text-xs text-slate-500">{getStageIcon(currentStage).worker}</span>
              </div>
            </motion.div>
          </div>
        </div>
      </motion.header>

      {/* Progress Bar */}
      <div className="bg-white/50 backdrop-blur-sm px-6 py-4 border-b border-slate-200/50">
        <div className="max-w-6xl mx-auto">
          <div className="flex items-center justify-between text-xs">
            {/* Step 1: Sales */}
            <div className={`flex items-center space-x-2 ${
              currentStage === 'sales' || currentStage === 'awaiting_verification_confirmation' 
                ? 'text-blue-600 font-semibold' 
                : 'text-gray-400'
            }`}>
              <div className={`w-8 h-8 rounded-lg ${
                currentStage === 'sales' || currentStage === 'awaiting_verification_confirmation'
                  ? 'bg-blue-600' 
                  : ['verification', 'awaiting_underwriting_confirmation', 'underwriting', 'awaiting_sanction_confirmation', 'sanction_letter', 'end'].includes(currentStage)
                  ? 'bg-blue-400'
                  : 'bg-gray-300'
              } flex items-center justify-center text-white font-semibold shadow-md transition-all duration-300`}>
                1
              </div>
              <span className="hidden sm:inline">Sales</span>
            </div>
            <div className="flex-1 h-1.5 mx-2 bg-gray-200 rounded-full overflow-hidden">
              <div 
                className={`h-full ${
                  ['verification', 'awaiting_underwriting_confirmation', 'underwriting', 'awaiting_sanction_confirmation', 'sanction_letter', 'end'].includes(currentStage)
                    ? 'bg-gradient-to-r from-blue-600 to-purple-600' 
                    : 'bg-gray-300'
                } transition-all duration-500`} 
                style={{ width: ['sales', 'awaiting_verification_confirmation'].includes(currentStage) ? '0%' : '100%' }}
              />
            </div>
            {/* Step 2: Verification */}
            <div className={`flex items-center space-x-2 ${
              ['verification', 'awaiting_underwriting_confirmation'].includes(currentStage)
                ? 'text-purple-600 font-semibold' 
                : 'text-gray-400'
            }`}>
              <div className={`w-8 h-8 rounded-lg ${
                ['verification', 'awaiting_underwriting_confirmation'].includes(currentStage)
                  ? 'bg-purple-600' 
                  : ['underwriting', 'awaiting_sanction_confirmation', 'sanction_letter', 'end'].includes(currentStage)
                  ? 'bg-purple-400'
                  : 'bg-gray-300'
              } flex items-center justify-center text-white font-semibold shadow-md transition-all duration-300`}>
                2
              </div>
              <span className="hidden sm:inline">Verify</span>
            </div>
            <div className="flex-1 h-1.5 mx-2 bg-gray-200 rounded-full overflow-hidden">
              <div 
                className={`h-full ${
                  ['underwriting', 'awaiting_sanction_confirmation', 'sanction_letter', 'end'].includes(currentStage)
                    ? 'bg-gradient-to-r from-purple-600 to-amber-600' 
                    : 'bg-gray-300'
                } transition-all duration-500`}
                style={{ width: ['underwriting', 'awaiting_sanction_confirmation', 'sanction_letter', 'end'].includes(currentStage) ? '100%' : '0%' }}
              />
            </div>
            {/* Step 3: Underwriting */}
            <div className={`flex items-center space-x-2 ${
              ['underwriting', 'awaiting_sanction_confirmation'].includes(currentStage)
                ? 'text-amber-600 font-semibold' 
                : 'text-gray-400'
            }`}>
              <div className={`w-8 h-8 rounded-lg ${
                ['underwriting', 'awaiting_sanction_confirmation'].includes(currentStage)
                  ? 'bg-amber-600' 
                  : ['sanction_letter', 'end'].includes(currentStage)
                  ? 'bg-amber-400'
                  : 'bg-gray-300'
              } flex items-center justify-center text-white font-semibold shadow-md transition-all duration-300`}>
                3
              </div>
              <span className="hidden sm:inline">Assess</span>
            </div>
            <div className="flex-1 h-1.5 mx-2 bg-gray-200 rounded-full overflow-hidden">
              <div 
                className={`h-full ${
                  ['sanction_letter', 'end'].includes(currentStage) || conversationComplete
                    ? 'bg-gradient-to-r from-amber-600 to-green-600' 
                    : 'bg-gray-300'
                } transition-all duration-500`}
                style={{ width: ['sanction_letter', 'end'].includes(currentStage) || conversationComplete ? '100%' : '0%' }}
              />
            </div>
            {/* Step 4: Sanction Letter */}
            <div className={`flex items-center space-x-2 ${
              conversationComplete || ['sanction_letter', 'end'].includes(currentStage)
                ? 'text-green-600 font-semibold' 
                : 'text-gray-400'
            }`}>
              <div className={`w-8 h-8 rounded-lg ${
                conversationComplete || ['sanction_letter', 'end'].includes(currentStage)
                  ? 'bg-green-600' 
                  : 'bg-gray-300'
              } flex items-center justify-center text-white font-semibold shadow-md transition-all duration-300`}>
                4
              </div>
              <span className="hidden sm:inline">Approve</span>
            </div>
          </div>
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto px-4 py-6">
        <div className="max-w-4xl mx-auto space-y-6">
          <AnimatePresence mode="popLayout">
            {messages.map((message, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20, scale: 0.95 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                transition={{ duration: 0.3, delay: index * 0.03 }}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className={`flex gap-3 max-w-[85%] ${message.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                    className={`flex-shrink-0 w-10 h-10 rounded-xl flex items-center justify-center shadow-lg ${
                      message.role === 'user'
                        ? 'bg-gradient-to-br from-blue-500 to-blue-600'
                        : 'bg-gradient-to-br from-purple-500 to-purple-600'
                    }`}
                  >
                    {message.role === 'user' ? (
                      <User className="w-5 h-5 text-white" />
                    ) : (
                      <Bot className="w-5 h-5 text-white" />
                    )}
                  </motion.div>

                  <motion.div
                    whileHover={{ scale: 1.01 }}
                    className={`px-5 py-4 rounded-2xl shadow-md ${
                      message.role === 'user'
                        ? 'bg-gradient-to-br from-blue-500 to-blue-600 text-white'
                        : 'bg-white border border-slate-200 text-slate-800'
                    }`}
                  >
                    <div className="prose prose-sm max-w-none">
                      <ReactMarkdown
                        components={{
                          p: ({ children }) => (
                            <p className={`mb-2 last:mb-0 ${message.role === 'user' ? 'text-white' : 'text-slate-700'}`}>
                              {children}
                            </p>
                          ),
                          strong: ({ children }) => (
                            <strong className={message.role === 'user' ? 'text-white font-semibold' : 'text-slate-900 font-semibold'}>
                              {children}
                            </strong>
                          ),
                        }}
                      >
                        {message.content}
                      </ReactMarkdown>
                    </div>
                  </motion.div>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>

          {isLoading && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex justify-start"
            >
              <div className="flex gap-3">
                <div className="w-10 h-10 rounded-xl flex items-center justify-center bg-gradient-to-br from-purple-500 to-purple-600 shadow-lg">
                  <Bot className="w-5 h-5 text-white" />
                </div>
                <div className="px-5 py-4 rounded-2xl bg-white border border-slate-200 shadow-md">
                  <div className="flex gap-1.5">
                    <motion.div
                      animate={{ scale: [1, 1.2, 1] }}
                      transition={{ repeat: Infinity, duration: 0.8, delay: 0 }}
                      className="w-2 h-2 bg-slate-400 rounded-full"
                    />
                    <motion.div
                      animate={{ scale: [1, 1.2, 1] }}
                      transition={{ repeat: Infinity, duration: 0.8, delay: 0.2 }}
                      className="w-2 h-2 bg-slate-400 rounded-full"
                    />
                    <motion.div
                      animate={{ scale: [1, 1.2, 1] }}
                      transition={{ repeat: Infinity, duration: 0.8, delay: 0.4 }}
                      className="w-2 h-2 bg-slate-400 rounded-full"
                    />
                  </div>
                </div>
              </div>
            </motion.div>
          )}

          <AnimatePresence>
            {showSalaryInput && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="w-full"
              >
                <div className="bg-gradient-to-r from-amber-50 to-orange-50 border-l-4 border-amber-500 rounded-r-xl p-6 shadow-lg">
                  <div className="flex items-start gap-4">
                    <div className="w-10 h-10 rounded-xl bg-amber-100 flex items-center justify-center flex-shrink-0">
                      <Upload className="w-5 h-5 text-amber-600" />
                    </div>
                    <div className="flex-1">
                      <h3 className="font-semibold text-amber-900 mb-2 text-lg">Salary Verification Required</h3>
                      <p className="text-sm text-amber-700 mb-4">
                        Please provide your monthly salary amount to proceed with the loan assessment
                      </p>
                      <div className="flex gap-3">
                        <input
                          type="number"
                          value={salaryAmount}
                          onChange={(e) => setSalaryAmount(e.target.value)}
                          placeholder="Enter monthly salary (₹)"
                          className="flex-1 px-4 py-3 rounded-xl border-2 border-amber-200 bg-white text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-transparent transition-all"
                        />
                        <motion.button
                          whileHover={{ scale: 1.02 }}
                          whileTap={{ scale: 0.98 }}
                          onClick={handleSalarySlipUpload}
                          disabled={isLoading}
                          className="px-6 py-3 rounded-xl bg-amber-600 text-white font-medium hover:bg-amber-700 disabled:bg-amber-300 disabled:cursor-not-allowed transition-colors shadow-md"
                        >
                          Submit
                        </motion.button>
                      </div>
                    </div>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {sanctionLetterAvailable && (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="w-full"
            >
              <div className="bg-gradient-to-r from-green-50 to-emerald-50 border-l-4 border-green-500 rounded-r-xl p-6 shadow-lg">
                <div className="flex items-center justify-between flex-wrap gap-4">
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 rounded-xl bg-green-100 flex items-center justify-center">
                      <CheckCircle2 className="w-6 h-6 text-green-600" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-green-900 text-lg">Sanction Letter Ready</h3>
                      <p className="text-sm text-green-700">Your loan has been approved!</p>
                    </div>
                  </div>
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={downloadSanctionLetter}
                    className="px-6 py-3 rounded-xl bg-gradient-to-r from-green-600 to-emerald-600 text-white font-medium hover:from-green-700 hover:to-emerald-700 transition-all flex items-center gap-2 shadow-lg"
                  >
                    <Download className="w-4 h-4" />
                    <span>Download PDF</span>
                  </motion.button>
                </div>
              </div>
            </motion.div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Quick Reply Buttons */}
      <AnimatePresence>
        {quickReplies.length > 0 && !isLoading && (
          <QuickReplyButtons
            quickReplies={quickReplies}
            onSelect={handleQuickReply}
            disabled={isLoading || conversationComplete}
          />
        )}
      </AnimatePresence>

      {/* Modern Input Area */}
      <motion.div 
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="bg-white/70 backdrop-blur-xl border-t border-slate-200/50 shadow-lg"
      >
        <div className="max-w-4xl mx-auto px-6 py-4">
          <div className="flex gap-3">
            <div className="flex-1 relative">
              <textarea
                ref={inputRef}
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type your message here..."
                rows={1}
                disabled={isLoading || conversationComplete}
                className="w-full px-5 py-3.5 rounded-xl border-2 border-slate-200 bg-white text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-slate-50 disabled:text-slate-400 disabled:cursor-not-allowed transition-all resize-none"
                style={{ minHeight: '52px', maxHeight: '120px' }}
              />
            </div>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={sendMessage}
              disabled={isLoading || !inputMessage.trim() || conversationComplete}
              className="px-6 rounded-xl flex items-center justify-center bg-gradient-to-r from-blue-600 to-purple-600 text-white font-medium hover:from-blue-700 hover:to-purple-700 disabled:from-slate-300 disabled:to-slate-400 disabled:cursor-not-allowed transition-all shadow-lg"
            >
              {isLoading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <Send className="w-5 h-5" />
              )}
            </motion.button>
          </div>
          
          {conversationComplete && (
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="text-sm text-slate-500 mt-3 text-center"
            >
              Conversation completed. Thank you for choosing Tata Capital!
            </motion.p>
          )}
        </div>
      </motion.div>
    </div>
  );
};

export default ChatInterface;
