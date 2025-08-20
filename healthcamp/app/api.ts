import axios from 'axios';

const API = axios.create({
  baseURL: process.env.EXPO_PUBLIC_API_BASE_URL,
  timeout: 15000,
});

// Attach Authorization header from public env (dev convenience)
API.interceptors.request.use((config) => {
  const token = process.env.EXPO_PUBLIC_AUTH_TOKEN;
  if (token) {
    config.headers = config.headers ?? {};
    (config.headers as any).Authorization = `Bearer ${token}`;
  }
  return config;
});

API.interceptors.response.use(
  (resp) => resp,
  (err) => {
    // Helpful debug log when "Network Error" happens
    const cfg = err?.config ?? {};
    console.log('API error', {
      message: err?.message,
      baseURL: cfg.baseURL,
      url: cfg.url,
      method: cfg.method,
      status: err?.response?.status,
      data: err?.response?.data,
    });
    return Promise.reject(err);
  }
);

export default API;
