# 导入pyqt5模块
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QLabel, QPushButton, QMessageBox
from PyQt5.QtGui import QPainter, QPen, QFont
from PyQt5.QtCore import Qt
import sys
import math
import cmath

# 定义一个三相电压类，用于存储和计算三相电压的相关参数
class ThreePhaseVoltage:
    def __init__(self, v1, a1, v2, a2, v3, a3):
        # 三相相电压的幅值和相位角，单位分别为V和度
        self.v1 = v1
        self.a1 = a1
        self.v2 = v2
        self.a2 = a2
        self.v3 = v3
        self.a3 = a3
        # 三相相电压的复数形式
        u1 = self.v1 * cmath.exp(1j * math.radians(self.a1))
        u2 = self.v2 * cmath.exp(1j * math.radians(self.a2))
        u3 = self.v3 * cmath.exp(1j * math.radians(self.a3))
        # 三相线电压的复数形式
        u12 = u1 - u2 # A相与B相之间的线电压
        u23 = u2 - u3 # B相与C相之间的线电压
        u31 = u3 - u1 # C相与A相之间的线电压
        # 三相线电压的幅值和相位角
        self.v12 = abs(u12) # A相与B相之间的线电压幅值
        self.v23 = abs(u23) # B相与C相之间的线电压幅值
        self.v31 = abs(u31) # C相与A相之间的线电压幅值
        self.a12 = math.degrees(cmath.phase(u12)) # A相与B相之间的线电压相位角
        self.a23 = math.degrees(cmath.phase(u23)) # B相与C相之间的线电压相位角
        self.a31 = math.degrees(cmath.phase(u31)) # C相与A相之间的线电压相位角
        # 正序、负序、零序电压的幅值和相位角，单位分别为V和度
        # 三相电压的正序分量
        u1p = (u1 + u2 * cmath.exp(1j * math.radians(120)) + u3 * cmath.exp(1j * math.radians(240))) / 3
        # 三相电压的负序分量
        u1n = (u1 + u2 * cmath.exp(1j * math.radians(240)) + u3 * cmath.exp(1j * math.radians(120))) / 3
        # 三相电压的零序分量
        u1z = (u1 + u2 + u3) / 3
        # 正序电压的幅值和相位角
        self.vp = abs(u1p) # 正序电压幅值
        self.ap = math.degrees(cmath.phase(u1p)) if self.vp > 0 else 0# 正序电压相位角
        # 负序电压的幅值和相位角
        self.vn = abs(u1n) # 负序电压幅值
        self.an = math.degrees(cmath.phase(u1n)) if self.vn > 0 else 0# 负序电压相位角
        # 零序电压的幅值和相位角
        self.vz = abs(u1z) # 零序电压幅值
        self.az = math.degrees(cmath.phase(u1z)) if self.vz > 0 else 0# 零序电压相位角

