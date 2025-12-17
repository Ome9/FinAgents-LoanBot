import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Chat API
export const chatAPI = {
  sendMessage: async (message, sessionId = null, customerId = null) => {
    const response = await apiClient.post('/api/chat', {
      message,
      session_id: sessionId,
      customer_id: customerId,
    });
    return response.data;
  },

  startConversation: async (customerId) => {
    const response = await apiClient.post(`/api/start-conversation?customer_id=${customerId}`);
    return response.data;
  },

  uploadSalarySlip: async (sessionId, salaryAmount) => {
    const response = await apiClient.post('/api/upload-salary-slip', {
      session_id: sessionId,
      salary_amount: salaryAmount,
    });
    return response.data;
  },

  downloadSanctionLetter: (sessionId) => {
    return `${API_BASE_URL}/api/download-sanction-letter/${sessionId}`;
  },

  getSession: async (sessionId) => {
    const response = await apiClient.get(`/api/session/${sessionId}`);
    return response.data;
  },
};

// Mock Services API (for testing)
export const mockAPI = {
  getCustomers: async () => {
    const response = await apiClient.get('/api/crm/customers/list');
    return response.data;
  },

  getCustomer: async (customerId) => {
    const response = await apiClient.get(`/api/crm/customer/${customerId}`);
    return response.data;
  },

  getOffers: async (customerId) => {
    const response = await apiClient.get(`/api/offers/preapproved/${customerId}`);
    return response.data;
  },
};

export default apiClient;
