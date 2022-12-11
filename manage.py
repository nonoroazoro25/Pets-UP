from core.admin import g_app
from flask_apidoc.commands import GenerateApiDoc
from flask_script import Manager

manager = Manager(g_app)
manager.add_command('apidoc', GenerateApiDoc())

if __name__ == "__main__":
    """
    restful接口风格利用apidoc生成api文档
    """
    manager.run()
