#!/usr/bin/env python
# coding: utf-8

import io

# Copyright (c) kyoungjun.
# Distributed under the terms of the Modified BSD License.

# GUI
from IPython.display import display
import ipywidgets as widgets
import pandas as pd
import qgrid

# Hyderdata
try:
    import hyper
except ModuleNotFoundError:
    pass

# Common Class
from jupyter_analysis_extension.widget_style import WidgetStyle
from jupyter_analysis_extension.statistics_widget.common_widget import CommonWidget
from jupyter_analysis_extension.statistics_operation.common_util import CommonUtil

# Statistic ANOVA
from jupyter_analysis_extension.statistics_operation.anova_oneway import ANOVAOneWay
from jupyter_analysis_extension.statistics_operation.anova_ancova import ANOVAANCOVA
from jupyter_analysis_extension.statistics_operation.anova_kruskal import ANOVAKruskal
from jupyter_analysis_extension.statistics_operation.anova_rm import ANOVARM

# Statistic Regression
from jupyter_analysis_extension.statistics_operation.general_linear_regression import GeneralLinearRegression
from jupyter_analysis_extension.statistics_operation.logistic_regression import LogisticRegression

# Statistic T-test
from jupyter_analysis_extension.statistics_operation.t_test_one_sample import TTestOneSample
from jupyter_analysis_extension.statistics_operation.t_test_ind_sample import TTestIndSample
from jupyter_analysis_extension.statistics_operation.t_test_pair_sample import TTestPairSample

# Statistic Frequencies
from jupyter_analysis_extension.statistics_operation.frequencies_chi_square import FrequenciesChiSquare

OPERATION_LIST = {
    "T-test": ['T-Test : One Sample', 'T-Test : Independent Sample', 'T-Test : Paired Sample'],
    "ANOVA": ['One-way ANOVA', 'ANOVA (Kruskal-Wallis)', 'Repeated Measure ANOVA', 'ANOVA & ANCOVA'],
    "Regression": ['Linear Regression', 'Logistic Regression'],
    "Frequencies": ['Frequencies : Chi-Square']
}


