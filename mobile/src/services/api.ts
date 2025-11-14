/**
 * API Service
 * Централизованный сервис для работы с API
 */
import axios, { AxiosInstance, AxiosError } from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { API_BASE_URL } from '../config/api';

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    // Request interceptor - добавление токена
    this.api.interceptors.request.use(
      async (config) => {
        const token = await AsyncStorage.getItem('auth_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor - обработка ошибок
    this.api.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        if (error.response?.status === 401) {
          // Токен истек - выход из системы
          await AsyncStorage.removeItem('auth_token');
          // TODO: Редирект на экран логина
        }
        return Promise.reject(error);
      }
    );
  }

  // Auth
  async login(email: string, password: string) {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    const response = await this.api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    const { access_token, user } = response.data;
    await AsyncStorage.setItem('auth_token', access_token);

    return { token: access_token, user };
  }

  async register(userData: any) {
    const response = await this.api.post('/auth/register', userData);
    return response.data;
  }

  async getCurrentUser() {
    const response = await this.api.get('/auth/me');
    return response.data;
  }

  // Projects
  async getProjects(params?: { skip?: number; limit?: number }) {
    const response = await this.api.get('/projects', { params });
    return response.data;
  }

  async getProject(id: number) {
    const response = await this.api.get(`/projects/${id}`);
    return response.data;
  }

  async createProject(projectData: any) {
    const response = await this.api.post('/projects', projectData);
    return response.data;
  }

  // Inspections
  async getInspections(params?: any) {
    const response = await this.api.get('/inspections', { params });
    return response.data;
  }

  async getInspection(id: number) {
    const response = await this.api.get(`/inspections/${id}`);
    return response.data;
  }

  async createInspection(inspectionData: any) {
    const response = await this.api.post('/inspections', inspectionData);
    return response.data;
  }

  async uploadInspectionPhoto(inspectionId: number, photoData: FormData) {
    const response = await this.api.post(
      `/inspections/${inspectionId}/photos`,
      photoData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    return response.data;
  }

  // Hidden Works
  async getHiddenWorks(params?: { project_id?: number; status?: string }) {
    const response = await this.api.get('/hidden-works', { params });
    return response.data;
  }

  async createHiddenWork(workData: any) {
    const response = await this.api.post('/hidden-works', workData);
    return response.data;
  }

  async createHiddenWorkAct(workId: number, actData: any) {
    const response = await this.api.post(`/hidden-works/${workId}/acts`, actData);
    return response.data;
  }

  // Regulations & AI Consultant
  async getRegulations(params?: { search?: string; regulation_type?: string }) {
    const response = await this.api.get('/regulations', { params });
    return response.data;
  }

  async aiConsult(question: string, context?: string) {
    const response = await this.api.post('/regulations/ai-consult', {
      question,
      context,
    });
    return response.data;
  }
}

export default new ApiService();
