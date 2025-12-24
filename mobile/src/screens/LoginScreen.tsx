import React, { useState } from 'react';
import { View, Text, StyleSheet, Alert, Image, KeyboardAvoidingView, Platform } from 'react-native';
import { useAppStore } from '../store/useAppStore';
import apiClient from '../api/client';
import { Button } from '../components/Button';
import { Input } from '../components/Input';
import { SafeAreaView } from 'react-native-safe-area-context';
import { colors, layout, spacing } from '../theme';

export const LoginScreen = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const setAuth = useAppStore((state) => state.setAuth);

  const handleLogin = async () => {
    if (!username || !password) {
      Alert.alert('Fehler', 'Bitte Benutzernamen und Passwort eingeben.');
      return;
    }

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);

      const response = await apiClient.post('/auth/token', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      const { access_token } = response.data;

      const meResponse = await apiClient.get('/auth/me', {
        headers: { Authorization: `Bearer ${access_token}` },
      });

      setAuth(access_token, meResponse.data);
      
    } catch (error: any) {
      let message = 'Ein unbekannter Fehler ist aufgetreten.';

      if (error.response) {
        // The request was made and the server responded with a status code
        if (error.response.status === 401) {
          message = 'Benutzername oder Passwort falsch.';
        } else if (error.response.status >= 500) {
          message = 'Server-Fehler. Bitte später erneut versuchen.';
        } else {
           message = `Server antwortete mit Fehlercode ${error.response.status}`;
        }
      } else if (error.request) {
        // The request was made but no response was received
        message = 'Server nicht erreichbar. Bitte Netzwerkverbindung prüfen.';
      } else {
        // Something happened in setting up the request that triggered an Error
        message = error.message;
      }
      
      Alert.alert('Anmeldung nicht möglich', message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <KeyboardAvoidingView 
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.keyboardView}
      >
        <View style={styles.content}>
          <View style={styles.header}>
            <Image 
              source={require('../../assets/logo.png')} 
              style={styles.logo}
              resizeMode="contain"
            />
            <Text style={styles.title}>Arqua42</Text>
            <Text style={styles.subtitle}>Bewertungs-App</Text>
          </View>

          <View style={styles.form}>
            <Text style={styles.loginTitle}>Anmelden</Text>
            <Input 
              label="Benutzername"
              value={username}
              onChangeText={setUsername}
              autoCapitalize="none"
              placeholder="benutzer@verein.de"
            />
            <Input 
              label="Passwort"
              value={password}
              onChangeText={setPassword}
              secureTextEntry
              placeholder="••••••••"
            />
            
            <View style={styles.buttonContainer}>
              <Button 
                title="Login" 
                onPress={handleLogin} 
                loading={loading} 
              />
            </View>
          </View>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  keyboardView: {
    flex: 1,
  },
  content: {
    flex: 1,
    padding: spacing.lg,
    justifyContent: 'center',
  },
  header: {
    alignItems: 'center',
    marginBottom: spacing.xxl,
  },
  logo: {
    width: 120,
    height: 120,
    marginBottom: spacing.md,
  },
  title: {
    fontSize: 42,
    fontWeight: '800',
    color: colors.primaryDark,
    marginBottom: spacing.xs,
  },
  subtitle: {
    fontSize: 20,
    color: colors.textLight,
    fontWeight: '500',
  },
  form: {
    backgroundColor: colors.surface,
    padding: spacing.lg,
    borderRadius: layout.borderRadius,
    shadowColor: colors.primary,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 12,
    elevation: 4,
  },
  loginTitle: {
    fontSize: 24,
    fontWeight: '700',
    color: colors.text,
    marginBottom: spacing.lg,
    textAlign: 'center',
  },
  buttonContainer: {
    marginTop: spacing.md,
  },
});
