import requests
import os
import copy

IMAGE_RESOURCE_URL = '/v1/image'
ENGAGEMENT_RESOURCE_URL = '/v1/engagement'

class SparkAIException(Exception):
    def __init__(self, code, message):
        message = 'Exception [{}] {}'.format(code, message)
        super(SparkAIException, self).__init__(message)

class SparkAIClient(object):
    def __init__(self, api_key, sandbox=False):
        self.api_key = api_key
        self.headers = {
            'Authorization': 'Bearer ' + self.api_key
        }
        if 'SPARKAI_HOST' in os.environ:
            self.base_url = os.environ['SPARKAI_HOST']
        elif sandbox:
            self.base_url = 'https://sandbox.spark.ai'
        else:
            self.base_url = 'https://app.spark.ai'

    def _post(self, path, json=None, files=None, data=None):
        r = requests.post(path, headers=self.headers, files=files, json=json, data=data)
        if r.status_code == 200:
            return r.json()
        else:
            try:
                print(r.json())
                message = r.json()['message']
                raise SparkAIException(r.status_code, message)
            except:
                raise SparkAIException(r.status_code, r.text)

    def _get(self, path, query_params):
        r = requests.get(path, headers=self.headers, params=query_params)
        if r.status_code == 200:
            return r.json()
        else:
            try:
                print(r.json())
                message = r.json()['message']
                raise SparkAIException(r.status_code, message)
            except:
                raise SparkAIException(r.status_code, r.text)

    def _make_payload(self, content_location, program_name, instructions, metadata, label_list, annotations):
        d = {
            'content_location': content_location,
            'program_name': program_name,
            'instructions': instructions,
            'metadata': metadata,
            'priors': {
                'label_list': label_list,
                'annotations': annotations
            }
        }
        if d['priors']['label_list'] is None and d['priors']['annotations'] is None:
            d['priors'] = None
        return {k:v for k,v in d.items() if v is not None}

    def upload_image(self, file_path, tag=None):
        binary_image = open(file_path, 'rb')
        image_name = os.path.basename(file_path)
        files = { 'image_file': (image_name, binary_image, 'multipart/form-data',{'Expires': '0'}) }
        data = {}
        if tag is not None:
            data = {'tag': tag}

        return self._post(path=self.base_url + IMAGE_RESOURCE_URL, files=files, data=data)

    def create_annotation(self, vertices, type, label, metadata):
        d = {
            'vertices': vertices,
            'type': type,
            'label': label,
            'metadata': metadata
        }
        return {k:v for k,v in d.items() if v is not None}


    def create_engagement_from_image_url(self, image_url, program_name=None, instructions=None, metadata=None, label_list=None, annotations=None):
        if isinstance(image_url, list):
            image_url = list(map(lambda x: x.strip(), image_url))
        else:
            image_url = image_url.strip()
        engagement_data = self._make_payload(image_url, program_name, instructions, metadata, label_list, annotations)
        return self._post(path=self.base_url + ENGAGEMENT_RESOURCE_URL, json=engagement_data)


    def create_engagement_from_file(self, file_path, program_name=None, instructions=None, metadata=None, label_list=None, annotations=None):
        image_url = self.upload_image(file_path)['url']
        engagement_data = self._make_payload(image_url, program_name, instructions, metadata, label_list, annotations)
        return self._post(path=self.base_url + ENGAGEMENT_RESOURCE_URL, json=engagement_data)

    def get_engagements(self, query_params={}, limit=10, cursor=0, count=False):
        _query_params = copy.deepcopy(query_params)
        if 'limit' not in query_params:
            _query_params['limit'] = limit
        if 'cursor' not in query_params:
            _query_params['cursor'] = cursor
        if 'count' not in query_params:
            _query_params['count'] = count
        return self._get(path=self.base_url + ENGAGEMENT_RESOURCE_URL, query_params=_query_params)
