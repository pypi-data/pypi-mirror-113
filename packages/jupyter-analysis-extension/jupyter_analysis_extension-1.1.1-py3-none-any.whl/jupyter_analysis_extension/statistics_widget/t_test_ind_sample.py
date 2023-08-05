#!/usr/bin/env python
# coding: utf-8

# Copyright (c) kyoungjun.
# Distributed under the terms of the Modified BSD License.
from os import name
from IPython.core.display import display
import ipywidgets as widgets
from ipywidgets.widgets.widget_layout import Layout

# Graph
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF
import plotly.express as px


class WidgetTTestIndSample:
    @ staticmethod
    def get_statistic_result_table(name, degree_freedom, test_result, statistic_tests_options):
        res_table_info = ''
        for pairindex, item in enumerate(test_result):
            target_degree_freedom = degree_freedom
            statistic_value = round(item.statistic, 3)
            if statistic_tests_options[pairindex] == 'Welch\'s' or statistic_tests_options[pairindex] == 'Mann-Whitney U':
                target_degree_freedom = '-'

            if statistic_tests_options[pairindex] == 'Mann-Whitney U':
                statistic_value = '{0:e}'.format(item.statistic)

            res_table_info += """
                        <tr>
                            <td>{0}</td>
                            <td>{1}</td>
                            <td>{2}</td>
                            <td>{3}</td>
                            <td>{4}</td>
                        </tr>
                        """.format(name[pairindex], statistic_tests_options[pairindex], statistic_value,
                                   target_degree_freedom, round(item.pvalue, 3))

        res_table = widgets.HTML(
            value="""
                <table style="width:100%">
                <tr style="border-bottom: 1px solid black;">
                    <th></th>
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
    def get_box_plot_plotly(charts, dependent_var_list, series_name):
        chart_list = []
        for chart_data, ylabel in zip(charts, dependent_var_list):
            fig = go.FigureWidget()
            for index, data in enumerate(chart_data):
                fig.add_trace(
                    go.Box(y=data,
                           name=str(series_name[index % 2]),
                           boxpoints='all',
                           jitter=0.2,
                           pointpos=-1.8))
            fig.layout.yaxis.title=ylabel
            chart_list.append(fig)
        return chart_list
