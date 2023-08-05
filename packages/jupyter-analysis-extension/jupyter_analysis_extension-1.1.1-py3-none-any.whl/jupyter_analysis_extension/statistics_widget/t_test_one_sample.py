#!/usr/bin/env python
# coding: utf-8

# Copyright (c) kyoungjun.
# Distributed under the terms of the Modified BSD License.
from os import name
import ipywidgets as widgets

# Graph
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF
import plotly.express as px
import numpy as np



class WidgetTTestOneSample:
    @ staticmethod
    def get_statistic_result_table(name, degree_freedom, test_result, statistic_tests_options):
        res_table_info = ''

        for pairindex, item in enumerate(test_result):
            statistic_value = round(item.statistic, 1)
            if statistic_tests_options[pairindex] == 'Wilcoxon signed-rank':
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
                                   degree_freedom, round(item.pvalue, 3))

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
    def get_box_plot_plotly(data_list):
        fig = go.FigureWidget()
        for data in data_list:
            fig.add_trace(
                go.Box(y=data,
                       name=data.name,
                       boxpoints='all',
                       jitter=0.2,
                       pointpos=-1.8
                       ))
        return fig
    #
    # @staticmethod
    # def get_box_plot_plotly(data_list):
    #     fig = go.FigureWidget()
    #     np.random.seed(1)
    #     x = np.random.randn(500)
    #     for data in data_list:
    #
    #         fig.add_trace(go.Histogram(x=data))
    #         # fig.add_trace(go.Heatmap(z=[[1, 20, 30, 50, 1], [20, 1, 60, 80, 30], [30, 60, 1, -10, 20]],
    #         #        x=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
    #         #        y=['Morning', 'Afternoon', 'Evening']))
    #     fig.update_layout(barmode='overlay')
    #     return fig