class WidgetFunc:
    def __init__(self, mode=None):
        WidgetStyle.style_default()

        if mode == "HD":

            hyper_do_list = {"Select DO": "Select DO"}
            hyper_do_list.update(hyper.list_do())

            dropdown = CommonWidget.get_dropdown(options=hyper_do_list, default_option="Select DO")
            mode_widget = CommonWidget.get_widget_with_label("HyperData", dropdown,
                                                             margin="0px 0px 0px 0px")
            dropdown.observe(self.on_do_selected, names='value')
        else:
            mode_widget = widgets.FileUpload(
                accept='.csv',  # Accepted file extension e.g. '.txt', '.pdf', 'image/*', 'image/*,.pdf'
                multiple=False  # True to accept multiple files upload else False
            )
            mode_widget.observe(self.on_file_uploaded, names='value')
        self.output = widgets.Output()
        display(mode_widget)

        self.tab = widgets.Tab()
        self.tab_count = 0
        self.tab_titles = []
        self.tab_children = []

        self.active_op_class = []
        self.combobox = None

        self.input_df = None
        self.column_type_dict = None
        self.mode = mode

    def on_file_uploaded(self, value):
        # Clear all the widgets
        self.reset_widget()

        # Consider the only new csv
        file_content = list(value['new'].items())[0][1]['content']

        df = pd.read_csv(
            io.BytesIO(file_content), encoding='utf-8')
        self.set_main_tab(df)

    def on_do_selected(self, value):
        # Clear all the widgets
        self.reset_widget()

        if value['new'] == "Select DO":
            return

        df = hyper.load_do(value['new'])

        self.set_main_tab(df)

    def set_main_tab(self, df):
        self.input_df = df

        # Sampling only 10000 rows
        max_len = 10000

        sampled_df = self.input_df.copy()
        if len(self.input_df) > max_len:
            sampled_df = sampled_df.sample(n=max_len, random_state=1, replace=False)

        qgrid_widget = qgrid.show_grid(sampled_df, show_toolbar=False)

        self.column_type_dict = self.get_type_dict()
        type_widget = self.get_type_dict_accordion(self.column_type_dict)

        qgrid_widget_width_label = CommonWidget.get_widget_with_label("Table Info (10,000 Rows Sampled)", qgrid_widget)

        menu_widgets = []
        for key in OPERATION_LIST.keys():
            menu_widget = CommonWidget.get_popup_menu(
                op_catogory=key,
                items=OPERATION_LIST[key],
                click_event=self.on_append_tab)
            menu_widgets.append(menu_widget)

        menu_layout = CommonWidget.get_hbox(menu_widgets, justify_content="flex-start")
        menu_layout.add_class("icon_menu")
        menu_layout_with_label = CommonWidget.get_widget_with_label("Operation Type", menu_layout)
        menu_layout_with_label.add_class("icon_menu")
        self.tab_children = [widgets.VBox(
            [menu_layout_with_label, qgrid_widget_width_label, type_widget])]

        self.tab_titles = ['Main']

        self.tab.children = self.tab_children
        self.tab.set_title(self.tab_count, self.tab_titles[self.tab_count])
        self.tab_count += 1

        display(self.tab)

    def reset_widget(self):
        self.tab.close_all()
        self.output.clear_output()
        self.output.close_all()
        self.__init__(self.mode)

    def refresh_tab(self, target_op):
        target_widget = self.get_operation_widget(target_op)
        tab_children = list(self.tab.children)
        tab_children[self.tab.selected_index] = target_widget
        self.tab.children = tuple(tab_children)

    def on_func_selected(self, value):
        if value['name'] == 'value' and value['new'] != {} and value['new'] != "":
            if value['owner'].options[0] == value['new']:
                return
            op_name = value['new']
            self.on_append_tab(op_name)
            value['owner'].index = 0

    def on_append_tab(self, op_name):
        if op_name not in self.tab_titles:
            self.tab_children.append(self.get_operation_widget(op_name))
            self.tab_titles.append(op_name)
            self.tab.children = self.tab_children
            self.tab.set_title(
                self.tab_count, self.tab_titles[self.tab_count])
            self.tab.selected_index = self.tab_count
            self.tab_count += 1
        else:
            self.tab.selected_index = self.tab_titles.index(op_name)

    def on_type_changed(self, change):
        if change['type'] == 'change' and change['name'] == 'value':
            self.column_type_dict[change['owner'].description] = change['new']
            for op_class in self.active_op_class:
                op_class.set_refresh_text(
                    str("Column types changed! Please refresh the tab (e.g., " + change['owner'].description)
                    + "'s type -> " + str(change['new']) + ").")
        return

    def get_type_dict(self):
        column_type_dict = {}
        for column in self.input_df.columns:
            abstract_type = CommonUtil.get_abstract_type(
                self.input_df[column])
            column_type_dict[column] = abstract_type
        return column_type_dict

    def get_type_dict_accordion(self, column_type_dict):
        accordion_widget_children = []
        for key in list(column_type_dict.keys()):
            avail_type_list = CommonUtil.get_avail_type_list(
                self.input_df[key])
            dropdown_with_label = CommonWidget.get_dropdown_with_description(
                key, avail_type_list, column_type_dict[key])
            accordion_widget_children.append(dropdown_with_label)
            dropdown_with_label.observe(self.on_type_changed)

        accordion_widget = widgets.Accordion(
            children=[widgets.VBox(accordion_widget_children,
                                   layout=widgets.Layout(margin="0px", width="100%", display="flex",
                                                         flex_flow="wrap"))], selected_index=None,
            layout=widgets.Layout(margin="0px", width="100%"))
        accordion_widget.set_title(0, "Controls of Column Types")
        return accordion_widget

    def get_operation_widget(self, op_name):
        result_widget = None
        target_op = None
        if op_name == "T-Test : One Sample":
            target_op = TTestOneSample(
                self.input_df, self.column_type_dict, self.refresh_tab)
        elif op_name == "T-Test : Independent Sample":
            target_op = TTestIndSample(
                self.input_df, self.column_type_dict, self.refresh_tab)
        elif op_name == "T-Test : Paired Sample":
            target_op = TTestPairSample(
                self.input_df, self.column_type_dict, self.refresh_tab)
        elif op_name == "Linear Regression":
            target_op = GeneralLinearRegression(
                self.input_df, self.column_type_dict, self.refresh_tab)
        elif op_name == "Logistic Regression":
            target_op = LogisticRegression(
                self.input_df, self.column_type_dict, self.refresh_tab)
        elif op_name == "One-way ANOVA":
            target_op = ANOVAOneWay(
                self.input_df, self.column_type_dict, self.refresh_tab)
        elif op_name == "ANOVA (Kruskal-Wallis)":
            target_op = ANOVAKruskal(
                self.input_df, self.column_type_dict, self.refresh_tab)
        elif op_name == "Repeated Measure ANOVA":
            target_op = ANOVARM(
                self.input_df, self.column_type_dict, self.refresh_tab)
        elif op_name == "ANOVA & ANCOVA":
            target_op = ANOVAANCOVA(
                self.input_df, self.column_type_dict, self.refresh_tab)
        elif op_name == "Frequencies : Chi-Square":
            target_op = FrequenciesChiSquare(
                self.input_df, self.column_type_dict, self.refresh_tab)
        else:
            result_widget = widgets.Text(description="New Tab")

        result_widget = target_op.get_tab_widget()

        if target_op is not None:
            self.active_op_class.append(target_op)

        return result_widget
