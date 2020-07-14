from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action, api_view
from rest_framework.permissions import AllowAny
from rest_framework_jwt.settings import api_settings
from rest_framework.decorators import permission_classes
from django.conf import settings
import logging
import random
import time
import hashlib
from ..models.user import User
from .serializers import UserSerializer
from .forms import ProfileForm
from django_todo.app.libs.result_handler import ResultGenerator
from django_todo.app.libs.exceptions import ServiceError

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

logger = logging.getLogger('django')


class UserViewSet(GenericViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('create_time')
    serializer_class = UserSerializer

    @action(detail=False, methods=['GET'])
    def info(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return ResultGenerator.gen_success_result(serializer.data)

    @action(detail=False, methods=['PUT', 'POST'])
    def modifyPassword(self, request):
        user = request.user
        password = request.data.get('password')
        new_password = request.data.get('newPassword')
        if user.check_password(password):
            user.set_password(new_password)
            user.save()
            return ResultGenerator.gen_success_result()
        raise ServiceError(message='原密码输入有误')

    @action(detail=False, methods=['PUT', 'POST'])
    def updateHeader(self, request):
        user = request.user
        header = request.data.get('header')
        user.header = header
        user.save()
        return ResultGenerator.gen_success_result()


@api_view(['POST'])
@permission_classes((AllowAny,))
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = User.objects.filter(username=username).first()
    if user is not None:
        raise ServiceError(message='user already exists')
    user = User()
    user.username = username
    user.set_password(password)
    user.save()
    serializer = UserSerializer(user)
    return ResultGenerator.gen_success_result(serializer.data)


@api_view(['POST'])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = User.objects.filter(username=username).first()
    if user is not None:
        if user.check_password(password):
            serializer = UserSerializer(user)
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            expire = settings.TOKEN_EXPIRE
            data = {
                'user': serializer.data,
                'token': token,
                'expire': expire,
            }
            return ResultGenerator.gen_success_result(data)
        else:
            raise ServiceError(message='account or password not match')
    else:
        raise ServiceError(message='no user')


@api_view(['POST'])
@permission_classes((AllowAny,))
def upload(request):
    # 获取前台传来的文件，request.POST用来接收title和content，request.FILES用来接收文件
    form = ProfileForm(request.POST, request.FILES)
    # 将数据保存到数据库
    if form.is_valid():
        # 1.获取上传文件的处理对象
        pic = request.FILES.get('picture')
        filename = _file_rename(pic.name)

        # 2.创建一个文件(用于保存图片)
        save_path = '%s/%s' % (settings.MEDIA_ROOT, filename)
        with open(save_path, 'wb') as f:
            # pic.chunks() 上传文件的内容
            for content in pic.chunks():
                f.write(content)
                file_url = '{}{}'.format(settings.MEDIA_URL, filename)
                return ResultGenerator.gen_success_result(file_url)
    else:
        raise Exception('参数有误')


# 重命名上传文件
def _file_rename(filename, user_id=None):
    code_list = []
    for i in range(10):  # 0-9数字
        code_list.append(str(i))
    # 从指定序列中随机获取指定长度的片断
    myslice = random.sample(code_list, 4)  # 从list中随机获取4个元素，作为一个片断返回
    random_str = ''.join(myslice)  # list to string
    # filename = secure_filename(filename)
    ext = filename.rsplit('.', 1)[1]
    if user_id:
        string = '{}{}'.format(random_str, user_id)
    else:
        string = str(int(time.time()))
    id_md5 = (hashlib.md5(string.encode('utf-8')).hexdigest())[0:12]
    filename = id_md5 + '.' + ext
    return filename
