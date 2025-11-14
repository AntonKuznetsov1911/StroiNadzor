/**
 * WatermelonDB модель: Document
 */
import { Model } from '@nozbe/watermelondb';
import { field, date, readonly, relation } from '@nozbe/watermelondb/decorators';

export class Document extends Model {
  static table = 'documents';
  static associations = {
    projects: { type: 'belongs_to', key: 'project_id' },
  } as const;

  @field('server_id') serverId!: number | null;
  @field('project_id') projectId!: string;
  @field('title') title!: string;
  @field('description') description!: string | null;
  @field('document_type') documentType!: string;
  @field('file_path') filePath!: string;
  @field('local_uri') localUri!: string | null;
  @field('file_size') fileSize!: number;
  @field('mime_type') mimeType!: string;
  @date('uploaded_at') uploadedAt!: Date;
  @readonly @date('created_at') createdAt!: Date;
  @readonly @date('updated_at') updatedAt!: Date;
  @date('synced_at') syncedAt!: Date | null;
  @field('is_dirty') isDirty!: boolean;

  @relation('projects', 'project_id') project: any;
}
