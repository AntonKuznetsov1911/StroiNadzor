/**
 * Экран деталей проекта
 */
import React, { useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
} from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { fetchProject } from '../store/slices/projectsSlice';
import { AppDispatch, RootState } from '../store/store';

const ProjectDetailScreen = ({ route, navigation }: any) => {
  const { id } = route.params;
  const dispatch = useDispatch<AppDispatch>();
  const { currentProject, loading } = useSelector(
    (state: RootState) => state.projects
  );

  useEffect(() => {
    dispatch(fetchProject(id));
  }, [id]);

  if (loading || !currentProject) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color="#1E3A8A" />
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>{currentProject.name}</Text>
        <Text style={styles.address}>📍 {currentProject.address}</Text>
        {currentProject.description && (
          <Text style={styles.description}>{currentProject.description}</Text>
        )}
      </View>

      {/* Progress */}
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Прогресс выполнения</Text>
        <View style={styles.progressBar}>
          <View
            style={[
              styles.progressFill,
              { width: `${currentProject.completion_percentage}%` },
            ]}
          />
        </View>
        <Text style={styles.progressText}>
          {currentProject.completion_percentage}% завершено
        </Text>
      </View>

      {/* Quick Actions */}
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Быстрые действия</Text>
        <View style={styles.actionsGrid}>
          <TouchableOpacity
            style={styles.actionButton}
            onPress={() => navigation.navigate('Camera', { projectId: id })}
          >
            <Text style={styles.actionIcon}>📸</Text>
            <Text style={styles.actionText}>Фотофиксация</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.actionButton}
            onPress={() =>
              navigation.navigate('HiddenWorks', { projectId: id })
            }
          >
            <Text style={styles.actionIcon}>📋</Text>
            <Text style={styles.actionText}>Скрытые работы</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.actionButton}>
            <Text style={styles.actionIcon}>✓</Text>
            <Text style={styles.actionText}>Чек-лист</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.actionButton}>
            <Text style={styles.actionIcon}>📄</Text>
            <Text style={styles.actionText}>Документы</Text>
          </TouchableOpacity>
        </View>
      </View>

      {/* Recent Inspections */}
      <View style={styles.card}>
        <View style={styles.cardHeader}>
          <Text style={styles.cardTitle}>Последние проверки</Text>
          <TouchableOpacity>
            <Text style={styles.linkText}>Все →</Text>
          </TouchableOpacity>
        </View>

        <View style={styles.emptyState}>
          <Text style={styles.emptyIcon}>🔍</Text>
          <Text style={styles.emptyText}>Нет проверок</Text>
          <TouchableOpacity
            style={styles.emptyButton}
            onPress={() => navigation.navigate('Camera', { projectId: id })}
          >
            <Text style={styles.emptyButtonText}>Создать проверку</Text>
          </TouchableOpacity>
        </View>
      </View>

      {/* Info */}
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Информация</Text>

        <View style={styles.infoRow}>
          <Text style={styles.infoLabel}>Статус:</Text>
          <Text style={styles.infoValue}>{currentProject.status}</Text>
        </View>

        <View style={styles.infoRow}>
          <Text style={styles.infoLabel}>Тип:</Text>
          <Text style={styles.infoValue}>{currentProject.project_type}</Text>
        </View>

        {currentProject.start_date && (
          <View style={styles.infoRow}>
            <Text style={styles.infoLabel}>Дата начала:</Text>
            <Text style={styles.infoValue}>
              {new Date(currentProject.start_date).toLocaleDateString('ru-RU')}
            </Text>
          </View>
        )}

        {currentProject.planned_end_date && (
          <View style={styles.infoRow}>
            <Text style={styles.infoLabel}>Планируемое завершение:</Text>
            <Text style={styles.infoValue}>
              {new Date(currentProject.planned_end_date).toLocaleDateString(
                'ru-RU'
              )}
            </Text>
          </View>
        )}
      </View>
    </ScrollView>
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
  header: {
    backgroundColor: '#fff',
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#E5E7EB',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#1F2937',
    marginBottom: 8,
  },
  address: {
    fontSize: 16,
    color: '#6B7280',
    marginBottom: 12,
  },
  description: {
    fontSize: 14,
    color: '#4B5563',
    lineHeight: 20,
  },
  card: {
    backgroundColor: '#fff',
    margin: 16,
    padding: 16,
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#1F2937',
    marginBottom: 16,
  },
  progressBar: {
    height: 12,
    backgroundColor: '#E5E7EB',
    borderRadius: 6,
    overflow: 'hidden',
    marginBottom: 8,
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#10B981',
  },
  progressText: {
    fontSize: 14,
    color: '#6B7280',
    textAlign: 'right',
  },
  actionsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginHorizontal: -8,
  },
  actionButton: {
    width: '48%',
    margin: '1%',
    padding: 16,
    backgroundColor: '#F3F4F6',
    borderRadius: 12,
    alignItems: 'center',
  },
  actionIcon: {
    fontSize: 32,
    marginBottom: 8,
  },
  actionText: {
    fontSize: 14,
    color: '#1F2937',
    fontWeight: '500',
  },
  linkText: {
    color: '#1E3A8A',
    fontSize: 14,
    fontWeight: '600',
  },
  emptyState: {
    alignItems: 'center',
    paddingVertical: 32,
  },
  emptyIcon: {
    fontSize: 48,
    marginBottom: 12,
  },
  emptyText: {
    fontSize: 16,
    color: '#6B7280',
    marginBottom: 16,
  },
  emptyButton: {
    backgroundColor: '#1E3A8A',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 8,
  },
  emptyButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#F3F4F6',
  },
  infoLabel: {
    fontSize: 14,
    color: '#6B7280',
  },
  infoValue: {
    fontSize: 14,
    color: '#1F2937',
    fontWeight: '500',
  },
});

export default ProjectDetailScreen;
