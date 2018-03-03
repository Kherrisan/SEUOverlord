from bs4 import BeautifulSoup as Soup


class Course(object):
    TYPE = {
        "sem": 44,
        "rwskl": 45,
        "jjygll": 46,
        "zl": 47
    }

    @staticmethod
    def parse_from_list(resp):
        return []

    @staticmethod
    def parse_from_page(resp):
        soup = Soup(resp)
        return []

    def __init__(self, cls, name, teacher, time, select_jxbbh, select_xkkclx, select_jhkcdm, selected=False):
        self.cls = cls
        self.name = name
        self.teacher = teacher
        self.time = time
        self.select_jxbbh = select_jxbbh
        self.select_xkkclx = select_xkkclx
        self.select_jhkcdm = select_jhkcdm
        self.selected = selected

    def __str__(self) -> str:
        return "{}[{}:{}:{}]({},{},{})".format(self.selected,
                                               self.name,
                                               self.teacher,
                                               self.time,
                                               self.select_jxbbh,
                                               self.select_xkkclx,
                                               self.select_jhkcdm)

    def update(self, another):
        self.select_jxbbh = another.select_jxbbh
        self.select_xkkclx = another.select_xkkclx
        self.select_jhkcdm = another.select_jhkcdm

    @property
    def select_url(self):
        url = "http://xk.urp.seu.edu.cn/jw_css/xk/runSelectclassSelectionAction.action?select_jxbbh={0}&select_xkkclx={1}&select_jhkcdm={2}".format(
            self.select_jxbbh,
            self.select_xkkclx,
            self.select_jhkcdm)
        return url
