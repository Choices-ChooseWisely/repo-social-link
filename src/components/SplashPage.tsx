import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Upload, Zap, Eye, DollarSign, FileText, ArrowRight, Sparkles, Bot, Clock } from 'lucide-react';

interface SplashPageProps {
  onGetStarted: () => void;
  onLogin: () => void;
}

const SplashPage: React.FC<SplashPageProps> = ({ onGetStarted, onLogin }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [isAnimating, setIsAnimating] = useState(false);

  const demoSteps = [
    {
      id: 'upload',
      title: 'Upload Your Item Photo',
      description: 'Simply drag & drop or click to upload',
      icon: Upload,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
      borderColor: 'border-blue-200'
    },
    {
      id: 'analyze',
      title: 'AI Analyzes Your Item',
      description: 'Advanced computer vision identifies details',
      icon: Eye,
      color: 'text-purple-600',
      bgColor: 'bg-purple-50',
      borderColor: 'border-purple-200'
    },
    {
      id: 'generate',
      title: 'Generate Perfect Listing',
      description: 'AI creates title, description & pricing',
      icon: FileText,
      color: 'text-green-600',
      bgColor: 'bg-green-50',
      borderColor: 'border-green-200'
    },
    {
      id: 'publish',
      title: 'Ready to List on eBay',
      description: 'Professional listing ready in seconds',
      icon: Zap,
      color: 'text-orange-600',
      bgColor: 'bg-orange-50',
      borderColor: 'border-orange-200'
    }
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setIsAnimating(true);
      setTimeout(() => {
        setCurrentStep((prev) => (prev + 1) % demoSteps.length);
        setIsAnimating(false);
      }, 300);
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  const mockData = {
    image: '/placeholder.svg',
    title: 'Vintage 1960s Omega Seamaster Watch',
    description: 'Beautiful vintage Omega Seamaster in excellent condition. Features original bracelet, automatic movement, and distinctive dial design. A true collector\'s piece with timeless appeal.',
    price: '$1,245'
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900 relative overflow-hidden">
      {/* Animated background particles */}
      <div className="absolute inset-0">
        {[...Array(50)].map((_, i) => (
          <div
            key={i}
            className="absolute w-1 h-1 bg-blue-300 rounded-full animate-pulse"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 3}s`,
              animationDuration: `${2 + Math.random() * 3}s`
            }}
          />
        ))}
      </div>

      <div className="relative z-10 container mx-auto px-6 py-12">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="flex items-center justify-center mb-6">
            <div className="relative">
              <div className="w-16 h-16 bg-gradient-to-r from-blue-400 to-purple-600 rounded-full flex items-center justify-center">
                <Bot className="w-8 h-8 text-white" />
              </div>
              <div className="absolute -top-1 -right-1 w-6 h-6 bg-green-400 rounded-full flex items-center justify-center">
                <Sparkles className="w-3 h-3 text-white" />
              </div>
            </div>
          </div>
          
          <h1 className="text-5xl md:text-6xl font-bold text-white mb-4">
            Runway & <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400">Rivets</span>
          </h1>
          <p className="text-xl text-blue-100 mb-2">AI-Powered eBay Listing Automation</p>
          <p className="text-lg text-blue-200 opacity-90">
            Transform your vintage items into professional eBay listings in seconds
          </p>
        </div>

        {/* Demo Workflow */}
        <div className="max-w-6xl mx-auto mb-16">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            {/* Demo Steps */}
            <div className="space-y-6">
              <div className="text-center lg:text-left mb-8">
                <h2 className="text-3xl font-bold text-white mb-2">See It In Action</h2>
                <p className="text-blue-200">Watch how AI transforms your photos into perfect listings</p>
              </div>

              {demoSteps.map((step, index) => {
                const Icon = step.icon;
                const isActive = index === currentStep;
                const isPast = index < currentStep;
                
                return (
                  <div
                    key={step.id}
                    className={`flex items-center space-x-4 p-4 rounded-lg transition-all duration-500 ${
                      isActive
                        ? `${step.bgColor} ${step.borderColor} border-2 scale-105`
                        : isPast
                        ? 'bg-gray-800 border border-gray-600'
                        : 'bg-gray-800/50 border border-gray-700'
                    } ${isAnimating && isActive ? 'animate-pulse' : ''}`}
                  >
                    <div className={`w-12 h-12 rounded-full flex items-center justify-center ${
                      isActive ? step.bgColor : isPast ? 'bg-green-100' : 'bg-gray-700'
                    }`}>
                      <Icon className={`w-6 h-6 ${
                        isActive ? step.color : isPast ? 'text-green-600' : 'text-gray-400'
                      }`} />
                    </div>
                    
                    <div className="flex-1">
                      <h3 className={`font-semibold ${
                        isActive ? 'text-gray-900' : 'text-white'
                      }`}>
                        {step.title}
                      </h3>
                      <p className={`text-sm ${
                        isActive ? 'text-gray-600' : 'text-gray-300'
                      }`}>
                        {step.description}
                      </p>
                    </div>
                    
                    {isActive && (
                      <div className="flex items-center space-x-1">
                        <Clock className="w-4 h-4 text-blue-600 animate-spin" />
                        <span className="text-xs text-blue-600 font-medium">Processing</span>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>

            {/* Mock Result Display */}
            <div className="lg:pl-8">
              <Card className="bg-white/95 backdrop-blur-sm shadow-2xl border-0">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-lg">Generated eBay Listing</CardTitle>
                    <Badge className="bg-green-100 text-green-800">
                      <Zap className="w-3 h-3 mr-1" />
                      AI Generated
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="aspect-square bg-gray-100 rounded-lg overflow-hidden">
                    <img
                      src={mockData.image}
                      alt="Demo item"
                      className="w-full h-full object-cover"
                    />
                  </div>
                  
                  <div>
                    <h3 className="font-bold text-lg text-gray-900 mb-2">
                      {mockData.title}
                    </h3>
                    <p className="text-gray-600 text-sm leading-relaxed mb-3">
                      {mockData.description}
                    </p>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <DollarSign className="w-5 h-5 text-green-600" />
                        <span className="text-2xl font-bold text-green-600">
                          {mockData.price}
                        </span>
                      </div>
                      <Badge variant="outline" className="text-blue-600 border-blue-200">
                        Market Optimized
                      </Badge>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>

        {/* Call to Actions */}
        <div className="max-w-4xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* New Users */}
            <Card className="bg-white/10 backdrop-blur-sm border-white/20 text-white">
              <CardHeader className="text-center">
                <div className="w-12 h-12 bg-gradient-to-r from-green-400 to-blue-500 rounded-full mx-auto mb-4 flex items-center justify-center">
                  <Sparkles className="w-6 h-6 text-white" />
                </div>
                <CardTitle className="text-xl">New to Runway & Rivets?</CardTitle>
                <CardDescription className="text-blue-100">
                  Start with free credits - no subscription required
                </CardDescription>
              </CardHeader>
              <CardContent className="text-center">
                <div className="mb-6">
                  <div className="text-3xl font-bold mb-2">5 Free Credits</div>
                  <p className="text-sm text-blue-200">
                    Generate up to 5 AI-powered listings to try our service
                  </p>
                </div>
                <Button 
                  onClick={onGetStarted}
                  className="w-full bg-gradient-to-r from-green-500 to-blue-600 hover:from-green-600 hover:to-blue-700 text-white border-0"
                  size="lg"
                >
                  Start Free Trial
                  <ArrowRight className="w-4 h-4 ml-2" />
                </Button>
              </CardContent>
            </Card>

            {/* Existing Users */}
            <Card className="bg-white/10 backdrop-blur-sm border-white/20 text-white">
              <CardHeader className="text-center">
                <div className="w-12 h-12 bg-gradient-to-r from-purple-400 to-pink-500 rounded-full mx-auto mb-4 flex items-center justify-center">
                  <Bot className="w-6 h-6 text-white" />
                </div>
                <CardTitle className="text-xl">Already a Subscriber?</CardTitle>
                <CardDescription className="text-blue-100">
                  Access your full AI-powered listing suite
                </CardDescription>
              </CardHeader>
              <CardContent className="text-center">
                <div className="mb-6">
                  <div className="text-3xl font-bold mb-2">Unlimited Access</div>
                  <p className="text-sm text-blue-200">
                    Generate unlimited listings with premium AI features
                  </p>
                </div>
                <Button 
                  onClick={onLogin}
                  variant="outline"
                  className="w-full border-white/30 text-white hover:bg-white/10"
                  size="lg"
                >
                  Login to Continue
                  <ArrowRight className="w-4 h-4 ml-2" />
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Features Footer */}
        <div className="mt-16 text-center">
          <div className="flex flex-wrap justify-center gap-6 text-blue-200">
            {[
              'Advanced Computer Vision',
              'Market Price Analysis',
              'SEO-Optimized Titles',
              'Professional Descriptions',
              'Direct eBay Integration'
            ].map((feature, index) => (
              <div key={index} className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-blue-400 rounded-full"></div>
                <span className="text-sm">{feature}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SplashPage;
