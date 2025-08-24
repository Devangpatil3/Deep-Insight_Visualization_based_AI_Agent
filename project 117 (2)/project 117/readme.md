📊 AI Data Visualization Agent
An intelligent Streamlit application that automatically generates data visualizations and analyses using AI. Simply upload your dataset, ask questions in natural language, and get instant insights with professional visualizations.
✨ Features

🤖 AI-Powered Analysis: Uses advanced language models to understand your data questions
📈 Automatic Visualizations: Generates appropriate charts, plots, and graphs automatically
🔒 Safe Code Execution: Runs analysis code in secure E2B sandbox environment
📊 Multiple Chart Types: Supports matplotlib, seaborn, plotly visualizations
📁 Multiple File Formats: CSV, Excel, JSON, Parquet support
🎯 Smart Data Processing: Automatic data cleaning and preprocessing
📱 User-Friendly Interface: Clean, intuitive Streamlit interface

🚀 Quick Start
Prerequisites

Python 3.8+
Together AI API key
E2B API key

Installation

Clone the repository

bashgit clone https://github.com/yourusername/ai-data-viz-agent.git
cd ai-data-viz-agent

Install dependencies

bashpip install -r requirements.txt

Set up environment variables

bashcp .env.example .env
# Edit .env and add your API keys:
# TOGETHER_API_KEY=your_together_api_key_here
# E2B_API_KEY=your_e2b_api_key_here

Run the application

bashstreamlit run app.py
🔧 Configuration
API Keys Setup

Together AI API Key

Sign up at together.ai
Generate an API key from your dashboard
Add to .env file or enter in the app sidebar


E2B API Key

Sign up at e2b.dev
Get your API key from the dashboard
Add to .env file



Model Selection
The app supports multiple AI models:

Llama 3 8B: Fast and efficient for simple visualizations
Llama 3 70B: Better for complex analysis
Mixtral 8x7B: Good balance of speed and capability
Mixtral 8x22B: Best for complex, large dataset analysis

📖 Usage

Upload Your Data

Drag and drop or click to upload CSV, Excel, JSON, or Parquet files
The app will automatically analyze your data structure


Ask Questions

Type natural language questions about your data
Examples:

"Show me the sales trends over time"
"Create a correlation matrix of all numeric columns"
"Plot the distribution of customer ages"
"Compare revenue by product category"




Get Insights

The AI will generate appropriate Python code
Code runs safely in a sandbox environment
Results are displayed with interactive visualizations



📁 Project Structure
ai-data-viz-agent/
├── app.py                     # Main Streamlit application
├── requirements.txt           # Python dependencies
├── .env                      # Environment variables
├── .gitignore               # Git ignore rules
├── config/
│   ├── settings.py          # App configuration
│   └── models.py            # AI model configurations
├── src/
│   ├── core/
│   │   ├── llm_client.py    # LLM interaction handler
│   │   ├── code_executor.py # Code execution in E2B
│   │   └── data_processor.py # Data processing utilities
│   ├── utils/
│   │   ├── file_handler.py  # File upload and management
│   │   ├── code_parser.py   # Code extraction utilities
│   │   └── validators.py    # Input validation
│   └── ui/
│       ├── components.py    # UI components
│       ├── sidebar.py       # Sidebar configuration
│       └── output_handler.py # Output formatting
├── tests/                   # Test files
├── docs/                    # Documentation
└── assets/                  # Static assets
🛡️ Security Features

Sandboxed Execution: All code runs in isolated E2B containers
Input Validation: Comprehensive validation of user inputs and uploaded files
Code Safety Checks: Prevents execution of dangerous operations
API Key Protection: Secure handling of API credentials

🎨 Supported Visualizations

Basic Charts: Line plots, bar charts, scatter plots, histograms
Statistical Plots: Box plots, violin plots, correlation heatmaps
Distribution Analysis: KDE plots, distribution comparisons
Time Series: Trend analysis, seasonal decomposition
Advanced: Multi-panel plots, interactive Plotly charts

🔍 Example Queries

"Show the relationship between price and sales"
"Create a dashboard with key metrics"
"Analyze customer segments by demographics"
"Plot monthly revenue trends with forecasting"
"Generate a comprehensive EDA report"

🛠️ Development
Running Tests
bashpython -m pytest tests/
Code Style
bash# Format code
black src/ tests/

# Check types
mypy src/
Adding New Features

Follow the existing project structure
Add appropriate tests in the tests/ directory
Update documentation
Ensure code passes validation checks

📊 Performance Tips

Large Datasets: Use sampling for initial exploration
Model Selection: Choose faster models for simple tasks
Memory Management: Monitor memory usage with large files
API Limits: Be aware of rate limits and token usage

🤝 Contributing

Fork the repository
Create a feature branch (git checkout -b feature/amazing-feature)
Commit your changes (git commit -m 'Add amazing feature')
Push to the branch (git push origin feature/amazing-feature)
Open a Pull Request

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
🙏 Acknowledgments

Streamlit for the amazing web app framework
Together AI for providing access to powerful language models
E2B for secure code execution environment
Open source visualization libraries: matplotlib, seaborn, plotly

🆘 Support

Documentation: Check the docs/ folder for detailed guides
Issues: Report bugs or request features via GitHub Issues
Discussions: Join our community discussions

🔄 Changelog
v1.0.0 (Current)

Initial release with core functionality
Support for major file formats
Multiple AI model options
Secure code execution
Comprehensive data validation


Made with ❤️ for the data science community