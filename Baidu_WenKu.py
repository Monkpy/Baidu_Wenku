# -*- coding: utf-8 -*-
import json
import re

import requests


class Bdwk(object):
	def __init__(self):
		pass
	
	def get_html(self, url):
		response = requests.get(url)
		if response.status_code == 200:
			response.encoding = 'gb2312'
			html = response.text
			content = re.findall('// htmlBcs迁移请求地址(.*?)WkInfo.verify_user_info', html, re.S)
			if content:
				return content[0]
			else:
				print('content is Fals')
		else:
			print('The Get Code is False:%s' % response.status_code)
	
	def get_link(self, html):
		# htmlurl = re.findall('\[{.*?pageIndex.*?pageLoadUrl.*?:\\\\x22(.*?)\\\\x22},', html, re.S)
		htmlurl = re.findall('(https:\\\\\\\\\\\\/\\\\\\\\\\\\/wkbjcloudbos.bdimg.com.*?)\\\\x22}', html, re.S)
		for i in htmlurl:
			link = i.replace('\\', '')
			response = requests.get(link)
			if response.status_code == 206:
				return response.text  # 只能返回一页
			else:
				print('The htmlurl Code is False:%s' % response.status_code)
	
	def parse_content(self, content):
		body = re.findall('"c":"(.*?)","p"', content, re.S)
		# cont = ''.join(body).encode('utf-8').decode('unicode_escape')
		# print(cont)
		for i in body:
			cont = i.encode('utf-8').decode('unicode_escape')
			cont = cont.replace('\u0020\u0020\u3001', '\u3001')
			print(cont)
	
	def run(self):
		url = 'https://wenku.baidu.com/view/c73922544b73f242336c5fc5.html'
		html = self.get_html(url)
		content = self.get_link(html)
		self.parse_content(content)


if __name__ == '__main__':
	bdwk = Bdwk()
	bdwk.run()
