import json
import os.path
import re

import requests
from loguru import logger
from bs4 import BeautifulSoup
from utils.common_utils import get_github_common_headers, get_mcpserverOrg_headers, get_mcpSo_headers, \
    get_awesomemcp_headers, get_reddit_headers, get_mcphubai_headers
from utils.cookie_utils import cookie_parser
from utils.gpt_utils import question_to_gpt


def extra_mcp_links_from_githubShareURL(url, cookie_str):
    headers = get_github_common_headers()
    cookie = cookie_parser(cookie_str)
    response = requests.get(url, headers=headers, cookies=cookie)
    res_text = response.text
    soup = BeautifulSoup(res_text, 'html.parser')
    a_tags = soup.find_all('a')
    all_links = []
    for a_tag in a_tags:
        href = a_tag.attrs.get('href', '')
        try:
            if href.startswith('https://github.com/'):
                all_links.append(href)
                logger.info(f"Found link: {href}")
            elif href.startswith('/'):
                all_links.append(f'https://github.com{href}')
                logger.info(f"Found link: {href}")
        except:
            logger.warning(f"Invalid link: {href}")
    logger.info(f"Found {len(all_links)} links")
    return list(set(all_links))

# https://mcpservers.org/
def extra_mcp_links_from_mcpserversOrg():
    headers = get_mcpserverOrg_headers()
    url = "https://mcpservers.org/"
    response = requests.get(url, headers=headers)
    all_links = re.findall(r'\\"url\\":\\"https://github\.com/(.*?)\\"', response.text)
    all_links = list(set(all_links))
    links = []
    for link in all_links:
        try:
            new_link = '/'.join(link.split('/')[:2])
            links.append(f'https://github.com/{new_link}')
            logger.info(f"Found link: {new_link}")
        except:
            logger.warning(f"Invalid link: {link}")
    logger.info(f"Found {len(links)} links")
    return links

# https://mcp.so
def extra_mcp_links_from_mcpSo(mcpSo_cookie_str):
    headers = get_mcpSo_headers()
    cookies = cookie_parser(mcpSo_cookie_str)
    url = "https://mcp.so/"
    response = requests.get(url, headers=headers, cookies=cookies)
    all_links = re.findall(r'\\"url\\":\\"https://github\.com/(.*?)\\"', response.text)
    all_links = list(set(all_links))
    links = []
    for link in all_links:
        try:
            new_link = '/'.join(link.split('/')[:2])
            links.append(f'https://github.com/{new_link}')
            logger.info(f"Found link: {new_link}")
        except:
            logger.warning(f"Invalid link: {link}")
    logger.info(f"Found {len(links)} links")
    return links

# https://www.awesomemcp.com/
def extra_mcp_links_from_awesomemcp(awesomeMcp_cookie_str):
    headers = get_awesomemcp_headers()
    cookies = cookie_parser(awesomeMcp_cookie_str)
    url = "https://mcp.so/"
    response = requests.get(url, headers=headers, cookies=cookies)
    all_links = re.findall(r'\\"url\\":\\"https://github\.com/(.*?)\\"', response.text)
    all_links = list(set(all_links))
    links = []
    for link in all_links:
        try:
            new_link = '/'.join(link.split('/')[:2])
            links.append(f'https://github.com/{new_link}')
            logger.info(f"Found link: {new_link}")
        except:
            logger.warning(f"Invalid link: {link}")
    logger.info(f"Found {len(links)} links")
    return links

# https://www.reddit.com/r/ClaudeAI/comments/1hje6qu/sorted_list_of_mcp_servers_50/
def extra_mcp_links_from_reddit(reddit_cookie_str):
    headers = get_reddit_headers()
    cookies = cookie_parser(reddit_cookie_str)
    url = "https://www.reddit.com/r/ClaudeAI/comments/1hje6qu/sorted_list_of_mcp_servers_50/"
    response = requests.get(url, headers=headers, cookies=cookies)
    all_links = re.findall(r'\\"url\\":\\"https://github\.com/(.*?)\\"', response.text)
    all_links = list(set(all_links))
    links = []
    for link in all_links:
        try:
            new_link = '/'.join(link.split('/')[:2])
            links.append(f'https://github.com/{new_link}')
            logger.info(f"Found link: {new_link}")
        except:
            logger.warning(f"Invalid link: {link}")
    logger.info(f"Found {len(links)} links")
    return links

