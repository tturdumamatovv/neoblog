from django.utils import timezone


def format_localized_datetime(datetime_obj):
    russian_months = {
        1: 'янв', 2: 'февр', 3: 'марта', 4: 'апр', 5: 'мая', 6: 'июня',
        7: 'июля', 8: 'авг', 9: 'сент', 10: 'окт', 11: 'нояб', 12: 'дек'
    }
    local_time = datetime_obj.astimezone(timezone.get_current_timezone())
    return "{day} {month} в {time}".format(
        day=local_time.strftime("%d"),
        month=russian_months[local_time.month],
        time=local_time.strftime("%H:%M")
    )
