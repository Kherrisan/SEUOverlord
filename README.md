# SEUOverlord

一个简单的抢课程序——未完成

## 说明

由于时间有限，仅仅分析并实现了用户登录、查询待选列表、选择课程的基本操作API，并没有实现一个完整可运行的抢课程序。

- UserSession.py中实现了各种基本操作API。
- Course.py中对课程信息进行了封装。

1. 欢迎二次开发。
2. 没有经过测试，请谨慎使用。
3. 验证码识别参考了小猴偷米的一部分开源代码。
4. 没有其他说明了。

## 食用方式

```
session, err = await UserSession.login(一卡通号,密码) #用户登录
course_list = await session.get_page() #得到的是可以服从推荐的课程
course_list_2 = await session.get_list(通识选修课标识符) #得到通识选修课信息
# 通识选修课标识符
# 经管 jjygll
# 人文 rwskl
# seminar sem
# 自然科学 zl
await session.select(course_list_2[0]) #选课
```
