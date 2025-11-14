/**
 * Projects Slice
 */
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import apiService from '../../services/api';

interface Project {
  id: number;
  name: string;
  description?: string;
  address: string;
  status: string;
  completion_percentage: number;
}

interface ProjectsState {
  projects: Project[];
  currentProject: Project | null;
  loading: boolean;
  error: string | null;
  total: number;
}

const initialState: ProjectsState = {
  projects: [],
  currentProject: null,
  loading: false,
  error: null,
  total: 0,
};

// Async thunks
export const fetchProjects = createAsyncThunk(
  'projects/fetchProjects',
  async (params?: { skip?: number; limit?: number }) => {
    const response = await apiService.getProjects(params);
    return response;
  }
);

export const fetchProject = createAsyncThunk(
  'projects/fetchProject',
  async (id: number) => {
    const response = await apiService.getProject(id);
    return response;
  }
);

export const createProject = createAsyncThunk(
  'projects/createProject',
  async (projectData: any) => {
    const response = await apiService.createProject(projectData);
    return response;
  }
);

const projectsSlice = createSlice({
  name: 'projects',
  initialState,
  reducers: {
    clearCurrentProject: (state) => {
      state.currentProject = null;
    },
  },
  extraReducers: (builder) => {
    // Fetch projects
    builder
      .addCase(fetchProjects.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchProjects.fulfilled, (state, action) => {
        state.loading = false;
        state.projects = action.payload.projects;
        state.total = action.payload.total;
      })
      .addCase(fetchProjects.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch projects';
      });

    // Fetch project
    builder
      .addCase(fetchProject.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchProject.fulfilled, (state, action) => {
        state.loading = false;
        state.currentProject = action.payload;
      })
      .addCase(fetchProject.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch project';
      });

    // Create project
    builder
      .addCase(createProject.fulfilled, (state, action) => {
        state.projects.unshift(action.payload);
        state.total += 1;
      });
  },
});

export const { clearCurrentProject } = projectsSlice.actions;
export default projectsSlice.reducer;
