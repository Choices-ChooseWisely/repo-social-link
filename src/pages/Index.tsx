
import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { Camera, Zap, Package, ArrowRight, CheckCircle } from 'lucide-react';
import { toast } from 'sonner';
import UserSetup from '@/components/UserSetup';
import Dashboard from '@/components/Dashboard';

const Index = () => {
  const [currentUser, setCurrentUser] = useState<string | null>(null);
  const [showSetup, setShowSetup] = useState(false);

  useEffect(() => {
    // Check if user exists in localStorage
    const savedUser = localStorage.getItem('pictopost_user');
    if (savedUser) {
      setCurrentUser(savedUser);
    }
  }, []);

  const handleUserCreated = (userId: string) => {
    setCurrentUser(userId);
    localStorage.setItem('pictopost_user', userId);
    toast.success('Welcome to PictoPost!');
  };

  const handleUserChange = (userId: string | null) => {
    setCurrentUser(userId);
    if (userId) {
      localStorage.setItem('pictopost_user', userId);
    } else {
      localStorage.removeItem('pictopost_user');
    }
  };

  // Show main dashboard if user is logged in
  if (currentUser) {
    return <Dashboard userId={currentUser} onUserChange={handleUserChange} />;
  }

  // Show setup modal if requested
  if (showSetup) {
    return (
      <UserSetup
        onUserCreated={handleUserCreated}
        onCancel={() => setShowSetup(false)}
      />
    );
  }

  // Show landing page
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Header */}
      <div className="bg-white/80 backdrop-blur-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg flex items-center justify-center">
                <Camera className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">PictoPost</h1>
                <p className="text-sm text-gray-500">From picture to posting</p>
              </div>
            </div>
            <Button 
              onClick={() => setShowSetup(true)}
              className="bg-blue-600 hover:bg-blue-700"
            >
              Get Started
              <ArrowRight className="w-4 h-4 ml-2" />
            </Button>
          </div>
        </div>
      </div>

      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-6 py-16">
        <div className="text-center mb-16">
          <h2 className="text-5xl font-bold text-gray-900 mb-6">
            AI-Powered eBay Listing
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600"> Automation</span>
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
            Transform your vintage items into compelling eBay listings with just a photo. 
            Our AI analyzes your images and creates professional titles, descriptions, and pricing suggestions.
          </p>
          <div className="flex items-center justify-center space-x-4">
            <Badge variant="outline" className="px-4 py-2">
              <Zap className="w-4 h-4 mr-2" />
              AI-Enhanced
            </Badge>
            <Badge variant="outline" className="px-4 py-2">
              <Package className="w-4 h-4 mr-2" />
              eBay Ready
            </Badge>
            <Badge variant="outline" className="px-4 py-2">
              <Camera className="w-4 h-4 mr-2" />
              Photo to Post
            </Badge>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
          <Card className="border-0 shadow-lg bg-white/80 backdrop-blur-sm">
            <CardHeader>
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <Camera className="w-6 h-6 text-blue-600" />
              </div>
              <CardTitle>Smart Image Analysis</CardTitle>
              <CardDescription>
                Upload photos of your vintage items and let AI identify key features, condition, and marketable details
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="border-0 shadow-lg bg-white/80 backdrop-blur-sm">
            <CardHeader>
              <div className="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center mb-4">
                <Zap className="w-6 h-6 text-indigo-600" />
              </div>
              <CardTitle>AI-Generated Content</CardTitle>
              <CardDescription>
                Automatically create compelling titles, detailed descriptions, and suggest optimal pricing for maximum sales
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="border-0 shadow-lg bg-white/80 backdrop-blur-sm">
            <CardHeader>
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
                <Package className="w-6 h-6 text-purple-600" />
              </div>
              <CardTitle>eBay Integration</CardTitle>
              <CardDescription>
                Seamlessly post to eBay with pre-filled listings, proper categorization, and optimized for search visibility
              </CardDescription>
            </CardHeader>
          </Card>
        </div>

        {/* How It Works */}
        <div className="bg-white/60 backdrop-blur-sm rounded-2xl p-8 mb-16">
          <h3 className="text-3xl font-bold text-center text-gray-900 mb-12">How It Works</h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-white">1</span>
              </div>
              <h4 className="font-semibold text-gray-900 mb-2">Upload Photos</h4>
              <p className="text-gray-600 text-sm">Take or upload clear photos of your vintage items</p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-indigo-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-white">2</span>
              </div>
              <h4 className="font-semibold text-gray-900 mb-2">AI Analysis</h4>
              <p className="text-gray-600 text-sm">Our AI analyzes images and generates listing content</p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-white">3</span>
              </div>
              <h4 className="font-semibold text-gray-900 mb-2">Review & Edit</h4>
              <p className="text-gray-600 text-sm">Review AI-generated content and make adjustments</p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-green-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-white">4</span>
              </div>
              <h4 className="font-semibold text-gray-900 mb-2">Post to eBay</h4>
              <p className="text-gray-600 text-sm">Publish your optimized listing directly to eBay</p>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="text-center">
          <Card className="border-0 shadow-xl bg-gradient-to-r from-blue-600 to-indigo-600 text-white max-w-2xl mx-auto">
            <CardContent className="p-12">
              <h3 className="text-3xl font-bold mb-4">Ready to Get Started?</h3>
              <p className="text-blue-100 text-lg mb-8">
                Join thousands of sellers using AI to create better eBay listings and increase sales.
              </p>
              <Button 
                onClick={() => setShowSetup(true)}
                size="lg"
                className="bg-white text-blue-600 hover:bg-gray-100 px-8 py-4 text-lg font-semibold"
              >
                Start Your First Listing
                <ArrowRight className="w-5 h-5 ml-2" />
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Footer */}
      <div className="bg-white/80 backdrop-blur-sm border-t border-gray-200 mt-20">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <div className="text-center text-gray-500">
            <p>&copy; 2025 PictoPost. Powered by AI for vintage eBay sellers.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Index;
