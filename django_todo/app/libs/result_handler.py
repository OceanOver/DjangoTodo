from rest_framework.response import Response

# 请求业务无效
FAIL = 1001
# 请求成功
SUCCESS = 1200
# 请求成功处理，但是返回的响应没有数据
NO_CONTENT = 1202
# 拒绝访问操作资源（权限）
FORBIDDEN = 1403
# 请求未包含身份验证信息，或者提供的凭据无效
UNAUTHORIZED = 1401
# 接口不存在
NOT_FOUND = 1404
# 服务器错误
ERROR = 1500


class ResultGenerator:
    @staticmethod
    def gen_result(result_code, msg=None, data=None):
        if msg is None:
            if result_code == NOT_FOUND:
                msg = '接口不存在'
            elif result_code == UNAUTHORIZED:
                msg = '请求未包含身份验证信息，或者提供的凭据无效'
            elif result_code == FORBIDDEN:
                msg = '拒绝访问操作资源'
        if data is None:
            return Response({
                'code': result_code,
                'msg': msg,
            })
        return Response({
            'code': result_code,
            'msg': msg,
            'data': data
        })

    @staticmethod
    def gen_success_result(data=None, msg='请求成功'):
        result = {
            'code': SUCCESS,
            'msg': msg
        }
        if data is not None:
            result['data'] = data
        return Response(result)

    @staticmethod
    def gen_fail_result(msg='请求失败'):
        return Response({
            'code': FAIL,
            'msg': msg
        })

    @staticmethod
    def gen_error_result(msg='服务器错误'):
        return Response({
            'code': ERROR,
            'msg': msg
        })

    @staticmethod
    def gen_no_content_result(msg='返回的响应没有数据'):
        return Response({
            'code': NO_CONTENT,
            'msg': msg
        })

    @staticmethod
    def gen_not_found_result(msg='接口不存在'):
        return Response({
            'code': NOT_FOUND,
            'msg': msg
        })
