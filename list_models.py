import google.generativeai as genai

api_key = input("Enter API Key: ")

genai.configure(api_key=api_key)

print("Available models:\n")

for model in genai.list_models():
    if "generateContent" in model.supported_generation_methods:
        print(model.name)
