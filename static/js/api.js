// // API Configuration
// const API_BASE_URL = 'http://localhost:8000/api';

// // API Helper Class
// class API {
//     static async request(endpoint, options = {}) {
//         const url = `${API_BASE_URL}${endpoint}`;
        
//         const defaultOptions = {
//             headers: {
//                 'Content-Type': 'application/json',
//             }
//         };
        
//         // Add auth token if exists
//         const token = localStorage.getItem('token');
//         if (token) {
//             defaultOptions.headers['Authorization'] = `Bearer ${token}`;
//         }
        
//         const config = { ...defaultOptions, ...options };
        
//         try {
//             const response = await fetch(url, config);
//             const data = await response.json();
            
//             if (!response.ok) {
//                 throw new Error(data.message || 'API request failed');
//             }
            
//             return data;
//         } catch (error) {
//             console.error('API Error:', error);
//             throw error;
//         }
//     }
    
//     static async get(endpoint) {
//         return this.request(endpoint, { method: 'GET' });
//     }
    
//     static async post(endpoint, data) {
//         return this.request(endpoint, {
//             method: 'POST',
//             body: JSON.stringify(data)
//         });
//     }
    
//     static async put(endpoint, data) {
//         return this.request(endpoint, {
//             method: 'PUT',
//             body: JSON.stringify(data)
//         });
//     }
    
//     static async delete(endpoint) {
//         return this.request(endpoint, { method: 'DELETE' });
//     }
// }

// // Export for use in other files
// window.API = API;