/**
 * WatermelonDB модель: InspectionPhoto
 */
import { Model } from '@nozbe/watermelondb';
import { field, date, readonly, relation, children } from '@nozbe/watermelondb/decorators';

export class InspectionPhoto extends Model {
  static table = 'inspection_photos';
  static associations = {
    inspections: { type: 'belongs_to', key: 'inspection_id' },
    defect_detections: { type: 'has_many', foreignKey: 'photo_id' },
  } as const;

  @field('server_id') serverId!: number | null;
  @field('inspection_id') inspectionId!: string;
  @field('file_path') filePath!: string;
  @field('local_uri') localUri!: string | null;
  @field('latitude') latitude!: number | null;
  @field('longitude') longitude!: number | null;
  @field('altitude') altitude!: number | null;
  @field('accuracy') accuracy!: number | null;
  @date('timestamp') timestamp!: Date;
  @field('has_defects') hasDefects!: boolean;
  @field('analyzed') analyzed!: boolean;
  @readonly @date('created_at') createdAt!: Date;
  @readonly @date('updated_at') updatedAt!: Date;
  @date('synced_at') syncedAt!: Date | null;
  @field('is_dirty') isDirty!: boolean;

  @relation('inspections', 'inspection_id') inspection: any;
  @children('defect_detections') defects: any;
}
