import axios from "axios";

const API_BASE = "http://localhost:8000/api";  // update if needed

const client = axios.create({
    baseURL: API_BASE,
    headers: {
        "Content-Type": "application/json",
    },
});

client.interceptors.request.use((config) => {
    const token = localStorage.getItem("token");
    if (token) {
        config.headers["Authorization"] = `Token ${token}`;
    }
    return config;
});

export default client;
