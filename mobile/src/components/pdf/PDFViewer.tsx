/**
 * Компонент просмотра PDF документов
 */
import React, { useState } from 'react';
import { View, Text, StyleSheet, ActivityIndicator, TouchableOpacity } from 'react-native';
import Pdf from 'react-native-pdf';
import { colors } from '../../theme/colors';
import { spacing } from '../../theme/spacing';
import { typography } from '../../theme/typography';

interface PDFViewerProps {
  source: { uri: string } | { path: string };
  onLoadComplete?: (numberOfPages: number) => void;
  onError?: (error: any) => void;
  showControls?: boolean;
  enablePaging?: boolean;
}

export const PDFViewer: React.FC<PDFViewerProps> = ({
  source,
  onLoadComplete,
  onError,
  showControls = true,
  enablePaging = true,
}) => {
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [loading, setLoading] = useState(true);

  const handleLoadComplete = (numberOfPages: number) => {
    setTotalPages(numberOfPages);
    setLoading(false);
    onLoadComplete?.(numberOfPages);
  };

  const handlePageChanged = (page: number, numberOfPages: number) => {
    setCurrentPage(page);
  };

  const handleError = (error: any) => {
    setLoading(false);
    console.error('PDF load error:', error);
    onError?.(error);
  };

  return (
    <View style={styles.container}>
      {loading && (
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color={colors.primary.main} />
          <Text style={styles.loadingText}>Загрузка документа...</Text>
        </View>
      )}

      <Pdf
        source={source}
        onLoadComplete={handleLoadComplete}
        onPageChanged={handlePageChanged}
        onError={handleError}
        style={styles.pdf}
        trustAllCerts={false}
        enablePaging={enablePaging}
        horizontal={false}
        spacing={10}
        fitPolicy={0} // 0 = width, 1 = height, 2 = both
      />

      {showControls && !loading && totalPages > 0 && (
        <View style={styles.controls}>
          <Text style={styles.pageInfo}>
            Страница {currentPage} из {totalPages}
          </Text>
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.neutral[100],
  },
  pdf: {
    flex: 1,
    backgroundColor: colors.neutral[100],
  },
  loadingContainer: {
    ...StyleSheet.absoluteFillObject,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: colors.neutral[100],
    zIndex: 10,
  },
  loadingText: {
    marginTop: spacing.md,
    fontSize: typography.fontSize.md,
    color: colors.neutral[600],
  },
  controls: {
    position: 'absolute',
    bottom: spacing.md,
    alignSelf: 'center',
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    borderRadius: 20,
  },
  pageInfo: {
    color: colors.neutral[50],
    fontSize: typography.fontSize.sm,
    fontWeight: typography.fontWeight.medium,
  },
});
