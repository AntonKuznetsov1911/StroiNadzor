/**
 * Экран статистики и аналитики
 */
import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ScrollView, RefreshControl } from 'react-native';
import { LineChart, BarChart, PieChart } from '../components/charts';
import { Card } from '../components/common/Card';
import { colors } from '../theme/colors';
import { spacing } from '../theme/spacing';
import { typography } from '../theme/typography';
import { apiService } from '../services/apiService';

interface DashboardStats {
  summary: {
    total_projects: number;
    active_projects: number;
    total_inspections: number;
    recent_inspections: number;
    total_defects: number;
    critical_defects: number;
    pending_hidden_works: number;
  };
  projects_by_status: Record<string, number>;
  inspections_by_result: Record<string, number>;
}

interface TrendsData {
  period_days: number;
  inspections_trend: Array<{ date: string; count: number }>;
  defects_trend: Array<{ date: string; count: number }>;
}

export const StatisticsScreen: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [trends, setTrends] = useState<TrendsData | null>(null);
  const [refreshing, setRefreshing] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStatistics();
  }, []);

  const loadStatistics = async () => {
    try {
      // Загрузка статистики дашборда
      const statsResponse = await apiService.get('/api/v1/statistics/dashboard');
      setStats(statsResponse.data);

      // Загрузка трендов за 7 дней
      const trendsResponse = await apiService.get('/api/v1/statistics/trends', {
        params: { days: 7 },
      });
      setTrends(trendsResponse.data);
    } catch (error) {
      console.error('Failed to load statistics:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const handleRefresh = () => {
    setRefreshing(true);
    loadStatistics();
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <Text style={styles.loadingText}>Загрузка статистики...</Text>
      </View>
    );
  }

  if (!stats || !trends) {
    return (
      <View style={styles.errorContainer}>
        <Text style={styles.errorText}>Не удалось загрузить статистику</Text>
      </View>
    );
  }

  // Данные для круговой диаграммы проектов
  const projectsPieData = Object.entries(stats.projects_by_status).map(
    ([status, count]) => {
      const statusColors: Record<string, string> = {
        in_progress: colors.warning.main,
        planning: colors.info.main,
        completed: colors.success.main,
        on_hold: colors.neutral[400],
      };

      const statusNames: Record<string, string> = {
        in_progress: 'В работе',
        planning: 'Планирование',
        completed: 'Завершено',
        on_hold: 'Приостановлено',
      };

      return {
        name: statusNames[status] || status,
        value: count,
        color: statusColors[status] || colors.primary.main,
      };
    }
  );

  // Данные для круговой диаграммы проверок
  const inspectionsPieData = Object.entries(stats.inspections_by_result).map(
    ([result, count]) => {
      const resultColors: Record<string, string> = {
        completed: colors.success.main,
        in_progress: colors.warning.main,
        failed: colors.error.main,
      };

      const resultNames: Record<string, string> = {
        completed: 'Завершено',
        in_progress: 'В процессе',
        failed: 'Не пройдено',
      };

      return {
        name: resultNames[result] || result,
        value: count,
        color: resultColors[result] || colors.primary.main,
      };
    }
  );

  // Данные для линейного графика проверок
  const inspectionsTrendData = trends.inspections_trend.map((item) => ({
    label: new Date(item.date).getDate().toString(),
    value: item.count,
  }));

  // Данные для линейного графика дефектов
  const defectsTrendData = trends.defects_trend.map((item) => ({
    label: new Date(item.date).getDate().toString(),
    value: item.count,
  }));

  return (
    <ScrollView
      style={styles.container}
      refreshControl={
        <RefreshControl
          refreshing={refreshing}
          onRefresh={handleRefresh}
          tintColor={colors.primary.main}
        />
      }
    >
      {/* Сводка */}
      <Card style={styles.summaryCard}>
        <Text style={styles.cardTitle}>Общая статистика</Text>

        <View style={styles.summaryGrid}>
          <View style={styles.summaryItem}>
            <Text style={styles.summaryValue}>{stats.summary.total_projects}</Text>
            <Text style={styles.summaryLabel}>Всего проектов</Text>
          </View>

          <View style={styles.summaryItem}>
            <Text style={[styles.summaryValue, { color: colors.warning.main }]}>
              {stats.summary.active_projects}
            </Text>
            <Text style={styles.summaryLabel}>Активных</Text>
          </View>

          <View style={styles.summaryItem}>
            <Text style={styles.summaryValue}>{stats.summary.total_inspections}</Text>
            <Text style={styles.summaryLabel}>Проверок</Text>
          </View>

          <View style={styles.summaryItem}>
            <Text style={[styles.summaryValue, { color: colors.error.main }]}>
              {stats.summary.critical_defects}
            </Text>
            <Text style={styles.summaryLabel}>Крит. дефектов</Text>
          </View>
        </View>
      </Card>

      {/* Проекты по статусам */}
      <Card style={styles.chartCard}>
        <PieChart
          data={projectsPieData}
          title="Проекты по статусам"
          showLegend={true}
        />
      </Card>

      {/* Проверки по результатам */}
      <Card style={styles.chartCard}>
        <PieChart
          data={inspectionsPieData}
          title="Проверки по результатам"
          showLegend={true}
        />
      </Card>

      {/* Тренд проверок */}
      <Card style={styles.chartCard}>
        <LineChart
          data={inspectionsTrendData}
          title="Проверки за последние 7 дней"
          color={colors.primary.main}
          showValues={false}
        />
      </Card>

      {/* Тренд дефектов */}
      <Card style={styles.chartCard}>
        <LineChart
          data={defectsTrendData}
          title="Дефекты за последние 7 дней"
          color={colors.error.main}
          showValues={false}
        />
      </Card>

      {/* Дополнительная информация */}
      <Card style={styles.infoCard}>
        <View style={styles.infoRow}>
          <Text style={styles.infoLabel}>Всего дефектов:</Text>
          <Text style={styles.infoValue}>{stats.summary.total_defects}</Text>
        </View>
        <View style={styles.infoRow}>
          <Text style={styles.infoLabel}>Критических:</Text>
          <Text style={[styles.infoValue, { color: colors.error.main }]}>
            {stats.summary.critical_defects}
          </Text>
        </View>
        <View style={styles.infoRow}>
          <Text style={styles.infoLabel}>Скрытых работ в ожидании:</Text>
          <Text style={styles.infoValue}>{stats.summary.pending_hidden_works}</Text>
        </View>
        <View style={styles.infoRow}>
          <Text style={styles.infoLabel}>Недавних проверок:</Text>
          <Text style={styles.infoValue}>{stats.summary.recent_inspections}</Text>
        </View>
      </Card>

      <View style={styles.bottomPadding} />
    </ScrollView>
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
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: colors.neutral[100],
  },
  errorText: {
    fontSize: typography.fontSize.md,
    color: colors.error.main,
  },
  summaryCard: {
    margin: spacing.md,
  },
  cardTitle: {
    fontSize: typography.fontSize.lg,
    fontWeight: typography.fontWeight.bold,
    color: colors.neutral[900],
    marginBottom: spacing.md,
  },
  summaryGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginHorizontal: -spacing.xs,
  },
  summaryItem: {
    width: '50%',
    paddingHorizontal: spacing.xs,
    paddingVertical: spacing.sm,
    alignItems: 'center',
  },
  summaryValue: {
    fontSize: typography.fontSize.xxxl,
    fontWeight: typography.fontWeight.bold,
    color: colors.primary.main,
  },
  summaryLabel: {
    fontSize: typography.fontSize.sm,
    color: colors.neutral[600],
    marginTop: spacing.xs,
    textAlign: 'center',
  },
  chartCard: {
    margin: spacing.md,
    marginTop: 0,
  },
  infoCard: {
    margin: spacing.md,
    marginTop: 0,
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: spacing.sm,
    borderBottomWidth: 1,
    borderBottomColor: colors.neutral[200],
  },
  infoLabel: {
    fontSize: typography.fontSize.md,
    color: colors.neutral[600],
  },
  infoValue: {
    fontSize: typography.fontSize.md,
    fontWeight: typography.fontWeight.semibold,
    color: colors.neutral[900],
  },
  bottomPadding: {
    height: spacing.lg,
  },
});
