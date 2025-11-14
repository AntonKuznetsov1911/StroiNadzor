/**
 * TypeScript типы для приложения
 */

// Пользователь
export interface User {
  id: number;
  email: string;
  full_name: string;
  role: UserRole;
  phone?: string;
  organization?: string;
  position?: string;
  created_at: string;
  is_active: boolean;
}

export type UserRole = 'admin' | 'engineer' | 'supervisor' | 'contractor' | 'viewer';

// Аутентификация
export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  full_name: string;
  role: UserRole;
  phone?: string;
  organization?: string;
  position?: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

// Проект
export interface Project {
  id: number;
  name: string;
  description?: string;
  project_type: ProjectType;
  status: ProjectStatus;
  start_date: string;
  end_date?: string;
  address: string;
  latitude?: number;
  longitude?: number;
  client_name?: string;
  client_contact?: string;
  budget?: number;
  created_at: string;
  updated_at: string;
  created_by_id: number;
  created_by?: User;
}

export type ProjectType =
  | 'residential'
  | 'commercial'
  | 'industrial'
  | 'infrastructure'
  | 'renovation';

export type ProjectStatus =
  | 'planning'
  | 'in_progress'
  | 'on_hold'
  | 'completed'
  | 'archived';

// Проверка (Осмотр)
export interface Inspection {
  id: number;
  project_id: number;
  project?: Project;
  inspection_date: string;
  location: string;
  latitude?: number;
  longitude?: number;
  result: InspectionResult;
  notes?: string;
  inspector_id: number;
  inspector?: User;
  photos?: InspectionPhoto[];
  defects?: DefectDetection[];
  created_at: string;
  updated_at: string;
}

export type InspectionResult = 'passed' | 'failed' | 'with_remarks' | 'pending';

// Фото проверки
export interface InspectionPhoto {
  id: number;
  inspection_id: number;
  photo_url: string;
  thumbnail_url?: string;
  latitude?: number;
  longitude?: number;
  taken_at: string;
  description?: string;
  has_defects: boolean;
  uploaded_at: string;
}

// Обнаружение дефекта
export interface DefectDetection {
  id: number;
  photo_id: number;
  photo?: InspectionPhoto;
  defect_type: DefectType;
  severity: DefectSeverity;
  confidence_score: number;
  bbox_x: number;
  bbox_y: number;
  bbox_width: number;
  bbox_height: number;
  description?: string;
  recommendation?: string;
  detected_at: string;
}

export type DefectType =
  | 'crack'
  | 'deviation'
  | 'reinforcement'
  | 'welding'
  | 'waterproofing'
  | 'concrete_quality'
  | 'other';

export type DefectSeverity = 'critical' | 'major' | 'minor' | 'cosmetic';

// Скрытые работы
export interface HiddenWork {
  id: number;
  project_id: number;
  project?: Project;
  work_type: string;
  description: string;
  location: string;
  status: HiddenWorkStatus;
  scheduled_date: string;
  completed_date?: string;
  contractor_id?: number;
  contractor?: User;
  supervisor_id?: number;
  supervisor?: User;
  photos?: string[];
  notes?: string;
  created_at: string;
  updated_at: string;
}

export type HiddenWorkStatus =
  | 'pending'
  | 'approved'
  | 'rejected'
  | 'revision_required';

// Акт освидетельствования скрытых работ
export interface HiddenWorkAct {
  id: number;
  hidden_work_id: number;
  hidden_work?: HiddenWork;
  act_number: string;
  act_date: string;
  result: string;
  notes?: string;
  signed_by_contractor?: boolean;
  signed_by_supervisor?: boolean;
  contractor_signature?: string;
  supervisor_signature?: string;
  pdf_url?: string;
  created_at: string;
}

// Чек-лист
export interface ChecklistTemplate {
  id: number;
  name: string;
  description?: string;
  work_type: string;
  items: ChecklistTemplateItem[];
  created_at: string;
}

export interface ChecklistTemplateItem {
  id: number;
  template_id: number;
  item_text: string;
  order_index: number;
  is_required: boolean;
}

