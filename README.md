# xProxy: Personalized Auto-Reply Bot for X Mentions

**xProxy** is a FastAPI-based bot that automatically replies to mentions on X (formerly Twitter) with personalized responses. It integrates web scraping, natural language processing, and caching to deliver context-aware interactions.

## ✨ Features

* **FastAPI Backend**: Handles incoming requests and orchestrates the reply workflow.
* **Web Scraping**: Utilizes Selenium and BeautifulSoup to extract mention data and metadata.
* **Personalized Replies**: Generates context-aware responses using the Gemini API.
* **X Integration**: Employs Tweepy to post replies directly to mentions on X.
* **Caching Mechanism**: Implements Redis write-through caching to prevent duplicate replies, with PostgreSQL as a fallback.

## 📂 Project Structure

```
xProxy/
├── bot/                   # Core bot logic and FastAPI routes
├── db/                    # Database models and SQLAlchemy setup
├── personalize_reply/     # Gemini API integration for generating replies
├── redisconfig/           # Redis caching configuration
├── scraper/               # Selenium and BeautifulSoup scraping scripts
├── main.py                # Entry point to start the FastAPI application
├── x_bot.py               # Bot initialization and orchestration
├── requirements.txt       # Python dependencies
└── .gitignore             # Git ignore file
```

## ⚒️ Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/ac8628026/xProxy.git
   cd xProxy
   ```

2. **Create and activate a virtual environment**:

   ```bash
   python -m venv venv
   venv\Scripts\activate  
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory and add your configuration settings, such as API keys and database URLs.

5. **Run the application**:

   ```bash
   python main.py
   ```

## ⚙️ Configuration

* **PostgreSQL**: Ensure you have a PostgreSQL database set up. Update the connection string in your `.env` file.
* **Redis**: Install and run Redis. Configure the Redis URL in your `.env` file.
* **Gemini API**: Obtain API credentials and add them to your `.env` file.
* **Tweepy (X API)**: Set up your X developer account and add the necessary credentials to your `.env` file.
## 🌐 Browser Requirements

This bot uses Selenium with Chrome, and requires:

* **Google Chrome**: Must be installed on your system
* **ChromeDriver**: A compatible version must be available in your system PATH
* **Dedicated Profile**: Recommended to avoid interfering with your default browser session

### Setting up a dedicated Chrome profile

```bash
# Launch Chrome with the custom profile by running the following command in your cmd:
"C:\Program Files\Google\Chrome\Application\chrome.exe" --user-data-dir="C:\SeleniumProfile" --profile-directory="Default"
```
after can login manually to your X account or put the login credentials in the `.env` file.

## 📈 Future Enhancements

* **Enhanced NLP**: Incorporate more advanced natural language processing techniques for better reply generation.
* **User Interface**: Develop a dashboard to monitor bot activity and performance metrics.
* **Deployment**: Containerize the application using Docker and deploy it.

## 👍 Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

