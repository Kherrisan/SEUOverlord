import requests
from PIL import Image
import io
import aiohttp
from bs4 import BeautifulSoup as Soup
from Course import Course
import logging
import re
import asyncio
import json

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

HEADERS = [{'Host': 'xk.urp.seu.edu.cn',
            'Proxy-Connection': 'keep-alive',
            'Origin': 'http://xk.urp.seu.edu.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1'},
           {
               'Host': 'xk.urp.seu.edu.cn',
               'Origin': 'http://xk.urp.seu.edu.cn',
               'Connection': 'keep-alive',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'},
           {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'xk.urp.seu.edu.cn',
            'Origin': 'http://xk.urp.seu.edu.cn',
            'User-Agent': 'Mozilla/6.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0'},
           {'Host': 'xk.urp.seu.edu.cn',
            'Connection': 'keep-alive',
            'Accept': 'text/html, */*; q=0.01',
            'User-Agent': 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36',
            'Origin': 'http://xk.urp.seu.edu.cn'}]

STANDARD = [
    [18.714286, 27.142857, 32.857143, 36.714286, 38.285714, 41.571429, 43.000000, 44.714286, 46.285714, 48.285714,
     48.285714, 36.428571, 27.714286, 24.714286, 23.285714, 22.285714, 21.428571, 19.428571, 19.285714, 19.000000,
     18.857143, 18.714286, 19.714286, 20.571429, 20.714286, 22.714286, 26.571429, 28.000000, 35.571429, 46.714286,
     46.714286, 44.857143, 43.000000, 41.285714, 39.571429, 36.142857, 34.428571, 31.000000, 26.000000, 18.714286],
    [0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000,
     0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000,
     0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000,
     0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000],
    [8.333333, 8.333333, 16.166667, 23.166667, 24.166667, 26.000000, 27.000000, 27.833333, 27.500000, 29.000000,
     29.500000, 30.333333, 30.000000, 30.000000, 28.666667, 27.666667, 27.333333, 27.833333, 28.000000, 28.333333,
     29.833333, 31.333333, 33.333333, 35.166667, 38.000000, 43.000000, 41.833333, 40.833333, 39.666667, 37.666667,
     36.833333, 34.500000, 32.333333, 29.500000, 26.500000, 21.500000, 7.333333, 7.166667, 7.166667, 7.333333],
    [8.200000, 8.400000, 8.400000, 8.200000, 13.200000, 18.800000, 19.000000, 19.400000, 19.000000, 26.000000,
     26.200000, 26.400000, 25.400000, 26.200000, 26.000000, 26.400000, 27.400000, 27.200000, 28.400000, 29.200000,
     31.200000, 33.200000, 36.400000, 41.400000, 46.800000, 48.800000, 52.600000, 51.200000, 49.200000, 48.200000,
     45.200000, 40.600000, 37.600000, 33.600000, 25.800000, 18.000000, 13.800000, 7.000000, 7.000000, 7.200000],
    [17.250000, 19.000000, 20.500000, 21.875000, 24.125000, 25.375000, 26.375000, 28.250000, 28.500000, 28.125000,
     28.000000, 27.750000, 25.875000, 25.250000, 25.125000, 26.250000, 25.000000, 24.625000, 25.625000, 24.750000,
     24.500000, 24.500000, 25.375000, 24.500000, 52.000000, 52.250000, 52.750000, 52.875000, 53.750000, 55.375000,
     55.125000, 55.000000, 54.625000, 18.625000, 18.375000, 18.375000, 18.250000, 17.750000, 17.375000, 9.875000],
    [8.428571, 8.285714, 8.142857, 8.285714, 8.428571, 8.285714, 14.000000, 36.285714, 36.142857, 35.857143, 36.000000,
     36.000000, 36.142857, 31.714286, 27.000000, 26.857143, 27.714286, 27.571429, 27.714286, 28.714286, 27.857143,
     29.142857, 29.714286, 31.000000, 34.142857, 41.000000, 40.142857, 39.285714, 38.000000, 37.857143, 36.428571,
     35.000000, 33.571429, 32.000000, 28.428571, 15.714286, 8.285714, 8.285714, 8.285714, 8.142857],
    [8.142857, 20.571429, 27.857143, 32.285714, 35.857143, 38.428571, 40.857143, 44.000000, 46.000000, 46.857143,
     47.571429, 49.142857, 37.000000, 32.857143, 29.857143, 27.428571, 25.714286, 26.285714, 25.571429, 24.714286,
     25.428571, 24.285714, 24.714286, 24.285714, 26.142857, 27.428571, 28.571429, 31.142857, 34.285714, 41.142857,
     40.857143, 39.142857, 37.571429, 36.571429, 34.571429, 32.857143, 24.000000, 21.714286, 16.428571, 8.000000],
    [8.428571, 8.285714, 8.142857, 8.285714, 8.285714, 8.285714, 16.285714, 16.285714, 19.000000, 21.857143, 24.000000,
     25.285714, 25.857143, 27.714286, 29.857143, 31.000000, 32.857143, 34.571429, 35.285714, 32.714286, 30.142857,
     29.571429, 29.142857, 28.142857, 27.285714, 27.000000, 26.000000, 26.857143, 26.428571, 26.285714, 26.428571,
     26.714286, 25.142857, 24.571429, 23.571429, 21.571429, 20.857143, 18.714286, 17.571429, 17.000000],
    [7.500000, 7.500000, 13.833333, 18.833333, 21.333333, 29.666667, 36.500000, 40.333333, 43.333333, 47.166667,
     49.833333, 52.833333, 48.666667, 45.833333, 37.500000, 33.500000, 30.833333, 30.000000, 28.000000, 27.500000,
     28.666667, 27.666667, 28.500000, 29.166667, 32.833333, 33.833333, 36.000000, 40.333333, 47.666667, 52.166667,
     49.166667, 47.166667, 44.166667, 40.666667, 37.166667, 32.500000, 27.000000, 18.833333, 14.833333, 8.000000],
    [8.142857, 15.857143, 20.285714, 24.142857, 30.428571, 32.571429, 34.142857, 36.285714, 38.142857, 38.000000,
     39.571429, 32.428571, 29.571429, 27.571429, 26.571429, 25.714286, 25.714286, 23.714286, 23.857143, 23.428571,
     24.428571, 23.142857, 23.000000, 26.285714, 26.285714, 26.428571, 30.000000, 33.857143, 39.000000, 50.142857,
     49.285714, 47.857143, 47.428571, 45.571429, 44.285714, 41.142857, 38.714286, 34.142857, 29.428571, 20.714286]
]


class UserSession(object):
    @staticmethod
    async def test(username, password):
        pass

    @staticmethod
    async def login(username, password):
        session = UserSession()
        err = None
        captcha = await session.__recognize_captcha()
        resp = await session.session.post("http://xk.urp.seu.edu.cn/jw_css/system/login.action", data={
            'userId': username,
            'userPassword': password,
            'checkCode': captcha,
            'x': 0,
            'y': 0
        })
        session.text = await resp.text()
        input = Soup(session.text, "html.parser").find("input", id="errorReason")
        if input is not None:
            logging.error("Login failed:" + input["value"])
            err = input["value"]
        else:
            logging.debug("Login succeed.")
        return session, err

    async def logout(self):
        await self.session.get("http://xk.urp.seu.edu.cn/jw_css/system/logout.action")

    def __init__(self):
        self.session = aiohttp.ClientSession(headers=HEADERS[0])
        self.text = None
        self.course_list = []

    async def get_list(self, cls):
        selected = [i.name for i in self.course_list]
        url = "http://xk.urp.seu.edu.cn/jw_css/xk/runViewsecondSelectClassAction.action?select_jhkcdm=000%d&select_mkbh=%s&select_xkkclx=%d&select_dxdbz=0" % (
            Course.TYPE[cls] - 11, cls, Course.TYPE[cls])
        resp = await self.session.get(url)
        logging.debug("Got " + cls + " class list.")
        soup = Soup(await resp.read(), "html.parser")
        course_list = []
        for row in soup.find(id="second1").find_all("tr"):
            if u"课程名称" in row.text:
                continue
            tds = [i.text.strip() for i in row.find_all("td")]
            course = Course(cls, tds[1], tds[2], tds[3],
                            select_jhkcdm="000" + str(Course.TYPE[cls] - 11),
                            select_xkkclx=Course.TYPE[cls],
                            select_jxbbh=row.find_all("td")[8]["id"])
            course_list.append(course)
        return course_list

    async def get_page(self):
        headers = HEADERS[0].copy()
        # await asyncio.sleep(6)
        # headers["Referer"] = "http://xk.urp.seu.edu.cn/jw_css/system/showLogin.action"
        # resp = await self.session.get("http://xk.urp.seu.edu.cn/jw_css/xk/runMainmainSelectClassAction.action")
        logging.debug("Got home page.")
        soup = Soup(self.text, "html.parser")
        # print(soup)
        course_list = []
        for row in soup.find_all(height="65"):
            tds = row.find_all("td")
            name = None
            jhkcdm = None
            jxbbh = None
            matches = None
            doubleps = row.find_all("td")[4].find_all("p")
            secondary = None
            tmp = [i for i in doubleps[0].stripped_strings]
            if u"[尚未选择]" in tmp:
                selected = False
            else:
                selected = True
            if u"推荐课表" in doubleps[1].text and "院系统一安排" not in row.find_all("td")[5].text:
                secondary = None
                matches = re.search(r"(\S+)\s+(\S+)\s+(\S+?\s\S+?)$", doubleps[1].text)
                name = matches[1]
                teacher = matches[2]
                time = matches[3]
                matches = re.search(r"^selectThis\('(.+?)','(.+?)',.+\)$", row.find_all("td")[5].button["onclick"])
                jhkcdm = matches[1]
                jxbbh = matches[2]
            elif "Seminar" in tds[0].text:
                secondary = "sem"
            elif "经济管理类" in tds[0].text:
                secondary = "jjygll"
            elif "人文社科类" in tds[0].text:
                secondary = "rwskl"
            elif "自然科学与技术科学类" in tds[0].text:
                secondary = "zl"
            if secondary is not None:
                if selected:
                    matches = re.search(r"(\S+)\s+(\S+)\s+\S+\s+(\S+?\s\S+?)$", doubleps[0].text.strip())
                    name = matches[1]
                    teacher = matches[2]
                    time = matches[3]
            if name is not None:
                course = Course(cls=secondary,
                                name=name,
                                teacher=teacher,
                                time=time,
                                select_jxbbh=jxbbh,
                                select_xkkclx=11,
                                select_jhkcdm=jhkcdm,
                                selected=selected)
                course_list.append(course)
        return course_list

    async def select(self, course):
        # http://xk.urp.seu.edu.cn/jw_css/xk/runSelectclassSelectionAction.action?select_jxbbh=GR11206201731731&select_xkkclx=47&select_jhkcdm=00036&select_mkbh=zl
        resp = await self.session.post(course.select_url)
        resp = json.loads(await resp.read())
        if resp["rso"]["isSuccess"]:
            logging.debug("Select " + course + " success!")
            return None
        else:
            logging.error("Select " + course + " success!")
            logging.debug("Reason " + resp["rso"]["errorStr"])
            return resp["rso"]["errorStr"]

    async def __recognize_captcha(self):
        """
        从小猴偷米处参考得到的验证码识别算法及代码。
        :return:
        """
        logging.debug("Try pass the captcha check.")
        async with self.session.get("http://xk.urp.seu.edu.cn/jw_css/getCheckCode") as resp:
            img = Image.open(io.BytesIO(await resp.read()))
            start = [13, 59, 105, 151]
            result = ''
            for i in start:
                sample = []
                for i in range(i, i + 40):
                    temp = 0
                    for j in range(0, 100):
                        temp += (img.getpixel((i, j))[1] < 40)
                    sample.append(temp)
                min_score = 1000
                max_match = 0
                for idx, val in enumerate(STANDARD):
                    diff = []
                    for i in range(len(sample)):
                        diff.append(sample[i] - val[i])
                    avg = float(sum(diff)) / len(diff)

                    for i in range(len(sample)):
                        diff[i] = abs(diff[i] - avg)
                    score = sum(diff)
                    if score < min_score:
                        min_score = score
                        max_match = idx

                result = result + str(max_match)
            logging.debug("Captcha is " + result)
            return result


def test_requests():
    import requests
    session = requests.Session()
    resp = session.get("http://xk.urp.seu.edu.cn/jw_css/getCheckCode")
    img = Image.open(io.BytesIO(resp.content))
    start = [13, 59, 105, 151]
    result = ''
    for i in start:
        sample = []
        for i in range(i, i + 40):
            temp = 0
            for j in range(0, 100):
                temp += (img.getpixel((i, j))[1] < 40)
            sample.append(temp)
        min_score = 1000
        max_match = 0
        for idx, val in enumerate(STANDARD):
            diff = []
            for i in range(len(sample)):
                diff.append(sample[i] - val[i])
            avg = float(sum(diff)) / len(diff)
            for i in range(len(sample)):
                diff[i] = abs(diff[i] - avg)
            score = sum(diff)
            if score < min_score:
                min_score = score
                max_match = idx
        result = result + str(max_match)

    session.post("http://xk.urp.seu.edu.cn/jw_css/system/login.action", data={
        'userId': 213151752,
        'userPassword': "zoudick970514",
        'checkCode': result,
        'x': 0,
        'y': 0
    })
    # resp = session.get("http://xk.urp.seu.edu.cn/jw_css/xk/runMainmainSelectClassAction.action")
    print(resp.content)


def test_login():
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(UserSession.login(213151752, "zoudick97051"))
    loop.run_forever()


async def test_get_page_async():
    session, err = await UserSession.login(213151752, "zoudick970514")
    clist = await session.get_page()
    print("\n".join([i.__str__() for i in clist]))


async def test_get_list_async():
    session, err = await UserSession.login(213151752, "zoudick970514")
    clist = await session.get_list("jjygll")
    print("\n".join([i.__str__() for i in clist]))


def test_async():
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_get_page_async())
    loop.run_forever()


if __name__ == '__main__':
    # test_login()
    test_async()
