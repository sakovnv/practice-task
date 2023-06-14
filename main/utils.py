form_attr = {'class': 'form-control'}


class DataMixin:
    def __init__(self):
        self.context = None
        self.request = None

    def get_context(self, **kwargs):
        kwargs_copy = kwargs.copy()
        self.context = kwargs

        return self.context
