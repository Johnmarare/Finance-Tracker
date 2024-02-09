import axios from 'axios';

const BASE_API_URL = process.env.REACT_APP_BASE_API_URL;

const instance = axios.create({
  baseURL: BASE_API_URL + '/api',
});

export default class FedhaApiClient {
  async request(options) {
    try {
      const response = await instance(options);
      return {
        ok: true,
        status: response.status,
        body: response.data,
      };
    } catch (error) {
      return {
        ok: false,
        status: error.response?.status || 500,
        body: {
          code: error.response?.status || 500,
          message: "Error in API request",
          description: error.message,
        },
      };
    }
  }

  async get(url, params) {
    const options = {
      method: "GET",
      url,
      params,
    };
    return this.request(options);
  }

  async post(url, data) {
    const options = {
      method: "POST",
      url,
      data,
    };
    return this.request(options);
  }

  async put(url, data) {
    const options = {
      method: "PUT",
      url,
      data,
    };
    return this.request(options);
  }

  async delete(url) {
    const options = {
      method: "DELETE",
      url,
    };
    return this.request(options);
  }
}
