/**
 * Inspections Slice
 */
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import apiService from '../../services/api';

interface Inspection {
  id: number;
  title: string;
  description?: string;
  status: string;
  project_id: number;
  photos: any[];
}

interface InspectionsState {
  inspections: Inspection[];
  currentInspection: Inspection | null;
  loading: boolean;
  error: string | null;
}

const initialState: InspectionsState = {
  inspections: [],
  currentInspection: null,
  loading: false,
  error: null,
};

// Async thunks
export const fetchInspections = createAsyncThunk(
  'inspections/fetchInspections',
  async (params?: any) => {
    const response = await apiService.getInspections(params);
    return response;
  }
);

export const fetchInspection = createAsyncThunk(
  'inspections/fetchInspection',
  async (id: number) => {
    const response = await apiService.getInspection(id);
    return response;
  }
);

export const createInspection = createAsyncThunk(
  'inspections/createInspection',
  async (inspectionData: any) => {
    const response = await apiService.createInspection(inspectionData);
    return response;
  }
);

const inspectionsSlice = createSlice({
  name: 'inspections',
  initialState,
  reducers: {
    clearCurrentInspection: (state) => {
      state.currentInspection = null;
    },
  },
  extraReducers: (builder) => {
    // Fetch inspections
    builder
      .addCase(fetchInspections.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchInspections.fulfilled, (state, action) => {
        state.loading = false;
        state.inspections = action.payload;
      })
      .addCase(fetchInspections.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch inspections';
      });

    // Fetch inspection
    builder
      .addCase(fetchInspection.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchInspection.fulfilled, (state, action) => {
        state.loading = false;
        state.currentInspection = action.payload;
      })
      .addCase(fetchInspection.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch inspection';
      });

    // Create inspection
    builder.addCase(createInspection.fulfilled, (state, action) => {
      state.inspections.unshift(action.payload);
    });
  },
});

export const { clearCurrentInspection } = inspectionsSlice.actions;
export default inspectionsSlice.reducer;
