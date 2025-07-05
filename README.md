# Runway & Rivets eBay Lister

An intelligent, AI-powered eBay listing automation tool designed for vintage and collectible inventory management. Built with user experience at the forefront, allowing users to use their own AI providers and control their own costs.

## 🚀 Features

### Core Functionality
- **AI-Enhanced Listings**: Automatically generate compelling titles, descriptions, and metadata from product images
- **Multi-AI Provider Support**: Use OpenAI GPT-4 Vision, Claude 3 Vision, Google Gemini, or custom providers
- **User-Controlled Costs**: Connect your own AI provider accounts - you control your usage and costs
- **Free-Only Mode**: Automatically cycle through your free AI quotas to minimize costs
- **eBay API Integration**: Direct integration with eBay's Inventory and Trading APIs
- **Batch Processing**: Process multiple items from CSV files with rich metadata
- **Draft Mode**: Create listings in draft mode for review before publishing

### User Experience
- **Clear Setup Guidance**: Step-by-step instructions with visual guides for API key setup
- **Always User Control**: Every action can be declined, skipped, or undone
- **Secure Storage**: API keys encrypted and stored securely
- **Usage Tracking**: Monitor your AI usage and costs
- **Flexible Configuration**: Add/remove AI providers anytime

## 💰 Business Model

- **No AI Usage Markup**: You pay your AI provider directly
- **5% Commission**: We take 5% of your eBay sale price
- **Transparent Pricing**: No hidden fees or surprise charges

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8+
- eBay Developer Account
- AI Provider Account (OpenAI, Google Gemini, Claude, etc.)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/runway-rivets-ebay-lister.git
   cd runway-rivets-ebay-lister
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your environment**
   ```bash
   cp env_example.txt .env
   # Edit .env with your eBay credentials
   ```

### AI Provider Setup

1. **Choose your AI provider(s)**
   - OpenAI GPT-4 Vision (best for detailed analysis)
   - Google Gemini (generous free tier)
   - Claude 3 Vision (safety-focused)
   - Custom providers

2. **Get your API key**
   - Follow the guided setup in the application
   - We'll open the provider's website for you
   - Copy your API key and paste it securely

3. **Enable Free-Only Mode (optional)**
   - Automatically use free quotas
   - Cycle through multiple providers
   - No surprise charges

### eBay API Setup

1. **Get eBay Developer Credentials**
   - Visit [eBay Developer Portal](https://developer.ebay.com/)
   - Create an application
   - Get your App ID, Cert ID, and Dev ID

2. **Configure in the application**
   - Enter your credentials when prompted
   - Complete OAuth authentication

## 📖 Usage

### Basic Usage

1. **Start the application**
   ```bash
   python ebay_lister.py
   ```

2. **Configure your settings**
   - Set up AI providers
   - Configure eBay credentials
   - Import your inventory CSV

3. **Create listings**
   - Upload product images
   - Review AI-generated content
   - Publish to eBay

### Advanced Features

- **Batch Processing**: Process multiple items at once
- **Custom AI Prompts**: Tailor AI analysis for your niche
- **Usage Analytics**: Track your AI usage and costs
- **Backup & Restore**: Export/import your configuration

## 🔧 Configuration

### AI Provider Configuration
```python
# Example configuration
{
    "user_id": "your_email",
    "ai_providers": {
        "openai": "sk-...",
        "google": "AIza...",
        "anthropic": "sk-ant-..."
    },
    "preferences": {
        "free_only_mode": true,
        "auto_enhance_listings": true,
        "draft_mode": true
    }
}
```

### eBay Configuration
```python
{
    "ebay_app_id": "your-app-id",
    "ebay_cert_id": "your-cert-id", 
    "ebay_dev_id": "your-dev-id",
    "ebay_refresh_token": "your-refresh-token"
}
```

## 🏗️ Architecture

### Core Components
- **AI Provider Manager**: Handles multiple AI providers and usage tracking
- **User Configuration Manager**: Secure storage and management of user settings
- **eBay API Client**: Integration with eBay's APIs
- **Image Analysis Engine**: AI-powered image processing and metadata extraction
- **Listing Generator**: Creates optimized eBay listings

### Security Features
- **Encrypted Storage**: All sensitive data encrypted at rest
- **Secure Key Management**: API keys never logged or exposed
- **User Isolation**: Each user's data is completely separate
- **Audit Logging**: Track all actions for security and debugging

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [Wiki](https://github.com/yourusername/runway-rivets-ebay-lister/wiki)
- **Issues**: [GitHub Issues](https://github.com/yourusername/runway-rivets-ebay-lister/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/runway-rivets-ebay-lister/discussions)

## 🔗 Lovable Integration

This project is designed to integrate with [Lovable](https://lovable.dev/) for UI/UX development and testing. The modular architecture allows for easy frontend integration while maintaining the robust backend functionality.

### Lovable Features
- **User Experience Testing**: Test the AI setup flow and user interactions
- **UI/UX Development**: Build beautiful interfaces for the listing creation process
- **User Research**: Gather feedback on the AI provider setup experience
- **A/B Testing**: Test different approaches to API key setup and user guidance

## 📊 Roadmap

- [ ] Web UI with drag-and-drop image upload
- [ ] Mobile app for on-the-go listing creation
- [ ] Advanced AI prompt customization
- [ ] Integration with more AI providers
- [ ] Real-time listing analytics
- [ ] Automated pricing optimization
- [ ] Multi-marketplace support (Amazon, Etsy, etc.)

## 🙏 Acknowledgments

- eBay Developer Program for API access
- AI providers for their powerful vision APIs
- Lovable for UI/UX development support
- Open source community for inspiration and tools 