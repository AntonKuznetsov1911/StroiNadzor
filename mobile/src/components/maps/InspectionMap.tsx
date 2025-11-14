/**
 * Компонент карты с точками проверок
 */
import React from 'react';
import { View, StyleSheet } from 'react-native';
import MapView, { Marker, Polyline, PROVIDER_GOOGLE, Region } from 'react-native-maps';
import { colors } from '../../theme/colors';

interface InspectionPoint {
  id: number;
  latitude: number;
  longitude: number;
  title: string;
  hasDefects: boolean;
}

interface InspectionMapProps {
  inspections: InspectionPoint[];
  initialRegion?: Region;
  showRoute?: boolean;
  onInspectionPress?: (inspectionId: number) => void;
  height?: number;
}

export const InspectionMap: React.FC<InspectionMapProps> = ({
  inspections,
  initialRegion,
  showRoute = false,
  onInspectionPress,
  height = 400,
}) => {
  // Начальный регион по умолчанию
  const defaultRegion: Region = {
    latitude: inspections[0]?.latitude || 55.751244,
    longitude: inspections[0]?.longitude || 37.618423,
    latitudeDelta: 0.05,
    longitudeDelta: 0.05,
  };

  const region = initialRegion || defaultRegion;

  // Координаты для линии маршрута
  const routeCoordinates = showRoute
    ? inspections.map((i) => ({
        latitude: i.latitude,
        longitude: i.longitude,
      }))
    : [];

  return (
    <View style={[styles.container, { height }]}>
      <MapView
        provider={PROVIDER_GOOGLE}
        style={styles.map}
        initialRegion={region}
        showsUserLocation={true}
      >
        {/* Линия маршрута */}
        {showRoute && routeCoordinates.length > 1 && (
          <Polyline
            coordinates={routeCoordinates}
            strokeColor={colors.primary.main}
            strokeWidth={3}
            lineDashPattern={[10, 5]}
          />
        )}

        {/* Маркеры проверок */}
        {inspections.map((inspection, index) => (
          <Marker
            key={inspection.id}
            coordinate={{
              latitude: inspection.latitude,
              longitude: inspection.longitude,
            }}
            pinColor={inspection.hasDefects ? colors.error.main : colors.success.main}
            title={inspection.title}
            description={`Точка ${index + 1}`}
            onPress={() => onInspectionPress?.(inspection.id)}
          />
        ))}
      </MapView>
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
});
