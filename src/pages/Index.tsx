
import React, { useState, useEffect } from 'react';
import Dashboard from '@/components/Dashboard';
import UserSetup from '@/components/UserSetup';

const Index = () => {
  const [currentUser, setCurrentUser] = useState<string | null>(null);

  // Check if user exists in localStorage on mount
  useEffect(() => {
    const savedUser = localStorage.getItem('runway_rivets_user');
    if (savedUser) {
      setCurrentUser(savedUser);
    }
  }, []);

  const handleUserCreated = (userId: string) => {
    localStorage.setItem('runway_rivets_user', userId);
    setCurrentUser(userId);
  };

  const handleUserChange = (userId: string | null) => {
    if (userId) {
      localStorage.setItem('runway_rivets_user', userId);
    } else {
      localStorage.removeItem('runway_rivets_user');
    }
    setCurrentUser(userId);
  };

  if (!currentUser) {
    return <UserSetup onUserCreated={handleUserCreated} />;
  }

  return (
    <Dashboard 
      userId={currentUser} 
      onUserChange={handleUserChange}
    />
  );
};

export default Index;
