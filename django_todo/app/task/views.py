from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import UpdateModelMixin
from rest_framework.decorators import action
from django.db.models import Q
import logging
import arrow
from django_todo.app.libs.pagination import CustomPagination
from django_todo.app.libs.result_handler import ResultGenerator
from ..models.task import Item
from .serializers import ItemSerializer
from .forms import ItemForm

logger = logging.getLogger('django')


class ItemViewSet(UpdateModelMixin, CustomPagination, GenericViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Item.objects.all().order_by('create_time')
    serializer_class = ItemSerializer

    def get(self, request, pk):
        logger.info(pk)
        res = Item.objects.get(pk=pk)
        serializer = ItemSerializer(res)
        return ResultGenerator.gen_success_result(serializer.data)

    def list(self, request):
        user = request.user
        params = request.query_params
        item_type = params.get('type')
        page = params.get('page')
        startDate = params.get('startDate')
        endDate = params.get('endDate')
        if startDate is not None:
            startDate = arrow.get(startDate, 'YYYYMMDDHHmmss').datetime
        if endDate is not None:
            endDate = arrow.get(endDate, 'YYYYMMDDHHmmss').datetime
        condition = Q(user_id=user.id)
        current_time = arrow.now().datetime
        if item_type == '1':
            condition = condition & Q(completed=0) & Q(
                expire_time__gt=current_time)
        elif item_type == '2':
            condition = condition & Q(completed=1)
        elif item_type == '3':
            condition = condition & Q(completed=0) & Q(
                expire_time__lt=current_time)
        if item_type == '2' or item_type == '3':
            if startDate is not None:
                condition = condition & Q(create_time__gt=startDate)
            if endDate is not None:
                condition = condition & Q(create_time__lt=endDate)
        queryset = Item.objects.filter(condition).order_by('create_time')
        if page is None:
            serializer = ItemSerializer(queryset, many=True)
            return ResultGenerator.gen_success_result(serializer.data)
        results = self.paginate_queryset(queryset, request, view=self)
        serializer = ItemSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request):
        user = request.user
        data = request.data
        data['user_id'] = user.id
        expire = data.get('expire')
        if expire is None:
            expire = arrow.now().shift(days=7).datetime
            data['expire_time'] = expire
        else:
            expire = arrow.get(expire).datetime
            data['expire_time'] = expire
        form = ItemForm(data)
        # 校验表单
        if form.is_valid():
            # 保存到数据库
            item = form.save()
            serializer = ItemSerializer(item)
            return ResultGenerator.gen_success_result(serializer.data)
        else:
            logger.info(form.errors.as_json)
            return ResultGenerator.gen_fail_result('check params')

    def update(self, request, *args, **kwargs):
        user = request.user
        request.data['user_id'] = user.id
        res = super().update(request, *args, **kwargs)
        return ResultGenerator.gen_success_result(res.data)

    def destroy(self, request, pk):
        Item.objects.filter(id=pk).delete()
        return ResultGenerator.gen_success_result()

    @action(detail=False, methods=['GET'])
    def statistics(self, request):
        user = request.user
        current_time = arrow.now().datetime
        condition1 = Q(user_id=user.id) & Q(completed=1)
        condition2 = Q(user_id=user.id) & Q(completed=0) & Q(
            expire_time__lt=current_time)
        all_items = Item.objects.filter(user_id=user.id).count()
        complete = Item.objects.filter(condition1).count()
        expire = Item.objects.filter(condition2).count()
        return ResultGenerator.gen_success_result({
            'all': all_items,
            'complete': complete,
            'expire': expire,
        })

    @action(detail=False, methods=['DELETE'])
    def delete(self, request):
        user = request.user
        params = request.query_params
        item_type = params.get('type')
        condition = Q(user_id=user.id)
        current_time = arrow.now().datetime
        if item_type == '1':
            condition = condition & Q(completed=0) & Q(
                expire_time__gt=current_time)
        elif item_type == '2':
            condition = condition & Q(completed=1)
        elif item_type == '3':
            condition = condition & Q(completed=0) & Q(
                expire_time__lt=current_time)
        Item.objects.filter(condition).delete()
        return ResultGenerator.gen_success_result()
