You can turn that CLI chatbot into a simple Django web app with one page containing a chat box.

### 1. Create a project folder

```bash
mkdir django_chatbot
cd django_chatbot
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install the packages:

```bash
pip install django openai python-dotenv
```

### 2. Create the Django project

```bash
django-admin startproject config .
```

Your folder will now look roughly like this:

```text
django_chatbot/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── manage.py
└── venv/
```

### 3. Create the chatbot app

Run:

```bash
python manage.py startapp chatbot
```

Now you will have:

```text
chatbot/
├── migrations/
├── admin.py
├── apps.py
├── models.py
├── tests.py
└── views.py
```

### 4. Add the app to Django

Open:

```text
config/settings.py
```

Find:

```python
INSTALLED_APPS = [
```

Add `chatbot`:

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "chatbot",
]
```

### 5. Create your `.env`

In the same folder as `manage.py`, create:

```text
.env
```

Add:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Do not put quotes around the key.

Also create a `.gitignore`:

```text
.env
venv/
__pycache__/
db.sqlite3
```

### 6. Create the chatbot view

Open:

```text
chatbot/views.py
```

Replace it with:

```python
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
```

The main difference from your CLI program is this:

```python
input()
```

is replaced by:

```python
request.POST.get("message")
```

And:

```python
print()
```

is replaced by sending the response into an HTML template.

### 7. Create app URLs

Create:

```text
chatbot/urls.py
```

Add:

```python
from django.urls import path
from . import views


urlpatterns = [
    path("", views.chat, name="chat"),
]
```

### 8. Connect the app URLs to the project

Open:

```text
config/urls.py
```

Change it to:

```python
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("chatbot.urls")),
]
```

Now visiting:

```text
http://127.0.0.1:8000/
```

will call:

```python
views.chat
```

### 9. Create the HTML template

Create these folders:

```text
chatbot/
└── templates/
    └── chatbot/
        └── chat.html
```

Put this inside `chat.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>OpenAI Chatbot</title>
</head>

<body>

    <h1>AI Chatbot</h1>

    <form method="POST">

        {% csrf_token %}

        <input
            type="text"
            name="message"
            placeholder="Ask something..."
            required
        >

        <button type="submit">
            Send
        </button>

    </form>


    {% if response %}

        <h3>GPT</h3>

        <p>
            {{ response }}
        </p>

    {% endif %}

</body>
</html>
```

`{% csrf_token %}` is required for Django POST forms.

### 10. Run Django migrations

```bash
python manage.py migrate
```

This creates Django's default database tables.

You'll see a new file:

```text
db.sqlite3
```

### 11. Start the server

```bash
python manage.py runserver
```

You should see:

```text
Starting development server at http://127.0.0.1:8000/
```

Open:

```text
http://127.0.0.1:8000/
```

Type something like:

```text
Explain RAG in simple words
```

The flow is:

```text
Browser
   ↓
HTML form
   ↓
POST request
   ↓
Django view
   ↓
OpenAI Responses API
   ↓
response.output_text
   ↓
Django template
   ↓
Browser
```

Your final project should look like:

```text
django_chatbot/
│
├── .env
├── .gitignore
├── db.sqlite3
├── manage.py
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
└── chatbot/
    ├── migrations/
    ├── templates/
    │   └── chatbot/
    │       └── chat.html
    │
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── tests.py
    ├── urls.py
    └── views.py
```

At this stage, this is basically your original program:

```python
user_input → OpenAI → response
```

but converted into:

```text
HTML input → Django → OpenAI → HTML response
```

The next useful upgrade would be storing conversation history using Django sessions, so GPT remembers previous messages instead of treating every message independently.
