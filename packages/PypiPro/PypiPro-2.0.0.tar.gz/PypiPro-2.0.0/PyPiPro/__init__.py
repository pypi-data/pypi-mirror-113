'''
说明：PYpiTools工具是一个提供开发者上传自己包到pypi上的简易小工具大家可以根据自己需求下载使用
里面提供了丰富的工具方法包括setup文件创建README.MD文件的创建，账号输入等一系列工具方法
'''
import os
class PyPiTools:
    '''
    创建setup.py文件
    '''
    def __init__(self):
        if os.path.exists('setup.py'):
            pass
        else:
            open('setup.py','w').close()
        if os.path.exists('README.md'):
            pass
        else:
            open('README.md', 'w').close()

    @staticmethod
    def buildSetupFile():
        if os.path.exists('setup.py'):
            pass
        else:
            open('setup.py','w').close()




    '''创建README.md文件'''
    @staticmethod
    def buildReadMeFile():
        if os.path.exists('README.md'):
            pass
        else:
            open('README.md', 'w').close()


    '''创建'''
    @staticmethod
    def buildReadMeFile():
        if os.path.exists('README.md'):
            pass
        else:
            open('README.md', 'w').close()

    '''上传到pypi'''
    @staticmethod
    def uploadPackage():
        #os.system('pip install twine')
        os.system('twine upload dist/*')
    '''打包'''
    @staticmethod
    def buildpackage():
        os.system('python setup.py sdist')



    '''文档说明'''
    @staticmethod
    def showdoc():
        '''函数方法说明'''
        doc='''
        此工具用于构建自己的包上传到pypi，步骤是先创建属于自己的包项目结构如下:
        projectname
             |-----packgename
             |         |---------packagename1
             |         |---------packagename2
             |         |                 |......xxxxxx.py
             |         |                 |.......xxxxxxxxx.py
             |         |---------.......xxx
             |         |---------........xxx
             
         
        然后在该packgename包文件同级目录下创建一个python文件名字自取在这一般我取为main.py在此文件写代码先调用
        PyPiPro()生成setup.py和README.md文件生成后目录如下所示:
        
        projectname
             |-----packgename
             |         |---------packagename1
             |         |---------packagename2
             |         |                 |......xxxxxx.py
             |         |                 |.......xxxxxxxxx.py
             |         |---------.......xxx
             |         |---------........xxx
             |---------setup.py
             |---------README.md
             |---------main.py
        此两文件必须位于包名同级目录,然后对setup文件里面设置进行配置
        ```
            from setuptools import setup
            import setuptools
            setup(
                  name='databasis',#项目名称 用户下载pip install xxx就是这个名可以任意起名字遵循变量命名规则即可并且保证pypi上没有重名冲突
                  version='1.0.0',版本号 版本号规范：https://www.python.org/dev/peps/pep-0440/
                  packages=setuptools.find_packages(),  如果项目由多个文件组成，我们可以使用find_packages()自动发现所有包和子包，而不是手动列出每个包
                  author="robin",作者名字
                  url='xxxxxxxx'项目开源地址，我这里写的是同性交友官网，大家可以写自己真实的开源网址
                  author_email="xiaoyaojianxians@163.com",邮箱
                  install_requires=['xxx','xxxxx'],  # 依赖的包
                  python_requires='>=3'#python版本大于3
                  )
        ```
        以上这些就是必须字段，大家如果感兴趣可以自行根据pipi规范设置更多以上不加赘述,完成以上步骤调用PyPiPro.buildpackage打包此语句等效于python setup.py sdist
        然后再在setup.py目录下打开dos界面输入twine upload dist/* 按要求输入pypi用户名命名密码
        Uploading distributions to https://upload.pypi.org/legacy/
        Enter your username: xiaoyaojianxianss
        1983273232jmz
        输入后即可上传如果出现403错误请检查是否版本或者包和pypi上面有人重名了修改一下删除打包文件重新生层一次再上传即可
        '''


PyPiTools.buildReadMeFile()