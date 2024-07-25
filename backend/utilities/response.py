import json


def JsonResponse(data):
    return json.dumps(data)


def res200(data, msg="success"):
    return JsonResponse({"code": 200, "msg": msg, "data": data})


def res400(msg):
    return JsonResponse({"code": 400, "error_msg": msg})


def res500(msg):
    return JsonResponse({"code": 500, "error_msg": msg})
