from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from django.template.loader import render_to_string
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
from .models import CV, RequestLog


class CVListView(ListView):
    """View to display a list of all CVs."""
    model = CV
    template_name = 'main/cv_list.html'
    context_object_name = 'cvs'
    paginate_by = 10

    def get_queryset(self):
        """Return all CVs ordered by creation date."""
        return CV.objects.all().order_by('-created_at')


class CVDetailView(DetailView):
    """View to display a single CV in detail."""
    model = CV
    template_name = 'main/cv_detail.html'
    context_object_name = 'cv'

    def get_object(self, queryset=None):
        """Get the CV object by ID."""
        return get_object_or_404(CV, pk=self.kwargs.get('pk'))

    def get_pdf_response(self, cv):
        """Generate PDF response for CV."""
        return generate_cv_pdf(cv)


class RequestLogListView(ListView):
    """View to display recent request logs."""
    model = RequestLog
    template_name = 'main/request_logs.html'
    context_object_name = 'logs'
    paginate_by = 20

    def get_queryset(self):
        """Return the 10 most recent request logs."""
        return RequestLog.objects.all().order_by('-timestamp')[:10]


def settings_view(request):
    """View to display Django settings."""
    return render(request, 'main/settings.html')


def generate_cv_pdf(cv):
    """Generate modern, professional PDF for CV using ReportLab."""
    # Create a file-like buffer to receive PDF data
    buffer = BytesIO()
    
    # Create the PDF object, using the file-like buffer as its "file."
    doc = SimpleDocTemplate(buffer, pagesize=A4, 
                          leftMargin=1.8*cm, rightMargin=1.8*cm,
                          topMargin=2*cm, bottomMargin=1.5*cm)
    
    # Container for the 'Flowable' objects
    story = []
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create modern custom styles with professional typography
    name_style = ParagraphStyle(
        'NameStyle',
        parent=styles['Heading1'],
        fontSize=28,
        spaceAfter=5,
        spaceBefore=0,
        alignment=TA_LEFT,
        textColor=colors.HexColor('#1a1a1a'),
        fontName='Helvetica-Bold',
        leading=32
    )
    
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Normal'],
        fontSize=14,
        spaceAfter=20,
        alignment=TA_LEFT,
        textColor=colors.HexColor('#666666'),
        fontName='Helvetica',
        leading=16
    )
    
    contact_style = ParagraphStyle(
        'ContactStyle',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=3,
        alignment=TA_RIGHT,
        textColor=colors.HexColor('#333333'),
        fontName='Helvetica',
        leading=12
    )
    
    section_heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=25,
        textColor=colors.HexColor('#2c3e50'),
        fontName='Helvetica-Bold',
        leftIndent=0,
        leading=18
    )
    
    content_style = ParagraphStyle(
        'ContentStyle',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=8,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor('#333333'),
        fontName='Helvetica',
        leading=14,
        leftIndent=0
    )
    
    skills_style = ParagraphStyle(
        'SkillsStyle',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        alignment=TA_LEFT,
        textColor=colors.HexColor('#34495e'),
        fontName='Helvetica',
        leading=14,
        leftIndent=0
    )
    
    footer_style = ParagraphStyle(
        'FooterStyle',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#95a5a6'),
        alignment=TA_CENTER,
        fontName='Helvetica',
        leading=10
    )
    
    # Header section with name, title, and contact info
    # Create a table for the header layout
    header_data = [
        [
            Paragraph(cv.get_full_name(), name_style),
            Paragraph(cv.contacts.replace('\n', '<br/>'), contact_style)
        ]
    ]
    
    header_table = Table(header_data, colWidths=[doc.width*0.6, doc.width*0.4])
    header_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(header_table)
    
    # Add professional title
    story.append(Paragraph("Software Developer", title_style))
    
    # Add decorative line
    story.append(Spacer(1, 15))
    
    # Professional Summary Section
    story.append(Paragraph("Professional Summary", section_heading_style))
    story.append(Paragraph(cv.bio.replace('\n', '<br/>'), content_style))
    
    # Skills & Expertise Section
    story.append(Paragraph("Technical Skills", section_heading_style))
    
    # Format skills with bullet points for better readability
    skills_list = [skill.strip() for skill in cv.skills.split(',')]
    skills_text = " • ".join(skills_list)
    story.append(Paragraph(skills_text, skills_style))
    
    # Projects & Achievements Section
    story.append(Paragraph("Projects & Achievements", section_heading_style))
    story.append(Paragraph(cv.projects.replace('\n', '<br/>'), content_style))
    
    # Add footer with metadata
    story.append(Spacer(1, 20))
    footer_text = f"Generated on {cv.updated_at.strftime('%B %d, %Y')} at {cv.updated_at.strftime('%H:%M')}"
    story.append(Paragraph(footer_text, footer_style))
    
    metadata_text = f"CV ID: {cv.pk} | Created: {cv.created_at.strftime('%b %d, %Y')} | Updated: {cv.updated_at.strftime('%b %d, %Y')}"
    story.append(Paragraph(metadata_text, footer_style))
    
    # Build PDF
    doc.build(story)
    
    # Get the value of the BytesIO buffer and write it to the response
    pdf = buffer.getvalue()
    buffer.close()
    
    # Create HTTP response with PDF
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{cv.get_full_name()}_CV.pdf"'
    return response


def cv_pdf_download(request, pk):
    """View to download CV as PDF."""
    cv = get_object_or_404(CV, pk=pk)
    return generate_cv_pdf(cv)
