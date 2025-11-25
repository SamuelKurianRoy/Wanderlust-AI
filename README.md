# ✈️ AI Travel Planner - Agentic System

An intelligent travel planning application powered by **Multi-Agent AI** and **Google Gemini**, featuring specialized agents that work together to create your perfect trip!

## 🤖 Features

### Multi-Agent Architecture
- **Planning Agent**: Destination research, itinerary creation, and activity recommendations
- **Travel Agent**: Flight searches, hotel recommendations, and transportation options
- **Finance Agent**: Budget planning, cost estimates, and money-saving tips
- **Search Agent**: Real-time web searches for places, restaurants, and activities
- **Gemini Orchestrator**: AI coordinator that bridges human language and agent actions

### Core Capabilities
- **AI Chat Assistant**: Natural conversation with intelligent travel agents
- **Automated Search**: AI-powered searches for flights, hotels, attractions, and more
- **Smart Itinerary Builder**: Create day-by-day schedules with AI recommendations
- **Real-time Budget Tracking**: Monitor spending with AI-generated insights
- **Complete Trip Planning**: One-click generation of comprehensive travel plans with option to apply
- **Origin & Destination Tracking**: Specify where you're traveling from and to
- **Multi-Currency Support**: Support for USD, EUR, GBP, INR, JPY, AUD, CAD
- **Interactive Packing List**: Pre-populated checklist organized by categories
- **Trip Notes**: Keep track of important information and reminders

## 📋 Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

## 🚀 Installation

1. **Clone the repository**:
```bash
git clone <your-repo-url>
cd "Wanderlust Agent"
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**:
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your Gemini API key
GEMINI_API_KEY=your_actual_api_key_here
```

## 🎯 Running the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 💡 How to Use

### 1. Initialize AI System
- Enter your Gemini API key in the sidebar
- Click "Initialize AI System"
- Wait for agents to activate (green status indicators)

### 2. Set Trip Details (Sidebar)
- Enter where you're traveling from (origin)
- Enter your destination
- Select start and end dates
- Specify number of travelers
- Set total budget and select currency (USD, EUR, GBP, INR, JPY, AUD, CAD)

### 3. Use AI Assistant (Tab 1)
Chat naturally with AI agents:
- "What are the top 10 things to do in Paris?"
- "Find me budget flights from Mumbai to Tokyo in March"
- "Create a 7-day itinerary for Rome with historical sites"
- "What's the best area to stay in Barcelona?"
- "How should I split my ₹200,000 budget?"

**Quick Actions**:
- **Generate Complete Itinerary**: Full AI-generated travel plan
  - After generation, you'll be asked if you want to apply the plan
  - Choose "Yes" to make it available in other tabs for reference
  - The plan appears in Itinerary, Budget, and Travel Search tabs
- **Get Destination Tips**: Personalized recommendations
- **Budget Analysis**: Detailed financial advice

### 4. Build Manual Itinerary (Tab 2)
- View AI-generated itinerary plan (if created)
- Add activities with times and costs
- Organize by day
- Edit or delete entries as needed

### 5. Track Budget (Tab 3)
- View AI-generated budget recommendations (if created)
- View spending vs. remaining budget
- See expense breakdown by day
- Get AI-suggested allocation

### 6. AI Travel Search (Tab 4)
- View AI-generated flight and hotel options (if created)
- Search for flights, hotels, attractions
- Get AI-summarized results
- Use popular quick-search buttons (includes flights from your origin)

### 7. Packing List (Tab 5)
- Check off items as you pack
- Organized by category

### 8. Notes (Tab 6)
- Save important contacts and reminders

## 🧠 AI Agent Examples

### Planning Agent
```
"Create a 5-day romantic itinerary for Paris focusing on art and cuisine"
```

### Travel Agent
```
"Find family-friendly hotels near Disneyland Paris under $200/night"
```

### Finance Agent
```
"Break down a $5000 budget for 2 people visiting Japan for 10 days"
```

### Search Agent
```
"What are the best local restaurants in Rome's Trastevere neighborhood?"
```

## 🏗️ Architecture

```
User Input
    ↓
Gemini Orchestrator (Natural Language Processing)
    ↓
Intent Parsing & Agent Coordination
    ↓
┌─────────────┬──────────────┬───────────────┬──────────────┐
│  Planning   │   Travel     │   Finance     │    Search    │
│   Agent     │   Agent      │   Agent       │    Agent     │
└─────────────┴──────────────┴───────────────┴──────────────┘
    ↓
Combined Results & AI-Generated Response
    ↓
User Interface
```

## 📦 Technologies

- **Streamlit**: Web application framework
- **Google Gemini**: AI language model for orchestration
- **Python**: Core programming language
- **Multi-Agent System**: Specialized agents for different tasks

## 🔐 Security Notes

- Never commit your `.env` file with real API keys
- Keep your Gemini API key secure
- The `.env` file is already in `.gitignore`

## 🎨 Customization

### Add New Agents
Edit `agents.py` to create specialized agents:
```python
class CustomAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Custom Agent", role="Your role")
    
    def process(self, task, context):
        # Your logic here
        return result
```

### Modify AI Behavior
Edit `orchestrator.py` to adjust:
- Prompt templates
- Agent coordination logic
- Response formatting

## 🐛 Troubleshooting

**AI System won't initialize**:
- Check API key is valid
- Ensure internet connection
- Verify `google-generativeai` is installed

**Search not working**:
- Confirm AI system is initialized
- Set destination in sidebar
- Check API quota limits

**Import errors**:
```bash
pip install -r requirements.txt --upgrade
```

## 📝 Tips

- Be specific with AI queries for better results
- Set all trip details for more accurate recommendations
- Use quick action buttons for common tasks
- Save generated itineraries to manual tab
- Check budget breakdown before finalizing plans

## 🚀 Future Enhancements

- Real-time flight and hotel price integration
- Google Maps integration
- Weather forecasts
- Multi-language support
- Export itineraries to PDF
- Calendar integration
- Collaborative trip planning

---

**Built with ❤️ using AI Agents & Google Gemini**

Happy travels! 🌍✨
