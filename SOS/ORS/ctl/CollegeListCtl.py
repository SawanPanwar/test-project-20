from .BaseCtl import BaseCtl
from django.shortcuts import render, redirect
from ..utility.DataValidator import DataValidator
from ..models import College
from ..service.CollegeService import CollegeService


class CollegeListCtl(BaseCtl):
    count = 1

    def request_to_form(self, requestForm):
        self.form['name'] = requestForm.get("name", None)
        self.form['address'] = requestForm.get('address', None)
        self.form['state'] = requestForm.get('state', None)
        self.form['city'] = requestForm.get('city', None)
        self.form['phoneNumber'] = requestForm.get('phoneNumber', None)
        self.form['ids'] = requestForm.getlist('ids', None)

    def display(self, request, params={}):
        CollegeListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['LastId'] = College.objects.last().id
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def previous(self, request, params={}):
        CollegeListCtl.count -= 1
        self.form['pageNo'] = CollegeListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def next(self, request, params={}):
        CollegeListCtl.count += 1
        self.form['pageNo'] = CollegeListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['LastId'] = College.objects.last().id
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def new(self, request, params={}):
        res = redirect("/ORS/College/")
        return res

    def submit(self, request, params={}):
        CollegeListCtl.count = 1
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        if self.page_list == []:
            self.form['message'] = "No record found"
        ress = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return ress

    def deleteRecord(self, request, params={}):
        self.form['pageNo'] = CollegeListCtl.count
        if (bool(self.form['ids']) == False):
            self.form['error'] = True
            self.form['message'] = "Please select at least one checkbox"
            record = self.get_service().search(self.form)
            self.page_list = record['data']
            res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        else:
            for ids in self.form['ids']:
                record = self.get_service().search(self.form)
                self.page_list = record['data']

                id = int(ids)
                if (id > 0):
                    r = self.get_service().get(id)
                    if r is not None:
                        self.get_service().delete(r.id)
                        self.form['pageNo'] = 1
                        record = self.get_service().search(self.form)
                        self.page_list = record['data']
                        self.form['LastId'] = College.objects.last().id
                        CollegeListCtl.count = 1

                        self.form['error'] = False
                        self.form['message'] = "Data has been deleted successfully"
                        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
                    else:
                        self.form['error'] = True
                        self.form['message'] = "Data was not deleted"
                        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def get_template(self):
        return "CollegeList.html"

    def get_service(self):
        return CollegeService()
