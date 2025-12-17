import React, { useState, useEffect } from 'react';
import ChatInterface from './components/ChatInterface';
import { mockAPI } from './services/api';
import { Users } from 'lucide-react';

function App() {
  const [customers, setCustomers] = useState([]);
  const [selectedCustomer, setSelectedCustomer] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCustomers();
  }, []);

  const fetchCustomers = async () => {
    try {
      const response = await mockAPI.getCustomers();
      setCustomers(response.data || []);
    } catch (error) {
      console.error('Error fetching customers:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCustomerSelect = (customerId) => {
    setSelectedCustomer(customerId);
  };

  if (selectedCustomer) {
    return (
      <div className="min-h-screen bg-gray-50 p-4">
        <div className="mb-4">
          <button
            onClick={() => setSelectedCustomer(null)}
            className="text-primary-600 hover:text-primary-700 font-semibold flex items-center space-x-2 transition-colors"
          >
            <span>←</span>
            <span>Back to Customer Selection</span>
          </button>
        </div>
        <ChatInterface customerId={selectedCustomer} />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Tata Capital Personal Loans
          </h1>
          <p className="text-lg text-gray-600">
            AI-Powered Loan Sales Assistant
          </p>
        </div>

        {loading ? (
          <div className="text-center py-12">
            <div className="animate-spin h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
            <p className="text-gray-600 mt-4">Loading customers...</p>
          </div>
        ) : (
          <div>
            <div className="flex items-center space-x-2 mb-6">
              <Users className="w-6 h-6 text-gray-700" />
              <h2 className="text-2xl font-semibold text-gray-900">Select Customer</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {customers.map((customer) => (
                <button
                  key={customer.customer_id}
                  onClick={() => handleCustomerSelect(customer.customer_id)}
                  className="bg-white p-6 shadow hover:shadow-lg transition-all text-left border border-gray-200 hover:border-primary-600"
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className="w-12 h-12 bg-primary-600 flex items-center justify-center">
                      <span className="text-white font-bold text-lg">
                        {customer.name.charAt(0)}
                      </span>
                    </div>
                    <span className="bg-green-50 text-green-700 text-xs font-semibold px-3 py-1 border border-green-200">
                      Pre-Approved
                    </span>
                  </div>
                  <h3 className="text-lg font-bold text-gray-900 mb-2">
                    {customer.name}
                  </h3>
                  <p className="text-sm text-gray-600 mb-3">
                    <span className="font-semibold">ID:</span> {customer.customer_id}
                  </p>
                  <div className="flex items-center justify-between text-sm text-gray-500">
                    <span>{customer.city}</span>
                    <span>{customer.phone.slice(-10)}</span>
                  </div>
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
