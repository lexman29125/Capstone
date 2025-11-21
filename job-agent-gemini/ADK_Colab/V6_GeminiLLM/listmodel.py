from google import genai

# Initialize the client with your AI Studio API key
GOOGLE_API_KEY = "AIzaSyCtS-y2FZcMI9HuV2MaP_Sl81iBmfd4SHU"
client = genai.Client(api_key=GOOGLE_API_KEY)

# List all available models
available_models = client.models.list()

for model in available_models:
    print(f"Name: {model.name}")
    print(f"Supported Methods: {model.supported_methods}")
    print("-" * 40)