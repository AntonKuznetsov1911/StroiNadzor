/**
 * Компонент столбчатой диаграммы
 */
import React from 'react';
import { View, Text, StyleSheet, Dimensions } from 'react-native';
import { BarChart as RNBarChart } from 'react-native-chart-kit';
import { colors } from '../../theme/colors';
import { spacing } from '../../theme/spacing';
import { typography } from '../../theme/typography';

const SCREEN_WIDTH = Dimensions.get('window').width;

interface DataPoint {
  label: string;
  value: number;
  color?: string;
}

interface BarChartProps {
  data: DataPoint[];
  title?: string;
  height?: number;
  showLegend?: boolean;
}

export const BarChart: React.FC<BarChartProps> = ({
  data,
  title,
  height = 220,
  showLegend = false,
}) => {
  const chartData = {
    labels: data.map((d) => d.label),
    datasets: [
      {
        data: data.map((d) => d.value),
      },
    ],
  };

  const chartConfig = {
    backgroundColor: colors.neutral[50],
    backgroundGradientFrom: colors.neutral[50],
    backgroundGradientTo: colors.neutral[50],
    decimalPlaces: 0,
    color: (opacity = 1) => colors.primary.main,
    labelColor: (opacity = 1) => colors.neutral[600],
    style: {
      borderRadius: 16,
    },
    propsForBackgroundLines: {
      strokeDasharray: '',
      stroke: colors.neutral[200],
    },
    barPercentage: 0.7,
  };

  return (
    <View style={styles.container}>
      {title && <Text style={styles.title}>{title}</Text>}

      <RNBarChart
        data={chartData}
        width={SCREEN_WIDTH - spacing.md * 2}
        height={height}
        chartConfig={chartConfig}
        style={styles.chart}
        withVerticalLabels={true}
        withHorizontalLabels={true}
        withInnerLines={true}
        showBarTops={true}
        showValuesOnTopOfBars={true}
        fromZero={true}
      />

      {showLegend && (
        <View style={styles.legendContainer}>
          {data.map((point, index) => (
            <View key={index} style={styles.legendItem}>
              <View
                style={[
                  styles.legendColor,
                  { backgroundColor: point.color || colors.primary.main },
                ]}
              />
              <Text style={styles.legendLabel}>{point.label}</Text>
              <Text style={styles.legendValue}>{point.value}</Text>
            </View>
          ))}
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
  chart: {
    marginVertical: spacing.sm,
    borderRadius: 16,
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
    width: 12,
    height: 12,
    borderRadius: 2,
    marginRight: spacing.sm,
  },
  legendLabel: {
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
