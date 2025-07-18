from ..models import College
from ..utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection


class CollegeService(BaseService):

    def search(self, params):
        pageNo = (params['pageNo'] - 1) * self.pageSize
        sql = "select * from sos_college where 1=1"
        val = params.get("name", None)
        if DataValidator.isNotNull(val):
            sql += " and name like '" + val + "%%'"
        sql += " limit %s, %s"
        cursor = connection.cursor()
        params['index'] = ((params['pageNo'] - 1) * self.pageSize) + 1
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ('id', 'name', 'address', 'state', 'city', 'phoneNumber')
        res = {
            "data": [],
            "MaxId": 1,
        }
        count = 0
        res["index"] = params["index"]
        for x in result:
            params['MaxId'] = x[0]
            res['data'].append({columnName[i]: x[i] for i, _ in enumerate(x)})
        return res

    def get_model(self):
        return College
