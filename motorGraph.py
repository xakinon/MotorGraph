# -*- coding: utf-8 -*-
import configparser
import csv
import numpy as np
import sys
from PyQt5 import QtWidgets, QtCore
import pyqtgraph.opengl as gl
import pyqtgraph as pg

from mainwindow import Ui_MainWindow
from model import Model, Delegate, DictTableView

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        # UI設定
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # iniファイル読み込み
        self.iniflename = 'settings.ini'
        self.inifile = configparser.ConfigParser()
        self.inifile.read(self.iniflename, encoding='utf8')

        # iniファイルから条件テーブルの設定取得
        self.model = Model()
        self.ui.tableView.setModel( self.model )
        self.ui.tableView.setItemDelegate( Delegate() )
        self.ui.tableView.setColumnWidth(0, 80)
        self.ui.tableView.setColumnWidth(1, 10)
        columns = self.inifile.get('conditions','columns').splitlines()
        items = []
        for i in range(1000):
            try:
                vals = self.inifile.get( 'conditions', 'items_{:0=3}'.format(i) ).splitlines()
                item = { column:val for column, val in zip(columns, vals) }
                items.append(item)
            except:
                break
        self.model.addColumns( columns )
        self.model.addItems( items )
        
        # 座標テーブルの設定
        self.coordinates = Model()
        self.ui.tableView_2.setModel( self.coordinates )
        self.ui.tableView_2.setItemDelegate( Delegate() )
        self.coordinates.addColumns( ['X', 'Y', 'Z', 'T', 'R'] )
        for i in range(5):
            self.ui.tableView_2.setColumnWidth(i, 60)

        # グラフ設定
        self.ui.plotWidget.setBackground("#FFFFFF00")
        self.ui.plotWidget.getViewBox().setAspectLocked(lock=True, ratio=1)
        self.ui.plotWidget_2.setBackground("#FFFFFF00")
        self.ui.plotWidget_2.getViewBox().setAspectLocked(lock=True, ratio=1)

        # イベント
        self.model.dataChanged.connect(self.modelDataChanged)

    def modelDataChanged(self, index):

        v = float( self.model.itemdata('項目', '最高速度', '値') )
        a = float( self.model.itemdata('項目', '最高加速度', '値') )
        #t = float( self.model.itemdata('項目', '移動時間', '値') )
        s = float( self.model.itemdata('項目', '移動距離', '値') )
        t4 = float( self.model.itemdata('項目', '停止時間', '値') )

        t1 = v / a # 加速時間
        s1 = 0.5 * v * v / a # 加速距離
        t2 = t - t1 - t4 # 等速時間
        s2 = s - s1 - s1
        t3 = t - t4

        changedDataType = self.model.items[index.row()]['項目']
        if changedDataType == '最高速度':
            # 移動時間を計算
            pass

        if changedDataType == '最高加速度':
            # 移動時間を計算
            pass
            
        if changedDataType == '移動時間':
            # 移動距離を計算
            pass
            
        if changedDataType == '移動距離':
            # 移動時間を計算
            pass
            
        T = [0, t1, t2, t3, t]
        V = [0, v, v, 0, 0]
        self.ui.plotWidget.clear()
        self.ui.plotWidget.plot(T, V) 

    def keyPressEvent(self, e):

        if (e.modifiers() & QtCore.Qt.ControlModifier):
            # Ctrlキーが押されたら
            
            if e.key() == QtCore.Qt.Key_C:
                if self.ui.tableView.hasFocus():
                    self.ui.tableView.CtrlC()

            if e.key() == QtCore.Qt.Key_V:
                if self.ui.tableView.hasFocus():
                    self.ui.tableView.CtrlV()
                
            if e.key() == QtCore.Qt.Key_U:
                if self.ui.tableView.hasFocus():
                    self.ui.tableView.toText()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()