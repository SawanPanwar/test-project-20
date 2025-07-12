from django.shortcuts import render, redirect
from .BaseCtl import BaseCtl
from ..models import User
from ..service.UserService import UserService


class UserListCtl(BaseCtl):
    count = 1

    def request_to_form(self, requestForm):
        self.form['firstName'] = requestForm.get("firstName", None)
        self.form['lastName'] = requestForm.get("lastName", None)
        self.form['loginId'] = requestForm.get("loginId", None)
        self.form['ids'] = requestForm.getlist('ids', None)

    def display(self, request, params={}):
        UserListCtl.count = self.form['pageNo']
        records = self.get_service().search(self.form)
        self.page_list = records['data']
        self.form['lastId'] = User.objects.last().id
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def submit(self, request, params={}):
        pass

    def get_template(self):
        return "UserList.html"

    def get_service(self):
        return UserService()
