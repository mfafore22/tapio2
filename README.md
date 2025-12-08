markdown# Tapio 2 - AI Food Delivery Price Comparison 🍕

AI assistant that compares food delivery prices across Wolt and Foodora to help you save money!

## What It Does

- Searches Wolt and Foodora simultaneously
- Compares prices for same restaurants
- Shows total cost (item + delivery)
- Provides direct order links
- Finds cheapest options

## Tech Stack

- **Python + LangChain** - AI Agent
- **Node.js** - API Gateway & Scrapers
- **OpenAI GPT-4o-mini** - Language Model
- **Docker** - Containerization

## Project Structure
```
tapio2/
├── ai-agent-service/       # Python AI Agent
│   ├── agent.py           # LangChain agent
│   ├── main.py            # FastAPI app
│   └── requirements.txt
├── scraper-service/        # Node.js Scrapers
│   └── src/
│       ├── woltScraper.js
│       └── foodoraScraper.js
├── api-gateway/            # Node.js Gateway
└── docker-compose.yml
```

## Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/mfafore22/tapio2.git
cd tapio2
```

### 2. Environment Variables

Create `ai-agent-service/.env`:
```
OPENAI_API_KEY=your_key_here
```

### 3. Run AI Agent
```bash
cd ai-agent-service
pip install -r requirements.txt
python agent.py
```

## Example Usage

**User:** "I want pizza"

**Tapio:** 
```
🍕 WOLT:
Pizza Palace - €11.90 + €2.90 delivery = €14.80

🍕 FOODORA:
Pizza Palace - €10.90 + €1.90 delivery = €12.80

💰 BEST DEAL: Foodora - Save €2.00!
📱 Order: https://www.foodora.fi/restaurant/pizza-palace
```

## API Endpoints
```bash
# Query Agent
POST /api/agent/query
{"query": "I want pizza"}

# Search Wolt
POST /api/scraper/wolt
{"query": "pizza", "location": "Helsinki"}

# Search Foodora
POST /api/scraper/foodora
{"query": "sushi", "location": "Helsinki"}
```

## Requirements

- Python 3.12+
- Node.js 18+
- OpenAI API Key
- Docker (optional)

## Roadmap

- [x] AI Agent with LangChain
- [x] Mock data for testing
- [ ] Real Wolt scraper
- [ ] Real Foodora scraper
- [ ] User accounts
- [ ] Price alerts
- [ ] Mobile app

## Author

**Michael Fafore**
- GitHub: [@mfafore22](https://github.com/mfafore22)
- Email: faforemichael001@gmail.com
- Location: Tampere, Finland

## License

MIT License

---

**Save money on every food order! 🚀**