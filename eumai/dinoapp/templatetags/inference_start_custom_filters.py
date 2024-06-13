from django import template

register = template.Library()


@register.filter(name='status_container')
def status_container(value):
    classes = {
        'WAITED': '접수대기',
        'CONFIRMED': '접수확인',
        'PROCESSING': '처리중',
        'PROCESSED': '처리완료',
        'CHECKING': '확검중',
        'CHECKED': '보수완료',
        'REPROCESSED': '재처리요청',
        'REEXAMINED': '재검토요청',
        'TRANSFERRED': '공종이관'
    }
    return classes.get(value, '')
