import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, FlatList, TouchableOpacity, Alert } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useAppStore } from '../store/useAppStore';
import apiClient from '../api/client';
import { Wettkampf } from '../types';
import { Button } from '../components/Button';

export const WettkampfSelectionScreen = () => {
  const navigation = useNavigation<any>();
  const [loading, setLoading] = useState(false);
  const { wettkaempfe, setWettkaempfe, selectWettkampf, logout, user } = useAppStore();

  const loadWettkaempfe = async () => {
    setLoading(true);
    try {
      // Assuming GET /wettkampf returns all competitions.
      // In a real app, might want to filter by date or relevance.
      const response = await apiClient.get('/wettkampf');
      setWettkaempfe(response.data);
    } catch (error) {
      Alert.alert('Fehler', 'Wettkämpfe konnten nicht geladen werden.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadWettkaempfe();
  }, []);

  const handleSelect = (wettkampf: Wettkampf) => {
    selectWettkampf(wettkampf);
    navigation.navigate('FigureSelection');
  };

  const renderItem = ({ item }: { item: Wettkampf }) => (
    <TouchableOpacity 
      style={styles.card} 
      onPress={() => handleSelect(item)}
    >
      <Text style={styles.cardTitle}>{item.name}</Text>
      <Text style={styles.cardDate}>{item.datum}</Text>
    </TouchableOpacity>
  );

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <View>
          <Text style={styles.welcome}>Hallo, {user?.full_name || user?.username}</Text>
          <Text style={styles.title}>Wettkampf wählen</Text>
        </View>
        <Button title="Logout" variant="outline" onPress={logout} />
      </View>

      <FlatList
        data={wettkaempfe}
        renderItem={renderItem}
        keyExtractor={(item) => item.id.toString()}
        contentContainerStyle={styles.list}
        refreshing={loading}
        onRefresh={loadWettkaempfe}
        ListEmptyComponent={
          <Text style={styles.empty}>Keine Wettkämpfe verfügbar.</Text>
        }
      />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8fafc',
  },
  header: {
    padding: 24,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: 'white',
    borderBottomWidth: 1,
    borderBottomColor: '#e2e8f0',
  },
  welcome: {
    fontSize: 14,
    color: '#64748b',
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#0f172a',
  },
  list: {
    padding: 16,
  },
  card: {
    backgroundColor: 'white',
    padding: 16,
    borderRadius: 12,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 2,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#0f172a',
    marginBottom: 4,
  },
  cardDate: {
    fontSize: 14,
    color: '#64748b',
  },
  empty: {
    textAlign: 'center',
    marginTop: 40,
    color: '#94a3b8',
  },
});