export interface Checklist {
  id: number;
  inspection_id: number;
  template_id: number;
  template?: ChecklistTemplate;
  items: ChecklistItem[];
  completed_at?: string;
}

export interface ChecklistItem {
  id: number;
  checklist_id: number;
  template_item_id: number;
  is_checked: boolean;
  notes?: string;
}

// Документ
export interface Document {
  id: number;
  project_id: number;
  project?: Project;
  document_type: DocumentType;
  title: string;
  description?: string;
  file_url: string;
  file_size?: number;
  uploaded_by_id: number;
  uploaded_by?: User;
  uploaded_at: string;
}

export type DocumentType =
  | 'act'
  | 'report'
  | 'prescription'
  | 'protocol'
  | 'certificate'
  | 'drawing'
  | 'other';

// Материал
export interface Material {
  id: number;
  project_id: number;
  name: string;
  manufacturer?: string;
  quantity: number;
  unit: string;
  delivery_date?: string;
  notes?: string;
  certificates?: MaterialCertificate[];
}

export interface MaterialCertificate {
  id: number;
  material_id: number;
  certificate_number: string;
  issue_date: string;
  valid_until?: string;
  file_url: string;
}

// Нормативный документ (СП, ГОСТ)
export interface Regulation {
  id: number;
  code: string;
  title: string;
  category: string;
  content: string;
  effective_date?: string;
  source_url?: string;
  created_at: string;
}

// AI Консультант
export interface AIConsultRequest {
  question: string;
  context?: string;
  project_id?: number;
}

export interface AIConsultResponse {
  answer: string;
  relevant_regulations: Regulation[];
  confidence: number;
}

// Статистика
export interface ProjectStatistics {
  total_inspections: number;
  passed_inspections: number;
  failed_inspections: number;
  total_defects: number;
  critical_defects: number;
  pending_hidden_works: number;
  completion_percentage: number;
}

// Пагинация
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

// API ошибка
export interface ApiError {
  message: string;
  status_code: number;
  errors?: Record<string, string[]>;
}

// Загрузка файла
export interface UploadProgress {
  loaded: number;
  total: number;
  percentage: number;
}

// Фильтры
export interface ProjectFilters {
  status?: ProjectStatus;
  project_type?: ProjectType;
  search?: string;
}

export interface InspectionFilters {
  project_id?: number;
  result?: InspectionResult;
  date_from?: string;
  date_to?: string;
}

// Настройки приложения
export interface AppSettings {
  theme: 'light' | 'dark' | 'auto';
  language: 'ru' | 'en';
  notifications_enabled: boolean;
  auto_sync: boolean;
  photo_quality: number;
  offline_mode: boolean;
}

// Навигация
export type RootStackParamList = {
  Login: undefined;
  Register: undefined;
  ForgotPassword: undefined;
  Home: undefined;
  Projects: undefined;
  ProjectDetail: { projectId: number };
  Inspections: undefined;
  InspectionDetail: { inspectionId: number };
  HiddenWorks: { projectId: number };
  HiddenWorkDetail: { hiddenWorkId: number };
  Camera: { inspectionId: number };
  PhotoPreview: { uri: string; inspectionId: number };
  AIConsultant: undefined;
  Profile: undefined;
  Settings: undefined;
  Notifications: undefined;
};

// Redux State
export interface RootState {
  auth: AuthState;
  projects: ProjectsState;
  inspections: InspectionsState;
  ui: UIState;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;
}

export interface ProjectsState {
  projects: Project[];
  currentProject: Project | null;
  loading: boolean;
  error: string | null;
  filters: ProjectFilters;
  pagination: {
    page: number;
    pageSize: number;
    total: number;
  };
}

export interface InspectionsState {
  inspections: Inspection[];
  currentInspection: Inspection | null;
  loading: boolean;
  error: string | null;
}

export interface UIState {
  isOnline: boolean;
  syncInProgress: boolean;
  lastSyncTime: string | null;
  settings: AppSettings;
}
