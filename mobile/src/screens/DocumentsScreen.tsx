/**
 * Экран документов
 */
import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  RefreshControl,
} from 'react-native';
import { colors } from '../theme/colors';
import { spacing } from '../theme/spacing';
import { typography } from '../theme/typography';
import { EmptyState } from '../components/common/EmptyState';
import { formatDate, formatFileSize } from '../utils';
import { Dropdown } from '../components/forms/Dropdown';

interface Document {
  id: number;
  title: string;
  type: 'act' | 'report' | 'prescription' | 'protocol' | 'certificate' | 'other';
  projectName: string;
  fileSize: number;
  uploadedAt: string;
  uploadedBy: string;
}

const MOCK_DOCUMENTS: Document[] = [
  {
    id: 1,
    title: 'Акт освидетельствования скрытых работ №АСВ-123',
    type: 'act',
    projectName: 'ЖК Солнечный',
    fileSize: 2547891,
    uploadedAt: '2025-11-08T10:00:00',
    uploadedBy: 'Иванов И.И.',
  },
  {
    id: 2,
    title: 'Отчет о проверке качества бетона',
    type: 'report',
    projectName: 'ЖК Солнечный',
    fileSize: 4123456,
    uploadedAt: '2025-11-07T14:30:00',
    uploadedBy: 'Петров П.П.',
  },
  {
    id: 3,
    title: 'Предписание об устранении нарушений №ПР-45',
    type: 'prescription',
    projectName: 'БЦ Москва-Сити',
    fileSize: 1234567,
    uploadedAt: '2025-11-06T09:15:00',
    uploadedBy: 'Сидоров С.С.',
  },
  {
    id: 4,
    title: 'Протокол испытаний арматуры',
    type: 'protocol',
    projectName: 'ЖК Солнечный',
    fileSize: 987654,
    uploadedAt: '2025-11-05T16:45:00',
    uploadedBy: 'Иванов И.И.',
  },
  {
    id: 5,
    title: 'Сертификат соответствия на бетон М350',
    type: 'certificate',
    projectName: 'БЦ Москва-Сити',
    fileSize: 567890,
    uploadedAt: '2025-11-04T11:20:00',
    uploadedBy: 'Петров П.П.',
  },
];

const DOCUMENT_TYPE_LABELS: Record<Document['type'], string> = {
  act: 'Акт',
  report: 'Отчет',
  prescription: 'Предписание',
  protocol: 'Протокол',
  certificate: 'Сертификат',
  other: 'Другое',
};

const DOCUMENT_TYPE_COLORS: Record<Document['type'], string> = {
  act: colors.primary.main,
  report: colors.info.main,
  prescription: colors.error.main,
  protocol: colors.accent.main,
  certificate: colors.success.main,
  other: colors.neutral[500],
};

