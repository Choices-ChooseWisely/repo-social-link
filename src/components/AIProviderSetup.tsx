
import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Zap, ExternalLink, CheckCircle, AlertCircle, Eye, EyeOff } from 'lucide-react';
import { apiEndpoints } from '@/config/api';
import { toast } from 'sonner';

interface AIProviderSetupProps {
  userId: string;
  onSetupComplete: () => void;
}

const AIProviderSetup: React.FC<AIProviderSetupProps> = ({ userId, onSetupComplete }) => {
  const [selectedProvider, setSelectedProvider] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [showApiKey, setShowApiKey] = useState(false);
  const [isValidating, setIsValidating] = useState(false);
  const [isSaving, setIsSaving] = useState(false);

  // Get AI setup information
  const { data: setupInfo } = useQuery({
    queryKey: ['aiSetup'],
    queryFn: async () => {
      const response = await fetch(apiEndpoints.getAISetup);
      if (!response.ok) throw new Error('Failed to fetch AI setup');
      return response.json();
    }
  });

  // Get current user AI provider
  const { data: currentProvider, refetch } = useQuery({
    queryKey: ['userAI', userId],
    queryFn: async () => {
      const response = await fetch(apiEndpoints.getUserAIProvider(userId));
      if (!response.ok) return null;
      return response.json();
    },
    enabled: !!userId
  });

  const validateApiKey = async () => {
    if (!selectedProvider || !apiKey.trim()) {
      toast.error('Please select a provider and enter an API key');
      return;
    }

    setIsValidating(true);
    
    try {
      const response = await fetch(apiEndpoints.validateAIKey, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          provider: selectedProvider,
          api_key: apiKey.trim(),
        }),
      });

      const data = await response.json();

      if (response.ok && data.is_valid) {
        toast.success('API key format is valid!');
        return true;
      } else {
        toast.error(data.message || 'Invalid API key format');
        return false;
      }
    } catch (error) {
      console.error('Error validating API key:', error);
      toast.error('Failed to validate API key');
      return false;
    } finally {
      setIsValidating(false);
    }
  };

  const saveProvider = async () => {
    const isValid = await validateApiKey();
    if (!isValid) return;

    setIsSaving(true);
    
    try {
      const response = await fetch(apiEndpoints.setUserAIProvider(userId), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          provider: selectedProvider,
          api_key: apiKey.trim(),
        }),
      });

      const data = await response.json();

      if (response.ok) {
        toast.success(`${selectedProvider.toUpperCase()} AI provider configured successfully!`);
        refetch();
        onSetupComplete();
        setApiKey('');
      } else {
        throw new Error(data.error || 'Failed to save AI provider');
      }
    } catch (error) {
      console.error('Error saving AI provider:', error);
      toast.error(error instanceof Error ? error.message : 'Failed to save AI provider');
    } finally {
      setIsSaving(false);
    }
  };

  const providerInstructions = setupInfo?.instructions || {};

  return (
    <div className="space-y-6">
      {/* Current Provider Status */}
      {currentProvider?.provider && (
        <Card className="bg-green-50 border-green-200">
          <CardContent className="pt-6">
            <div className="flex items-center">
              <CheckCircle className="w-5 h-5 text-green-600 mr-3" />
              <div>
                <p className="font-medium text-green-900">
                  AI Provider Configured
                </p>
                <p className="text-sm text-green-700">
                  Currently using {currentProvider.provider.toUpperCase()} AI
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* AI Provider Setup */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Zap className="w-5 h-5 mr-2" />
            AI Provider Setup
          </CardTitle>
          <CardDescription>
            Choose your preferred AI provider to enhance your eBay listings with intelligent descriptions and titles.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Provider Selection */}
          <div className="space-y-2">
            <Label htmlFor="provider">Select AI Provider</Label>
            <Select value={selectedProvider} onValueChange={setSelectedProvider}>
              <SelectTrigger>
                <SelectValue placeholder="Choose an AI provider" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="openai">OpenAI (GPT-4)</SelectItem>
                <SelectItem value="claude">Anthropic Claude</SelectItem>
                <SelectItem value="gemini">Google Gemini</SelectItem>
                <SelectItem value="ollama">Local Ollama</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Provider Info */}
          {selectedProvider && providerInstructions[selectedProvider] && (
            <Card className="bg-blue-50 border-blue-200">
              <CardContent className="pt-4">
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <h4 className="font-medium text-blue-900">
                      {providerInstructions[selectedProvider].name}
                    </h4>
                    <Badge variant={providerInstructions[selectedProvider].free_tier.includes('free') ? 'default' : 'secondary'}>
                      {providerInstructions[selectedProvider].free_tier.includes('free') ? 'Free Available' : 'Paid'}
                    </Badge>
                  </div>
                  
                  <p className="text-sm text-blue-700">
                    {providerInstructions[selectedProvider].instructions}
                  </p>
                  
                  <div className="flex items-center text-sm text-blue-600">
                    <span className="mr-2">Key format: {providerInstructions[selectedProvider].format}</span>
                  </div>
                  
                  <Button
                    variant="outline"
                    size="sm"
                    className="text-blue-600 border-blue-200 hover:bg-blue-100"
                    onClick={() => window.open(providerInstructions[selectedProvider].url, '_blank')}
                  >
                    Get API Key
                    <ExternalLink className="w-3 h-3 ml-1" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          )}

          {/* API Key Input */}
          {selectedProvider && (
            <div className="space-y-2">
              <Label htmlFor="apiKey">API Key</Label>
              <div className="relative">
                <Input
                  id="apiKey"
                  type={showApiKey ? 'text' : 'password'}
                  placeholder={`Enter your ${selectedProvider.toUpperCase()} API key`}
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                  className="pr-10"
                />
                <button
                  type="button"
                  onClick={() => setShowApiKey(!showApiKey)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                >
                  {showApiKey ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
              <p className="text-xs text-gray-500">
                Your API key is stored securely and encrypted
              </p>
            </div>
          )}

          {/* Action Buttons */}
          {selectedProvider && apiKey && (
            <div className="flex space-x-3">
              <Button
                onClick={validateApiKey}
                variant="outline"
                disabled={isValidating}
              >
                {isValidating ? (
                  <>
                    <div className="w-4 h-4 border-2 border-gray-400 border-t-transparent rounded-full animate-spin mr-2" />
                    Validating...
                  </>
                ) : (
                  <>
                    <AlertCircle className="w-4 h-4 mr-2" />
                    Validate Key
                  </>
                )}
              </Button>
              
              <Button
                onClick={saveProvider}
                disabled={isSaving}
                className="bg-blue-600 hover:bg-blue-700"
              >
                {isSaving ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2" />
                    Saving...
                  </>
                ) : (
                  <>
                    <CheckCircle className="w-4 h-4 mr-2" />
                    Save Provider
                  </>
                )}
              </Button>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Feature Benefits */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Why Use AI Enhancement?</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <h4 className="font-medium text-gray-900">Intelligent Titles</h4>
              <p className="text-sm text-gray-600">
                AI analyzes your images to create compelling, keyword-rich titles that attract buyers
              </p>
            </div>
            
            <div className="space-y-2">
              <h4 className="font-medium text-gray-900">Detailed Descriptions</h4>
              <p className="text-sm text-gray-600">
                Generate comprehensive descriptions highlighting key features and selling points
              </p>
            </div>
            
            <div className="space-y-2">
              <h4 className="font-medium text-gray-900">Category Detection</h4>
              <p className="text-sm text-gray-600">
                Automatically suggest the best eBay categories for your vintage items
              </p>
            </div>
            
            <div className="space-y-2">
              <h4 className="font-medium text-gray-900">Price Optimization</h4>
              <p className="text-sm text-gray-600">
                Get AI-powered pricing suggestions based on market analysis
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default AIProviderSetup;