# 定义一个绘图类，用于在界面右侧绘制三相电压的矢量图
class PlotWidget(QWidget):
    def __init__(self,width=400, height=400, parent=None ):
        super().__init__(parent)
        # 设置窗口大小和标题
        self.setFixedSize(width, height) # 可以在初始化时传入窗口大小
        self.setWindowTitle('三相电压矢量图')
        self.setStyleSheet('color: gray')
        # 初始化三相电压对象
        self.voltage = ThreePhaseVoltage(0, 0, 0, 0, 0, 0)
        # 初始化最大电压幅值
        self.max_voltage = max(self.voltage.v1, self.voltage.v2, self.voltage.v3)
        # 初始化比例因子
        self.scale = min(width, height) / 400 # 根据窗口大小计算比例因子
        # 初始化字体
        self.font = QFont()
        self.font.setFamily('微软雅黑')
        self.font.setPointSize(9)
        self.font.setWeight(500)

    def paintEvent(self, event):
        # 创建一个绘图对象
        painter = QPainter(self)
        # 绘制一个白色底的圆形
        pen = QPen(Qt.black, 2)
        painter.setBrush(Qt.white) # 设置画刷颜色为白色
        painter.setPen(pen) # 设置画笔颜色为黑色
        radius = 170 # 设置圆形的半径
        painter.drawEllipse(int(self.width() / 2 - radius), int(self.height() / 2 - radius), int(2 * radius), int(2 * radius)) # 绘制圆形
        # 设置画笔颜色和宽度
        pen = QPen(Qt.black, 1)
        painter.setPen(pen)
        # 绘制坐标轴
        painter.drawLine(0, int(self.height() / 2), int(self.width()), int(self.height() / 2))
        painter.drawLine(int(self.width() / 2), 0, int(self.width() / 2), int(self.height()))
        # 设置字体大小和颜色
        painter.setFont(self.font)
        painter.setPen(Qt.gray)
        # 设置画笔颜色和宽度
        pen = QPen(Qt.red, 3)
        painter.setPen(pen)
        # 绘制三相相电压的矢量
        a = self.width() / 2 + self.voltage.v1 * math.cos(math.radians(self.voltage.a1)) * self.scale
        b = self.height() / 2 - self.voltage.v1 * math.sin(math.radians(self.voltage.a1)) * self.scale
        pen = QPen(Qt.yellow, 3)
        painter.setPen(pen)
        painter.drawLine(int(self.width() / 2), int(self.height() / 2), int(a), int(b))
        a = self.width() / 2 + self.voltage.v2 * math.cos(math.radians(self.voltage.a2)) * self.scale
        b = self.height() / 2 - self.voltage.v2 * math.sin(math.radians(self.voltage.a2)) * self.scale
        pen = QPen(Qt.green, 3)
        painter.setPen(pen)
        painter.drawLine(int(self.width() / 2), int(self.height() / 2), int(a), int(b))
        a = self.width() / 2 + self.voltage.v3 * math.cos(math.radians(self.voltage.a3)) * self.scale
        b = self.height() / 2 - self.voltage.v3 * math.sin(math.radians(self.voltage.a3)) * self.scale
        pen = QPen(Qt.red, 3)
        painter.setPen(pen)
        painter.drawLine(int(self.width() / 2), int(self.height() / 2), int(a), int(b))
        # 设置字体大小和颜色
        painter.setFont(self.font)
        painter.setPen(Qt.black)
        # 绘制三相相电压的标签
        painter.drawText(int(self.width() / 2 + self.voltage.v1 * math.cos(math.radians(self.voltage.a1)) * self.scale + 10), int(self.height() / 2 - self.voltage.v1 * math.sin(math.radians(self.voltage.a1)) * self.scale - 10), 'Va')
        painter.drawText(int(self.width() / 2 + self.voltage.v2 * math.cos(math.radians(self.voltage.a2)) * self.scale + 10), int(self.height() / 2 - self.voltage.v2 * math.sin(math.radians(self.voltage.a2)) * self.scale - 10), 'Vb')
        painter.drawText(int(self.width() / 2 + self.voltage.v3 * math.cos(math.radians(self.voltage.a3)) * self.scale + 10), int(self.height() / 2 - self.voltage.v3 * math.sin(math.radians(self.voltage.a3)) * self.scale - 10), 'Vc')
        # 绘制坐标轴刻度
        painter.setPen(Qt.blue)
        self.font.setBold(200)
        self.font.setPointSize(9)
        painter.setFont(self.font)

        marker_scaler = 1.0 # 刻度线比例
        num = 4 # 刻度线的数量
        step = int(self.max_voltage/4) # 刻度线的间隔
        for i in range(1, num + 1):
            # 计算刻度值
            value = i * step
            # 计算刻度位置
            x = self.width() / 2 + value * self.scale
            y = self.height() / 2 - value * self.scale
            # 绘制刻度线
            painter.drawLine(int(x), int(self.height() / 2 - 5 * marker_scaler), int(x), int(self.height() / 2 + 5 * marker_scaler))
            painter.drawLine(int(self.width() / 2 - 5 * marker_scaler), int(y), int(self.width() / 2 + 5 * marker_scaler), int(y))
            # 绘制刻度标签
            painter.drawText(int(x + 5 * marker_scaler), int(self.height() / 2 + 15 * marker_scaler), str(value))
            painter.drawText(int(self.width() / 2 - 25 * marker_scaler), int(y - 5 * marker_scaler), str(value))
    
    def update_voltage(self, voltage):
        # 更新三相电压对象
        self.voltage = voltage
        # 更新最大电压幅值
        self.max_voltage = max(self.voltage.v1, self.voltage.v2, self.voltage.v3)
        #重新规定比例因子
        self.scale = min(self.width(), self.height()) / 400 / self.max_voltage * 150
        # 重新绘制界面
        self.update()