export const DocumentsScreen: React.FC = () => {
  const [documents, setDocuments] = useState<Document[]>(MOCK_DOCUMENTS);
  const [refreshing, setRefreshing] = useState(false);
  const [filterType, setFilterType] = useState<string>('all');

  const onRefresh = async () => {
    setRefreshing(true);
    // Загрузка документов
    setTimeout(() => {
      setRefreshing(false);
    }, 1000);
  };

  const handleDocumentPress = (document: Document) => {
    // Открыть документ
    console.log('Open document:', document.id);
  };

  const filteredDocuments =
    filterType === 'all'
      ? documents
      : documents.filter((doc) => doc.type === filterType);

  const renderDocument = ({ item }: { item: Document }) => (
    <TouchableOpacity
      style={styles.documentItem}
      onPress={() => handleDocumentPress(item)}
      activeOpacity={0.7}
    >
      <View style={styles.documentIcon}>
        <Text style={styles.documentIconText}>📄</Text>
      </View>

      <View style={styles.documentContent}>
        <Text style={styles.documentTitle} numberOfLines={2}>
          {item.title}
        </Text>

        <View style={styles.documentMeta}>
          <View
            style={[
              styles.typeBadge,
              { backgroundColor: DOCUMENT_TYPE_COLORS[item.type] },
            ]}
          >
            <Text style={styles.typeBadgeText}>
              {DOCUMENT_TYPE_LABELS[item.type]}
            </Text>
          </View>

          <Text style={styles.projectName} numberOfLines={1}>
            {item.projectName}
          </Text>
        </View>

        <View style={styles.documentFooter}>
          <Text style={styles.documentInfo}>
            {formatFileSize(item.fileSize)}
          </Text>
          <Text style={styles.documentInfo}>•</Text>
          <Text style={styles.documentInfo}>
            {formatDate(new Date(item.uploadedAt))}
          </Text>
          <Text style={styles.documentInfo}>•</Text>
          <Text style={styles.documentInfo} numberOfLines={1}>
            {item.uploadedBy}
          </Text>
        </View>
      </View>

      <View style={styles.documentActions}>
        <TouchableOpacity style={styles.actionButton}>
          <Text style={styles.actionIcon}>👁️</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.actionButton}>
          <Text style={styles.actionIcon}>⬇️</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.actionButton}>
          <Text style={styles.actionIcon}>📤</Text>
        </TouchableOpacity>
      </View>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <View style={styles.filterContainer}>
        <Dropdown
          value={filterType}
          options={[
            { label: 'Все документы', value: 'all' },
            { label: 'Акты', value: 'act' },
            { label: 'Отчеты', value: 'report' },
            { label: 'Предписания', value: 'prescription' },
            { label: 'Протоколы', value: 'protocol' },
            { label: 'Сертификаты', value: 'certificate' },
          ]}
          onChange={(value) => setFilterType(value as string)}
          placeholder="Фильтр по типу"
        />
      </View>

      <FlatList
        data={filteredDocuments}
        renderItem={renderDocument}
        keyExtractor={(item) => item.id.toString()}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={onRefresh}
            tintColor={colors.primary.main}
          />
        }
        ListEmptyComponent={
          <EmptyState
            icon="📁"
            title="Нет документов"
            description="Документы появятся здесь после создания актов и отчетов"
          />
        }
        contentContainerStyle={
          filteredDocuments.length === 0 && styles.emptyContainer
        }
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.neutral[100],
  },
  filterContainer: {
    padding: spacing.md,
    backgroundColor: colors.neutral.white,
    borderBottomWidth: 1,
    borderBottomColor: colors.neutral[200],
  },
  documentItem: {
    flexDirection: 'row',
    padding: spacing.md,
    backgroundColor: colors.neutral.white,
    marginBottom: spacing.sm,
    borderRadius: spacing.borderRadius.md,
    marginHorizontal: spacing.md,
    elevation: 1,
    shadowColor: colors.neutral.black,
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
  },
  documentIcon: {
    width: 48,
    height: 48,
    borderRadius: spacing.borderRadius.md,
    backgroundColor: colors.neutral[100],
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: spacing.md,
  },
  documentIconText: {
    fontSize: typography.fontSize.xl,
  },
  documentContent: {
    flex: 1,
  },
  documentTitle: {
    fontSize: typography.fontSize.md,
    fontWeight: typography.fontWeight.semibold,
    color: colors.neutral[900],
    marginBottom: spacing.xs,
  },
  documentMeta: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: spacing.xs,
  },
  typeBadge: {
    paddingHorizontal: spacing.sm,
    paddingVertical: spacing.xs / 2,
    borderRadius: spacing.borderRadius.sm,
    marginRight: spacing.sm,
  },
  typeBadgeText: {
    fontSize: typography.fontSize.xs,
    fontWeight: typography.fontWeight.semibold,
    color: colors.neutral.white,
  },
  projectName: {
    flex: 1,
    fontSize: typography.fontSize.sm,
    color: colors.neutral[600],
  },
  documentFooter: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.xs,
  },
  documentInfo: {
    fontSize: typography.fontSize.xs,
    color: colors.neutral[500],
  },
  documentActions: {
    justifyContent: 'space-around',
    marginLeft: spacing.sm,
  },
  actionButton: {
    padding: spacing.xs,
  },
  actionIcon: {
    fontSize: typography.fontSize.md,
  },
  emptyContainer: {
    flex: 1,
  },
});
