/**
 * Компонент графика линий для статистики
 */
import React from 'react';
import { View, Text, StyleSheet, Dimensions } from 'react-native';
import { LineChart as RNLineChart } from 'react-native-chart-kit';
import { colors } from '../../theme/colors';
import { spacing } from '../../theme/spacing';
import { typography } from '../../theme/typography';

const SCREEN_WIDTH = Dimensions.get('window').width;

interface DataPoint {
  label: string;
  value: number;
}

interface LineChartProps {
  data: DataPoint[];
  title?: string;
  color?: string;
  height?: number;
  showValues?: boolean;
}

export const LineChart: React.FC<LineChartProps> = ({
  data,
  title,
  color = colors.primary.main,
  height = 220,
  showValues = false,
}) => {
  const chartData = {
    labels: data.map((d) => d.label),
    datasets: [
      {
        data: data.map((d) => d.value),
        color: (opacity = 1) => `rgba(59, 130, 246, ${opacity})`,
        strokeWidth: 2,
      },
    ],
  };

  const chartConfig = {
    backgroundColor: colors.neutral[50],
    backgroundGradientFrom: colors.neutral[50],
    backgroundGradientTo: colors.neutral[50],
    decimalPlaces: 0,
    color: (opacity = 1) => color,
    labelColor: (opacity = 1) => colors.neutral[600],
    style: {
      borderRadius: 16,
    },
    propsForDots: {
      r: '4',
      strokeWidth: '2',
      stroke: color,
    },
    propsForBackgroundLines: {
      strokeDasharray: '',
      stroke: colors.neutral[200],
    },
  };

  return (
    <View style={styles.container}>
      {title && <Text style={styles.title}>{title}</Text>}

      <RNLineChart
        data={chartData}
        width={SCREEN_WIDTH - spacing.md * 2}
        height={height}
        chartConfig={chartConfig}
        bezier
        style={styles.chart}
        withVerticalLabels={true}
        withHorizontalLabels={true}
        withDots={true}
        withShadow={false}
        withInnerLines={true}
        withOuterLines={false}
        withVerticalLines={false}
        withHorizontalLines={true}
        fromZero={true}
      />

      {showValues && (
        <View style={styles.valuesContainer}>
          {data.map((point, index) => (
            <View key={index} style={styles.valueItem}>
              <Text style={styles.valueLabel}>{point.label}:</Text>
              <Text style={styles.valueNumber}>{point.value}</Text>
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
  valuesContainer: {
    marginTop: spacing.md,
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: spacing.sm,
  },
  valueItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: spacing.sm,
    paddingVertical: spacing.xs,
    backgroundColor: colors.neutral[100],
    borderRadius: 8,
  },
  valueLabel: {
    fontSize: typography.fontSize.sm,
    color: colors.neutral[600],
    marginRight: spacing.xs,
  },
  valueNumber: {
    fontSize: typography.fontSize.sm,
    fontWeight: typography.fontWeight.semibold,
    color: colors.neutral[900],
  },
});
