import { create } from "zustand";
import apiClient from "../services/api";

const useAuthStore = create((set, get) => ({
  user: null,
  isAuthenticated: false,
  error: null,
  loading: false,
  isLoading: true,
  token: localStorage.getItem("token") || null,

  login: async (email, password) => {
    set({ loading: true, error: null });
    try {
      const params = new URLSearchParams();
      params.append("username", email);
      params.append("password", password);

      const response = await apiClient.post("/login", params, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      });

      const { access_token } = response.data;
      localStorage.setItem("token", access_token);
      set({ token: access_token });

      const userResponse = await apiClient.get("/users/me");
      set({
        user: userResponse.data,
        isAuthenticated: true,
        loading: false,
      });
      return true;
    } catch (err) {
      const errorMessage =
        err.response?.data?.detail ||
        "Ocorreu um erro ao tentar fazer o login.";
      set({
        error: errorMessage,
        loading: false,
        isAuthenticated: false,
        user: null,
        token: null,
      });
      localStorage.removeItem("token");
      return false;
    }
  },

  logout: () => {
    localStorage.removeItem("token");
    set({ user: null, isAuthenticated: false, token: null });
  },

  checkAuth: async () => {
    set({ isLoading: true });
    const token = get().token;
    if (token) {
      try {
        const response = await apiClient.get("/users/me");
        set({ user: response.data, isAuthenticated: true, isLoading: false });
      } catch (error) {
        set({
          user: null,
          isAuthenticated: false,
          isLoading: false,
          token: null,
        });
        localStorage.removeItem("token");
      }
    } else {
      set({ isLoading: false });
    }
  },
}));

export default useAuthStore;
