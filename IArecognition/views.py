import os
import requests
import json
from django.shortcuts import render
from google.cloud import vision
from django.core.files.storage import default_storage

def detect_labels(image_path):
    """Detecta etiquetas en la imagen."""
    client = vision.ImageAnnotatorClient()

    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations

    if response.error.message:
        raise Exception(f"Error: {response.error.message}")

    return [label.description for label in labels]

def get_ai_response(prompt):
    """Obtiene respuesta de Gemini AI."""
    endpoint = os.getenv("GEMINI_API_ENDPOINT")
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    response = requests.post(endpoint, headers=headers, json=data)

    if response.status_code == 200:
        respuesta = response.json()
        return respuesta["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"Error: {response.status_code}, {response.text}"

def image_upload(request):
    context = {}

    if request.method == "POST" and request.FILES.get("image"):
        image = request.FILES["image"]
        image_path = default_storage.save("temp/" + image.name, image)

        # Obtener etiquetas de la imagen
        labels = detect_labels(image_path)

        # Enviar etiquetas a la IA
        prompt = f"{labels}, intenta identificar posibles razas de perro con estos datos. Si no es un perro, indica que no es un perro."
        ai_response = get_ai_response(prompt)

        context["image_url"] = image_path
        context["labels"] = labels
        context["ai_response"] = ai_response

    return render(request, "upload.html", context)
