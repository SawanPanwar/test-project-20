from django.shortcuts import render
from .BaseCtl import BaseCtl
from ..utility.DataValidator import DataValidator
from ..models import Role
from ..service.RoleService import RoleService


class RoleCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['name'] = requestForm['name']
        self.form['description'] = requestForm['description']

    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.name = self.form['name']
        obj.description = self.form['description']
        return obj

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form["id"] = obj.id
        self.form["name"] = obj.name
        self.form["description"] = obj.description

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']
        if (DataValidator.isNull(self.form['name'])):
            inputError['name'] = "Role Name is required"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['name'])):
                inputError['name'] = "Role Name contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['description'])):
            inputError['description'] = "Description is required"
            self.form['error'] = True
        return self.form['error']

    def display(self, request, params={}):
        if (params['id'] > 0):
            obj = self.get_service().get(params['id'])
            self.model_to_form(obj)
        res = render(request, self.get_template(), {"form": self.form})
        return res

    def submit(self, request, params={}):
        if (int(self.form['id']) > 0):
            pk = int(self.form['id'])
            dup = self.get_service().get_model().objects.exclude(id=pk).filter(name=self.form['name'])
            if dup.count() > 0:
                self.form['error'] = True
                self.form['message'] = "Role already exist"
                res = render(request, self.get_template(), {'form': self.form})
            else:
                r = self.form_to_model(Role())
                self.get_service().save(r)
                self.form['id'] = r.id

                self.form['error'] = False
                self.form['message'] = "Data updated successfully"
                res = render(request, self.get_template(), {'form': self.form})
        else:
            duplicate = self.get_service().get_model().objects.filter(name=self.form['name'])
            if duplicate.count() > 0:
                self.form['error'] = True
                self.form['message'] = "Role already exist"
                res = render(request, self.get_template(), {'form': self.form})
            else:
                r = self.form_to_model(Role())
                self.get_service().save(r)
                self.form['error'] = False
                self.form['message'] = "Role Added successfully..!!"
                res = render(request, self.get_template(), {'form': self.form})
        return res

    def get_template(self):
        return "Role.html"

    def get_service(self):
        return RoleService()
