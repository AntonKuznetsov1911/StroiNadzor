/**
 * WatermelonDB Schema для офлайн-режима
 */
import { appSchema, tableSchema } from '@nozbe/watermelondb';

export const schema = appSchema({
  version: 1,
  tables: [
    // Проекты
    tableSchema({
      name: 'projects',
      columns: [
        { name: 'server_id', type: 'number', isOptional: true },
        { name: 'name', type: 'string' },
        { name: 'description', type: 'string', isOptional: true },
        { name: 'project_type', type: 'string' },
        { name: 'status', type: 'string' },
        { name: 'start_date', type: 'number' },
        { name: 'end_date', type: 'number', isOptional: true },
        { name: 'address', type: 'string' },
        { name: 'latitude', type: 'number', isOptional: true },
        { name: 'longitude', type: 'number', isOptional: true },
        { name: 'client_name', type: 'string', isOptional: true },
        { name: 'budget', type: 'number', isOptional: true },
        { name: 'created_at', type: 'number' },
        { name: 'updated_at', type: 'number' },
        { name: 'synced_at', type: 'number', isOptional: true },
        { name: 'is_dirty', type: 'boolean' },
      ],
    }),

    // Проверки
    tableSchema({
      name: 'inspections',
      columns: [
        { name: 'server_id', type: 'number', isOptional: true },
        { name: 'project_id', type: 'string', isIndexed: true },
        { name: 'inspection_date', type: 'number' },
        { name: 'location', type: 'string' },
        { name: 'result', type: 'string' },
        { name: 'notes', type: 'string', isOptional: true },
        { name: 'latitude', type: 'number', isOptional: true },
        { name: 'longitude', type: 'number', isOptional: true },
        { name: 'inspector_id', type: 'number' },
        { name: 'created_at', type: 'number' },
        { name: 'updated_at', type: 'number' },
        { name: 'synced_at', type: 'number', isOptional: true },
        { name: 'is_dirty', type: 'boolean' },
      ],
    }),

    // Фотографии проверок
    tableSchema({
      name: 'inspection_photos',
      columns: [
        { name: 'server_id', type: 'number', isOptional: true },
        { name: 'inspection_id', type: 'string', isIndexed: true },
        { name: 'file_path', type: 'string' },
        { name: 'local_uri', type: 'string', isOptional: true },
        { name: 'latitude', type: 'number', isOptional: true },
        { name: 'longitude', type: 'number', isOptional: true },
        { name: 'altitude', type: 'number', isOptional: true },
        { name: 'accuracy', type: 'number', isOptional: true },
        { name: 'timestamp', type: 'number' },
        { name: 'has_defects', type: 'boolean' },
        { name: 'analyzed', type: 'boolean' },
        { name: 'created_at', type: 'number' },
        { name: 'updated_at', type: 'number' },
        { name: 'synced_at', type: 'number', isOptional: true },
        { name: 'is_dirty', type: 'boolean' },
      ],
    }),

    // Дефекты на фотографиях
    tableSchema({
      name: 'defect_detections',
      columns: [
        { name: 'server_id', type: 'number', isOptional: true },
        { name: 'photo_id', type: 'string', isIndexed: true },
        { name: 'defect_type', type: 'string' },
        { name: 'severity', type: 'string' },
        { name: 'confidence', type: 'number' },
        { name: 'bbox_x', type: 'number', isOptional: true },
        { name: 'bbox_y', type: 'number', isOptional: true },
        { name: 'bbox_width', type: 'number', isOptional: true },
        { name: 'bbox_height', type: 'number', isOptional: true },
        { name: 'description', type: 'string', isOptional: true },
        { name: 'detected_at', type: 'number' },
        { name: 'created_at', type: 'number' },
        { name: 'updated_at', type: 'number' },
        { name: 'synced_at', type: 'number', isOptional: true },
        { name: 'is_dirty', type: 'boolean' },
      ],
    }),

    // Скрытые работы
    tableSchema({
      name: 'hidden_works',
      columns: [
        { name: 'server_id', type: 'number', isOptional: true },
        { name: 'project_id', type: 'string', isIndexed: true },
        { name: 'work_type', type: 'string' },
        { name: 'description', type: 'string' },
        { name: 'location', type: 'string' },
        { name: 'status', type: 'string' },
        { name: 'scheduled_date', type: 'number' },
        { name: 'completed_date', type: 'number', isOptional: true },
        { name: 'notes', type: 'string', isOptional: true },
        { name: 'created_at', type: 'number' },
        { name: 'updated_at', type: 'number' },
        { name: 'synced_at', type: 'number', isOptional: true },
        { name: 'is_dirty', type: 'boolean' },
      ],
    }),

    // Документы
    tableSchema({
      name: 'documents',
      columns: [
        { name: 'server_id', type: 'number', isOptional: true },
        { name: 'project_id', type: 'string', isIndexed: true },
        { name: 'title', type: 'string' },
        { name: 'description', type: 'string', isOptional: true },
        { name: 'document_type', type: 'string' },
        { name: 'file_path', type: 'string' },
        { name: 'local_uri', type: 'string', isOptional: true },
        { name: 'file_size', type: 'number' },
        { name: 'mime_type', type: 'string' },
        { name: 'uploaded_at', type: 'number' },
        { name: 'created_at', type: 'number' },
        { name: 'updated_at', type: 'number' },
        { name: 'synced_at', type: 'number', isOptional: true },
        { name: 'is_dirty', type: 'boolean' },
      ],
    }),

    // Очередь синхронизации
    tableSchema({
      name: 'sync_queue',
      columns: [
        { name: 'entity_type', type: 'string' },
        { name: 'entity_id', type: 'string' },
        { name: 'action', type: 'string' }, // 'create', 'update', 'delete'
        { name: 'payload', type: 'string' }, // JSON
        { name: 'priority', type: 'number' },
        { name: 'retry_count', type: 'number' },
        { name: 'last_error', type: 'string', isOptional: true },
        { name: 'created_at', type: 'number' },
      ],
    }),
  ],
});
