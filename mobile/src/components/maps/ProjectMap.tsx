/**
 * Компонент карты проектов с маркерами
 */
import React, { useState, useRef } from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import MapView, { Marker, PROVIDER_GOOGLE, Region, Callout } from 'react-native-maps';
import { colors } from '../../theme/colors';
import { spacing } from '../../theme/spacing';
import { typography } from '../../theme/typography';

interface ProjectMarker {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
  status: string;
  completionPercentage?: number;
}

interface ProjectMapProps {
  projects: ProjectMarker[];
  initialRegion?: Region;
  onProjectPress?: (projectId: number) => void;
  showUserLocation?: boolean;
  height?: number;
}

export const ProjectMap: React.FC<ProjectMapProps> = ({
  projects,
  initialRegion,
  onProjectPress,
  showUserLocation = true,
  height = 400,
}) => {
  const mapRef = useRef<MapView>(null);
  const [selectedProject, setSelectedProject] = useState<number | null>(null);

  // Начальный регион по умолчанию (Москва)
  const defaultRegion: Region = {
    latitude: 55.751244,
    longitude: 37.618423,
    latitudeDelta: 0.1,
    longitudeDelta: 0.1,
  };

  const region = initialRegion || defaultRegion;

  // Цвет маркера в зависимости от статуса
  const getMarkerColor = (status: string): string => {
    switch (status) {
      case 'planning':
        return colors.info.main;
      case 'in_progress':
        return colors.warning.main;
      case 'completed':
        return colors.success.main;
      case 'on_hold':
        return colors.neutral[400];
      default:
        return colors.primary.main;
    }
  };

  // Центрировать карту на всех проектах
  const fitToMarkers = () => {
    if (projects.length > 0 && mapRef.current) {
      mapRef.current.fitToSuppliedMarkers(
        projects.map((p) => p.id.toString()),
        {
          edgePadding: {
            top: 50,
            right: 50,
            bottom: 50,
            left: 50,
          },
          animated: true,
        }
      );
    }
  };

  const handleMarkerPress = (projectId: number) => {
    setSelectedProject(projectId);
    if (onProjectPress) {
      onProjectPress(projectId);
    }
  };

  return (
    <View style={[styles.container, { height }]}>
      <MapView
        ref={mapRef}
        provider={PROVIDER_GOOGLE}
        style={styles.map}
        initialRegion={region}
        showsUserLocation={showUserLocation}
        showsMyLocationButton={showUserLocation}
        showsCompass={true}
        showsScale={true}
        toolbarEnabled={false}
      >
        {projects.map((project) => (
          <Marker
            key={project.id}
            identifier={project.id.toString()}
            coordinate={{
              latitude: project.latitude,
              longitude: project.longitude,
            }}
            pinColor={getMarkerColor(project.status)}
            onPress={() => handleMarkerPress(project.id)}
          >
            <Callout onPress={() => handleMarkerPress(project.id)}>
              <View style={styles.callout}>
                <Text style={styles.calloutTitle}>{project.name}</Text>
                <Text style={styles.calloutStatus}>
                  Статус: {project.status}
                </Text>
                {project.completionPercentage !== undefined && (
                  <Text style={styles.calloutProgress}>
                    Прогресс: {project.completionPercentage}%
                  </Text>
                )}
              </View>
            </Callout>
          </Marker>
        ))}
      </MapView>

      {projects.length > 1 && (
        <TouchableOpacity
          style={styles.fitButton}
          onPress={fitToMarkers}
          activeOpacity={0.8}
        >
          <Text style={styles.fitButtonText}>Показать все</Text>
        </TouchableOpacity>
      )}

      {/* Легенда */}
      <View style={styles.legend}>
        <View style={styles.legendItem}>
          <View style={[styles.legendDot, { backgroundColor: colors.info.main }]} />
          <Text style={styles.legendText}>Планирование</Text>
        </View>
        <View style={styles.legendItem}>
          <View style={[styles.legendDot, { backgroundColor: colors.warning.main }]} />
          <Text style={styles.legendText}>В работе</Text>
        </View>
        <View style={styles.legendItem}>
          <View style={[styles.legendDot, { backgroundColor: colors.success.main }]} />
          <Text style={styles.legendText}>Завершено</Text>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    width: '100%',
    borderRadius: 12,
    overflow: 'hidden',
  },
  map: {
    width: '100%',
    height: '100%',
  },
  callout: {
    padding: spacing.sm,
    minWidth: 150,
  },
  calloutTitle: {
    fontSize: typography.fontSize.md,
    fontWeight: typography.fontWeight.semibold,
    color: colors.neutral[900],
    marginBottom: spacing.xs,
  },
  calloutStatus: {
    fontSize: typography.fontSize.sm,
    color: colors.neutral[600],
  },
  calloutProgress: {
    fontSize: typography.fontSize.sm,
    color: colors.primary.main,
    marginTop: spacing.xs,
  },
  fitButton: {
    position: 'absolute',
    top: spacing.md,
    right: spacing.md,
    backgroundColor: colors.neutral[900],
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  fitButtonText: {
    color: colors.neutral[50],
    fontSize: typography.fontSize.sm,
    fontWeight: typography.fontWeight.medium,
  },
  legend: {
    position: 'absolute',
    bottom: spacing.md,
    left: spacing.md,
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    padding: spacing.sm,
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  legendItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginVertical: 2,
  },
  legendDot: {
    width: 10,
    height: 10,
    borderRadius: 5,
    marginRight: spacing.sm,
  },
  legendText: {
    fontSize: typography.fontSize.xs,
    color: colors.neutral[700],
  },
});
