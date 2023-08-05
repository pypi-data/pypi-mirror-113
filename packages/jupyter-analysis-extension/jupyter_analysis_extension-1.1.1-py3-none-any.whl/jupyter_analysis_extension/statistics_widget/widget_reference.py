#!/usr/bin/env python
# coding: utf-8

# Copyright (c) kyoungjun.
# Distributed under the terms of the Modified BSD License.
import ipywidgets as widgets
from scipy import stats

# Graph
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF
import plotly.express as px

import statsmodels
import statsmodels.api as sm
from statsmodels.formula.api import ols
import seaborn as sns
import matplotlib.pyplot as plt


class WidgetTTest:
    def __init__(self, df):
        self.input_df = df

        self.group_sub = widgets.Dropdown(
            options=self.input_df.columns,
            description='Grouping Subject: ',
            style=dict(description_width='initial')
        )
        self.column = widgets.Dropdown(
            options=self.input_df.columns,
            description='Column: ',
            style=dict(description_width='initial')
        )
        click_button = widgets.Button(
            description='Analyze',
            disabled=False,
            button_style='',
            tooltip='Analyze',
            icon='check')

        click_button.on_click(self.on_analyze_button_clicked)
        margin = widgets.Layout(margin='5px 5px 5px 5px', align_items='center')
        self.agg_widget = widgets.VBox(
            [widgets.HBox([self.group_sub, self.column, click_button], layout=margin)], layout=margin)

    def get_t_test_intro_widget(self):
        return self.agg_widget

    def on_analyze_button_clicked(self, widget):
        sub1 = self.input_df.groupby(self.group_sub.value)[
            self.column.value].nth(0)
        sub2 = self.input_df.groupby(self.group_sub.value)[
            self.column.value].nth(1)

        self.agg_widget.children += (self.get_accordion_widgets(sub1, sub2),)
        # self.agg_widget.children = (*self.agg_widget.children, sharpiro_agg_widget)

    def get_accordion_widgets(self, sub1, sub2):
        sharpiro_agg_widget = self.get_shapiro_widgets(sub1, sub2)
        int_test_ind_widget = self.get_int_test_ind_widget(sub1, sub2)
        box_plot_plotly_widget = self.get_box_plot_plotly(sub1, sub2)
        box_plot_seaborn_widget = self.get_box_plot_seaborn(
            self.input_df, self.group_sub.value, self.column.value)
        accordion_widget = widgets.Accordion(children=[sharpiro_agg_widget, int_test_ind_widget,
                                                       box_plot_plotly_widget, box_plot_seaborn_widget], layout=widgets.Layout(width='100%'))
        title_list = ['Sharpiro', 'INT IND',
                      'Box Plot (plotly)', 'Box Plot (seaborn)']
        for i in range(len(accordion_widget.children)):
            accordion_widget.set_title(i, title_list[i])
        return accordion_widget

    @staticmethod
    def get_box_plot_plotly(sub1, sub2):
        f = go.FigureWidget()
        f.add_trace(go.Box(y=sub1))
        f.add_trace(go.Box(y=sub2))
        return f

    @staticmethod
    def get_box_plot_seaborn(input_df, group_sub, column):
        out = widgets.Output()
        with out:
            sns.boxplot(data=input_df, x=group_sub, y=column)
            plt.show()
        return out

    @staticmethod
    def get_shapiro_widgets(sub1, sub2):
        sub1_shapiro = stats.shapiro(sub1)
        sub2_shapiro = stats.shapiro(sub2)
        sub1_shapiro = widgets.HTML(
            value='statistics: {0}, pvalue: {1}'.format(round(sub1_shapiro.statistic, 4),
                                                        round(sub1_shapiro.pvalue, 4)),
            description="sub1's shapiro > ",
            disabled=True
        )
        sub2_shapiro = widgets.HTML(
            value='statistics: {0}, pvalue: {1}'.format(round(sub2_shapiro.statistic, 4),
                                                        round(sub2_shapiro.pvalue, 4)),
            description="sub2's shapiro > ",
            disabled=True
        )
        sharpiro_agg_widget = widgets.VBox([sub1_shapiro, sub2_shapiro])
        return sharpiro_agg_widget

    @staticmethod
    def get_int_test_ind_widget(sub1, sub2):
        res = stats.ttest_ind(sub1, sub2,
                              equal_var=True)
        sub1_int_test = widgets.HTML(
            value='statistics: {0}, pvalue: {1}'.format(
                round(res.statistic, 4), round(res.pvalue, 4)),
            description="inttest_ind > ",
            disabled=True
        )
        int_test_agg_widget = widgets.VBox([sub1_int_test])

        return int_test_agg_widget
