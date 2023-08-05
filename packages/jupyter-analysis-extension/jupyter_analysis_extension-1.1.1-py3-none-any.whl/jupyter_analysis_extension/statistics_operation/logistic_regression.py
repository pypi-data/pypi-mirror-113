#!/usr/bin/env python
# coding: utf-8

# Copyright (c) TmaxEnterprise.
# Distributed under the terms of the Modified BSD License.
import numpy as np
from pandas.core.dtypes.common import is_numeric_dtype

# Graph
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF
import plotly.express as px

import statsmodels
import statsmodels.api as sm
from statsmodels.formula.api import ols, logit
from patsy.contrasts import Treatment

from jupyter_analysis_extension.statistics_operation.common_util import CommonUtil
from jupyter_analysis_extension.statistics_widget.common_widget import CommonWidget
from jupyter_analysis_extension.statistics_widget.logistic_regression import WidgetLogisticRegression

import warnings

class LogisticRegression:
    def __init__(self, df, column_type_list, refresh_tab):
        # Data
        self.input_df = df
        self.column_type_list = column_type_list
        self.op_name = "Logistic Regression"

        self.column_value = {}
        self.control_data = None

        # func
        self.refresh_tab = refresh_tab

        # Widget & Layout
        self.control_panel = None
        self.analyze_layout = None
        self.analyze_textfield = None
        self.refresh_textfield = None

        self.construct_control_panel()

    def construct_control_panel(self):
        """
        Construct the overall visual frames of linear regressions.
        Returns
        -------
        None
        """
        self.control_panel, self.control_data = CommonWidget.make_control_panel(
            df=self.input_df,
            type_list=self.column_type_list,
            title=self.op_name,
            sub=[
                {"name": "Dependent Variable", "type": ["C"], "max_count": 1},
                {"name": "Covariates", "type": ["N"], "max_count": 0},
                {"name": "Factors", "type": ["C"], "max_count": 0}
            ],
            option=[
                {"name": "Baseline (DV)",
                 "type": "connected_unique_dropdown",
                 "connect": "Dependent Variable"},
                {"name": "Baseline (Factors)",
                 "type": "individual_connected_unique_dropdown",
                 "connect": ["Factors"], "acc_title": "List of Factors"}
                ],
            callback={"refresh": self.refresh_tab}
        )
        self.column_value = self.control_data["column"]
        self.analyze_layout = self.control_panel.children[1]

        self.analyze_layout.children[1].children[0].on_click(self.on_analyze_button_clicked)

        self.analyze_textfield = self.analyze_layout.children[0].children[0]
        self.refresh_textfield = self.analyze_layout.children[0].children[1]

    def on_analyze_button_clicked(self, widget):
        """
        Perform the check of column types and the creation of analysis results of accordion widgets.
        Returns
        -------
        None
        """
        self.set_analyze_text('In progress...')

        # catch invalid data
        is_valid = self.validate_input_data(self.control_data)
        if not is_valid:
            return

        covariates = []
        factors = []
        if 'Dependent Variable' in self.control_data.keys():
            dependent_var = self.column_value[self.control_data['Dependent Variable'][0]]
        if 'Covariates' in self.control_data.keys():
            for item in self.control_data['Covariates']:
                covariates.append(self.column_value[item])
        if 'Factors' in self.control_data.keys():
            for item in self.control_data['Factors']:
                factors.append(self.column_value[item])

        option = self.control_data['option']
        baseline_dv = option['Baseline (DV)']
        baseline_iv = option['Baseline (Factors)']
        result_widgets = self.get_result_widgets(dependent_var, baseline_dv, covariates, factors, baseline_iv)

        CommonUtil.update_result_layout(self.control_panel, result_widgets)

        self.set_analyze_text('Done.')

    def validate_input_data(self, control_data):
        """
        Check the requirement numbers of columns and types.
        Returns
        -------
        str
            None if successful, error message otherwise.
        """
        error_msg = CommonUtil.check_variables_types(control_data, 'Dependent Variable', '2-Category',
                                                     self.column_type_list, self.column_value, 1)
        if error_msg is not None:
            self.set_analyze_text(error_msg, 'warning')
            return False

        error_msg = CommonUtil.check_variables_types(control_data, 'Covariates', 'Number',
                                                     self.column_type_list, self.column_value)
        if error_msg is not None:
            self.set_analyze_text(error_msg, 'warning')
            return False

        error_msg = CommonUtil.check_variables_types(control_data, 'Factors', ['N-Category', '2-Category'],
                                                     self.column_type_list, self.column_value)
        if error_msg is not None:
            self.set_analyze_text(error_msg, 'warning')
            return False

        if ('Covariates' not in control_data.keys()) and ('Factors' not in control_data.keys()):
            self.set_analyze_text('Please enter at least 1 column in Covariates or Factors', 'warning')
            return False

        return True

    def set_analyze_text(self, text, mode="plain"):
        target_text = """<div style="display:flex;justify-content:flex-end">{0}</div>""".format(
            text)

        if mode == "warning":
            target_text = """<div style="font-size:1.5rem;color:red;display:flex;justify-content:flex-end">{0}</div>"""\
                .format(text)

        self.analyze_textfield.value = target_text

    def get_result_widgets(self, dependent_name, baseline_dv, covariates, factors, baseline_iv):
        df = self.input_df
        # Drop unrelated columns
        df = df[[dependent_name] + covariates + factors]
        # Drop the rows that have missing values in target columns.
        df = df.dropna(subset=[dependent_name] + covariates + factors)
        df[dependent_name] = (df[dependent_name]!=baseline_dv).astype(int)

        y = 'Q(\"' + dependent_name + '\")'
        X = ''
        if len(covariates) > 0:
            for comp in covariates:
                x = ' Q(\"' + comp + '\")'
                X+=x
                X+=" +"
        else:
            pass

        if len(factors) > 0:
            for comp in factors:
                x = ' C(Q(\"' + comp + '\")'
                x += ', Treatment(reference=\''+baseline_iv[comp]+'\'))'
                X += x
                X += " +"

        if len(X) > 2:
            X = X[:-2]
        else:
            raise Exception('No independent variables in the model')

        f = y + ' ~' + X
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            logitfit = logit(formula=f, data=df).fit(disp=0)
        result_table = logitfit.summary2()

        #Convert column names to original
        ls = result_table.tables[1].index.to_list()
        new_ls = []
        for i in ls:
            if i[0] == 'C':
                i = i[5:]
                i = i.replace('"), Treatment', ' ')
                i = i.replace('erence', '')
                i = i.replace('))', ')')
            elif i[0] == 'Q':
                i = i[3:]
                i = i.replace('")', '')
            else:
                pass
            new_ls.append(i)
        result_table.tables[1].index = new_ls

        dep_var = result_table.tables[0].iloc[1, 1]
        dep_var = dep_var[3:]
        dep_var = dep_var.replace('")', '')
        result_table.tables[0].iloc[1, 1] = dep_var

        stat_result_table = WidgetLogisticRegression.get_statistic_result_table(result_table)

        """
        exog = sm.add_constant(np.array(df[covariates+factors]))
        endog = np.array(df[dependent_name]==baseline)

        model = sm.Logit(endog, exog)
        result = model.fit()

        stat_result_table = result.summary2()
        """
        return CommonWidget.get_accordion_widget([stat_result_table],
                                                 ['Regression Model Info'])

    def get_tab_widget(self):
        return self.control_panel

    def set_refresh_text(self, text):
        if hasattr(self, "refresh_textfield"):
            self.refresh_textfield.value = """<div style="font-size:1.5rem;color:red;display:flex;justify-content:flex-end">{0}</div>""".format(
                text)