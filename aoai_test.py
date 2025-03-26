#To use interactive authentication with Entra ID, import InteractiveBrowserCredential class and get_bearer_token_provider function from azure.identity package and instantiate your token provider.

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI

aoai_endpoint = "https://msechackathon-eastus2.openai.azure.com/"

model = "gpt-4o"
token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")
api_version = "2025-01-01-preview"

#Now you can instantiate AzureOpenAI client and set azure_ad_token_provider parameter to your token provider from step above.
client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=aoai_endpoint,
    azure_ad_token_provider=token_provider,
)

response = client.chat.completions.create(
    model = model,
    messages = [
        {"role": "system", "content": "You are a friendly chatbot"},
        {"role": "user", "content": "Choose a random flower and describe it to me in 3 sentences."}
    ]
)

print(response.choices[0].message.content)
#If authentication is successful, the called GPT model should generate relevant completion, e.g.:
#The sunflower, a vibrant echo of the summer sun, stands tall with its large, rough stem that hoists the bright yellow petals aloft. Each flower is actually a composite of hundreds of small florets that cluster together to form the eye-catching disk, circled by the flamboyant sun-like halo. This cheerful bloom not only follows the day's sun, performing a slow dance from east to west, but is also a symbol of loyalty and adoration.