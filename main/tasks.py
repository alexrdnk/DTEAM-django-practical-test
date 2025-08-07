import time
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import CV, RequestLog


@shared_task
def send_email_task(subject, message, recipient_list):
    """
    Background task to send emails.
    
    Args:
        subject (str): Email subject
        message (str): Email message
        recipient_list (list): List of recipient email addresses
    """
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@cvproject.com',
            recipient_list=recipient_list,
            fail_silently=False,
        )
        return f"Email sent successfully to {recipient_list}"
    except Exception as e:
        return f"Failed to send email: {str(e)}"


@shared_task
def send_cv_notification_task(cv_id, recipient_email):
    """
    Background task to send CV notification email.
    
    Args:
        cv_id (int): ID of the CV
        recipient_email (str): Email address to send notification to
    """
    try:
        cv = CV.objects.get(id=cv_id)
        subject = f"New CV Added: {cv.get_full_name()}"
        message = f"""
        A new CV has been added to the system:
        
        Name: {cv.get_full_name()}
        Skills: {cv.skills}
        Bio: {cv.bio[:100]}...
        
        You can view the full CV at: http://localhost:8000/cv/{cv.id}/
        """
        
        return send_email_task.delay(subject, message, [recipient_email])
    except CV.DoesNotExist:
        return f"CV with ID {cv_id} not found"
    except Exception as e:
        return f"Failed to send CV notification: {str(e)}"


@shared_task
def generate_cv_pdf_task(cv_id):
    """
    Background task to generate CV PDF.
    
    Args:
        cv_id (int): ID of the CV to generate PDF for
    """
    try:
        cv = CV.objects.get(id=cv_id)
        # Simulate PDF generation process
        time.sleep(2)  # Simulate processing time
        
        # In a real implementation, you would generate the PDF here
        # For now, we'll just return a success message
        return f"PDF generated successfully for {cv.get_full_name()}"
    except CV.DoesNotExist:
        return f"CV with ID {cv_id} not found"
    except Exception as e:
        return f"Failed to generate PDF: {str(e)}"


@shared_task
def cleanup_old_logs_task():
    """
    Background task to cleanup old request logs.
    Keeps only the last 1000 logs.
    """
    try:
        total_logs = RequestLog.objects.count()
        if total_logs > 1000:
            # Delete logs older than 30 days, keeping only the latest 1000
            logs_to_delete = RequestLog.objects.order_by('timestamp')[:total_logs - 1000]
            deleted_count = logs_to_delete.count()
            logs_to_delete.delete()
            return f"Cleaned up {deleted_count} old logs. Total logs: {RequestLog.objects.count()}"
        else:
            return f"No cleanup needed. Total logs: {total_logs}"
    except Exception as e:
        return f"Failed to cleanup logs: {str(e)}"


@shared_task
def send_daily_report_task():
    """
    Background task to send daily report.
    This task is scheduled to run daily via Celery Beat.
    """
    try:
        # Get statistics
        total_cvs = CV.objects.count()
        total_logs = RequestLog.objects.count()
        
        # Get today's logs
        from django.utils import timezone
        from datetime import timedelta
        
        today = timezone.now().date()
        today_logs = RequestLog.objects.filter(
            timestamp__date=today
        ).count()
        
        subject = "Daily CV Project Report"
        message = f"""
        Daily Report for {today}:
        
        Total CVs: {total_cvs}
        Total Request Logs: {total_logs}
        Today's Requests: {today_logs}
        
        This is an automated daily report from the CV Project system.
        """
        
        # Send to admin (you can modify this to send to actual admin email)
        admin_email = 'admin@cvproject.com'
        
        return send_email_task.delay(subject, message, [admin_email])
    except Exception as e:
        return f"Failed to send daily report: {str(e)}"


@shared_task
def test_task():
    """
    Simple test task for debugging.
    """
    return "Test task completed successfully!"


@shared_task
def long_running_task():
    """
    Simulates a long-running task for testing.
    """
    time.sleep(10)  # Simulate 10 seconds of work
    return "Long running task completed!" 