import os
import json
import hashlib
import pdfplumber
from google import genai

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Research
from transformers import pipeline
from dotenv import load_dotenv

load_dotenv()

# ---------------- AI Detector ----------------
ai_detector = pipeline(
    "text-classification",
    model="roberta-base-openai-detector",
    device=-1
)

# ---------------- Gemini Client ----------------
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ---------------- HOME ----------------
def home(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    return redirect('core:login')

# ---------------- DASHBOARD ----------------
@login_required
def dashboard(request):
    researches = Research.objects.filter(user=request.user)
    return render(request, 'research/dashboard.html', {'researches': researches})


# ---------------- AUTH ----------------
def register(request):
    # 🔒 Redirect already logged-in users
    if request.user.is_authenticated:
        return redirect('core:dashboard')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:dashboard')
        messages.error(request, "Registration failed.")
    else:
        form = UserCreationForm()

    return render(request, 'research/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')

    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )

        if user:
            login(request, user)
            return redirect('core:dashboard')

        messages.error(request, "Invalid credentials")

    return render(request, "research/login.html")


@login_required
def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('core:login')


# ---------------- UPLOAD ----------------
@login_required
def upload_research(request):
    if request.method == 'POST':
        try:
            research_file = request.FILES['file']

            if not research_file.name.lower().endswith('.pdf'):
                return render(request, 'research/upload.html', {
                    'error': 'Only PDF files are allowed'
                })

            # Hash file
            file_bytes = research_file.read()
            file_hash = hashlib.sha256(file_bytes).hexdigest()
            research_file.seek(0)

            # Duplicate check
            if Research.objects.filter(user=request.user, file_hash=file_hash).exists():
                return render(request, 'research/upload.html', {
                    'error': 'This research paper is already uploaded.'
                })

            # Save
            research = Research.objects.create(
                user=request.user,
                file=research_file,
                file_hash=file_hash
            )

            # Extract text
            with pdfplumber.open(research.file.path) as pdf:
                pdf_text = "\n".join(
                    filter(None, (page.extract_text() for page in pdf.pages))
                )

                # AI detection
                research.ai_probability = check_ai_content(pdf_text)

                # Title extraction
                if pdf.pages:
                    first_page = pdf.pages[0].extract_text()
                    if first_page:
                        research.title = first_page.split('\n')[0][:255]

            research.save()

            return redirect('core:summarize', research.id)

        except Exception as e:
            return render(request, 'research/upload.html', {'error': str(e)})

    return render(request, 'research/upload.html')


# ---------------- DELETE ----------------
@login_required
def delete_research(request, research_id):
    research = Research.objects.get(id=research_id, user=request.user)

    if request.method == "POST":
        if research.file:
            research.file.delete(save=False)
        research.delete()
        messages.success(request, "Research deleted.")
        return redirect('core:dashboard')

    return render(request, 'research/confirm_delete.html', {'research': research})


# ---------------- AI UTILS ----------------
def check_ai_content(text):
    result = ai_detector(text[:1000])[0]
    return result['score'] if result['label'] == 'AI' else 1 - result['score']


# ---------------- SUMMARY ----------------
@login_required
def summarize_research(request, research_id):
    research = Research.objects.get(id=research_id, user=request.user)
    return render(request, 'research/summary.html', {'research': research})


@login_required
def stream_summary(request, research_id):
    research = Research.objects.get(id=research_id, user=request.user)

    def generate():
        try:
            with pdfplumber.open(research.file.path) as pdf:
                text = "\n".join(
                    filter(None, (p.extract_text() for p in pdf.pages[:3]))
                )

            text = text[:3000]

            prompt = f"""
Generate a structured academic summary in markdown.

Include:
- Title
- Problem Statement
- Methodology
- Key Findings
- Conclusion

Text:
{text}
"""

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            if not response or not response.text:
                raise Exception("Empty response from Gemini")

            summary = response.text.strip()

            for i in range(0, len(summary), 120):
                yield f"data: {json.dumps({'content': summary[i:i+120]})}\n\n"

            yield f"data: {json.dumps({'done': True})}\n\n"

        except Exception as e:
            print("GEMINI ERROR:", e)
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingHttpResponse(
        generate(),
        content_type="text/event-stream",
        headers={"Cache-Control": "no-cache"},
    )


# ---------------- TRANSLATION ----------------
@csrf_exempt
@login_required
def translate_text(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data.get('text', '')

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Translate the following text into Chinese:\n{text}"
        )

        return JsonResponse({'translation': response.text})

    return JsonResponse({'error': 'Invalid request'}, status=400)
