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

from statsmodels.stats.anova import AnovaRM
import seaborn as sns
import matplotlib.pyplot as plt
from collections import namedtuple
import scipy.special as special
from jupyter_analysis_extension.statistics_widget.anova_rm import WidgetANOVARM
from jupyter_analysis_extension.statistics_widget.common_widget import CommonWidget
from jupyter_analysis_extension.statistics_operation.common_util import CommonUtil, StatsUtil

class ANOVARM:
    def __init__(self, df, column_type_list, refresh_tab):
        # Data
        self.input_df = df
        self.column_type_list = column_type_list
        self.op_name = "Repeated Measure ANOVA"

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
                {"name": "Dependent Variable (R.M.)", "type": ["N"], "max_count": 1},
                {"name": "Subject ID", "type": [], "max_count": 1},
                {"name": "Within-Subject Factors", "type": ["C"], "max_count": 0}
            ],
            option=[],
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

        dependent_var = list(self.control_data['Dependent Variable (R.M.)'])[0]

        #self.input_df.dropna(inplace = True)

        subject_id = list(self.control_data['Subject ID'])[0]
        if 'Within-Subject Factors' in self.control_data.keys():
            within_factors_list = list(self.control_data['Within-Subject Factors'])
        else:
            within_factors_list = []
        result_widgets = self.get_result_widgets(
            degree_freedom, dependent_var, subject_id, within_factors_list)
        if CommonUtil.update_result_layout(self.control_panel, result_widgets):
            self.set_analyze_text('Done.')
        else:
            return

    def validate_input_data(self, control_data):

        error_msg = CommonUtil.check_variables_types(control_data, 'Dependent Variable (R.M.)', 'Number',
                                                     self.column_type_list, self.column_value, 1)
        if error_msg is not None:
            self.set_analyze_text(error_msg, 'warning')
            return False

        error_msg = CommonUtil.check_variables_types(control_data, 'Subject ID', ['Object', 'N-Category', 'Number'],
                                                     self.column_type_list, self.column_value, 1)
        if error_msg is not None:
            self.set_analyze_text(error_msg, 'warning')
            return False

        error_msg = CommonUtil.check_variables_types(control_data, 'Within-Subject Factors', ['N-Category', '2-Category'],
                                                     self.column_type_list, self.column_value)
        if error_msg is not None:
            self.set_analyze_text(error_msg, 'warning')
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

    def get_result_widgets(self, degree_freedom, dependent_var, subject_id, within_factors_list):
        statistic_chart = []
        statistic_chart_title = []
        dep_var = self.column_value[dependent_var]
        subject = self.column_value[subject_id]
        within_factors_ls = []
        if len(within_factors_list) > 0:
            for within_factor in within_factors_list:
                within_factors_ls.append(self.column_value[within_factor])
        try:
            aovrm = AnovaRM(self.input_df, dep_var, subject, within=within_factors_ls)
            table = aovrm.fit().anova_table
        except Exception as e:
            self.set_analyze_text(str(e).split('.')[0], 'warning')
            return None

        statistic_result_table = WidgetANOVARM.get_statistic_result_table(table)

        """
        boxplot_sns = WidgetANOVAANCOVA.get_boxplot_sns()
        statistic_chart.append(boxplot_sns)
        statistic_chart_title.append('Box Plot (plotly): ' + str(dep))
        """

        return CommonWidget.get_accordion_widget([statistic_result_table, *statistic_chart], ['Test Result(s)', *statistic_chart_title])