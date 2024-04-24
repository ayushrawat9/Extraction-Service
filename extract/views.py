from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.decorators import api_view
from django.core.exceptions import PermissionDenied
from rest_framework import viewsets
from extract.serializers import ExtractedTextSerializer

from asgiref.sync import sync_to_async
import requests
import base64

from .models import ExtractedText
# from .utils import extract_text_from_pdf, extract_text_from_docx_or_doc
from .utils import get_filename_from_url
from .tasks import send_email_task, extract_text_from_pdf, extract_text_from_docx_or_doc


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def extract(request):
    if not request.user.is_authenticated:
        raise PermissionDenied("User is not authenticated")
    if not request.method == 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed'})
    # Check if a file is provided in the request
    if not ('file' in request.FILES or 'url' in request.POST):
        return JsonResponse({'error': 'No file or url provided'})
    if 'file' in request.FILES:
        uploaded_file = request.FILES['file']
        filename = uploaded_file.name
    if 'url' in request.POST:
        url = request.POST['url']
        response = requests.get(url)
        if response.status_code == 200:
            uploaded_file = response.content
            filename = get_filename_from_url(url)

    # file process
    file_extension = filename.split('.')[-1].lower()
    uploaded_file = base64.b64encode(uploaded_file.read()).decode('utf-8')
    if file_extension == 'pdf':
        text = extract_text_from_pdf.delay(filename, uploaded_file, request.user.id)
    elif file_extension == 'doc' or file_extension == 'docx':
        extract_text_from_docx_or_doc.delay(filename, uploaded_file, file_extension, request.user.id)
    else:
        return JsonResponse({'error': 'Unsupported file format'})
    return JsonResponse({'request': 'done'})

class ExtractedTextViewSet(viewsets.ModelViewSet):
    serializer_class = ExtractedTextSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ExtractedText.objects.filter(created_by=self.request.user)
    