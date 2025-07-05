
import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Camera, Settings, LogOut, Plus, Upload, Zap, Package } from 'lucide-react';
import { toast } from 'sonner';
import { supabase } from '@/integrations/supabase/client';
import type { User, Listing } from '@/types/database';

interface DashboardProps {
  userId: string;
  onUserChange: (userId: string | null) => void;
}

const Dashboard: React.FC<DashboardProps> = ({ userId, onUserChange }) => {
  const [userData, setUserData] = useState<User | null>(null);
  const [listings, setListings] = useState<Listing[]>([]);
  const [showAISetup, setShowAISetup] = useState(false);
  const [showImageUpload, setShowImageUpload] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadUserData();
    loadListings();
  }, [userId]);

  const loadUserData = async () => {
    try {
      const { data, error } = await supabase
        .from('users' as any)
        .select('*')
        .eq('id', userId)
        .single();

      if (error) {
        console.error('Error loading user data:', error);
        return;
      }

      setUserData(data);
    } catch (error) {
      console.error('Error loading user data:', error);
    }
  };

  const loadListings = async () => {
    try {
      const { data, error } = await supabase
        .from('listings' as any)
        .select('*')
        .eq('user_id', userId)
        .order('created_at', { ascending: false });

      if (error) {
        console.error('Error loading listings:', error);
        return;
      }

      setListings(data || []);
    } catch (error) {
      console.error('Error loading listings:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    onUserChange(null);
    toast.success('Logged out successfully');
  };

  const handleAISetupComplete = () => {
    setShowAISetup(false);
    loadUserData();
    toast.success('AI provider configured successfully!');
  };

  const handleImageUploadComplete = () => {
    setShowImageUpload(false);
    loadListings();
    toast.success('Listing created successfully!');
  };

  // For now, we'll show placeholder components instead of the missing ones
  if (showAISetup) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <Card className="w-full max-w-md">
          <CardHeader>
            <CardTitle>AI Provider Setup</CardTitle>
            <CardDescription>This feature is coming soon</CardDescription>
          </CardHeader>
          <CardContent>
            <Button onClick={() => setShowAISetup(false)}>Back to Dashboard</Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (showImageUpload) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <Card className="w-full max-w-md">
          <CardHeader>
            <CardTitle>Image Upload</CardTitle>
            <CardDescription>This feature is coming soon</CardDescription>
          </CardHeader>
          <CardContent>
            <Button onClick={() => setShowImageUpload(false)}>Back to Dashboard</Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
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
                <p className="text-sm text-gray-500">Welcome back, {userData?.name || userId}</p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowAISetup(true)}
              >
                <Settings className="w-4 h-4 mr-2" />
                AI Setup
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={handleLogout}
              >
                <LogOut className="w-4 h-4 mr-2" />
                Logout
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Listings</CardTitle>
              <Package className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{listings.length}</div>
              <p className="text-xs text-muted-foreground">
                All time listings created
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Active Listings</CardTitle>
              <Zap className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {listings.filter(l => l.status === 'active').length}
              </div>
              <p className="text-xs text-muted-foreground">
                Currently listed on eBay
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">AI Provider</CardTitle>
              <Settings className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {userData?.ai_provider ? (
                  <Badge variant="outline">{userData.ai_provider}</Badge>
                ) : (
                  <span className="text-gray-400">Not Set</span>
                )}
              </div>
              <p className="text-xs text-muted-foreground">
                Current AI configuration
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 mb-8">
          <Button
            onClick={() => setShowImageUpload(true)}
            className="bg-blue-600 hover:bg-blue-700 flex-1 sm:flex-none"
            size="lg"
          >
            <Plus className="w-5 h-5 mr-2" />
            Create New Listing
          </Button>
          
          {!userData?.ai_provider && (
            <Button
              onClick={() => setShowAISetup(true)}
              variant="outline"
              size="lg"
              className="flex-1 sm:flex-none"
            >
              <Settings className="w-5 h-5 mr-2" />
              Setup AI Provider
            </Button>
          )}
        </div>

        {/* Listings Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
          {listings.length === 0 ? (
            <Card className="col-span-full">
              <CardContent className="flex flex-col items-center justify-center py-12">
                <Upload className="w-12 h-12 text-gray-400 mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">No listings yet</h3>
                <p className="text-gray-500 text-center mb-6">
                  Upload your first image to create an AI-enhanced eBay listing
                </p>
                <Button onClick={() => setShowImageUpload(true)}>
                  <Plus className="w-4 h-4 mr-2" />
                  Create Your First Listing
                </Button>
              </CardContent>
            </Card>
          ) : (
            listings.map((listing) => (
              <Card key={listing.id} className="overflow-hidden">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <CardTitle className="text-lg line-clamp-2">{listing.title}</CardTitle>
                      <CardDescription className="mt-1">
                        {listing.category && (
                          <Badge variant="secondary" className="mr-2">{listing.category}</Badge>
                        )}
                        <Badge variant={listing.status === 'active' ? 'default' : 'outline'}>
                          {listing.status}
                        </Badge>
                      </CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  {listing.description && (
                    <p className="text-sm text-gray-600 mb-3 line-clamp-3">{listing.description}</p>
                  )}
                  
                  <div className="flex items-center justify-between text-sm text-gray-500">
                    <span>
                      {listing.condition && `${listing.condition} • `}
                      {listing.estimated_price && `$${listing.estimated_price}`}
                    </span>
                    <span>{listing.created_at ? new Date(listing.created_at).toLocaleDateString() : ''}</span>
                  </div>
                  
                  {listing.image_urls && Array.isArray(listing.image_urls) && listing.image_urls.length > 0 && (
                    <div className="mt-3 text-xs text-gray-500">
                      {listing.image_urls.length} image{listing.image_urls.length > 1 ? 's' : ''}
                    </div>
                  )}
                </CardContent>
              </Card>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
