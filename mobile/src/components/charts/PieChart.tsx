/**
 * Компонент круговой диаграммы
 */
import React from 'react';
import { View, Text, StyleSheet, Dimensions } from 'react-native';
import { PieChart as RNPieChart } from 'react-native-chart-kit';
import { colors } from '../../theme/colors';
import { spacing } from '../../theme/spacing';
import { typography } from '../../theme/typography';

const SCREEN_WIDTH = Dimensions.get('window').width;

interface DataPoint {
  name: string;
  value: number;
  color: string;
  legendFontColor?: string;
  legendFontSize?: number;
}

interface PieChartProps {
  data: DataPoint[];
  title?: string;
  size?: number;
  showLegend?: boolean;
}

export const PieChart: React.FC<PieChartProps> = ({
  data,
  title,
  size = 200,
  showLegend = true,
}) => {
  const chartData = data.map((item) => ({
    name: item.name,
    population: item.value,
    color: item.color,
    legendFontColor: item.legendFontColor || colors.neutral[700],
    legendFontSize: item.legendFontSize || typography.fontSize.sm,
  }));

  const total = data.reduce((sum, item) => sum + item.value, 0);

  const chartConfig = {
    color: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
  };

  return (
    <View style={styles.container}>
      {title && <Text style={styles.title}>{title}</Text>}

      <View style={styles.chartContainer}>
        <RNPieChart
          data={chartData}
          width={SCREEN_WIDTH - spacing.md * 2}
          height={size}
          chartConfig={chartConfig}
          accessor="population"
          backgroundColor="transparent"
          paddingLeft="15"
          absolute={false}
          hasLegend={showLegend}
        />
      </View>

      {showLegend && (
        <View style={styles.legendContainer}>
          {data.map((item, index) => {
            const percentage = total > 0 ? ((item.value / total) * 100).toFixed(1) : 0;
            return (
              <View key={index} style={styles.legendItem}>
                <View style={[styles.legendColor, { backgroundColor: item.color }]} />
                <Text style={styles.legendName}>{item.name}</Text>
                <Text style={styles.legendValue}>
                  {item.value} ({percentage}%)
                </Text>
              </View>
            );
          })}
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    marginVertical: spacing.md,
  },
  title: {
    fontSize: typography.fontSize.lg,
    fontWeight: typography.fontWeight.bold,
    color: colors.neutral[900],
    marginBottom: spacing.md,
  },
  chartContainer: {
    alignItems: 'center',
  },
  legendContainer: {
    marginTop: spacing.md,
    gap: spacing.sm,
  },
  legendItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: spacing.xs,
  },
  legendColor: {
    width: 16,
    height: 16,
    borderRadius: 8,
    marginRight: spacing.sm,
  },
  legendName: {
    flex: 1,
    fontSize: typography.fontSize.md,
    color: colors.neutral[700],
  },
  legendValue: {
    fontSize: typography.fontSize.md,
    fontWeight: typography.fontWeight.semibold,
    color: colors.neutral[900],
  },
});
