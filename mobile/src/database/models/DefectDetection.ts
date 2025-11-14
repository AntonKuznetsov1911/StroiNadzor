/**
 * WatermelonDB модель: DefectDetection
 */
import { Model } from '@nozbe/watermelondb';
import { field, date, readonly, relation } from '@nozbe/watermelondb/decorators';

export class DefectDetection extends Model {
  static table = 'defect_detections';
  static associations = {
    inspection_photos: { type: 'belongs_to', key: 'photo_id' },
  } as const;

  @field('server_id') serverId!: number | null;
  @field('photo_id') photoId!: string;
  @field('defect_type') defectType!: string;
  @field('severity') severity!: string;
  @field('confidence') confidence!: number;
  @field('bbox_x') bboxX!: number | null;
  @field('bbox_y') bboxY!: number | null;
  @field('bbox_width') bboxWidth!: number | null;
  @field('bbox_height') bboxHeight!: number | null;
  @field('description') description!: string | null;
  @date('detected_at') detectedAt!: Date;
  @readonly @date('created_at') createdAt!: Date;
  @readonly @date('updated_at') updatedAt!: Date;
  @date('synced_at') syncedAt!: Date | null;
  @field('is_dirty') isDirty!: boolean;

  @relation('inspection_photos', 'photo_id') photo: any;
}
