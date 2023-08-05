import numpy as np
import pandas as pd
from collections import namedtuple
from scipy import stats
import scipy.special as special
from pandas.api.types import is_numeric_dtype
from statsmodels.stats.outliers_influence import variance_inflation_factor

class CommonUtil:
    bool_cond_list = ["0", "1", "x", "X", "y", "Y", "Yes", "No", "yes",
                      "no", "true", "false", "True", "False", "YES", "NO", "TRUE", "FALSE"]
    type_dic = {}
    # distinct_list's elem in bool_cond_list

    @staticmethod
    def get_abstract_type(col):
        # Check whether NaN values exist in columns
        if len(col.dropna().unique())==2:
            abstract_type = '2-Category'
        else:
            if col.isnull().all():
                abstract_type = 'NaN'
            elif col.dtype == np.float or col.dtype == np.int64:
                abstract_type = 'Number'
            elif col.dtype == np.bool:
                abstract_type = '2-Category'
            elif col.dtype == np.object:
                abstract_type = 'Object'
            else:
                abstract_type = 'Object'
        return abstract_type

    @staticmethod
    def get_avail_type_list(column_data):
        uniq = len(column_data.dropna().unique())
        type_list = ['Object', 'N-Category']

        if column_data.isnull().all():
            type_list.append('NaN')
            return type_list

        if is_numeric_dtype(column_data):
            type_list.append('Number')

        if uniq < 3:
            type_list.remove('N-Category')
            if uniq == 2:
                type_list.append('2-Category')
            elif uniq == 1:
                if column_data.isnull().any():
                    type_list.append('2-Category')
                else:
                    type_list.append('Constant')
            else:
                return ['NaN']

        return type_list

    @staticmethod
    def get_column_name_with_type(column_name_list, column_type_list):
        column_with_type = {}
        for column in column_name_list:
            type_name = column_type_list[column]
            if type_name != 'NaN':
                name_with_type = column + " (" + str(type_name) + ")"
                column_with_type[name_with_type] = column
        return column_with_type

    @staticmethod
    def connect_multiples_by_button(control_data, from_title,from_widget, to_title,to_widget, add_btn, delete_btn,
                                    max_count=0):
        def add_btn_clicked(self):
            changed_options = list(to_widget.options)
            changed_options.extend(from_widget.value)
            if max_count > 0:
                changed_options = changed_options[-max_count:]
            to_widget.options = tuple(changed_options)
            control_data[to_title] = changed_options
            from_widget.value = ()
            to_widget.value = ()
        add_btn.on_click(add_btn_clicked)

        def delete_btn_clicked(self):
            changed_options = list(to_widget.options)
            for item in to_widget.value:
                changed_options.remove(item)
            to_widget.options = tuple(changed_options)
            control_data[to_title] = changed_options
            from_widget.value = ()
            to_widget.value = ()
        delete_btn.on_click(delete_btn_clicked)
        return

    @staticmethod
    def update_result_layout(control_panel, result_widget):
        if result_widget is not None:
            target_widget = list(control_panel.children)
            target_widget[2] = result_widget
            control_panel.children = tuple(target_widget)
            return True
        else:
            return False
    @staticmethod
    def check_variables_types(control_data, col_name, target_types, column_type_list, column_value, count_limit=None):
        """
        Check the requirements of types in the control panel

        Parameters
        ----------
        control_data : dict
        col_name : str
            Name of the target column.
        target_types
        column_type_list
        column_value
        count_limit : int
            (Optional) Required number of columns, None means no limitation in counts.

        Returns
        -------
        object
        """
        error_msg = None
        if count_limit is not None:
            if col_name not in control_data.keys():
                error_msg = 'Please enter the ' + col_name + '.'
            elif len(control_data[col_name]) < count_limit:
                error_msg = 'Please set the number of ' + col_name + ' above ' + str(count_limit) + '.'

        if col_name in control_data.keys():
            type_condition = True
            column_list = []
            for item in control_data[col_name]:
                if str(column_type_list[column_value[item]]) not in target_types:
                    column_list.append(column_value[item])
                    type_condition = False

            if not type_condition:
                if len(column_list) > 1:
                    error_msg = col_name + ' of [' + ', '.join(column_list) + '] are not ' + str(target_types) + ' type.'
                else:
                    error_msg = col_name + ' of [' + ', '.join(column_list) + '] is not ' + str(target_types) + ' type.'
        return error_msg

    @staticmethod
    def check_option_checkbox(control_data, option_name, minimum_checked=None):
        error_msg = None
        target_option = control_data["option"][option_name]

        checked_list = []
        if minimum_checked is not None:
            for key in target_option.keys():
                checked_list.append(target_option[key])
            if checked_list.count(True) < minimum_checked:
                error_msg = 'Please check Option-'+option_name+' at least '+str(minimum_checked)
        return error_msg