# 定义一个主窗口类，用于在界面左侧显示输入框和计算按钮
class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 设置窗口大小和标题
        self.resize(600, 400)
        self.setWindowTitle('三相电压计算器')
        # 创建一个网格布局
        layout = QGridLayout()
        # 创建六个输入框，用于输入三相相电压的幅值和相位角
        self.v1_edit = QLineEdit()
        self.a1_edit = QLineEdit()
        self.v2_edit = QLineEdit()
        self.a2_edit = QLineEdit()
        self.v3_edit = QLineEdit()
        self.a3_edit = QLineEdit()
        # 设置输入框默认值
        self.v1_edit.setText('120')
        self.a1_edit.setText('0')
        self.v2_edit.setText('120')
        self.a2_edit.setText('-120')
        self.v3_edit.setText('120')
        self.a3_edit.setText('120')
        # 创建六个标签，用于显示输入框的单位和名称
        self.v1_label = QLabel('Ua (V)')
        self.a1_label = QLabel('θa (°)')
        self.v2_label = QLabel('Ub (V)')
        self.a2_label = QLabel('θb (°)')
        self.v3_label = QLabel('Uc (V)')
        self.a3_label = QLabel('θc (°)')

        # 将输入框和标签添加到网格布局中
        layout.addWidget(self.v1_label, 0, 0)
        layout.addWidget(self.v1_edit, 0, 1)
        layout.addWidget(self.a1_label, 0, 2)
        layout.addWidget(self.a1_edit, 0, 3)
        layout.addWidget(self.v2_label, 1, 0)
        layout.addWidget(self.v2_edit, 1, 1)
        layout.addWidget(self.a2_label, 1, 2)
        layout.addWidget(self.a2_edit, 1, 3)
        layout.addWidget(self.v3_label, 2, 0)
        layout.addWidget(self.v3_edit, 2, 1)
        layout.addWidget(self.a3_label, 2, 2)
        layout.addWidget(self.a3_edit, 2, 3)
        # 创建一个计算按钮，用于触发计算事件
        self.calc_button = QPushButton('计 算')
        self.calc_button.setFixedHeight(120)
        font = QFont()
        font.setFamily('微软雅黑')
        font.setPointSize(40)
        font.setWeight(500)
        self.calc_button.setFont(font)
        
        # 将计算按钮添加到网格布局中
        layout.addWidget(self.calc_button, 3, 0, 1, 4)
        # 创建十二个计算结果标签
        self.v12_label = QLabel('Uab (V)')
        self.a12_label = QLabel('θab (°)')
        self.v23_label = QLabel('Ubc (V)')
        self.a23_label = QLabel('θbc (°)')
        self.v31_label = QLabel('Uca (V)')
        self.a31_label = QLabel('θca (°)')
        self.vp_label = QLabel('U1 (V)')
        self.ap_label = QLabel('θ1 (°)')
        self.vn_label = QLabel('U2 (V)')
        self.an_label = QLabel('θ2 (°)')
        self.vz_label = QLabel('U0 (V)')
        self.az_label = QLabel('θ0 (°)')
        # 创建十二个计算结果值标签
        self.v12_result = QLineEdit()
        self.a12_result = QLineEdit()
        self.v23_result = QLineEdit()
        self.a23_result = QLineEdit()
        self.v31_result = QLineEdit()
        self.a31_result = QLineEdit()
        self.vp_result = QLineEdit()
        self.ap_result = QLineEdit()
        self.vn_result = QLineEdit()
        self.an_result = QLineEdit()
        self.vz_result = QLineEdit()
        self.az_result = QLineEdit()
        layout.addWidget(self.v12_label, 4, 0)
        layout.addWidget(self.v12_result, 4, 1)
        layout.addWidget(self.a12_label, 4, 2)
        layout.addWidget(self.a12_result, 4, 3)
        layout.addWidget(self.v23_label, 5, 0)
        layout.addWidget(self.v23_result, 5, 1)
        layout.addWidget(self.a23_label, 5, 2)
        layout.addWidget(self.a23_result, 5, 3)
        layout.addWidget(self.v31_label, 6, 0)
        layout.addWidget(self.v31_result, 6, 1)
        layout.addWidget(self.a31_label, 6, 2)
        layout.addWidget(self.a31_result, 6, 3)
        layout.addWidget(self.vp_label, 7, 0)
        layout.addWidget(self.vp_result, 7, 1)
        layout.addWidget(self.ap_label, 7, 2)
        layout.addWidget(self.ap_result, 7, 3)
        layout.addWidget(self.vn_label, 8, 0)
        layout.addWidget(self.vn_result, 8, 1)
        layout.addWidget(self.an_label, 8, 2)
        layout.addWidget(self.an_result, 8, 3)
        layout.addWidget(self.vz_label, 9, 0)
        layout.addWidget(self.vz_result, 9, 1)
        layout.addWidget(self.az_label, 9, 2)
        layout.addWidget(self.az_result, 9, 3)
        # 设置标签的对齐方式和字体颜色
        for label in [self.v12_label, self.a12_label, self.v23_label, self.a23_label, self.v31_label, self.a31_label, self.vp_label, self.ap_label, self.vn_label, self.an_label, self.vz_label, self.az_label]:
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet('color: blue')

        # 创建一个署名标签，用于显示软件作者
        self.author_label = QLabel('Version:1.0.0.2  Author:Astro Teng')
        # 将署名标签添加到网格布局中
        layout.addWidget(self.author_label, 10, 0, 1, 4)
        # 设置署名标签的对齐方式和字体颜色
        self.author_label.setAlignment(Qt.AlignLeft)
        self.author_label.setStyleSheet('color: gray')

        #创建一个标签用于绘图
        self.paintArea = PlotWidget(350,350)
        layout.addWidget(self.paintArea, 0, 5, 11, 1)


        # 设置窗口的布局
        self.setLayout(layout)
        # 连接计算按钮的点击信号和计算槽函数
        self.calc_button.clicked.connect(self.calculate)
        # 立即计算一次
        self.calculate()

    def calculate(self):
        # 获取输入框中的值
        try:
            v1 = float(self.v1_edit.text())
            a1 = float(self.a1_edit.text())
            v2 = float(self.v2_edit.text())
            a2 = float(self.a2_edit.text())
            v3 = float(self.v3_edit.text())
            a3 = float(self.a3_edit.text())
        except ValueError as e:
            box = QMessageBox()
            box.setText('存在非法输入!')
            box.setWindowTitle('错误提示')
            box.show()
            box.exec_()
            return
        
        # 创建一个三相电压对象
        voltage = ThreePhaseVoltage(v1, a1, v2, a2, v3, a3)
        # 更新计算结果的标签
        self.v12_result.setText(f'{voltage.v12:.2f}')
        self.a12_result.setText(f'{voltage.a12:.2f}')
        self.v23_result.setText(f'{voltage.v23:.2f}')
        self.a23_result.setText(f'{voltage.a23:.2f}')
        self.v31_result.setText(f'{voltage.v31:.2f}')
        self.a31_result.setText(f'{voltage.a31:.2f}')
        self.vp_result.setText(f'{voltage.vp:.2f}')
        self.ap_result.setText(f'{voltage.ap:.2f}')
        self.vn_result.setText(f'{voltage.vn:.2f}')
        self.an_result.setText(f'{voltage.an:.2f}')
        self.vz_result.setText(f'{voltage.vz:.2f}')
        self.az_result.setText(f'{voltage.az:.2f}')
        # 更新绘图窗口的三相电压对象
        self.paintArea.update_voltage(voltage)

# 创建一个应用对象
app = QApplication(sys.argv)
# 创建一个主窗口对象
main_window = MainWindow()
# 显示主窗口和绘图窗口
main_window.show()
# 进入应用的主循环
sys.exit(app.exec_())
