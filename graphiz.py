from graphviz import Digraph
import numpy as np
import xlrd
import openpyxl
import pandas as pd


def build_dot():
    dot = Digraph()
    dot.attr(label='服务调用热点监控 Service HotSpot Monitor', labelloc="t")
    sheet = pd.read_excel("data/services.xlsx", sheet_name='services')
    print(sheet)
    for index, row in sheet.iterrows():
        print(row)
        from_node = str(row['from'])
        dot.node(from_node, from_node, shape='circle', color='blue')
        to_node = str(row['to'])
        dot.node(to_node, to_node, shape='circle', color='blue')
        count = str(row['count'])
        color = 'blue'
        if int(count) > 1000:
            color = 'red'
        dot.edge(from_node, to_node, label=count, constraint='true', color=color)

    dot.render('output/services.gv', view=True)


if __name__ == '__main__':
    build_dot()
