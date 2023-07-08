import axios from 'axios';
import { makeUseAxios } from 'axios-hooks';

import Cookies from 'js-cookie';

const baseURL = process.env.NODE_ENV === 'development' ? 'http://127.0.0.1:8000' : '';

const instance = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'multipart/form-data',
  },
  withCredentials: true,
});

instance.interceptors.request.use(
  async (request) => {
    const csrf = Cookies.get('csrftoken');
    if (csrf !== undefined) {
      request.headers['X-CSRFToken'] = csrf;
    }
    return request;
  },
  (error) => Promise.reject(error),
);

instance.interceptors.response.use(
  async (response) => response,
  (error) => {
    if (error.response && typeof error.response.data.details === 'string' && error.response.data.details.includes('CSRF')) {
      window.location.reload();
    }
    return Promise.reject(error);
  },
);

const useAxios = makeUseAxios({
  axios: instance,
});

export default useAxios;
