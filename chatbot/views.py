from django.shortcuts import render

# Create your views here.
import os

from django.shortcuts import render
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def chat(request):

    response_text = ""

    if request.method == "POST":

        user_input = request.POST.get("message")

        if user_input:

            response = client.responses.create(
                model="gpt-5-mini",
                input=user_input
            )

            response_text = response.output_text

    return render(
        request,
        "chatbot/chat.html",
        {
            "response": response_text
        }
    )