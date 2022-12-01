import requests


class RequestAPI:
    """Базовый класс для запросов"""

    def __init__(self, server):
        self.connect_timeout = 10
        self.read_timeout = 10
        self.max_retries = 3
        self._session = None
        self.server = server
        self.headers = {}
        self.certificate = ()

    def session(self):
        """Получение сессии."""

        if self._session is None:
            self._session = requests.Session()
            self._session.mount("http://", requests.adapters.HTTPAdapter(max_retries=self.max_retries))
            self._session.mount("https://", requests.adapters.HTTPAdapter(max_retries=self.max_retries))
        return self._session

    def request(self, url, method, data=None, json=None, headers=None, verify=False, **kwargs):
        """Отправка запроса."""

        session = self.session()

        if headers is None:
            headers = self.headers

        if self.certificate:
            kwargs['cert'] = self.certificate
            verify = "mts_sfr_cert/mts-all-root-bundle.crt"

        if method == 'post':
            invoke_meth = session.post
        elif method == 'patch':
            invoke_meth = session.patch
        elif method == 'delete':
            invoke_meth = session.delete
        elif method == 'put':
            invoke_meth = session.put
        elif method == 'get':
            invoke_meth = session.get
        else:
            raise ValueError('Bad method passed "%s"' % method)

        absolute_url = self.server + url

        response = invoke_meth(url=absolute_url,
                               data=data,
                               timeout=(self.connect_timeout, self.read_timeout),
                               verify=verify,
                               headers=headers,
                               json=json, **kwargs)
        return response

    def get(self, url, data=None, json=None, **kwargs):
        """Отправка get запроса."""

        return self.request(url, 'get', data=data, json=json, **kwargs)


class FiscalRegistrationServiceAPI:
    """API фискализации для СФР."""

    VERSION = '1.0'
    PATH_CERT_SFR = "mts_sfr_cert/srf-billing-crt.cer"
    PATH_KEY_SFR = "mts_sfr_cert/srf-billing-crt.key"

    def __init__(self):
        self.request_api = RequestAPI('https://10.73.18.114')
        self.request_api.max_retries = 1
        self.request_api.certificate = (self.PATH_CERT_SFR, self.PATH_KEY_SFR)  # SFR API certificate
        self.uuid = 'f2f5fc3e-7f1e-499e-aaee-f502182ca617'
        self.headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'X-Request-Id': self.uuid
        }

    def get_req(self):
        url = f'/fiscalregistrar/{self.VERSION}/receipts/clients/me/operations/{self.uuid}/'
        response = self.request_api.get(url)
        print(response)


FiscalRegistrationServiceAPI().get_req()
