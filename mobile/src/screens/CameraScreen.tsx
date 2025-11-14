/**
 * Экран камеры для фотофиксации (Модуль 1 MVP)
 */
import React, { useState, useRef } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Alert,
} from 'react-native';
import { Camera, useCameraDevices } from 'react-native-vision-camera';
import Geolocation from 'react-native-geolocation-service';

const CameraScreen = ({ navigation, route }: any) => {
  const { inspectionId } = route.params || {};
  const [hasPermission, setHasPermission] = useState(false);
  const camera = useRef<Camera>(null);
  const devices = useCameraDevices();
  const device = devices.back;

  React.useEffect(() => {
    (async () => {
      const cameraPermission = await Camera.requestCameraPermission();
      setHasPermission(cameraPermission === 'authorized');
    })();
  }, []);

  const takePhoto = async () => {
    if (camera.current) {
      try {
        // Получение GPS координат
        const position = await new Promise<any>((resolve, reject) => {
          Geolocation.getCurrentPosition(resolve, reject, {
            enableHighAccuracy: true,
            timeout: 15000,
            maximumAge: 10000,
          });
        });

        // Съемка фото
        const photo = await camera.current.takePhoto({
          flash: 'auto',
          enableShutterSound: true,
        });

        // Переход на экран предпросмотра с метаданными
        navigation.navigate('PhotoPreview', {
          photo: photo.path,
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
          timestamp: new Date().toISOString(),
          inspectionId,
        });
      } catch (error) {
        console.error('Error taking photo:', error);
        Alert.alert('Ошибка', 'Не удалось сделать фото');
      }
    }
  };

  if (!device || !hasPermission) {
    return (
      <View style={styles.container}>
        <Text>Нет доступа к камере</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Camera
        ref={camera}
        style={StyleSheet.absoluteFill}
        device={device}
        isActive={true}
        photo={true}
      />

      {/* Overlay с информацией */}
      <View style={styles.overlay}>
        <View style={styles.topBar}>
          <Text style={styles.infoText}>
            {new Date().toLocaleString('ru-RU')}
          </Text>
          <Text style={styles.infoText}>GPS: Определение...</Text>
        </View>

        {/* Кнопка съемки */}
        <View style={styles.bottomBar}>
          <TouchableOpacity style={styles.captureButton} onPress={takePhoto}>
            <View style={styles.captureButtonInner} />
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
  },
  overlay: {
    ...StyleSheet.absoluteFillObject,
    justifyContent: 'space-between',
  },
  topBar: {
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    padding: 16,
  },
  infoText: {
    color: '#fff',
    fontSize: 14,
    marginBottom: 4,
  },
  bottomBar: {
    alignItems: 'center',
    paddingBottom: 40,
  },
  captureButton: {
    width: 70,
    height: 70,
    borderRadius: 35,
    backgroundColor: '#fff',
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 5,
    borderColor: '#1E3A8A',
  },
  captureButtonInner: {
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: '#1E3A8A',
  },
});

export default CameraScreen;
