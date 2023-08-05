from setuptools import setup, find_packages
__author__ = '神秘的·'
__date__ = '2020/7/15'
import codecs,os
def read(fname):
    '''
    定义read()，用来读取目录下的长描述
    我们一般将README文件中的内容读取出来叫做长描述，这个会在pypi中你的包的页面展现出来
    你也可以不用此办法，直接手动写内容
    pypi上支持.rst格式的文件，暂时不支持md格式；rst格式的文件在pypi上会自动转化为html形式显示在你的包的信息页面上
    '''
    return codecs.open(os.path.join(os.path.dirname(__file__),fname)).read()

setup(
    name='3y', # 名称
    py_modules=['main','beginnings','y','yh','yz','log','__init__'],
    version='2.5.4',
    description='三圆计算器,cmd或命令行 python -m main 命令开始运行', # 简单描述
#    long_description='MADE IN CHINE,THE PROJUCT MAKER IS CHINESE\npython方便你我他现在免费推出3圆(圆环圆圆柱)计算器，欢迎下载使用\n使用方法:运用cd命令或其他方式运行main.py\n请自觉观看README.md文件', 
    long_description=read('README.rst'),
    classifiers=[
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
],
    keywords='3y', # 关键字
    author='神秘的·', # 作者
    author_email='3046479366@qq.com', # 邮箱
    url='', # 包含包的项目地址
    license='MIT', # 授权方式
    packages=find_packages(), # 包列表
    install_requires=['pdsystem','beginnings'],
    include_package_data=True,
    zip_safe=True,
)