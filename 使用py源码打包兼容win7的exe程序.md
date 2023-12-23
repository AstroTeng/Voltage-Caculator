1.打开cmd（或类似的命令行工具）

2.确保已经安装了3.8及以下版本的python（以便能够兼容win7，且要注意如果你希望程序运行在32位的win7版本上，要确保安装的python也是32位的）

3.使用以下命令创建虚拟环境
```shell
python -m venv [虚拟环境名称] 
```
然后在所创建的虚拟环境的目录下找到文件pyvenv.cfg，修改该文件中的路径以重新指向你所希望版本的python程序
```
home = [指定版本的python文件夹路径]

include-system-site-packages = false

version = 3.8

executable = [指定版本的python程序路径]

command = [指定版本的python程序路径] -m venv [虚拟环境目录]
```

4.使用以下命令进入虚拟环境
```shell
[虚拟环境名称]\Scripts\activate
```

5.进入虚拟环境后使用pip命令安装所需要的包以及pyinstaller，此处略过不表

6.随后在虚拟环境中使用如下命令打包成exe程序
```shell
pyinstaller -F -w [py源码文件路径] --distpath [指定的exe输出路径] -n [输出的exe程序名称] -i [exe程序图标路径]
```

附:使用清华源加速pip install
```
-i https://pypi.tuna.tsinghua.edu.cn/simple
```

