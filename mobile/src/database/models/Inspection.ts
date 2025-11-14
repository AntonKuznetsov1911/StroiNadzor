/**
 * WatermelonDB модель: Inspection
 */
import { Model } from '@nozbe/watermelondb';
import { field, date, readonly, relation, children } from '@nozbe/watermelondb/decorators';

export class Inspection extends Model {
  static table = 'inspections';
  static associations = {
    projects: { type: 'belongs_to', key: 'project_id' },
    inspection_photos: { type: 'has_many', foreignKey: 'inspection_id' },
  } as const;

  @field('server_id') serverId!: number | null;
  @field('project_id') projectId!: string;
  @date('inspection_date') inspectionDate!: Date;
  @field('location') location!: string;
  @field('result') result!: string;
  @field('notes') notes!: string | null;
  @field('latitude') latitude!: number | null;
  @field('longitude') longitude!: number | null;
  @field('inspector_id') inspectorId!: number;
  @readonly @date('created_at') createdAt!: Date;
  @readonly @date('updated_at') updatedAt!: Date;
  @date('synced_at') syncedAt!: Date | null;
  @field('is_dirty') isDirty!: boolean;

  @relation('projects', 'project_id') project: any;
  @children('inspection_photos') photos: any;
}
