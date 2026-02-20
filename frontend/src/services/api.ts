import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000/api",
  headers: {
    "Content-Type": "application/json",
  },
});

/* ===============================
   Attach JWT Automatically
================================= */
API.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

/* ===============================
   Handle 401 Gracefully
================================= */
API.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      console.warn("Unauthorized. Clearing token.");
      localStorage.removeItem("access_token");
    }
    return Promise.reject(error);
  }
);

/* ===============================
   AUTH APIs
================================= */

export const registerUser = async (
  email: string,
  password: string,
  organization_name: string
) => {
  const response = await API.post("/users/register", {
    email,
    password,
    organization_name,
  });

  return response.data;
};

export const loginUser = async (email: string, password: string) => {
  const formData = new URLSearchParams();
  formData.append("username", email);
  formData.append("password", password);

  const response = await API.post("/users/login", formData, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });

  localStorage.setItem("access_token", response.data.access_token);

  return response.data;
};

export default API;
