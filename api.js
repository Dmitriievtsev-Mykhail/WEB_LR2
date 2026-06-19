import axios from 'axios';

// Базову адресу змінено на відносний шлях, щоб запити йшли через локальний проксі Vite
const api = axios.create({
    baseURL: '/api',
    headers: {
        'Content-Type': 'application/json',
    }
});

api.interceptors.request.use(
    (config) => {
        try {
            const token = localStorage.getItem('token');
            if (token) {
                config.headers.Authorization = `Token ${token}`;
            }
        } catch (error) {
            console.error('Помилка доступу до localStorage під час формування запиту:', error);
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

export default api;