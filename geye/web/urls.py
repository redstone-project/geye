#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    geye.web.urls
    ~~~~~~~~~~~~~


    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

from django.urls import path

from geye.web.controller.leaks import leaks
from .controller.rule import search, filter, globalFilter, monitor
from .controller.token import token
from .controller.handleCenter import searchResults, monitorResults


# 总的路由
# http://example.com/api/v1/rule/search/v1/all

# api下的总路由
urlpatterns = [
    # search rule URL
    path("v1/rule/search/all", search.ListSearchRuleView.as_view()),
    path("v1/rule/search/new", search.AddSearchRuleView.as_view()),
    path("v1/rule/search/delete", search.DeleteSearchRuleView.as_view()),
    path("v1/rule/search/change_status", search.ChangeStatusSearchRuleView.as_view()),
    path("v1/rule/search/get_detail", search.GetDetailView.as_view()),
    path("v1/rule/search/update", search.UpdateSearchRuleView.as_view()),

    # filter rule URL
    path("v1/rule/filter/new", filter.AddFilterRuleView.as_view()),
    path("v1/rule/filter/delete", filter.DeleteFilterRuleView.as_view()),
    path("v1/rule/filter/detail", filter.GetFilterRuleDetailView.as_view()),
    path("v1/rule/filter/update", filter.UpdateFilterRuleView.as_view()),

    # global filter rule
    path("v1/rule/global/all", globalFilter.AllGlobalFilterRulesView.as_view()),
    path("v1/rule/global/new", globalFilter.AddGlobalFilterRuleView.as_view()),
    path("v1/rule/global/delete", globalFilter.DeleteGlobalFilterRuleView.as_view()),
    path("v1/rule/global/detail", globalFilter.GetDetailView.as_view()),
    path("v1/rule/global/update", globalFilter.UpdateGlobalFilterRuleView.as_view()),

    # Token 相关的路由
    path("v1/token/all", token.TokensView.as_view()),
    path("v1/token/new", token.AddTokenView.as_view()),
    path("v1/token/update", token.EditTokenView.as_view()),
    path("v1/token/delete", token.DeleteTokenView.as_view()),
    path("v1/token/change_status", token.UpdateStatus.as_view()),
    path("v1/token/detail", token.TokenDetailsView.as_view()),

    # search handle center 相关的路由
    path("v1/results/all", searchResults.AllSearchResults.as_view()),
    path("v1/results/ignore", searchResults.IgnoreSearchResult.as_view()),
    path("v1/results/confirm", searchResults.ConfirmSearchResult.as_view()),

    # leaks 相关的路由
    path("v1/leaks/all", leaks.AllLeaksView.as_view()),
    path("v1/leaks/delete", leaks.DeleteLeakView.as_view()),
    path("v1/leaks/change_status", leaks.ChangeStatusLeakView.as_view()),
    path("v1/leaks/batch_change_status", leaks.BatchChangeStatusLeakView.as_view()),

    # monitor rule 相关的路由
    path("v1/rule/monitor/new", monitor.AddMonitorRuleView.as_view()),
    path("v1/rule/monitor/update", monitor.UpdateMonitorRuleView.as_view()),
    path("v1/rule/monitor/delete", monitor.DeleteMonitorRuleView.as_view()),
    path("v1/rule/monitor/all", monitor.MonitorRulesView.as_view()),

    # monitor results router
    path("v1/results/monitor/all", monitorResults.AllMonitorResults.as_view()),
]