class StatsUtil:

    @staticmethod
    def welch_anova(*args, var_equal=False):
        # https://svn.r-project.org/R/trunk/src/library/stats/R/oneway.test.R
        # translated from R Welch ANOVA (not assuming equal variance)
        # as cited in https://github.com/scipy/scipy/issues/11122
        F_onewayResult = namedtuple('F_onewayResult', ('statistic', 'pvalue'))
        args = [np.asarray(arg, dtype=float) for arg in args]
        k = len(args)
        ni = np.array([len(arg) for arg in args]).astype(float)
        mi = np.array([np.mean(arg) for arg in args]).astype(float)
        vi = np.array([np.var(arg, ddof=1) for arg in args]).astype(float)
        wi = np.divide(ni, vi, out=np.zeros_like(ni), where=vi!=0)

        tmp = sum((1 - wi / sum(wi)) ** 2 / (ni - 1))
        tmp /= (k ** 2 - 1)

        dfbn = k - 1
        dfwn = 1 / (3 * tmp)

        m = sum(mi * wi) / sum(wi)
        f = sum(wi * (mi - m) ** 2) / ((dfbn) * (1 + 2 * (dfbn - 1) * tmp))
        prob = special.fdtrc(dfbn, dfwn, f)  # equivalent to stats.f.sf
        return F_onewayResult(f, prob)

    @staticmethod
    def vif(X, thresh=5.0):
        variables = list(range(X.shape[1]))
        dropped = True
        while dropped:
            dropped = False
            vif = [variance_inflation_factor(X.iloc[:, variables].values, ix)
                   for ix in range(X.iloc[:, variables].shape[1])]

            maxloc = vif.index(max(vif))
            if max(vif) > thresh:
                print('dropping \'' + X.iloc[:, variables].columns[maxloc] +
                      '\' at index: ' + str(maxloc))
                del variables[maxloc]
                dropped = True

        print('Remaining variables:')
        print(X.columns[variables])
        return X.iloc[:, variables]

    @staticmethod
    def stratified_sample(df, strata, size=10000, seed=None, keep_index=True):
        '''
        It samples data from a pandas dataframe using strata. These functions use
        proportionate stratification:
        n1 = (N1/N) * n
        where:
            - n1 is the sample size of stratum 1
            - N1 is the population size of stratum 1
            - N is the total population size
            - n is the sampling size
        Parameters
        ----------
        :df: pandas dataframe from which data will be sampled.
        :strata: list containing columns that will be used in the stratified sampling.
        :size: sampling size. Fixed to 10000 temporarily.
        :seed: sampling seed
        :keep_index: if True, it keeps a column with the original population index indicator

        Returns
        -------
        A sampled pandas dataframe based in a set of strata.
        '''
        population = len(df)
        tmp = df[strata]
        tmp['size'] = 1
        tmp_grpd = tmp.groupby(strata).count().reset_index()
        tmp_grpd['samp_size'] = round(size / population * tmp_grpd['size']).astype(int)

        # controlling variable to create the dataframe or append to it
        first = True
        for i in range(len(tmp_grpd)):
            # query generator for each iteration
            qry = ''
            for s in range(len(strata)):
                stratum = strata[s]
                value = tmp_grpd.iloc[i][stratum]
                n = tmp_grpd.iloc[i]['samp_size']

                if type(value) == str:
                    value = "'" + str(value) + "'"

                if s != len(strata) - 1:
                    qry = qry + stratum + ' == ' + str(value) + ' & '
                else:
                    qry = qry + stratum + ' == ' + str(value)

            # final dataframe
            if first:
                stratified_df = df.query(qry).sample(n=n, random_state=seed).reset_index(drop=(not keep_index))
                first = False
            else:
                tmp_df = df.query(qry).sample(n=n, random_state=seed).reset_index(drop=(not keep_index))
                stratified_df = stratified_df.append(tmp_df, ignore_index=True)

        return stratified_df