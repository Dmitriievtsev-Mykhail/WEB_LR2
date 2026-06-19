import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate, useNavigate } from 'react-router-dom';
import api from './api';
import Login from './pages/Login';
import Register from './pages/Register';
import Profile from './pages/Profile';
import About from './pages/About';
import Tasks from './pages/Tasks';
import Admin from './pages/Admin';

function Navigation() {
    const navigate = useNavigate();
    const token = localStorage.getItem('token');
    
    // Стан для збереження прав та даних користувача
    const [isStaff, setIsStaff] = useState(false);
    const [userData, setUserData] = useState(null);

    useEffect(() => {
        if (token) {
            // Запит даних профілю для перевірки прав та отримання імені з ID
            api.get('/auth/profile/')
                .then(response => {
                    setIsStaff(response.data.is_staff === true);
                    setUserData({
                        id: response.data.id,
                        name: response.data.name || 'Без імені'
                    });
                })
                .catch(error => {
                    console.error('Помилка отримання профілю:', error);
                });
        } else {
            setIsStaff(false);
            setUserData(null);
        }
    }, [token]);

    const handleLogout = () => {
        try {
            localStorage.removeItem('token');
            localStorage.removeItem('user_id');
            localStorage.removeItem('email');
            setIsStaff(false);
            setUserData(null);
            navigate('/login');
        } catch (error) {
            console.error('Помилка очищення локального сховища:', error);
        }
    };

    return (
        <nav className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white p-4 shadow-xl border-b border-slate-800 w-full">
            <div className="container mx-auto flex justify-between items-center px-4">
                <div className="text-2xl font-black tracking-wider bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-400">
                    To-Do App
                </div>
                <div className="space-x-2 flex items-center">
                    <Link to="/about" className="text-slate-300 hover:text-white px-3 py-2 rounded-xl hover:bg-slate-800 transition-colors font-medium">Про додаток</Link>
                    {token ? (
                        <>
                            <Link to="/tasks" className="text-slate-300 hover:text-white px-3 py-2 rounded-xl hover:bg-slate-800 transition-colors font-medium">Завдання</Link>
                            <Link to="/profile" className="text-slate-300 hover:text-white px-3 py-2 rounded-xl hover:bg-slate-800 transition-colors font-medium">Профіль</Link>
                            {isStaff && (
                                <Link to="/admin" className="text-slate-300 hover:text-white px-3 py-2 rounded-xl hover:bg-slate-800 transition-colors font-medium">Адмін-панель</Link>
                            )}
                            
                            {/* Блок відображення імені та ID залогіненого користувача */}
                            {userData && (
                                <div className="flex flex-col items-end px-4 border-l border-slate-700 ml-2">
                                    <span className="text-sm font-bold text-blue-400">{userData.name}</span>
                                    <span className="text-xs font-semibold text-slate-500 tracking-wide">ID: {userData.id}</span>
                                </div>
                            )}

                            <button onClick={handleLogout} className="bg-gradient-to-r from-red-600 to-pink-600 text-white px-4 py-2 rounded-xl hover:from-red-700 hover:to-pink-700 shadow-md font-bold transition-all transform hover:scale-105 active:scale-95 ml-2">Вихід</button>
                        </>
                    ) : (
                        <>
                            <Link to="/login" className="text-slate-300 hover:text-white px-3 py-2 rounded-xl hover:bg-slate-800 transition-colors font-medium">Вхід</Link>
                            <Link to="/register" className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-4 py-2 rounded-xl hover:from-blue-700 hover:to-indigo-700 shadow-md font-bold transition-all transform hover:scale-105 active:scale-95">Реєстрація</Link>
                        </>
                    )}
                </div>
            </div>
        </nav>
    );
}

function App() {
    return (
        <Router>
            <div className="min-h-screen w-full flex flex-col bg-slate-950 text-slate-100 font-sans m-0 p-0">
                <Navigation />
                <main className="flex-grow w-full bg-slate-950 p-6 md:p-12">
                    <div className="container mx-auto">
                        <Routes>
                            <Route path="/" element={<Navigate to="/tasks" />} />
                            <Route path="/login" element={<Login />} />
                            <Route path="/register" element={<Register />} />
                            <Route path="/profile" element={<Profile />} />
                            <Route path="/about" element={<About />} />
                            <Route path="/tasks" element={<Tasks />} />
                            <Route path="/admin" element={<Admin />} />
                        </Routes>
                    </div>
                </main>
            </div>
        </Router>
    );
}

export default App;