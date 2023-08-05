#!/usr/bin/env python
# coding: utf-8

# Copyright (c) TmaxEnterprise.
# Distributed under the terms of the Modified BSD License.
import ipywidgets as widgets
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.express as px
from plotly import subplots


class WidgetLogisticRegression:
    @staticmethod
    def get_statistic_result_table(table):

        res_table = widgets.HTML(table.as_html())
        statistic_result_table = widgets.VBox([res_table])
        statistic_result_table.add_class('styledTable')

        return statistic_result_table

    @staticmethod
    def get_all_scatter_plot(data, columns):
        dim_list = []
        for column in columns:
            dim_dict = {'label': column, 'values': data[column]}
            dim_list.append(dim_dict)
        fig = go.FigureWidget()
        # fig.add_trace(go.Splom(dimensions=[dict(label='Period', values=data['Period']), dict(label='Data_value', values=data['Data_value'])]))
        fig.add_trace(go.Splom(dimensions=dim_list))
        fig.update_layout(
            title='Scatter Plot',
            title_x=0.5,
            title_font_size=30,
            dragmode='select',
            width=600,
            height=600,
            hovermode='closest',
        )

        return fig

    @staticmethod
    def get_heatmap_plot(data, columns):
        fig = go.FigureWidget()
        fig.add_trace(go.Heatmap(x=columns, y=columns, z=data.corr()))
        fig.update_layout(
            title='Heatmap of Variables',
            title_x=0.5,
            title_font_size=30,
            dragmode='select',
            width=600,
            height=600,
            hovermode='closest',
        )
        return fig

    @staticmethod
    def get_eda_plot(data, columns):
        scatter_plot = WidgetLogisticRegression.get_all_scatter_plot(data, columns)
        heatmap_plot = WidgetLogisticRegression.get_heatmap_plot(data, columns)
        return widgets.HBox([scatter_plot, heatmap_plot])
