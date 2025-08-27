from murf import Murf

client = Murf(
    api_key="ap2_54e91e5e-8ac8-4d96-ab04-cdae5ff7a0f3", # Not required if you have set the MURF_API_KEY environment variable
)

response = client.text.translate(
    target_language="es-ES",
    texts=["Hello, I am Vedant!"],
)

print(response.translations[0].translated_text)

# for t in response.translations:
#     print(t.translated_text)