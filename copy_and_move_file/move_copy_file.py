#-*- coding: utf-8 -*-

import os
import requests
from copy import deepcopy
from base64 import b64encode
from urllib.parse import quote, unquote


class QuertUpyun(object):
	def __init__(self, bucket, username, password):
		self.bucket = bucket
		self.username = username
		self.password = password
		self.upyun_api = 'http://v0.api.upyun.com'
		

	def _auth(self):
		req_headers = {
			"Authorization": "Basic " + b64encode((self.username + ':' + self.password).encode()).decode(),
			'User-Agent':'Auth-Nie-Python'

		}
		return req_headers

	def reqMoveFile(self, move_source, move_destination):
		headers = deepcopy(self._auth())
		headers['X-Upyun-Move-Source'] = ('/' + self.bucket + move_source).encode('utf-8').decode('latin1')
		s = requests.Session()
		key = '/' + self.bucket  + move_destination + move_source

		respMove = s.put(self.upyun_api + key, headers=headers)
		print("Move " + move_source + " to " + move_destination + move_source)

		if respMove.status_code != 200:
			with open('movePathError.txt', 'a') as f:
				f.write(move_source + '\n')

	def reqCopyFile(self, copy_source, copy_destination):
		headers = deepcopy(self._auth())
		headers['X-Upyun-Copy-Source'] = ('/' + self.bucket + copy_source).encode('utf-8').decode('latin1')
		s = requests.Session()
		key = '/' + self.bucket  + copy_destination + copy_source

		respCopy = s.put(self.upyun_api + key, headers=headers)
		print("Copy " + copy_source + ' To ' + copy_destination + copy_source)

		if respCopy.status_code != 200:
			with open('copyPathError.txt', 'a') as f:
				f.write(copy_source +  '\n')



if __name__ == '__main__':
	copyAndMoveInit = QuertUpyun('BUCKET_NAME', 'OperatorName', 'OperatorPass')
	for path in open('LocalListFilePath'):
		path = (path.rstrip())
		
		# copyAndMoveInit.reqCopyFile(path, '/COPYPATH')
		copyAndMoveInit.reqMoveFile(path, '/MOVEPATH')
	else:
		print("Job is done!")