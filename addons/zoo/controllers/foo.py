import odoo
from odoo.http import request, Response
import json

import logging
_logger = logging.getLogger(__name__)

class FooAPI(odoo.http.Controller):
    @odoo.http.route('/api/foo/<val>', type='json', auth='none', cors='*', csrf=False)
    def api_foo(self, val, **kw):
        """
        $ curl -H "Content-Type: application/json" -X POST --data '{"params": {"a": 2, "b": 3, "c": 4}}' localhost:10014/api/foo/calc/
        {"jsonrpc": "2.0", "id": null, "result": {"val": "calc", "result": 12, "data": "{'a': 2, 'b': 3, 'c': 4}", "request_json": "{'params': {'a': 2, 'b': 3, 'c': 4}}", "request_param": "{'a': 2, 'b': 3, 'c': 4}"}}
        """
        request_httprequest_args = request.httprequest.args.to_dict()
        # → lấy từ URL query string: /api/foo/calc/?a=2&b=3

        request_params = request.params
        # → lấy từ body JSON: {"params": {"a": 2, "b": 3, "c": 4}}
        #   Odoo tự parse JSON body, lấy phần "params" ra

        data = request_params if request_params else request_httprequest_args
        # → ưu tiên dùng JSON body, nếu không có thì dùng query string
        a = data.get("a", 1)
        b = data.get("b", 2)
        c = data.get("c", 3)
        result = a
        for _ in range(abs(b-1)):
            result *= a
        result = result + c
        return {
            "val": val,
            "result": result,
            "data": str(data),
            "request_httprequest_args": str(request_httprequest_args),
            "request_params": str(request_params),
        }
        
    # Các khai báo thư viện đã hiện thực ở I...
class ZooAPI(odoo.http.Controller):
    # ...
    # code vào cuối class "ZooAPI", liền sau phương thức đã hiện thực ở I.
    @odoo.http.route('/api/html/<val>', type='http', auth='none', cors='*', csrf=False)
    def api_simple_html(self, val, **kw):
        """
        $ curl -X POST -d "a=2" -d "b=3" -d "c=4" localhost:10014/api/html/minh/
        {"result": "{'a': '2', 'b': '3', 'c': '4'} => minh @ 12.00"}
        """
        # → lấy từ form data: a=2&b=3&c=4
        # Lưu ý: giá trị là STRING, phải ép kiểu int/float
        data = dict(request.params)
        a = int(data.get("a", 1))
        b = int(data.get("b", 2))
        c = int(data.get("c", 3))
        result = a
        for _ in range(abs(b-1)):
            result *= a
        result = result + c
        # Khi type='http' thì "request" sẽ là "odoo.http.HttpRequest" 
        # và ta có thể gọi phương thức "make_response"
        # https://www.odoo.com/documentation/14.0/reference/http.html#request
        return request.make_response(data=json.dumps({"result": "%s => %s @ %.2f" % (str(data), val, result)}), headers=[('Content-Type', 'application/json')])
        # type='http' → phải tự tạo response thủ công
        # không tự wrap như type='json'