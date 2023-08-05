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

import statsmodels
import statsmodels.api as sm
from statsmodels.formula.api import ols
import seaborn as sns
import matplotlib.pyplot as plt
from collections import namedtuple
import scipy.special as special
from jupyter_analysis_extension.statistics_widget.anova_ancova import WidgetANOVAANCOVA
from jupyter_analysis_extension.statistics_widget.common_widget import CommonWidget
from jupyter_analysis_extension.statistics_operation.common_util import CommonUtil, StatsUtil

class ANOVAANCOVA:
    def __init__(self, df, column_type_list, refresh_tab):
        # Data
        self.input_df = df
        self.column_type_list = column_type_list
        self.op_name = "ANOVA & ANCOVA"

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
                {"name": "Dependent Variable", "type": ["N"], "max_count": 1},
                {"name": "Fixed Factors", "type": ["C"], "max_count": 0},
                {"name": "Covariates", "type": ["N"], "max_count": 0}
            ],
            option=[
                {"name": "Type", "type": "radio", "value": ['Type 1', 'Type 2', 'Type 3']},
                {"name": "Model-Fit", "type": "connected_multiple", "acc_title": "Model",
                 "value": ["Components", "Model Terms"], "connect": ["Fixed Factors", "Covariates"]},
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
        option = self.control_data['option']
        is_valid = self.validate_input_data(self.control_data)
        if not is_valid:
            return

        # get analysis data & option
        degree_freedom = len(self.input_df)-2

        dependent_var = self.control_data['Dependent Variable']

        model_terms_list = list(option['Model Terms'])

        test_type = option['Type']['radio']
        test_type = int(test_type[-1])

        result_widgets = self.get_result_widgets(
            degree_freedom, dependent_var, model_terms_list, test_type)

        CommonUtil.update_result_layout(self.control_panel, result_widgets)

        self.set_analyze_text('Done.')

    def validate_input_data(self, control_data):

        error_msg = CommonUtil.check_variables_types(control_data, 'Dependent Variable', 'Number',
                                                     self.column_type_list, self.column_value, 1)
        if error_msg is not None:
            self.set_analyze_text(error_msg, 'warning')
            return False

        error_msg = CommonUtil.check_variables_types(control_data, 'Covariates', 'Number',
                                                     self.column_type_list, self.column_value)
        if error_msg is not None:
            self.set_analyze_text(error_msg, 'warning')
            return False

        error_msg = CommonUtil.check_variables_types(control_data, 'Fixed Factors', ['N-Category', '2-Category'],
                                                     self.column_type_list, self.column_value)
        if error_msg is not None:
            self.set_analyze_text(error_msg, 'warning')
            return False

        if 'Fixed Factors' in control_data.keys():
            fixed_factors_list = list(control_data['Fixed Factors'])
            if len(fixed_factors_list) > 3:
                self.set_analyze_text('Invalid model due to too many Fixed Factor(s)', "warning")
                return False

        if "Model Terms" not in control_data['option']:
            self.set_analyze_text('Option[Model-Fit] Model Terms should have at least 1 column', "warning")
            return False
        else:
            if len(list(control_data['option']['Model Terms'])) == 0:
                self.set_analyze_text('Option[Model-Fit] Model Terms should have at least 1 column', "warning")
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

    def get_result_widgets(self, degree_freedom, dependent_var, model_terms_list, test_type):
        interaction_mark = ' ※ '

        dep_var = self.column_value[dependent_var[0]]
        statistic_chart = []
        statistic_chart_title = []
        statistic_result = []
        df = self.input_df
        y = 'Q(\"' + dep_var + '\")'
        X = ''
        for comp in model_terms_list:
            if interaction_mark in comp:
                ls = comp.split(interaction_mark)
                x = ' C(Q(\"' + ls[0] + '\"))'+'*'+'C(Q(\"' + ls[1] + '\"))'
            else:
                if self.column_type_list[comp] == 'Number':
                    x = ' Q(\"' + comp + '\")'
                elif self.column_type_list[comp] == 'N-Category':
                    x = ' C(Q(\"' + comp + '\"))'
                elif self.column_type_list[comp] == '2-Category':
                    x = ' C(Q(\"' + comp + '\"))'
                    if len(df[comp].dropna().unique()) == 1:
                        df[comp] = df[comp].fillna('null')

            X+=x
            X+=" +"

        X = X[:-2]

        formula = y + ' ~' + X
        model = ols(formula, data=df).fit()

        table = sm.stats.anova_lm(model, typ=test_type)
        #Convert column names to original
        ls = table.index.to_list()
        new_ls = []
        for i in ls:
            if i[0] == 'C':
                i = i[5:]
                i = i.replace('"))', '')
            elif i[0] == 'Q':
                i = i[3:]
                i = i.replace('")', '')
            else:
                pass
            new_ls.append(i)
        table.index = new_ls
        statistic_result_table = WidgetANOVAANCOVA.get_statistic_result_table(table, degree_freedom, test_type)

        ## TODO. Which plot to draw for ANOVA & ANCOVA?
        """
        boxplot_sns = WidgetANOVAANCOVA.get_boxplot_sns()
        statistic_chart.append(boxplot_sns)
        statistic_chart_title.append('Box Plot (plotly): ' + str(dep))
        """

        return CommonWidget.get_accordion_widget([statistic_result_table, *statistic_chart], ['Test Result(s)', *statistic_chart_title])


    """

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