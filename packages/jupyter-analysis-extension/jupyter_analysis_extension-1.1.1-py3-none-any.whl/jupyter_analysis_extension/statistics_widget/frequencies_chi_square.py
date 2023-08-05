import ipywidgets as widgets

# Graph
import plotly.graph_objs as go


class WidgetFrequenciesChiSquare:
    @staticmethod
    def get_statistic_result_table(first_col_values, df_count, statistic_result, statistic_tests_options):
        res_table_info = ''

        for key in statistic_result.keys():
            if key == 'Chi-square':
                res_table_info += """
                                    <tr>
                                        <td>{0}</td>
                                        <td>{1}</td>
                                        <td>{2}</td>
                                        <td>{3}</td>
                                    </tr>
                                    """.format(key, round(statistic_result[key][0], 1), statistic_result[key][2], round(statistic_result[key][1], 3))
            if key == "Fisher\'s exact":
                res_table_info += """
                                    <tr>
                                        <td>{0}</td>
                                        <td>{1}</td>
                                        <td>{2}</td>
                                        <td>{3}</td>
                                    </tr>
                                    """.format(key, "-", "-", round(statistic_result[key][0], 3))

        res_table_info += """
                    <tr>
                        <td>{0}</td>
                        <td>{1}</td>
                        <td>{2}</td>
                        <td>{3}</td>
                    </tr>
                    """.format("N", df_count, "", "")

        res_table = widgets.HTML(
            value="""
                <table>
                <tr>
                    <th></th>
                    <th>Value</th>
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
                go.Box(y=data, name=data.name))
        return fig

    @staticmethod
    def get_data_table(cross_tab):
        tab_column_length = len(cross_tab.to_numpy()[0]) + 1
        res_header_info = "<th></th>"
        for index, item in enumerate(cross_tab.columns):
            res_header_info += "<th>{0}</th>".format(item)

        res_table_info = ""
        for index, item in enumerate(cross_tab.index):
            res_row_info = "<td>{0}</td>".format(item)
            for count in range(tab_column_length-1):
                res_row_info += """
                            <td>{0}</td>
                            """.format(cross_tab.to_numpy()[index][count])
            res_table_info += """
                        <tr>
                            {0}
                        </tr>
                        """.format(res_row_info)

        res_table = widgets.HTML(
            value="""
                <table table-layout: fixed;">
                <tr>
                    {0}
                </tr>
                {1}
                </table>""".format(res_header_info,res_table_info),
            disabled=True
        )
        res_table.add_class('styledTable')
        return widgets.VBox([res_table])
