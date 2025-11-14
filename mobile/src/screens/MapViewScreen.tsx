/**
 * Экран карты с проектами
 */
import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Alert } from 'react-native';
import { ProjectMap } from '../components/maps/ProjectMap';
import { colors } from '../theme/colors';
import { spacing } from '../theme/spacing';
import { typography } from '../theme/typography';
import { apiService } from '../services/apiService';

interface Project {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
  status: string;
  completion_percentage?: number;
}

export const MapViewScreen: React.FC = ({ navigation }: any) => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState<'map' | 'satellite'>('map');

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      const response = await apiService.get('/api/v1/projects');
      const projectsData = response.data;

      // Фильтруем только проекты с координатами
      const projectsWithLocation = projectsData.filter(
        (p: any) => p.latitude && p.longitude
      );

      setProjects(
        projectsWithLocation.map((p: any) => ({
          id: p.id,
          name: p.name,
          latitude: p.latitude,
          longitude: p.longitude,
          status: p.status,
          completion_percentage: p.completion_percentage,
        }))
      );
    } catch (error) {
      console.error('Failed to load projects:', error);
      Alert.alert('Ошибка', 'Не удалось загрузить проекты');
    } finally {
      setLoading(false);
    }
  };

  const handleProjectPress = (projectId: number) => {
    navigation.navigate('ProjectDetail', { projectId });
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <Text style={styles.loadingText}>Загрузка карты...</Text>
      </View>
    );
  }

  if (projects.length === 0) {
    return (
      <View style={styles.emptyContainer}>
        <Text style={styles.emptyText}>Нет проектов с геолокацией</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <ProjectMap
        projects={projects}
        onProjectPress={handleProjectPress}
        showUserLocation={true}
        height={StyleSheet.absoluteFillObject.height || 600}
      />

      {/* Счетчик проектов */}
      <View style={styles.counter}>
        <Text style={styles.counterText}>
          {projects.length} {projects.length === 1 ? 'проект' : 'проектов'}
        </Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.neutral[100],
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: colors.neutral[100],
  },
  loadingText: {
    fontSize: typography.fontSize.md,
    color: colors.neutral[600],
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: colors.neutral[100],
  },
  emptyText: {
    fontSize: typography.fontSize.md,
    color: colors.neutral[600],
  },
  counter: {
    position: 'absolute',
    top: spacing.md,
    left: spacing.md,
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    borderRadius: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  counterText: {
    fontSize: typography.fontSize.sm,
    fontWeight: typography.fontWeight.semibold,
    color: colors.neutral[900],
  },
});
