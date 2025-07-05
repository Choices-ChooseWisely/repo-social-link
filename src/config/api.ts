
export const API_BASE_URL = 'http://localhost:8000/api';

export const apiEndpoints = {
  // User management
  createUser: `${API_BASE_URL}/users`,
  getUser: (userId: string) => `${API_BASE_URL}/users/${userId}`,
  deleteUser: (userId: string) => `${API_BASE_URL}/users/${userId}`,
  
  // AI providers
  getAIProviders: `${API_BASE_URL}/ai/providers`,
  getAISetup: `${API_BASE_URL}/ai/setup`,
  validateAIKey: `${API_BASE_URL}/ai/validate`,
  setUserAIProvider: (userId: string) => `${API_BASE_URL}/users/${userId}/ai-provider`,
  getUserAIProvider: (userId: string) => `${API_BASE_URL}/users/${userId}/ai-provider`,
  
  // eBay integration
  getEbayCategories: `${API_BASE_URL}/ebay/categories`,
  listItem: `${API_BASE_URL}/ebay/list-item`,
  
  // File upload
  uploadImage: `${API_BASE_URL}/upload/image`,
  getImage: (filename: string) => `${API_BASE_URL}/images/${filename}`,
  
  // Health check
  healthCheck: 'http://localhost:8000/'
};
