#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    geye.web.controller.rule.monitor
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Monitor Rule相关的控制器

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2019 lightless. All rights reserved
"""
import json
from typing import List

from django.db import transaction
from django.views import View
from django.http import JsonResponse

from geye.utils.log import logger
from geye.utils.validator import RequestValidator
from geye.database.models.monitorRules import MonitorEventTypeConstant, MonitorTaskTypeConstant, GeyeMonitorRules


class MonitorRulesView(View):
    """
    获取所有的monitor rule信息
    """

    @staticmethod
    def get(request):
        rows: List[GeyeMonitorRules] = GeyeMonitorRules.instance.get_all()
        return JsonResponse({
            "code": 1001, "message": "获取成功!",
            "data": [
                {
                    "id": row.id,
                    "taskType": row.task_type,
                    "eventType": row.event_type.split(","),
                    "ruleContent": row.rule_content,
                    "status": row.status,
                    "interval": row.interval,
                    "priority": row.priority,
                    "lastFetchTime": row.last_fetch_time,
                } for row in rows
            ]})


class AddMonitorRuleView(View):
    """
    添加一条 monitor rule
    eventType: (...)
    interval: (...)
    priority: (...)
    ruleContent: (...)
    status: (...)
    taskType: (...)
    """

    @staticmethod
    def post(request):

        logger.debug(f"POST data: {request.body}")

        # 校验参数
        validator = RequestValidator()
        result = validator.check_params(request, check_params=[
            "taskType", "eventType", "interval", "priority", "ruleContent", "status"
        ], check_empty=True)
        if result.has_error:
            return JsonResponse({"code": 1004, "message": result.error_message})

        # 校验参数
        params = result.params
        # logger.debug(f"params: {params}")
        task_type = params.get("taskType")
        event_type = params.get("eventType")
        logger.debug(f"TaskTypeConstantList: {MonitorTaskTypeConstant.lst()}")
        logger.debug(f"EventTypeConstantList: {MonitorEventTypeConstant.lst()}")
        if task_type not in MonitorTaskTypeConstant.lst():
            return JsonResponse({"code": 1003, "message": "taskType有误!"})
        for _post_event_type in event_type:
            if _post_event_type not in MonitorEventTypeConstant.lst():
                return JsonResponse({"code": 1003, "message": "eventType有误!"})

        # 插入数据
        obj = GeyeMonitorRules.instance.create(
            task_type=task_type, event_type=",".join(event_type), rule_content=params.get("ruleContent"),
            status=params.get("status"), interval=params.get("interval"), priority=params.get("priority")
        )
        if obj:
            return JsonResponse({"code": 1001, "message": "添加成功", "data": obj.convert_to_dict()})
        else:
            return JsonResponse({"code": 1002, "message": "添加失败"})


class UpdateMonitorRuleView(View):
    """
    更新一条 monitor rule
    """

    @staticmethod
    def post(request):

        logger.debug(f"POST data: {request.body}")

        # 校验参数
        validator = RequestValidator()
        result = validator.check_params(request, check_params=[
            "taskType", "eventType", "interval", "priority", "ruleContent", "status"
        ], check_empty=True)
        if result.has_error:
            return JsonResponse({"code": 1004, "message": result.error_message})

        # 校验参数
        params = result.params
        task_type = params.get("taskType")
        event_type = params.get("eventType")
        if task_type not in MonitorTaskTypeConstant.lst():
            return JsonResponse({"code": 1003, "message": "taskType有误!"})
        for _post_event_type in event_type:
            if _post_event_type not in MonitorEventTypeConstant.lst():
                return JsonResponse({"code": 1003, "message": "eventType有误!"})

        # 更新数据
        with transaction.atomic():
            obj: GeyeMonitorRules = GeyeMonitorRules.instance.select_for_update(). \
                filter(is_deleted=False, pk=params.get("id")).first()
            if not obj:
                return JsonResponse({"code": 1003, "message": "规则不存在!"})

            obj.task_type = task_type
            obj.event_type = ",".join(event_type)
            obj.rule_content = params.get("ruleContent")
            obj.status = params.get("status")
            obj.interval = params.get("interval")
            obj.priority = params.get("priority")
            obj.save()

            return JsonResponse({"code": 1001, "message": "更新成功!"})


class DeleteMonitorRuleView(View):
    """
    删除一条 monitor rule
    """

    @staticmethod
    def post(request):
        rule_id = json.loads(request.body).get("id", None)
        if not rule_id or not GeyeMonitorRules.instance.is_pk_exist(rule_id):
            return JsonResponse({"code": 1004, "message": "规则不存在!"})

        obj = GeyeMonitorRules.instance.fake_delete_by_pk(rule_id)
        if obj:
            return JsonResponse({"code": 1001, "message": "删除成功!"})
        else:
            return JsonResponse({"code": 1002, "message": "删除失败!"})
