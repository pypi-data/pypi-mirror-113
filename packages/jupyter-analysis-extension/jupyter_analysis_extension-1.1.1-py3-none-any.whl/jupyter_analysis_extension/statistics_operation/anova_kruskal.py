#!/usr/bin/env python
# coding: utf-8

# Copyright (c) TmaxBI.
# Distributed under the terms of the Modified BSD License.
import ipywidgets as widgets
import io
import numpy as np
import pandas as pd
from scipy import stats
from pandas.core.dtypes.common import is_numeric_dtype
from numpy.random import default_rng


import statsmodels
import statsmodels.api as sm
from statsmodels.formula.api import ols
import seaborn as sns
import matplotlib.pyplot as plt
from collections import namedtuple
import scipy.special as special
from jupyter_analysis_extension.statistics_widget.anova_kruskal import WidgetANOVAKruskal
from jupyter_analysis_extension.statistics_widget.common_widget import CommonWidget
from jupyter_analysis_extension.statistics_operation.common_util import CommonUtil, StatsUtil

class ANOVAKruskal:
    def __init__(self, df, column_type_list, refresh_tab):
        # Data
        self.input_df = df
        self.column_type_list = column_type_list
        self.op_name = "ANOVA (Kruskal-Wallis)"

        # func
        self.refresh_tab = refresh_tab

        # Widget & Layout
        self.control_panel = None
        self.analyze_layout = None
        self.analyze_textfield = None
        self.refresh_textfield = None

        self.construct_control_panel()

    def construct_control_panel(self):

        self.control_panel, self.control_data = CommonWidget.make_control_panel(
            df=self.input_df,
            type_list=self.column_type_list,
            title=self.op_name,
            sub=[
                {"name": "Dependent Variable(s)", "type": ["N"], "max_count": 0},
                {"name": "Grouping Variable", "type": ["C"], "max_count": 1}
            ],
            callback={"refresh": self.refresh_tab}
        )

        self.column_value = self.control_data["column"]
        self.analyze_layout = self.control_panel.children[1]

        self.analyze_layout.children[1].children[0].on_click(self.on_analyze_button_clicked)

        self.analyze_textfield = self.analyze_layout.children[0].children[0]
        self.refresh_textfield = self.analyze_layout.children[0].children[1]


    def get_tab_widget(self):
        return self.control_panel

    def on_analyze_button_clicked(self, widget):
        self.set_analyze_text('In progress...')

        # catch invalid data
        is_valid = self.validate_input_data(self.control_data)
        if not is_valid:
            return

        # get analysis data & option
        degree_freedom = len(self.input_df)-2

        dependent_layout_var_list = list(self.control_data['Dependent Variable(s)'])
        dependent_var_list = []
        for layout_var in dependent_layout_var_list:
            dependent_var_list.append(self.column_value[layout_var])

        grouping_layout_var_list = list(self.control_data['Grouping Variable'])
        group_var = self.column_value[grouping_layout_var_list[0]]
        group_var_unique_list = self.input_df[group_var].unique()

        result_widgets = self.get_result_widgets(
            degree_freedom, dependent_var_list, group_var, group_var_unique_list)

        CommonUtil.update_result_layout(self.control_panel, result_widgets)

        self.set_analyze_text('Done.')

    def validate_input_data(self, control_data):

        error_msg = CommonUtil.check_variables_types(control_data, 'Dependent Variable(s)', 'Number',
                                                     self.column_type_list, self.column_value)
        if error_msg is not None:
            self.set_analyze_text(error_msg, 'warning')
            return False

        error_msg = CommonUtil.check_variables_types(control_data, 'Grouping Variable', ['N-Category'],
                                                     self.column_type_list, self.column_value, 1)
        if error_msg is not None:
            self.set_analyze_text(error_msg, 'warning')
            return False

        grouping_var_list = control_data['Grouping Variable']
        group_var = self.column_value[grouping_var_list[0]]
        group_var_unique_count = len(self.input_df[group_var].unique())

        if group_var_unique_count > 20:
            self.set_analyze_text(
                'Grouping variable ['+group_var+'] have too many unique values', "warning")
            return False

        return True

    def set_analyze_text(self, text, mode="plain"):
        target_text = """<div style="display:flex;justify-content:flex-end">{0}</div>""".format(
            text)

        if mode == "warning":
            target_text = """<div style="font-size:1.5rem;color:red;display:flex;justify-content:flex-end">{0}</div>""".format(
                text)

        self.analyze_textfield.value = target_text

    def set_refresh_text(self, text):
        if hasattr(self, "refresh_textfield"):
            self.refresh_textfield.value = """<div style="font-size:1.5rem;color:red;display:flex;justify-content:flex-end">{0}</div>""".format(
                text)

    def get_result_widgets(self, degree_freedom, dependent_var_list, grp_var, group_var_unique_list):
        rng = default_rng(1)
        target_column_names = []
        statistic_chart = []
        statistic_chart_title = []
        statistic_result = []
        stratify_size = []
        df = self.input_df
        for dep in dependent_var_list:
            grouped_data = []
            target_column_names.append(dep)

            if len(df[df[dep].notnull()]) > 10000:
                sample = True
            else:
                sample = False

            for grp in group_var_unique_list:
                data = df[(df[grp_var] == grp) & (df[dep].notnull())][dep].values
                size = len(data)

                if size > 2:
                    grouped_data.append(data)
                else:
                    pass
            stratify_size = list(np.array(stratify_size) * 10000 / (np.sum(stratify_size)))

            target_column_names.append('')
            statistic_result.append(stats.kruskal(
                *grouped_data, nan_policy='omit'))
            target_column_names.pop()

            if sample:
                grouped_data_sample = []
                for data, size in zip (grouped_data, stratify_size):
                    if size > 2:
                       data_sample = rng.choice(data, int(size), replace=False)
                    else:
                       data_sample = rng.choice(data, 2, replace=False)
                    grouped_data_sample.append(data_sample)
            else:
                grouped_data_sample = grouped_data

            boxplot_sns = WidgetANOVAKruskal.get_boxplot_sns(
                grouped_data_sample, group_var_unique_list, dep, grp_var)
            statistic_chart.append(boxplot_sns)
            statistic_chart_title.append('Box Plot ('+str(dep) + ')')
        statistic_result_table = WidgetANOVAKruskal.get_statistic_result_table(
            target_column_names, degree_freedom, statistic_result)

        return CommonWidget.get_accordion_widget([statistic_result_table, *statistic_chart], ['Test Result(s)', *statistic_chart_title])


    """
    @staticmethod
    def get_shapiro_widgets(dependent):
        shapiro = stats.shapiro(dependent)
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

    def Ftest(df, dim, mes):
        dim = 'C(Q(\"' + dim + '\"))'
        mes = 'Q(\"' + mes + '\")'
        equation = mes + ' ~ ' + dim
        try:
            model = ols(equation, data=df).fit()
        except Exception as e:
            return np.nan, 1.
        table = sm.stats.anova_lm(model, typ=2)
        table['mean_sq'] = table[:]['sum_sq'] / table[:]['df']
        table['eta_sq'] = table[:-1]['sum_sq'] / sum(table['sum_sq'])
        table['omega_sq'] = (table[:-1]['sum_sq'] - (table[:-1]['df'] * table['mean_sq'][-1])) / (
                sum(table['sum_sq']) + table['mean_sq'][-1])
        p_value = table.at[dim, 'PR(>F)']
        eta_sq = table.at[dim, 'eta_sq']
        omega_sq = np.abs(table.at[dim, 'omega_sq'])
        effect_size = omega_sq ** (0.4 - (2 * omega_sq)) if omega_sq <= 0.2 else 1.0
        return effect_size, p_value
    """