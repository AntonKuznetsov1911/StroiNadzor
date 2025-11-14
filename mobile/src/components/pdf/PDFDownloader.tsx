/**
 * Компонент для скачивания и открытия PDF документов
 */
import React, { useState } from 'react';
import { View, Text, StyleSheet, Alert, Platform } from 'react-native';
import RNFS from 'react-native-fs';
import { Button } from '../common/Button';
import { colors } from '../../theme/colors';
import { spacing } from '../../theme/spacing';
import { typography } from '../../theme/typography';
import { ProgressBar } from '../construction/ProgressBar';

interface PDFDownloaderProps {
  url: string;
  filename: string;
  onDownloadComplete?: (filePath: string) => void;
  onError?: (error: any) => void;
}

export const PDFDownloader: React.FC<PDFDownloaderProps> = ({
  url,
  filename,
  onDownloadComplete,
  onError,
}) => {
  const [downloading, setDownloading] = useState(false);
  const [progress, setProgress] = useState(0);

  const downloadPDF = async () => {
    try {
      setDownloading(true);
      setProgress(0);

      // Путь для сохранения
      const downloadDest = `${RNFS.DocumentDirectoryPath}/${filename}`;

      // Опции загрузки
      const options = {
        fromUrl: url,
        toFile: downloadDest,
        progress: (res: any) => {
          const progressPercent = (res.bytesWritten / res.contentLength) * 100;
          setProgress(progressPercent);
        },
      };

      // Загрузка файла
      const result = await RNFS.downloadFile(options).promise;

      if (result.statusCode === 200) {
        setDownloading(false);
        Alert.alert(
          'Успешно',
          'PDF документ успешно загружен',
          [
            {
              text: 'OK',
              onPress: () => onDownloadComplete?.(downloadDest),
            },
          ]
        );
      } else {
        throw new Error(`Download failed with status ${result.statusCode}`);
      }
    } catch (error) {
      setDownloading(false);
      setProgress(0);
      console.error('Download error:', error);
      onError?.(error);
      Alert.alert('Ошибка', 'Не удалось загрузить документ');
    }
  };

  const openPDF = async () => {
    const filePath = `${RNFS.DocumentDirectoryPath}/${filename}`;

    try {
      const exists = await RNFS.exists(filePath);

      if (exists) {
        onDownloadComplete?.(filePath);
      } else {
        Alert.alert('Файл не найден', 'Необходимо сначала загрузить документ');
      }
    } catch (error) {
      console.error('Open PDF error:', error);
      Alert.alert('Ошибка', 'Не удалось открыть документ');
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.info}>
        <Text style={styles.filename}>{filename}</Text>
        <Text style={styles.url} numberOfLines={1}>
          {url}
        </Text>
      </View>

      {downloading && (
        <View style={styles.progressContainer}>
          <ProgressBar progress={progress / 100} />
          <Text style={styles.progressText}>
            Загрузка: {Math.round(progress)}%
          </Text>
        </View>
      )}

      <View style={styles.actions}>
        <Button
          title="Скачать"
          onPress={downloadPDF}
          variant="primary"
          size="medium"
          disabled={downloading}
          style={styles.button}
        />
        <Button
          title="Открыть"
          onPress={openPDF}
          variant="outline"
          size="medium"
          disabled={downloading}
          style={styles.button}
        />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: spacing.md,
    backgroundColor: colors.neutral[50],
    borderRadius: 12,
    borderWidth: 1,
    borderColor: colors.neutral[200],
  },
  info: {
    marginBottom: spacing.md,
  },
  filename: {
    fontSize: typography.fontSize.md,
    fontWeight: typography.fontWeight.semibold,
    color: colors.neutral[900],
    marginBottom: spacing.xs,
  },
  url: {
    fontSize: typography.fontSize.sm,
    color: colors.neutral[600],
  },
  progressContainer: {
    marginBottom: spacing.md,
  },
  progressText: {
    marginTop: spacing.xs,
    fontSize: typography.fontSize.sm,
    color: colors.neutral[600],
    textAlign: 'center',
  },
  actions: {
    flexDirection: 'row',
    gap: spacing.sm,
  },
  button: {
    flex: 1,
  },
});
