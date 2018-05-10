from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

from index.models import UserModel


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        """
        统一验证登录

        :param request:
        :return:
        """
        a = request.path
        if request.path == '/uauth/login/' or request.path == '/uauth/logout/':
            return None
        ticket = request.COOKIES.get('ticket')
        if request.path == '/axf/cart/':

            if not ticket:
                return HttpResponseRedirect('/uauth/login')
        else:
            if not ticket:
                return None

        users = UserModel.objects.filter(u_ticket=ticket)
        if not users:
            return HttpResponseRedirect('/uauth/login')

        request.user = users[0]
