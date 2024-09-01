import random
import string
import os
from DrissionPage import ChromiumPage, ChromiumOptions
from time import sleep

# 创建一个配置对象，并设置自动分配端口，自动端口不会保存cookies
# co = ChromiumOptions().auto_port

# 创建一个配置对象，并设置8080端口
co = ChromiumOptions().set_local_port(8082)
co2 = ChromiumOptions().set_local_port(8081)

# 设置代理（如需要）
# co.set_proxy('http://127.0.0.1:6666')

# 使用配置对象创建一个 ChromiumPage 对象
page = ChromiumPage(co)
page2 = ChromiumPage(co2)

# 生成随机用户名和密码的函数
def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# 文件名
output_file = 'accounts.txt'

# 检测文件是否存在，如果不存在则创建一个
if not os.path.exists(output_file):
    with open(output_file, 'w') as file:
        pass  # 创建一个空文件

# 循环10次注册账号
for i in range(100):

    username = generate_random_string()
    password = generate_random_string()

    # 打开目标页面
    # new_tab 方法用于在当前浏览器窗口中创建一个新的标签页。
    # 参数 new_context=True 意味着为这个新的标签页创建一个新的浏览器上下文。
    mail_Tab = page.new_tab(new_context=True)
    mail_Tab.get(url='https://www.linshiyouxiang.net/')

    email = mail_Tab.ele('css:input#active-mail').value

    print(f"邮 箱: {email}")

    Linuxdo_Tab = page.new_tab()
    Linuxdo_Tab.get(url='https://linux.do/')

    sleep(1)

    # 点击注册按钮
    button = Linuxdo_Tab.ele('css:#ember5 > header > div > div > div.panel > span > button.widget-button.btn.btn-primary.btn-small.sign-up-button.btn-text')
    button.click()

    # # 可选：添加延迟以观察效果
    # sleep(2)

    # 输入邮箱地址
    email_input = Linuxdo_Tab.ele('css:#new-account-email')
    email_input.input(email)

    # 输入用户名
    username_input = Linuxdo_Tab.ele('css:#new-account-username')
    username_input.input(username)

    # mail_Tab.ele('xpath://*[@id="main"]/div/div/div[1]/ul/li[2]/a/i').click()

    # 输入密码
    password_input = Linuxdo_Tab.ele('css:#new-account-password')
    password_input.input(password)

    # 可选：添加延迟以观察效果
    sleep(2)

    # 点击提交按钮，重试机制
    max_retries = 5
    retries = 0

    while retries < max_retries:
        try:
            submit_button = Linuxdo_Tab.ele('css:button.btn.btn-text.btn-large.btn-primary[type="button"] span.d-button-label')
            submit_button.click()
            break  # 点击成功后跳出循环
        except Exception as e:
            print(f"点击提交按钮失败，重试次数: {retries + 1}，错误: {e}")
            sleep(2)  # 等待2秒后重试
            retries += 1

    if retries == max_retries:
        print(f"Failed to click submit button after {max_retries} retries.")
        raise Exception("Submit button not clicked.")

    print(f"用户名: {username}")
    print(f"密 码: {password}")

    # 刷新页面并等待元素出现的尝试次数
    max_retries = 5
    retries = 0

    while retries < max_retries:
        try:
            # 尝试查找邮件中的激活链接
            title_subject_element = mail_Tab.ele('css:a.title-subject')
            if title_subject_element:
                title_subject_element.click()
                # mail_Tab.ele('xpath://*[@id="main"]/div/div/div[2]/div[1]/div/div[3]/p[2]/a').click()
                active_link = mail_Tab.ele('xpath://*[@id="main"]/div/div/div[2]/div[1]/div/div[3]/p[2]/a').attr('href')
                # print(f"激活链接：{active_link}")
                sleep(4)
                # mail_Tab.ele('css:#activate-account-button').click()
                Linuxdo_Tab2 = page2.new_tab()
                Linuxdo_Tab2.get(url=active_link)
                Linuxdo_Tab2.ele('css:#activate-account-button').click()
                break
        except:
            pass

        # 刷新页面并增加重试计数
        mail_Tab.refresh()
        sleep(5)
        retries += 1

    if retries == max_retries:
        print(f"Failed to find the element 'a.title-subject' after {max_retries} retries.")
        raise Exception("Element not found.")

    # 将注册信息以 UTF-8 编码写入文件
    with open(output_file, 'a', encoding='utf-8') as file:
        file.write(f"邮 箱: {email}\n")
        file.write(f"用户名: {username}\n")
        file.write(f"密 码: {password}\n")
        # file.write(f"激活链接：{active_link}\n")
        file.write("\n\n\n")

    # 关闭标签页
    mail_Tab.close()
    Linuxdo_Tab.close()
    Linuxdo_Tab2.close()



# 关闭浏览器
page.close()
page2.close()
