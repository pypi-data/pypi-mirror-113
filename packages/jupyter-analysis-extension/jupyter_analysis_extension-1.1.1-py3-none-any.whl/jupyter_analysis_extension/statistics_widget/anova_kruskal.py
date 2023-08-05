#!/usr/bin/env python
# coding: utf-8

# Copyright (c) TmaxBI.
# Distributed under the terms of the Modified BSD License.
import ipywidgets as widgets

# Graph
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF
import plotly.express as px

import statsmodels
import statsmodels.api as sm
from statsmodels.formula.api import ols
import seaborn as sns
import matplotlib.pyplot as plt


class WidgetANOVAKruskal:
    @ staticmethod
    def get_statistic_result_table(name, degree_freedom, test_result):
        res_table_info = ''

        for pairindex, item in enumerate(test_result):
            target_degree_freedom = degree_freedom
            statistic_value = round(item.statistic, 3)
            target_degree_freedom = '-'

            res_table_info += """
                        <tr>
                            <td>{0}</td>
                            <td>{1}</td>
                            <td>{2}</td>
                            <td>{3}</td>
                        </tr>
                        """.format(name[pairindex], statistic_value,
                                   target_degree_freedom, round(item.pvalue, 3))

        res_table = widgets.HTML(
            value="""
                <table style="width:100%">
                <tr style="border-bottom: 1px solid black;">
                    <th></th>
                    <th>Statistic</th>
                    <th>df</th>
                    <th>p-value</th>
                </tr>
               {0}
                </table>""".format(res_table_info),
            disabled=True
        )
        statistic_result_table = widgets.VBox([res_table])
        statistic_result_table.add_class('styledTable')

        return statistic_result_table

    @staticmethod
    def get_boxplot_sns(grouped_data, group_val_distinct, dep, grp_var):
        fig = go.FigureWidget()
        for data, index in zip(grouped_data, group_val_distinct):
            fig.add_trace(go.Box(y=data,
                                 name=str(index),
                                 boxpoints='all',
                                 jitter=0.2,
                                 pointpos=-1.8
                                 ))
        fig.layout.yaxis.title = dep
        fig.layout.xaxis.title = grp_var
        return fig