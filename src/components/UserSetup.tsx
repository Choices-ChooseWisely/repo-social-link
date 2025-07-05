
import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { User, ArrowRight, X } from 'lucide-react';
import { toast } from 'sonner';
import { supabase } from '@/integrations/supabase/client';

interface UserSetupProps {
  onUserCreated: (userId: string) => void;
  onCancel: () => void;
}

const UserSetup: React.FC<UserSetupProps> = ({ onUserCreated, onCancel }) => {
  const [userId, setUserId] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleCreateUser = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!userId.trim()) {
      toast.error('Please enter a user ID');
      return;
    }

    setIsLoading(true);
    
    try {
      // Check if user already exists
      const { data: existingUser } = await supabase
        .from('users')
        .select('id')
        .eq('id', userId.trim())
        .single();

      if (existingUser) {
        toast.success(`Welcome back, ${userId}!`);
        onUserCreated(userId.trim());
        return;
      }

      // Create new user
      const { data, error } = await supabase
        .from('users')
        .insert([
          {
            id: userId.trim(),
            name: userId.trim(),
            preferences: {},
            usage_stats: {}
          }
        ])
        .select();

      if (error) {
        console.error('Error creating user:', error);
        toast.error('Failed to create user account');
        return;
      }

      if (data && data.length > 0) {
        toast.success(`Welcome, ${userId}! Your account has been created.`);
        onUserCreated(userId.trim());
      }
    } catch (error) {
      console.error('Error creating user:', error);
      toast.error('Failed to create user account');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-6">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center relative">
          <Button
            variant="ghost"
            size="sm"
            className="absolute top-2 right-2"
            onClick={onCancel}
          >
            <X className="w-4 h-4" />
          </Button>
          <div className="mx-auto w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mb-4">
            <User className="w-6 h-6 text-blue-600" />
          </div>
          <CardTitle className="text-2xl font-bold">Welcome to PictoPost</CardTitle>
          <CardDescription className="text-base">
            Create your account to start listing vintage items with AI assistance
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleCreateUser} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="userId">Choose a User ID</Label>
              <Input
                id="userId"
                type="text"
                placeholder="e.g., john_collector"
                value={userId}
                onChange={(e) => setUserId(e.target.value)}
                className="h-12"
                disabled={isLoading}
              />
              <p className="text-sm text-gray-500">
                This will be used to save your preferences and AI settings
              </p>
            </div>
            
            <Button 
              type="submit" 
              className="w-full h-12 bg-blue-600 hover:bg-blue-700 text-white"
              disabled={isLoading || !userId.trim()}
            >
              {isLoading ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2" />
                  Creating Account...
                </>
              ) : (
                <>
                  Get Started
                  <ArrowRight className="w-4 h-4 ml-2" />
                </>
              )}
            </Button>
          </form>
          
          <div className="mt-6 p-4 bg-blue-50 rounded-lg">
            <h4 className="font-medium text-blue-900 mb-2">What's Next?</h4>
            <ul className="text-sm text-blue-700 space-y-1">
              <li>• Set up your preferred AI provider</li>
              <li>• Upload images of your items</li>
              <li>• Generate AI-enhanced listings</li>
              <li>• List directly to eBay</li>
            </ul>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default UserSetup;
