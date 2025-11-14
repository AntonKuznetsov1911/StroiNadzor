/**
 * WatermelonDB модель: Project
 */
import { Model } from '@nozbe/watermelondb';
import { field, date, readonly, children } from '@nozbe/watermelondb/decorators';

export class Project extends Model {
  static table = 'projects';
  static associations = {
    inspections: { type: 'has_many', foreignKey: 'project_id' },
    hidden_works: { type: 'has_many', foreignKey: 'project_id' },
    documents: { type: 'has_many', foreignKey: 'project_id' },
  } as const;

  @field('server_id') serverId!: number | null;
  @field('name') name!: string;
  @field('description') description!: string | null;
  @field('project_type') projectType!: string;
  @field('status') status!: string;
  @date('start_date') startDate!: Date;
  @date('end_date') endDate!: Date | null;
  @field('address') address!: string;
  @field('latitude') latitude!: number | null;
  @field('longitude') longitude!: number | null;
  @field('client_name') clientName!: string | null;
  @field('budget') budget!: number | null;
  @readonly @date('created_at') createdAt!: Date;
  @readonly @date('updated_at') updatedAt!: Date;
  @date('synced_at') syncedAt!: Date | null;
  @field('is_dirty') isDirty!: boolean;

  @children('inspections') inspections: any;
  @children('hidden_works') hiddenWorks: any;
  @children('documents') documents: any;
}
