# app1/context_processors.py

from django.utils import timezone
from .models import Message, Appointment, Report

def global_notifications(request):

    if not request.user.is_authenticated:
        return {}

    me = request.user.profile

    qs = Message.objects.filter(recipient=me, is_read=False)
    unread_count = qs.count()
    unread_notifs = (
        qs
        .order_by("-timestamp")
        .values("listing__id", "listing__title")
        .distinct()
    )
    # Convert qs.values() into a list of {pk, title}
    unread_notifs = [
        {"pk": o["listing__id"], "title": o["listing__title"]}
        for o in unread_notifs
    ]

    # Pending appointments (seller only)
    pending_qs = Appointment.objects.filter(
        listing__seller=me,
        completed=False,
    ).select_related("listing", "buyer").order_by("scheduled_time")
    pending_count = pending_qs.count()

    if request.user.is_staff:
        reports_qs = Report.objects.order_by("-created_at")
        report_count   = reports_qs.count()
        recent_reports = reports_qs[:5]
    else:
        report_count   = 0
        recent_reports = []


    return {
        "unread_count":        unread_count,
        "unread_notifs":       unread_notifs,
        "pending_count":       pending_count,
        "pending_appointments": pending_qs,
        "report_count":         report_count,
        "recent_reports":       recent_reports,
    }
