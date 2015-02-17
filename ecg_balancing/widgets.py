from datetime import date
from datetime import date
from django.forms import widgets
from django.utils.translation import ugettext_lazy as _

class DateSelectorWidget(widgets.MultiWidget):
    def __init__(self, attrs=None):
        this_year = date.today().year
        years = [(year, year) for year in range(this_year-11, this_year+1)]
        years.reverse()
        months = [
            (1, _('January')),
            (2, _('February')),
            (3, _('March')),
            (4, _('April')),
            (5, _('May')),
            (6, _('June')),
            (7, _('July')),
            (8, _('August')),
            (9, _('September')),
            (10, _('October')),
            (11, _('November')),
            (12, _('December'))
        ]
        _widgets = (
            widgets.Select(attrs=attrs, choices=months),
            widgets.Select(attrs=attrs, choices=years),
        )
        super(DateSelectorWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.month, value.year]
        return [None, None]

    def format_output(self, rendered_widgets):
        return u''.join(rendered_widgets)

    def value_from_datadict(self, data, files, name):
        datelist = [
            widget.value_from_datadict(data, files, name + '_%s' % i)
            for i, widget in enumerate(self.widgets)]
        try:
            D = date(day=1,
                    month=int(datelist[0]),
                    year=int(datelist[1]))
        except ValueError:
            return ''
        else:
            return str(D)