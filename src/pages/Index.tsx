
import React, { useState, useEffect } from 'react';
import Dashboard from '@/components/Dashboard';
import UserSetup from '@/components/UserSetup';
import SplashPage from '@/components/SplashPage';

const Index = () => {
  const [currentUser, setCurrentUser] = useState<string | null>(null);
  const [showSplash, setShowSplash] = useState(true);

  // Check if user exists in localStorage on mount
  useEffect(() => {
    const savedUser = localStorage.getItem('runway_rivets_user');
    if (savedUser) {
      setCurrentUser(savedUser);
      setShowSplash(false); // Skip splash if user already exists
    }
  }, []);

  const handleUserCreated = (userId: string) => {
    localStorage.setItem('runway_rivets_user', userId);
    setCurrentUser(userId);
    setShowSplash(false);
  };

  const handleUserChange = (userId: string | null) => {
    if (userId) {
      localStorage.setItem('runway_rivets_user', userId);
    } else {
      localStorage.removeItem('runway_rivets_user');
    }
    setCurrentUser(userId);
  };

  const handleGetStarted = () => {
    setShowSplash(false);
  };

  const handleLogin = () => {
    // For now, this will just take them to the user setup
    // In a real app, this would show a login form
    setShowSplash(false);
  };

  // Show splash page first
  if (showSplash) {
    return <SplashPage onGetStarted={handleGetStarted} onLogin={handleLogin} />;
  }

  // Show user setup if no current user
  if (!currentUser) {
    return <UserSetup onUserCreated={handleUserCreated} />;
  }

  // Show main dashboard
  return (
    <Dashboard 
      userId={currentUser} 
      onUserChange={handleUserChange}
    />
  );
};

export default Index;
