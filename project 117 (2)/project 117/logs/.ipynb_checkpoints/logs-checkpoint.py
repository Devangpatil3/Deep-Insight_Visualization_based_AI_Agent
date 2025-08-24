import os

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

# Then configure logging
logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
