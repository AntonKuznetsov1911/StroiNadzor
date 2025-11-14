/**
 * Главный навигатор приложения
 */
import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import { Text } from 'react-native';

import HomeScreen from '../screens/HomeScreen';
import ProjectsScreen from '../screens/ProjectsScreen';
import ProjectDetailScreen from '../screens/ProjectDetailScreen';
import CameraScreen from '../screens/CameraScreen';
import AIConsultantScreen from '../screens/AIConsultantScreen';
import ProfileScreen from '../screens/ProfileScreen';
import HiddenWorksScreen from '../screens/HiddenWorksScreen';
import InspectionDetailScreen from '../screens/InspectionDetailScreen';

const Tab = createBottomTabNavigator();
const Stack = createStackNavigator();

// Stack для проектов
const ProjectsStack = () => (
  <Stack.Navigator>
    <Stack.Screen
      name="ProjectsList"
      component={ProjectsScreen}
      options={{ title: 'Проекты' }}
    />
    <Stack.Screen
      name="ProjectDetail"
      component={ProjectDetailScreen}
      options={{ title: 'Детали проекта' }}
    />
    <Stack.Screen
      name="InspectionDetail"
      component={InspectionDetailScreen}
      options={{ title: 'Проверка' }}
    />
  </Stack.Navigator>
);

// Stack для главного экрана
const HomeStack = () => (
  <Stack.Navigator>
    <Stack.Screen
      name="HomeMain"
      component={HomeScreen}
      options={{ title: 'Главная' }}
    />
    <Stack.Screen
      name="Camera"
      component={CameraScreen}
      options={{ headerShown: false }}
    />
    <Stack.Screen
      name="HiddenWorks"
      component={HiddenWorksScreen}
      options={{ title: 'Скрытые работы' }}
    />
  </Stack.Navigator>
);

const MainNavigator = () => {
  return (
    <Tab.Navigator
      screenOptions={{
        tabBarActiveTintColor: '#1E3A8A',
        tabBarInactiveTintColor: '#6B7280',
        tabBarStyle: {
          backgroundColor: '#fff',
          borderTopWidth: 1,
          borderTopColor: '#E5E7EB',
          paddingBottom: 5,
          height: 60,
        },
      }}
    >
      <Tab.Screen
        name="Home"
        component={HomeStack}
        options={{
          headerShown: false,
          tabBarLabel: 'Главная',
          tabBarIcon: ({ color }) => <Text style={{ fontSize: 24 }}>🏠</Text>,
        }}
      />
      <Tab.Screen
        name="Projects"
        component={ProjectsStack}
        options={{
          headerShown: false,
          tabBarLabel: 'Проекты',
          tabBarIcon: ({ color }) => <Text style={{ fontSize: 24 }}>🏗️</Text>,
        }}
      />
      <Tab.Screen
        name="Camera"
        component={CameraScreen}
        options={{
          headerShown: false,
          tabBarLabel: 'Камера',
          tabBarIcon: ({ color }) => <Text style={{ fontSize: 24 }}>📸</Text>,
        }}
      />
      <Tab.Screen
        name="AIConsultant"
        component={AIConsultantScreen}
        options={{
          title: 'ИИ-консультант',
          tabBarLabel: 'Консультант',
          tabBarIcon: ({ color }) => <Text style={{ fontSize: 24 }}>💬</Text>,
        }}
      />
      <Tab.Screen
        name="Profile"
        component={ProfileScreen}
        options={{
          title: 'Профиль',
          tabBarLabel: 'Профиль',
          tabBarIcon: ({ color }) => <Text style={{ fontSize: 24 }}>👤</Text>,
        }}
      />
    </Tab.Navigator>
  );
};

export default MainNavigator;
