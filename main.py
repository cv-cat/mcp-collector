import json
import re

import requests
from loguru import logger
from bs4 import BeautifulSoup
from utils.common_utils import get_github_common_headers, get_mcpserverOrg_headers
from utils.cookie_utils import cookie_parser
from utils.gpt_utils import question_to_gpt


def extra_mcp_links_from_githubShareURL(url, cookie_str):
    curr_username, curr_repo = url.split('/')[3:5]
    headers = get_github_common_headers()
    cookie = cookie_parser(cookie_str)
    response = requests.get(url, headers=headers, cookies=cookie)
    res_text = response.text
    soup = BeautifulSoup(res_text, 'html.parser')
    a_tags = soup.find_all('a')
    all_links = []
    for a_tag in a_tags:
        href = a_tag.attrs.get('href', '')
        if href.startswith('https://github.com/'):
            try:
                username, repo = href.split('/')[3:5]
                if not username == curr_username or not repo == curr_repo:
                    all_links.append(href)
                    logger.info(f"Found link: {href}")
            except:
                logger.warning(f"Invalid link: {href}")
    logger.info(f"Found {len(all_links)} links")
    return list(set(all_links))

def extra_mcp_links_from_mcpserversOrg():
    headers = get_mcpserverOrg_headers()
    url = "https://mcpservers.org/"
    response = requests.get(url, headers=headers)
    res_text = response.text
    soup = BeautifulSoup(res_text, 'html.parser')
    a_tags = soup.find_all('a')
    all_links = []
    for a_tag in a_tags:
        href = a_tag.attrs.get('href', '')
        if href.startswith('https://mcpservers.org/'):
            all_links.append(href)
            logger.info(f"Found link: {href}")
    logger.info(f"Found {len(all_links)} links")
    return list(set(all_links))

def extra_mcp_links_from_mcpIo():
    pass

def extra_mcp_links_from_reddit():
    pass

def extra_mcp_links_from_mcphubAi():
    pass

def extra_real_mcp_links(all_links, cookie_str):
    mcp_links = []
    cookie = cookie_parser(cookie_str)
    headers = get_github_common_headers()
    for i, link in enumerate(all_links):
        logger.info(f"Checking link {i + 1}/{len(all_links)}: {link}")
        response = requests.get(link, headers=headers, cookies=cookie)
        res_text = response.text

        prompt = """
            我将给你github网页的静态源代码，你需要提取页面的数据转换成json，如果能够成功转换，你只需回复json数据，不要加上任何其他语句！如果无法转换，只需回复无法转换。
            json数据格式如下：每个字段都是必须的，其中configSchema和argsMapping字段是可选的。{
              "id": "filesystem", # 项目的唯一标识符
              "name": "Filesystem", # 项目的名称
              "description": "Secure file operations with configurable access controls", # 项目的描述
              "tags":["filesystem","access-control"], # 项目的标签
              "repo":"https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem", # 项目的仓库地址
              "command": "npx", # 项目的命令
              "baseArgs": ["-y", "@modelcontextprotocol/server-filesystem"], # 项目的基础参数
              "env": {}, # 项目的环境变量
              "configurable": true, # 项目是否可配置
              "configSchema": {
                "properties": {
                  "paths": {
                    "type": "array",
                    "description": "Allowed file system paths",
                    "required": true,
                    "minItems": 1
                  }
                }
              },
              "argsMapping": {
                "paths": {
                  "type": "spread",
                  "position": 2
                }
              }
            }
        """ + f'网页源代码：{res_text}和链接：{link}'
        res_json = question_to_gpt(prompt)
        logger.info(str(res_json))
        try:
            res = res_json['choices'][0]['message']['content']
            if '无法转换' in res:
                logger.info(f"{link} is not a real MCP link")
            else:
                if '```' in res:
                    ans = re.findall(r'```(.*?)```', res, re.S)
                    ans = ans[0][4:]
                else:
                    ans = res
                ans = json.loads(ans)
                logger.info(json.dumps(ans, indent=4))
                mcp_links.append(link)
                logger.info(f"{link} is a real MCP link")
        except Exception as e:
            logger.error(f"Error: {e}")
        logger.info('-' * 100)
    logger.info(f"Found {len(mcp_links)} MCP links")
    return mcp_links


if __name__ == '__main__':
    url = "https://github.com/punkpeye/awesome-mcp-servers/blob/main/README.md"
    cookie_str = r'_octo=GH1.1.67071983.1728714395; _device_id=03a2257b297d9b100259ac23fb364a7e; user_session=O-OBEyjUj6m2nHv9cMTsFYOof2aN5dygTjeSgRHOKLPeGRCF; __Host-user_session_same_site=O-OBEyjUj6m2nHv9cMTsFYOof2aN5dygTjeSgRHOKLPeGRCF; logged_in=yes; dotcom_user=cv-cat; GHCC=Required:1-Analytics:1-SocialMedia:1-Advertising:1; MicrosoftApplicationsTelemetryDeviceId=03179cb2-5f23-46f0-a939-a712c2d5468f; MSFPC=GUID=be967db050704355b04e081b78bf073b&HASH=be96&LV=202410&V=4&LU=1728720058810; color_mode=%7B%22color_mode%22%3A%22auto%22%2C%22light_theme%22%3A%7B%22name%22%3A%22light%22%2C%22color_mode%22%3A%22light%22%7D%2C%22dark_theme%22%3A%7B%22name%22%3A%22dark%22%2C%22color_mode%22%3A%22dark%22%7D%7D; cpu_bucket=xlg; preferred_color_mode=light; tz=Asia%2FShanghai; _gh_sess=f3aqT7Jo9u%2F3QSxH1eki7Z36pP22yvfx1bERjUyyHBNeGU8JezuqRLUmCpmh0%2B%2FE6tNZE6uu%2FKweqCs0agRnhzzJwtnYB04b4Ai4Nxe6v62cTGYUoKFe644qZGMt6T2t5A1usvkSN5GkBjJ91tIzyBaZl1wbcik9yKMXsdgtFx4AF%2BHMK24RX9D7N6Jp3zYB%2FVaNjJxKDBHTY2Mzh3otiGPJvsn5S3enwm1sPRCLCPzHLRCzZQ8XFaUCAwwHwsebIgwS8Qe3iannI75xNPjP6aVIa%2F%2FoZ0wrbDyW%2F3S8uvNbeciDkhes5mvX6HEdUgcK71gDjR01%2BWZX08JuyvZF4fU6VRwSTBIPjWiY4w%3D%3D--yMOXlFfgU94a02C9--6WSO4%2B0wpB7DeC5q%2FB%2Bj3A%3D%3D'
    mcp_links = extra_mcp_links_from_githubShareURL(url, cookie_str)
    real_mcp_links = extra_real_mcp_links(mcp_links, cookie_str)
    for link in real_mcp_links:
        logger.info(link)