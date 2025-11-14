/**
 * WatermelonDB модель: HiddenWork
 */
import { Model } from '@nozbe/watermelondb';
import { field, date, readonly, relation } from '@nozbe/watermelondb/decorators';

export class HiddenWork extends Model {
  static table = 'hidden_works';
  static associations = {
    projects: { type: 'belongs_to', key: 'project_id' },
  } as const;

  @field('server_id') serverId!: number | null;
  @field('project_id') projectId!: string;
  @field('work_type') workType!: string;
  @field('description') description!: string;
  @field('location') location!: string;
  @field('status') status!: string;
  @date('scheduled_date') scheduledDate!: Date;
  @date('completed_date') completedDate!: Date | null;
  @field('notes') notes!: string | null;
  @readonly @date('created_at') createdAt!: Date;
  @readonly @date('updated_at') updatedAt!: Date;
  @date('synced_at') syncedAt!: Date | null;
  @field('is_dirty') isDirty!: boolean;

  @relation('projects', 'project_id') project: any;
}
