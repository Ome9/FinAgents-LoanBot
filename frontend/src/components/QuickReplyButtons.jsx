import React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle, Edit, FileText, Mail, ThumbsUp, X } from 'lucide-react';

const QuickReplyButtons = ({ quickReplies, onSelect, disabled }) => {
  if (!quickReplies || quickReplies.length === 0) return null;

  const getIcon = (label) => {
    const lowerLabel = label.toLowerCase();
    if (lowerLabel.includes('yes') || lowerLabel.includes('proceed') || lowerLabel.includes('correct')) {
      return <CheckCircle className="w-4 h-4" />;
    }
    if (lowerLabel.includes('change') || lowerLabel.includes('update') || lowerLabel.includes('edit')) {
      return <Edit className="w-4 h-4" />;
    }
    if (lowerLabel.includes('generate') || lowerLabel.includes('letter')) {
      return <FileText className="w-4 h-4" />;
    }
    if (lowerLabel.includes('email') || lowerLabel.includes('later')) {
      return <Mail className="w-4 h-4" />;
    }
    if (lowerLabel.includes('no')) {
      return <X className="w-4 h-4" />;
    }
    return <ThumbsUp className="w-4 h-4" />;
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      className="flex flex-wrap gap-2 max-w-4xl mx-auto px-6 py-3"
    >
      {quickReplies.map((reply, index) => (
        <motion.button
          key={index}
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: index * 0.1 }}
          whileHover={{ scale: 1.05, y: -2 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => !disabled && onSelect(reply.value)}
          disabled={disabled}
          className={`
            inline-flex items-center gap-2 px-4 py-2.5 rounded-xl
            font-medium text-sm shadow-md
            transition-all duration-200
            ${disabled 
              ? 'bg-gray-200 text-gray-400 cursor-not-allowed' 
              : 'bg-gradient-to-r from-blue-500 to-purple-600 text-white hover:from-blue-600 hover:to-purple-700 hover:shadow-lg cursor-pointer'
            }
          `}
        >
          {getIcon(reply.label)}
          <span>{reply.label}</span>
        </motion.button>
      ))}
    </motion.div>
  );
};

export default QuickReplyButtons;
