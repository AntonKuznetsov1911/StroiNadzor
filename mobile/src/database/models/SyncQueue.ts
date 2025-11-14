/**
 * WatermelonDB модель: SyncQueue
 */
import { Model } from '@nozbe/watermelondb';
import { field, date, readonly } from '@nozbe/watermelondb/decorators';

export class SyncQueue extends Model {
  static table = 'sync_queue';

  @field('entity_type') entityType!: string;
  @field('entity_id') entityId!: string;
  @field('action') action!: 'create' | 'update' | 'delete';
  @field('payload') payload!: string; // JSON string
  @field('priority') priority!: number;
  @field('retry_count') retryCount!: number;
  @field('last_error') lastError!: string | null;
  @readonly @date('created_at') createdAt!: Date;

  // Вспомогательные методы
  getPayload<T>(): T {
    return JSON.parse(this.payload) as T;
  }

  async incrementRetry(error: string) {
    await this.update((record: any) => {
      record.retryCount += 1;
      record.lastError = error;
    });
  }
}
