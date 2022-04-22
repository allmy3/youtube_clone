from django.http import Http404


class CheckAuthorMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user != obj.channel.user:
            raise Http404('Вы не автор!')
        return super().dispatch(request, *args, **kwargs)