# https://www.mcphub.ai/servers
def extra_mcp_links_from_mcphubAi(mcphubAi_cookie_str):
    headers = get_mcphubai_headers()
    cookies = cookie_parser(mcphubAi_cookie_str)
    url = "https://www.mcphub.ai/servers"
    response = requests.get(url, headers=headers, cookies=cookies)
    all_links = re.findall(r'\\"url\\":\\"https://github\.com/(.*?)\\"', response.text)
    all_links = list(set(all_links))
    links = []
    for link in all_links:
        try:
            new_link = '/'.join(link.split('/')[:2])
            links.append(f'https://github.com/{new_link}')
            logger.info(f"Found link: {new_link}")
        except:
            logger.warning(f"Invalid link: {link}")
    logger.info(f"Found {len(links)} links")
    return links

def extra_real_mcp_links(all_links, cookie_str):
    all_json_data = []
    mcp_links = []
    cookie = cookie_parser(cookie_str)
    headers = get_github_common_headers()
    for i, link in enumerate(all_links):
        try:
            logger.info(f"Checking link {i + 1}/{len(all_links)}: {link}")
            username, repo = link.split('/')[3:5]
            rstr = r"[\/\\\:\*\?\"\<\>\|]"
            file_name = re.sub(rstr, "_", link)
            if os.path.exists(f'./static/{file_name}.json'):
                logger.info(f"Skip {link}")
                continue

            response = requests.get(link, headers=headers, cookies=cookie)
            res_text = response.text
            soup = BeautifulSoup(res_text, 'html.parser')
            # script = soup.find_all('script', attrs={'data-target': 'react-app.embeddedData'})
            # <react-partial partial-name="repos-overview" data-ssr="true" data-attempted-ssr="true">
            # react_partial = soup.find_all('react-partial', attrs={'partial-name': 'repos-overview', 'data-ssr': 'true', 'data-attempted-ssr': 'true'})
            # script = react_partial[0].find_all('script', attrs={'data-target': 'react-partial.embeddedData'})
            scripts = soup.find_all('script', attrs={'data-target': 'react-partial.embeddedData'})
            for script in scripts:
                if '"displayName":"README.md"' in script.string:
                    res_text = script.string
                    break
            prompt = """
                    你是MCP分析提取大师！
                    下面我将给你github页面的json数据，你需要将复杂的json数据转化成我给你的参考例子的json格式，如果能够成功转换，你只需回复json数据，不要加上任何其他语句！如果无法转换，只需回复无法转换。
                    {
                      "mcpServers": {
                        "postgres": {
                          "command": "npx",
                          "args": [
                            "-y",
                            "@modelcontextprotocol/server-postgres",
                            "postgresql://localhost/mydb"
                          ]
                        }
                      }
                    }Replace /mydb with your database name.
                    会被转化为
                    id": "postgres",
                    "name": "PostgreSQL",
                    "description": "Read-only database access with schema inspection",
                    "repo": "https://github.com/modelcontextprotocol/servers/tree/main/src/postgres",
                    "tags": ["database", "postgresql", "sql"],
                    "command": "npx",
                    "baseArgs": ["-y", "@modelcontextprotocol/server-postgres"],
                    "configurable": true,
                    "configSchema": {
                      "properties": {
                        "connectionString": {
                          "type": "string",
                          "description": "PostgreSQL connection string",
                          "required": true
                        }
                      }
                    },
                    "argsMapping": { // 说明args中的第三个参数是变量，需要手动指定
                      "connectionString": {
                        "type": "single",
                        "position": 2
                      }
                    }
                  }, 
                    json数据格式如下：
                    参考例子
                    #1 {
                        "id": "filesystem", # 项目的唯一标识符
                        "name": "Filesystem", # 项目的名称
                        "description": "Secure file operations with configurable access controls", # 项目的描述
                        "tags":["filesystem","access-control"], # 项目的标签
                        "repo":"https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem", # 项目的仓库地址
                        "command": "npx", # 项目的命令 如果有多个命令npm > Python > docker
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
                    #2
                    {
                        "id": "github",
                        "name": "GitHub",
                        "description": "Repository management, file operations, and GitHub API integration",
                        "tags": ["github","repository","api"],
                        "repo": "https://github.com/modelcontextprotocol/servers/tree/main/src/github",
                        "command": "npx",
                        "baseArgs": ["-y", "@modelcontextprotocol/server-github"],
                        "configurable": true,
                        "configSchema": {
                            "properties": {
                                "token": {
                                    "type": "string",
                                    "description": "GitHub Personal Access Token",
                                    "required": true
                                }
                            }
                        },
                        "argsMapping": {
                            "token": {
                                "type": "env",
                                "key": "GITHUB_PERSONAL_ACCESS_TOKEN"
                            }
                        }
                    },

                    #3{
                        "id": "gdrive",
                        "name": "Google Drive",
                        "tags": ["google","filesystem","api"],
                        "description": "File access and search capabilities for Google Drive",
                        "repo": "https://github.com/modelcontextprotocol/servers/tree/main/src/gdrive",
                        "command": "npx",
                        "baseArgs": ["-y", "@modelcontextprotocol/server-gdrive"],
                        "configurable": false
                    }""" + f'''网页json数据：{res_text}和链接：{link} MCP识别出来的json结果：（直接给出）（不要回复任何其他内容） '''
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
                    # logger.info(json.dumps(ans, indent=4))
                    all_json_data.append({
                        'json': json.dumps(ans, indent=4),
                        'file_name': file_name
                    })
                    mcp_links.append(link)
                    logger.info(f"{link} is a real MCP link")
            except Exception as e:
                logger.error(f"Error 1: {e}")
            logger.info('-' * 100)
        except Exception as e:
            logger.error(f"Error 2: {e}")
    logger.info(f"Found {len(mcp_links)} MCP links")
    return all_json_data

