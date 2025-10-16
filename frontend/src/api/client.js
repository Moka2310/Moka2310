import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Create axios instance
const apiClient = axios.create({
  baseURL: API,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add token to requests
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('tradalife_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// API methods
export const authAPI = {
  register: (email, password) => 
    apiClient.post('/auth/register', { email, password }),
  
  login: (email, password) =>
    apiClient.post('/auth/login', { email, password }),
  
  getMe: () =>
    apiClient.get('/auth/me')
};

export const formationsAPI = {
  getAll: () =>
    apiClient.get('/formations'),
  
  getById: (id) =>
    apiClient.get(`/formations/${id}`)
};

export const purchasesAPI = {
  create: (formationId, paymentMethod) =>
    apiClient.post('/purchases/create', { formationId, paymentMethod }),
  
  confirm: (purchaseId) =>
    apiClient.post(`/purchases/confirm/${purchaseId}`),
  
  getMyPurchases: () =>
    apiClient.get('/purchases/my-purchases')
};

export const kycAPI = {
  submit: (formData) => {
    const config = {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    };
    return apiClient.post('/kyc/submit', formData, config);
  },
  
  getStatus: () =>
    apiClient.get('/kyc/status'),
  
  getDocuments: () =>
    apiClient.get('/kyc/documents')
};

export const adminAPI = {
  getKycRequests: () =>
    apiClient.get('/admin/kyc-requests'),
  
  approveKyc: (userId) =>
    apiClient.post(`/admin/kyc-approve/${userId}`),
  
  rejectKyc: (userId, reason) =>
    apiClient.post(`/admin/kyc-reject/${userId}`, { reason }),
  
  getStats: () =>
    apiClient.get('/admin/stats')
};

export default apiClient;
