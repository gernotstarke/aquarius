import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { StatusBar } from 'expo-status-bar';
import { useAppStore } from './src/store/useAppStore';

import { LoginScreen } from './src/screens/LoginScreen';
import { WettkampfSelectionScreen } from './src/screens/WettkampfSelectionScreen';
import { FigureSelectionScreen } from './src/screens/FigureSelectionScreen';

const Stack = createNativeStackNavigator();

export default function App() {
  const token = useAppStore((state) => state.token);

  return (
    <NavigationContainer>
      <StatusBar style="auto" />
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        {!token ? (
          <Stack.Screen name="Login" component={LoginScreen} />
        ) : (
          <>
            <Stack.Screen name="WettkampfSelection" component={WettkampfSelectionScreen} />
            <Stack.Screen name="FigureSelection" component={FigureSelectionScreen} />
          </>
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
}