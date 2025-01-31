from windows.Dashboard import Ui_MainWindow
from PyQt5.QtWidgets import *   
from analysis.database_analyze import *
from PyQt5.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PyQt5.QtChart import *
from PyQt5.QtGui import QPainter,  QBrush, QColor,QPen
class MainWindow(QMainWindow):
    try:
        def __init__(self,filename1,filename2):
            super().__init__()
            self.ui = Ui_MainWindow()
            self.setWindowTitle("Data Analysis of Alphabet ")
            self.ui.setupUi(self)
            self.ui.actionQuit.triggered.connect(self.close)
            self.ui.actionnew.triggered.connect(lambda: self.new_())
            self.chart_view = None
            self.nov,self.aug,self.high,self.low,self.equal,self.new = Overall()
            self.overtbl = Overall_tbl()
            self.high_data = high_data()
            self.low_data = low_data()
            self.equal_data = equal_data()
            self.new_data = new_data()  
            # print(len(self.overtbl))
            self.ui.label_5.setText(filename1)
            self.ui.label.setText(filename2)
            self.company_name = filename1.split('_')[0]
            self.ui.label_2.setText(f"{self.company_name}")
            self.display_overalldata(self.aug,self.nov)
            self.ui.comboBox.setCurrentIndex(0)
            self.on_combobox_changed()

            self.ui.comboBox.currentIndexChanged.connect(lambda: self.on_combobox_changed())

        def new_(self):
            import main
            window = main.FileDialogExample()
            window.show()
        def display_overalldata(self,aug, nov):
            self.ui.buy_label.setText(QCoreApplication.translate("MainWindow", f"{aug}", None))
            self.ui.sale_label.setText(QCoreApplication.translate("MainWindow", f"{nov}", None))
    

    #---------------
        def search_(self):
            self.name_Of_Issuer=self.ui.inputtext.text()
            # print(self.name_Of_Issuer)


        def pieChart_(self):
            self.highpr =percentage(self.high[0])
            self.lowpr =percentage(self.low[0])
            self.equalpr= percentage(self.equal[0])
            self.newpr =  percentage(self.new[0])
            # print(self.high)
            if self.high == 0:
                self.high = 1

            #-----------CHANGING LABELS--------------
            self.ui.high_lbl.setText(f"+ {str(self.high[0])}")
            self.ui.low_lbl.setText(f"- {str(self.low[0])}")
            self.ui.equal_lbl.setText(f"= {str(self.equal[0])}")
            self.ui.new_lbl.setText(f"{str(self.new[0])}")


            self.ui.frame_18.setStyleSheet('background-color: transparent')
            self.series = QPieSeries()
            self.series.append(f"{self.highpr}%",self.highpr )
            self.series.append(f"{self.lowpr}%", self.lowpr)
            self.series.append(f"{self.equalpr}%", self.equalpr) 
            self.series.append(f"{self.newpr}%", self.newpr)
            self.series.setLabelsVisible(False)
            
            self.colors = [QColor(0, 255, 0, 200),  # GREEN
                    QColor(255, 0, 0, 200),    # Red
                    QColor(255, 255, 0, 200),  # Yellow
                    QColor(0, 0, 255, 200)]  
            # Customize slices
            for i, slice_ in enumerate(self.series.slices()):
                slice_.setLabelVisible(False)  # Display labels
                slice_.setBrush(QColor(self.colors[i]))
                slice_.setLabelBrush(QColor(Qt.white))
                slice_.setPen(QPen(Qt.NoPen))  # No border for slices
            # Create a chart
            self.chart = QChart()
            self.chart.addSeries(self.series)
            # self.chart.setTitle("Donut Chart Example")    
            self.chart.setAnimationOptions(QChart.SeriesAnimations)

            # Adjust the pie hole size (to make it a donut chart)
            self.series.setHoleSize(0.5)

            # Make the chart background transparent
            self.chart.setBackgroundBrush(Qt.transparent)  # Solid blue background
            self.chart.setBackgroundPen(QPen(Qt.NoPen)) 
            self.legend = self.chart.legend()
            self.legend.setVisible(True)
            self.legend.setAlignment(Qt.AlignLeft)  # Align the legend to the left
            self.legend.setLabelColor(Qt.white)  # Set legend text color to white
            # self.chart.legend().setVisible(False)
            # Create a ChartView

            #global chart_view
            self.chart_view = QChartView(self.chart)
            self.chart_view.setRenderHint(QPainter.Antialiasing)   
            self.ui.verticalLayout_14.addWidget(self.chart_view) 
            self.chart_view.setMinimumSize(400, 400)
        
        def barChart(self,data):
            if len(data[0]) == 2:
                self.bar_set = QBarSet("Values")
                self.bar_set.append(self.new)  # Example data

            # Create a QBarSeries and add the QBarSet
                self.bar_series = QBarSeries()
                self.bar_series.append(self.bar_set)

            # Create a QChart and add the QBarSeries
                self.chart = QChart()
                self.chart.addSeries(self.bar_series)
                # self.chart.setTitle("Simple Bar Chart")
                self.chart.setAnimationOptions(QChart.SeriesAnimations)

            # Customize axes
                self.categories = [self.new_data[0][0]]  # Example categories
                self.axisX = QBarCategoryAxis()
                self.axisX.append(self.categories)
                self.chart.addAxis(self.axisX, Qt.AlignBottom)
                self.bar_series.attachAxis(self.axisX)

                self.axisY = QValueAxis()
                self.chart.addAxis(self.axisY, Qt.AlignLeft)
                self.bar_series.attachAxis(self.axisY)

                self.chart_view = QChartView(self.chart)
                self.ui.verticalLayout_14.addWidget(self.chart_view)
                self.chart_view.setRenderHint(QPainter.Antialiasing)
                return
            if len(data) == 0:
                self.chart = QChart()
                self.chart.setTitle("No values found!")
                self.chart_view = QChartView(self.chart)
                self.ui.verticalLayout_14.addWidget(self.chart_view)
                self.chart_view.setRenderHint(QPainter.Antialiasing)
                return
            self.nov_set = QBarSet("November")
            self.aug_set = QBarSet("August")

            self.series = QBarSeries()
            for name, nov_value, aug_value, differences in data:
                # Add the values to the bar sets
                self.nov_set << nov_value
                self.aug_set << aug_value
            self.series.append(self.nov_set)
            self.series.append(self.aug_set)

            # Create the chart
            self.chart = QChart()
            self.chart.addSeries(self.series)
            self.chart.setTitle("Amount Comparison: November vs August")
            self.chart.setAnimationOptions(QChart.SeriesAnimations)

            # Create and configure the X-axis (categories)
            self.categories = [name for name, _, _, _ in data]  # Extract the names for the X-axis
            self.axisX = QBarCategoryAxis()
            self.axisX.append(self.categories)
            self.chart.addAxis(self.axisX, Qt.AlignBottom)
            self.series.attachAxis(self.axisX)

            # Create and configure the Y-axis (numeric values)
            self.axisY = QValueAxis()
            # self.axisY.setRange(100000, 20000000)  # Adjust Y-axis range based on your data
            self.chart.addAxis(self.axisY, Qt.AlignLeft)
            self.series.attachAxis(self.axisY)

            # Display the chart in a QChartView
            self.chart_view = QChartView(self.chart)
            self.ui.verticalLayout_14.addWidget(self.chart_view)
            self.chart_view.setRenderHint(QPainter.Antialiasing)
        def hide(self):
            if self.chart_view:
                self.chart_view.hide()

        def disp_tbl(self,data):
            column_names = ["Name of Issuer", "Recent Shares", "Previous Shares","Differences"]
            # data = [('1', 'John Doe', 30), ('2', 'Jane Doe', 28), ('3', 'Mike Doe', 35)]

        
            self.ui.tableWidget.setRowCount(len(data))
            self.ui.tableWidget.setColumnCount(len(column_names))
            for column_index, column_name in enumerate(column_names):
                self.ui.tableWidget.setHorizontalHeaderItem(column_index, QTableWidgetItem(column_name))
            for row_index, row_data in enumerate(data):
                for column_index, cell_data in enumerate(row_data):
                    self.ui.tableWidget.setItem(row_index, column_index, QTableWidgetItem(str(cell_data)))
            self.ui.tableWidget.resizeColumnsToContents()
        
        def hide_tbl(self):
            self.ui.tableWidget.setRowCount(0)


        def on_combobox_changed(self):
            index = self.ui.comboBox.currentIndex()
            if index == 0:
                self.hide()
                self.hide_tbl()     # "Overall of nov_aug"
                self.pieChart_()
                self.display_overalldata(self.aug,self.nov)
                self.disp_tbl(self.overtbl)
            elif index == 1:  # Shares Gained
                self.hide()
                self.hide_tbl()
                self.data1 = sumof(self.high_data)
                self.display_overalldata(self.data1[1],self.data1[0])
                self.barChart(self.high_data)
                self.disp_tbl(self.high_data)
            elif index == 2:
                self.hide()  # Shares Reduced
                self.hide_tbl()
                self.data2 = sumof(self.low_data)
                self.display_overalldata(self.data2[1],self.data2[0])
                self.barChart(self.low_data)
                self.disp_tbl(self.low_data)
            elif index == 3:  # Unchanged share
                self.hide()  # Shares Reduced
                self.hide_tbl()
                self.data3 = sumof(self.equal_data)
                self.display_overalldata(self.data3[1],self.data3[0])
                self.barChart(self.equal_data)
                self.disp_tbl(self.equal_data)
            elif index == 4:  # New added
                self.hide()  # Shares Reduced
                self.hide_tbl()
                self.data4 = sumof(self.new_data)
                self.display_overalldata(0,self.data4)
                self.barChart(self.new_data)
                self.disp_tbl(self.new_data)
    except Exception as e:
        # print(f"An error occurred: {e}")
        pass

if __name__ == '__main__':  
    app = QApplication([])
    window = MainWindow('hh','uu')
    window.show()
    app.exec_()