def download_json_data(all_json_data):
    if not os.path.exists('./static'):
        os.makedirs('./static')
    for i, json_data in enumerate(all_json_data):
        try:
            file_name = json_data['file_name']
            with open(f'./static/{file_name}.json', 'w') as f:
                f.write(json_data['json'])
                logger.info(f"Write json data to ./static/{file_name}.json")
        except Exception as e:
            logger.error(f"Error 3: {e}")

def combine_json_data():
    all_json_data = []
    all_json_files = os.listdir('./static')
    if os.path.exists('./static/all_json_data.json'):
        os.remove('./static/all_json_data.json')
    for json_file in all_json_files:
        with open(f'./static/{json_file}', 'r') as f:
            json_data = f.read()
            json_data = json.loads(json_data)
            all_json_data.append(json_data)
    with open('./static/all_json_data.json', 'w') as f:
        f.write(json.dumps(all_json_data, indent=4))




if __name__ == '__main__':
    cookie_str = r'_octo=GH1.1.67071983.1728714395; _device_id=03a2257b297d9b100259ac23fb364a7e; user_session=O-OBEyjUj6m2nHv9cMTsFYOof2aN5dygTjeSgRHOKLPeGRCF; __Host-user_session_same_site=O-OBEyjUj6m2nHv9cMTsFYOof2aN5dygTjeSgRHOKLPeGRCF; logged_in=yes; dotcom_user=cv-cat; GHCC=Required:1-Analytics:1-SocialMedia:1-Advertising:1; MicrosoftApplicationsTelemetryDeviceId=03179cb2-5f23-46f0-a939-a712c2d5468f; MSFPC=GUID=be967db050704355b04e081b78bf073b&HASH=be96&LV=202410&V=4&LU=1728720058810; color_mode=%7B%22color_mode%22%3A%22auto%22%2C%22light_theme%22%3A%7B%22name%22%3A%22light%22%2C%22color_mode%22%3A%22light%22%7D%2C%22dark_theme%22%3A%7B%22name%22%3A%22dark%22%2C%22color_mode%22%3A%22dark%22%7D%7D; cpu_bucket=xlg; preferred_color_mode=light; tz=Asia%2FShanghai; _gh_sess=f3aqT7Jo9u%2F3QSxH1eki7Z36pP22yvfx1bERjUyyHBNeGU8JezuqRLUmCpmh0%2B%2FE6tNZE6uu%2FKweqCs0agRnhzzJwtnYB04b4Ai4Nxe6v62cTGYUoKFe644qZGMt6T2t5A1usvkSN5GkBjJ91tIzyBaZl1wbcik9yKMXsdgtFx4AF%2BHMK24RX9D7N6Jp3zYB%2FVaNjJxKDBHTY2Mzh3otiGPJvsn5S3enwm1sPRCLCPzHLRCzZQ8XFaUCAwwHwsebIgwS8Qe3iannI75xNPjP6aVIa%2F%2FoZ0wrbDyW%2F3S8uvNbeciDkhes5mvX6HEdUgcK71gDjR01%2BWZX08JuyvZF4fU6VRwSTBIPjWiY4w%3D%3D--yMOXlFfgU94a02C9--6WSO4%2B0wpB7DeC5q%2FB%2Bj3A%3D%3D'
    # github_share_urls = [
    #     'https://github.com/punkpeye/awesome-mcp-servers',
    #     'https://github.com/modelcontextprotocol/servers',
    #     'https://github.com/wong2/awesome-mcp-servers'
    # ]
    # for url in github_share_urls:
    #     mcp_links = extra_mcp_links_from_githubShareURL(url, cookie_str)
    #     real_mcp_links = extra_real_mcp_links(mcp_links, cookie_str)
    #     download_json_data(real_mcp_links)
    #
    # # https://mcpservers.org/
    # mcpserversOrg_mcp_links = extra_mcp_links_from_mcpserversOrg()
    # mcpserversOrg_real_mcp_links = extra_real_mcp_links(mcpserversOrg_mcp_links, cookie_str)
    # download_json_data(mcpserversOrg_real_mcp_links)

    # https://mcp.so
    mcpSo_cookie_str = r'_ga=GA1.1.20734558.1736835531; _ga_9ZWF7FKDR8=GS1.1.1736916926.3.1.1736917639.0.0.0'
    mcpSo_mcp_links = extra_mcp_links_from_mcpSo(mcpSo_cookie_str)
    mcpSo_real_mcp_links = extra_real_mcp_links(mcpSo_mcp_links, mcpSo_cookie_str)
    download_json_data(mcpSo_real_mcp_links)

    # https://www.awesomemcp.com/
    awesomeMcp_cookie_str = r'NEXT_LOCALE=zh; __Host-next-auth.csrf-token=2becb30594d9ab565e5bda59a04c973759a504469347d56afe216efc50e634c9%7C875759a03df936c52e5b00169fddb0da65b341f591ef1be2f5e9cf71dff929cd; __Secure-next-auth.callback-url=https%3A%2F%2Fwww.awesomemcp.com'
    awesomeMcp_mcp_links = extra_mcp_links_from_awesomemcp(awesomeMcp_cookie_str)
    awesomeMcp_real_mcp_links = extra_real_mcp_links(awesomeMcp_mcp_links, awesomeMcp_cookie_str)
    download_json_data(awesomeMcp_real_mcp_links)

    # https://www.reddit.com/r/ClaudeAI/comments/1hje6qu/sorted_list_of_mcp_servers_50/
    reddit_cookie_str = r'edgebucket=FI3S7ekrKoQf6nz2WN; loid=000000001h42t77iks.2.1736835820963.Z0FBQUFBQm5oZ0xzQjg5WW5VLVZqSWFfMzNwRF9GUTRVNWhpR09wQkM2N2U4NVlqTmFvWUVYSUFGZ0NaX1RXZjBJck9NSmZ0dVU4WmJfdFg5bGlvaDd0UWt4TGlSZ3FGR1IwNGlNY1NOcUNveTNTVFdZbXBPOVJubVhEMmxGdkdnaEUzUldLekMyQjQ; token_v2=eyJhbGciOiJSUzI1NiIsImtpZCI6IlNIQTI1NjpzS3dsMnlsV0VtMjVmcXhwTU40cWY4MXE2OWFFdWFyMnpLMUdhVGxjdWNZIiwidHlwIjoiSldUIn0.eyJzdWIiOiJsb2lkIiwiZXhwIjoxNzM2OTIyMjIwLjk2MzUwNywiaWF0IjoxNzM2ODM1ODIwLjk2MzUwNywianRpIjoibVVIeDBTZ0p0ZGJLaTlFTTEzQWdLQnppNTlFVi13IiwiY2lkIjoiMFItV0FNaHVvby1NeVEiLCJsaWQiOiJ0Ml8xaDQydDc3aWtzIiwibGNhIjoxNzM2ODM1ODIwOTYzLCJzY3AiOiJlSnhra2RHT3REQUloZC1GYTVfZ2Y1VV9tMDF0Y1lhc0xRYW9rM243RFZvY2s3MDdjRDRwSFA5REtvcUZEQ1pYZ3FuQUJGZ1RyVERCUnVUOW5MbTNnMmlOZTh0WXNabkNCRm13RkRya21MR3NpUVFtZUpJYXl4c21vSUxOeUZ5dXRHTk5MVDBRSnFoY01yZUZIcGMyb2JrYmk1NmRHRlc1ckR5b3NWZmwwdGpHRkxZbnhqY2JxdzJwdUM2bk1rbkxRdmtzWHZUak45VzM5dm16X1NhMEo4T0txdW1CM2hsSkNHNHNmcGltM2Q5VGs1NnRDeGExOTNxUTJ1ZDYzSzU5MWl3ME83ZWY2X2xySXhtWFkyaC1KdnQzMXktaEE0ODhMelBxQUVhczRVY1pkbVFkX2xVSFVMbWdKR01KNHRNSTVNcmwyMzhKdG12VHY4YnRFejk4TS1LbU5feldETlJ6Q2VMUXBfSDFHd0FBX184UTFlVFIiLCJmbG8iOjF9.oqZ94NtJzqhzE6aDgaKizhNic05XTeUnohDHJYsExd1TaDA0T8N7KUp5if-ZDYWky-7PYUfLBEWjN3rqV9iD6MKexh6PPDOd-aVDbMPNh5lsijMYbY9DTeGG6JSWxcK9IsrbHaEVhjXRiUfD5YpVqRIpKy3KNAgf1xssYgbloGMe2iEM7Fj6Gnb-0EcgRPHOy5U_7h7NT7OXrxMHx9Si9UL6no0tn3XbRc7ef9tUzHp1C0yg9ZOqEhQ3oKdfpiGvLpN5C7tIek2-7F5-qW_vPD_mCZnpDcTL8lku0z_NjqaLxE6NZiSAgM8hx-_OchiZnwlo9tBYO2OnLwNuDwpDvw; csv=2; csrf_token=3dceae2ef690206c772bbdce77ce0cf4; session_tracker=fqndnprfegpjjjhpem.0.1736918069056.Z0FBQUFBQm5oMFExZXpGZjBBaWEwYnZLN3o2S2ktcTNmUk9UYl9qU1RETDBMSmtjRy1PNW5vT3JKOFJRMlVHME5wMk01bTQ2eV93cE5mN3pwOWVlVzhodkVTNFdSa0x1ckVpcEhSUW5lNjBZWUtQQkgyblVpaDVnUlJkZ2dQWUsyMWtJSkY4bV9MR2g'
    reddit_mcp_links = extra_mcp_links_from_reddit(reddit_cookie_str)
    reddit_real_mcp_links = extra_real_mcp_links(reddit_mcp_links, reddit_cookie_str)
    download_json_data(reddit_real_mcp_links)

    # https://www.mcphub.ai/servers
    mcphubAi_cookie_str = r'__client_uat=0; __clerk_db_jwt=dvb_2reSqwtfZidi2foKzeASk0rKSE3; _ga_GHY6R27303=GS1.1.1736918246.1.0.1736918246.0.0.0; _ga=GA1.1.1247452290.1736918246; __clerk_db_jwt_2dNeylqY=dvb_2reSqwtfZidi2foKzeASk0rKSE3; __client_uat_2dNeylqY=0'
    mcphubAi_mcp_links = extra_mcp_links_from_mcphubAi(mcphubAi_cookie_str)
    mcphubAi_real_mcp_links = extra_real_mcp_links(mcphubAi_mcp_links, mcphubAi_cookie_str)
    download_json_data(mcphubAi_real_mcp_links)

    combine_json_data()
