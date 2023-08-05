#!/usr/bin/env python
# coding: utf-8

# Copyright (c) kyoungjun.
# Distributed under the terms of the Modified BSD License.
import numpy as np
from pandas.core.dtypes.common import is_numeric_dtype
import pandas as pd
# from sklearn.linear_model import LinearRegression

# Graph
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF
import plotly.express as px

import statsmodels
import statsmodels.api as sm

from jupyter_analysis_extension.statistics_operation.common_util import CommonUtil
from jupyter_analysis_extension.statistics_widget.common_widget import CommonWidget
from jupyter_analysis_extension.statistics_widget.general_linear_regression import WidgetGeneralLinearRegression
from jupyter_analysis_extension.statistics_widget.t_test_one_sample import WidgetTTestOneSample


class GeneralLinearRegression:
    def __init__(self, df, column_type_list, refresh_tab):
        # Data
        self.input_df = df
        self.column_type_list = column_type_list
        self.op_name = "Linear Regression"

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
                {"name": "Dependent Variable", "type": ["N"], "max_count": 1},
                {"name": "Numeric Variables", "type": ["N"], "max_count": 0},
                {"name": "Categorical Variables", "type": ["C"], "max_count": 0}
            ],
            option=[
                {"name": "Baseline (CV)",
                 "type": "individual_connected_unique_dropdown",
                 "connect": ["Categorical Variables"], "acc_title": "List of CVs"}
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

        dependent_var = None
        numeric_vars = None
        categorical_vars = None
        if 'Dependent Variable' in self.control_data.keys():
            dependent_var = self.column_value[self.control_data['Dependent Variable'][0]]
        if 'Numeric Variables' in self.control_data.keys():
            numeric_vars = []
            for item in self.control_data['Numeric Variables']:
                numeric_vars.append(self.column_value[item])
        if 'Categorical Variables' in self.control_data.keys():
            categorical_vars = []
            for item in self.control_data['Categorical Variables']:
                categorical_vars.append(self.column_value[item])

        option = self.control_data['option']
        baseline_cv = option['Baseline (CV)']

        result_widgets = self.get_result_widgets(dependent_var, numeric_vars, categorical_vars, baseline_cv)

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
        error_msg = CommonUtil.check_variables_types(control_data, 'Dependent Variable', 'Number',
                                                     self.column_type_list, self.column_value, 1)
        if error_msg is not None:
            self.set_analyze_text(error_msg, 'warning')
            return False

        error_msg = CommonUtil.check_variables_types(control_data, 'Numeric Variables', 'Number',
                                                     self.column_type_list, self.column_value)
        if error_msg is not None:
            self.set_analyze_text(error_msg, 'warning')
            return False

        error_msg = CommonUtil.check_variables_types(control_data, 'Categorical Variables', ['N-Category', '2-Category'],
                                                     self.column_type_list, self.column_value)
        if error_msg is not None:
            self.set_analyze_text(error_msg, 'warning')
            return False

        if ('Numeric Variables' not in control_data.keys()) and ('Categorical Variables' not in control_data.keys()):
            self.set_analyze_text('Please enter at least 1 column in Numeric Variables or Categorical Variables', 'warning')
            return False

        return True

    def set_analyze_text(self, text, mode="plain"):
        target_text = """<div style="display:flex;justify-content:flex-end">{0}</div>""".format(
            text)

        if mode == "warning":
            target_text = """<div style="font-size:1.5rem;color:red;display:flex;justify-content:flex-end">{0}</div>"""\
                .format(text)

        self.analyze_textfield.value = target_text

    def get_result_widgets(self, dependent_name, numeric_names, categorical_names, baseline_cv):
        if not categorical_names:
            eda_plot, stat_result_table, EDA_plot_title= self.get_linear_regression_info(dependent_name, numeric_names)
        else:
            eda_plot, stat_result_table, EDA_plot_title = self.get_linear_regression_with_categorical_info(dependent_name, numeric_names, categorical_names, baseline_cv)

        return CommonWidget.get_accordion_widget([eda_plot, stat_result_table],
                                                 [EDA_plot_title, 'Regression Model Info'])

    def get_linear_regression_info(self, dependent_name, numeric_names):
        df = self.input_df
        target_col_list = list(set([dependent_name] + numeric_names))
        # Drop unrelated columns
        df = df[target_col_list]
        # Drop the rows that have missing values in target columns.
        df = df.dropna(subset=target_col_list)

        x_data = np.array(df[numeric_names])
        # x_data_refined = x_data.reshape((-1, 1))
        y_data = np.array(df[dependent_name])

        # OLS Regression result
        x_data_sm = sm.add_constant(x_data)
        ls = sm.OLS(y_data, x_data_sm).fit()
        summary_table = ls.summary(yname=dependent_name, xname=['Intercept'] + numeric_names)
        # summary_table = ls.summary()
        # model = LinearRegression().fit(x_data, y_data)
        # Coefficient of determination, R^2
        # r_sq = round(model.score(x_data, y_data), 4)

        # coefficient (b_0)
        # intercept = np.round(model.intercept_, 4)
        # coefficient (b_1)
        # slope = np.round(model.coef_, 4)

        # Widget Generation
        # - EDA
        # Dependent & Target 들의 pairplot
        # Dependent & Target 들의 corr의 heatmap
        # (cate) Dependent & Target 들의 pairplot w/ categorical
        # eda_graphs = WidgetGeneralLinearRegression.get_eda_graphs()
        EDA_plot_title = "Exploratory Data Analysis (EDA)"
        sampled_df = df.copy()
        if len(self.input_df) > 10000:
            EDA_plot_title += " (Sampling 10000 rows)"
            # Sampling only 10000 rows
            sampled_df = sampled_df.sample(n=10000, random_state=1, replace=False)
        eda_plot = WidgetGeneralLinearRegression.get_eda_plot(sampled_df, target_col_list)

        # - Regression
        # R^2, intercept, ...
        # (cate x) regplot
        # (cate) boxplot of Dependent & Target based on categorical
        # Coef
        # stat_result_table = WidgetGeneralLinearRegression.get_statistic_result_table(numeric_names, r_sq, intercept, slope)
        overall_results_as_html = summary_table.tables[0].as_html()
        params_results_as_html = summary_table.tables[1].as_html()
        # pd.read_html(results_as_html, header=0, index_col=0)[0]
        stat_result_table = WidgetGeneralLinearRegression.get_statistic_result_table(overall_results_as_html, params_results_as_html)

        # Prediction
        # y_preds = model.predict(x_data)
        #print(y_preds.shape)
        # for numeric_name, y_pred in zip(numeric_names, y_preds):
            # sns.scatterplot(data=df, x=dependent_name, y=numeric_name)
            # sns.lineplot(x=x_data, y=y_pred)
        # plt.scatter(x_data_refined, y_data_refined, color='black')
        # plt.plot(x_data_refined, y_pred, color='blue', linewidth=3)

        return eda_plot, stat_result_table, EDA_plot_title

    def get_linear_regression_with_categorical_info(self, dependent_name, numeric_names, categorical_names, baseline_cv):
        df = self.input_df
        type_list = self.column_type_list
        target_col_list = list(set([dependent_name] + numeric_names + categorical_names))

        # Drop unrelated columns
        df = df[target_col_list]

        # Drop the rows that have missing values in target columns.
        df = df.dropna(subset=target_col_list)
        # consider k-1 levels of k categorical levels if drop_first is True.
        twocategory = []
        set_baseline = []
        multicategory = []
        drop_baseline = []
        for key, value in baseline_cv.items():
            if type_list[key] == '2-Category':
                uniq = df[key].dropna().unique()
                add = str(uniq[uniq!=value][0])
                df[key+'_'+add] = (df[key] != value).astype(int)
                drop_baseline.append(key)
            else:
                multicategory.append(key)
                drop_baseline.append(key+'_'+value)
        if len(multicategory) > 0:
            df_dummy = pd.concat((df, pd.get_dummies(df[multicategory], prefix=multicategory, drop_first=False)), axis=1)
        else:
            df_dummy = df
        df_dummy = df_dummy.drop(multicategory + drop_baseline, axis=1)
        x_cols_dummy = list(df_dummy.columns)
        x_cols_dummy.remove(dependent_name)
        x_data = np.array(df_dummy[x_cols_dummy])
        # x_data_refined = x_data.reshape((-1, 1))
        y_data = np.array(df_dummy[dependent_name])

        # OLS Regression result
        x_data_sm = sm.add_constant(x_data)
        ls = sm.OLS(y_data, x_data_sm).fit()
        summary_table = ls.summary(yname=dependent_name, xname=['Constant'] + x_cols_dummy)

        # Widget Generation
        # - EDA
        # Dependent & Target 들의 pairplot
        # Dependent & Target 들의 corr의 heatmap
        # (cate) Dependent & Target 들의 pairplot w/ categorical
        # eda_graphs = WidgetGeneralLinearRegression.get_eda_graphs()
        EDA_plot_title = "Exploratory Data Analysis (EDA)"
        sampled_df = df.copy()
        if len(self.input_df) > 10000:
            EDA_plot_title += " (Sampling 10000 rows)"
            # Sampling only 10000 rows
            sampled_df = sampled_df.sample(n=10000, random_state=1, replace=False)
        eda_plot = WidgetGeneralLinearRegression.get_categorical_eda_plot(sampled_df, [dependent_name] + numeric_names, categorical_names)

        # - Regression
        # R^2, intercept, ...
        # (cate x) regplot
        # (cate) boxplot of Dependent & Target based on categorical
        # Coef
        # stat_result_table = WidgetGeneralLinearRegression.get_statistic_result_table(numeric_names, r_sq, intercept, slope)
        overall_results_as_html = summary_table.tables[0].as_html()
        params_results_as_html = summary_table.tables[1].as_html()
        # pd.read_html(results_as_html, header=0, index_col=0)[0]
        stat_result_table = WidgetGeneralLinearRegression.get_statistic_result_table(overall_results_as_html, params_results_as_html)

        # Prediction
        # y_preds = model.predict(x_data)
        #print(y_preds.shape)
        # for numeric_name, y_pred in zip(numeric_names, y_preds):
            # sns.scatterplot(data=df, x=dependent_name, y=numeric_name)
            # sns.lineplot(x=x_data, y=y_pred)
        # plt.scatter(x_data_refined, y_data_refined, color='black')
        # plt.plot(x_data_refined, y_pred, color='blue', linewidth=3)

        return eda_plot, stat_result_table, EDA_plot_title

    def get_tab_widget(self):
        return self.control_panel

    def set_refresh_text(self, text):
        if hasattr(self, "refresh_textfield"):
            self.refresh_textfield.value = """<div style="font-size:1.5rem;color:red;display:flex;justify-content:flex-end">{0}</div>""".format(
                text)