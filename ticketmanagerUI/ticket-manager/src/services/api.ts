import axios from "axios";
import type {
  UserLogin,
  UserCreate,
  AuthResponse,
  TicketResponse,
} from "../types";

const API_BASE_URL = "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Request interceptor to add token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authService = {
  login: async (credentials: UserLogin): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>("/auth/login", credentials);
    return response.data;
  },
  register: async (userData: UserCreate): Promise<{ msg: string }> => {
    const response = await api.post("/auth/register", userData);
    return response.data;
  },
  getCurrentUser: async () => {
    const response = await api.get("/auth/me");
    return response.data;
  },
};

export const ticketService = {
  getMyTickets: async (): Promise<TicketResponse[]> => {
    const response = await api.get("/tickets/my-tickets");
    return response.data;
  },
  getUnassignedTickets: async (): Promise<TicketResponse[]> => {
    const response = await api.get("/tickets/unassigned");
    return response.data;
  },
  getMyTasks: async (): Promise<TicketResponse[]> => {
    const response = await api.get("/tickets/my-tasks");
    return response.data;
  },
  createTicket: async (ticket: any): Promise<TicketResponse> => {
    const response = await api.post("/tickets/", ticket);
    return response.data;
  },
  assignToMe: async (ticketId: string): Promise<TicketResponse> => {
    const response = await api.put(`/tickets/${ticketId}/assign-to-me`);
    return response.data;
  },
  updateTicket: async (
    ticketId: string,
    data: any,
  ): Promise<TicketResponse> => {
    const response = await api.put(`/tickets/${ticketId}`, data);
    return response.data;
  },
};

export default api;
