
import React, { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Upload, Settings, Zap, Package, Plus } from 'lucide-react';
import { apiEndpoints } from '@/config/api';
import { toast } from 'sonner';
import UserSetup from './UserSetup';
import ImageUpload from './ImageUpload';
import AIProviderSetup from './AIProviderSetup';

interface DashboardProps {
  userId: string;
  onUserChange: (userId: string | null) => void;
}

const Dashboard: React.FC<DashboardProps> = ({ userId, onUserChange }) => {
  const [activeTab, setActiveTab] = useState<'upload' | 'setup' | 'listings'>('upload');
  const [uploadedImages, setUploadedImages] = useState<string[]>([]);

  // Check backend health
  const { data: healthData, isError: healthError } = useQuery({
    queryKey: ['health'],
    queryFn: async () => {
      const response = await fetch(apiEndpoints.healthCheck);
      if (!response.ok) throw new Error('Backend unavailable');
      return response.json();
    },
    retry: 2,
    refetchInterval: 30000 // Check every 30 seconds
  });

  // Get user AI provider
  const { data: userAI, refetch: refetchUserAI } = useQuery({
    queryKey: ['userAI', userId],
    queryFn: async () => {
      const response = await fetch(apiEndpoints.getUserAIProvider(userId));
      if (!response.ok) return null;
      return response.json();
    },
    enabled: !!userId
  });

  useEffect(() => {
    if (healthError) {
      toast.error('Backend is not available. Please start the Python server.');
    } else if (healthData) {
      toast.success('Connected to backend successfully!');
    }
  }, [healthData, healthError]);

  const handleImageUpload = (filename: string) => {
    setUploadedImages(prev => [...prev, filename]);
    toast.success('Image uploaded successfully!');
  };

  const handleAIProviderSetup = () => {
    refetchUserAI();
    toast.success('AI provider configured successfully!');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold text-gray-900 mb-2">
                Runway & Rivets eBay Lister
              </h1>
              <p className="text-gray-600 text-lg">
                AI-powered listing automation for vintage & collectible inventory
              </p>
            </div>
            <div className="flex items-center space-x-3">
              {healthData && (
                <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">
                  <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                  Backend Connected
                </Badge>
              )}
              {userAI?.provider && (
                <Badge variant="outline" className="bg-blue-50 text-blue-700 border-blue-200">
                  <Zap className="w-3 h-3 mr-1" />
                  {userAI.provider.toUpperCase()} AI
                </Badge>
              )}
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Sidebar Navigation */}
          <div className="lg:col-span-1">
            <Card>
              <CardHeader>
                <CardTitle className="text-sm font-medium">Navigation</CardTitle>
              </CardHeader>
              <CardContent className="p-0">
                <nav className="space-y-1">
                  <button
                    onClick={() => setActiveTab('upload')}
                    className={`w-full flex items-center px-4 py-3 text-sm text-left transition-colors ${
                      activeTab === 'upload'
                        ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-500'
                        : 'text-gray-600 hover:bg-gray-50'
                    }`}
                  >
                    <Upload className="w-4 h-4 mr-3" />
                    Upload Images
                  </button>
                  <button
                    onClick={() => setActiveTab('setup')}
                    className={`w-full flex items-center px-4 py-3 text-sm text-left transition-colors ${
                      activeTab === 'setup'
                        ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-500'
                        : 'text-gray-600 hover:bg-gray-50'
                    }`}
                  >
                    <Settings className="w-4 h-4 mr-3" />
                    AI Setup
                  </button>
                  <button
                    onClick={() => setActiveTab('listings')}
                    className={`w-full flex items-center px-4 py-3 text-sm text-left transition-colors ${
                      activeTab === 'listings'
                        ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-500'
                        : 'text-gray-600 hover:bg-gray-50'
                    }`}
                  >
                    <Package className="w-4 h-4 mr-3" />
                    My Listings
                  </button>
                </nav>
              </CardContent>
            </Card>

            {/* Quick Stats */}
            <Card className="mt-6">
              <CardHeader>
                <CardTitle className="text-sm font-medium">Quick Stats</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Images Uploaded</span>
                    <Badge variant="secondary">{uploadedImages.length}</Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">AI Provider</span>
                    <Badge variant={userAI?.provider ? "default" : "outline"}>
                      {userAI?.provider || 'Not Set'}
                    </Badge>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Main Content Area */}
          <div className="lg:col-span-3">
            {activeTab === 'upload' && (
              <ImageUpload userId={userId} onImageUpload={handleImageUpload} />
            )}
            
            {activeTab === 'setup' && (
              <AIProviderSetup userId={userId} onSetupComplete={handleAIProviderSetup} />
            )}
            
            {activeTab === 'listings' && (
              <Card>
                <CardHeader>
                  <CardTitle>My eBay Listings</CardTitle>
                  <CardDescription>
                    Manage your eBay listings and track performance
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="text-center py-12">
                    <Package className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-gray-900 mb-2">
                      No listings yet
                    </h3>
                    <p className="text-gray-500 mb-4">
                      Upload some images and create your first AI-enhanced listing
                    </p>
                    <Button 
                      onClick={() => setActiveTab('upload')}
                      className="bg-blue-600 hover:bg-blue-700"
                    >
                      <Plus className="w-4 h-4 mr-2" />
                      Create First Listing
                    </Button>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
