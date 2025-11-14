/**
 * Экран скрытых работ (Модуль 2 MVP)
 */
import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  FlatList,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
} from 'react-native';
import apiService from '../services/api';

interface HiddenWork {
  id: number;
  title: string;
  description?: string;
  work_type: string;
  status: string;
  floor_level?: string;
  section?: string;
  planned_inspection_date?: string;
}

const HiddenWorksScreen = ({ route }: any) => {
  const { projectId } = route.params || {};
  const [works, setWorks] = useState<HiddenWork[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadHiddenWorks();
  }, []);

  const loadHiddenWorks = async () => {
    try {
      setLoading(true);
      const data = await apiService.getHiddenWorks({ project_id: projectId });
      setWorks(data);
    } catch (error) {
      console.error('Failed to load hidden works:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    const colors: any = {
      pending: '#EAB308',
      in_review: '#F97316',
      approved: '#10B981',
      rejected: '#EF4444',
      closed: '#6B7280',
    };
    return colors[status] || '#6B7280';
  };

  const getStatusText = (status: string) => {
    const texts: any = {
      pending: 'Ожидает',
      in_review: 'На проверке',
      approved: 'Одобрено',
      rejected: 'Отклонено',
      closed: 'Закрыто',
    };
    return texts[status] || status;
  };

  const getWorkTypeText = (type: string) => {
    const types: any = {
      foundation: 'Фундамент',
      reinforcement: 'Армирование',
      waterproofing: 'Гидроизоляция',
      utilities: 'Коммуникации',
      electrical: 'Электрика',
      ventilation: 'Вентиляция',
      other: 'Другое',
    };
    return types[type] || type;
  };

  const renderWork = ({ item }: { item: HiddenWork }) => (
    <TouchableOpacity style={styles.workCard}>
      <View style={styles.workHeader}>
        <Text style={styles.workTitle} numberOfLines={2}>
          {item.title}
        </Text>
        <View
          style={[
            styles.statusBadge,
            { backgroundColor: getStatusColor(item.status) },
          ]}
        >
          <Text style={styles.statusText}>{getStatusText(item.status)}</Text>
        </View>
      </View>

      <Text style={styles.workType}>📂 {getWorkTypeText(item.work_type)}</Text>

      {item.description && (
        <Text style={styles.workDescription} numberOfLines={2}>
          {item.description}
        </Text>
      )}

      <View style={styles.workDetails}>
        {item.floor_level && (
          <Text style={styles.detailText}>🏢 Этаж: {item.floor_level}</Text>
        )}
        {item.section && (
          <Text style={styles.detailText}>📍 Секция: {item.section}</Text>
        )}
        {item.planned_inspection_date && (
          <Text style={styles.detailText}>
            📅 Проверка:{' '}
            {new Date(item.planned_inspection_date).toLocaleDateString('ru-RU')}
          </Text>
        )}
      </View>

      {item.status === 'pending' && (
        <TouchableOpacity style={styles.actButton}>
          <Text style={styles.actButtonText}>Создать акт</Text>
        </TouchableOpacity>
      )}
    </TouchableOpacity>
  );

  if (loading) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color="#1E3A8A" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <FlatList
        data={works}
        renderItem={renderWork}
        keyExtractor={(item) => item.id.toString()}
        contentContainerStyle={styles.listContent}
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Text style={styles.emptyIcon}>📋</Text>
            <Text style={styles.emptyText}>Нет скрытых работ</Text>
            <Text style={styles.emptySubtext}>
              Создайте запись о скрытых работах для контроля
            </Text>
          </View>
        }
      />

      <TouchableOpacity style={styles.fab}>
        <Text style={styles.fabIcon}>+</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F9FAFB',
  },
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  listContent: {
    padding: 16,
  },
  workCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  workHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 8,
  },
  workTitle: {
    flex: 1,
    fontSize: 16,
    fontWeight: '600',
    color: '#1F2937',
    marginRight: 8,
  },
  statusBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
  },
  statusText: {
    color: '#fff',
    fontSize: 11,
    fontWeight: '600',
  },
  workType: {
    fontSize: 14,
    color: '#6B7280',
    marginBottom: 8,
  },
  workDescription: {
    fontSize: 14,
    color: '#4B5563',
    marginBottom: 12,
  },
  workDetails: {
    marginTop: 8,
  },
  detailText: {
    fontSize: 12,
    color: '#6B7280',
    marginBottom: 4,
  },
  actButton: {
    backgroundColor: '#1E3A8A',
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 12,
  },
  actButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
  },
  emptyContainer: {
    alignItems: 'center',
    paddingTop: 60,
  },
  emptyIcon: {
    fontSize: 64,
    marginBottom: 16,
  },
  emptyText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#1F2937',
    marginBottom: 8,
  },
  emptySubtext: {
    fontSize: 14,
    color: '#6B7280',
    textAlign: 'center',
    paddingHorizontal: 40,
  },
  fab: {
    position: 'absolute',
    right: 20,
    bottom: 20,
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: '#1E3A8A',
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 8,
  },
  fabIcon: {
    color: '#fff',
    fontSize: 32,
    fontWeight: '300',
  },
});

export default HiddenWorksScreen;
