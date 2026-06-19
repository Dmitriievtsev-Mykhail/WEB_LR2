import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import './index.css';

const rootElement = document.getElementById('root');

if (!rootElement) {
    console.error('Кореневий елемент root не знайдено');
} else {
    ReactDOM.createRoot(rootElement).render(
        <React.StrictMode>
            <App />
        </React.StrictMode>,
    );
}