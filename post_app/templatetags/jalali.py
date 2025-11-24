from django import template
import jdatetime

register = template.Library()


@register.filter
def jalali_words(dt):
    if not dt:
        return ''
    jalali = jdatetime.date.fromgregorian(date=dt.date())
    months = [
        "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
        "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"
    ]
    month_name = months[jalali.month - 1]
    return f"{jalali.day} {month_name} {jalali.year}"
