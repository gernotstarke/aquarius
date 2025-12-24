import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, FlatList, TouchableOpacity, Alert } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useAppStore } from '../store/useAppStore';
import apiClient from '../api/client';
import { Wettkampf } from '../types';
import { Button } from '../components/Button';
import { colors, layout, spacing } from '../theme';

export const WettkampfSelectionScreen = () => {
  const navigation = useNavigation<any>();
  const [loading, setLoading] = useState(false);
  const { wettkaempfe, setWettkaempfe, selectWettkampf, logout, user } = useAppStore();

  const loadWettkaempfe = async () => {
    setLoading(true);
    try {
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
      <View style={styles.cardIcon}>
        <Text style={styles.iconText}>🏆</Text>
      </View>
      <View style={styles.cardContent}>
        <Text style={styles.cardTitle}>{item.name}</Text>
        <Text style={styles.cardDate}>{item.datum}</Text>
      </View>
      <Text style={styles.chevron}>›</Text>
    </TouchableOpacity>
  );

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <View>
          <Text style={styles.welcome}>Willkommen,</Text>
          <Text style={styles.userName}>{user?.full_name || user?.username}</Text>
        </View>
        <Button title="Logout" variant="outline" onPress={logout} />
      </View>

      <Text style={styles.sectionTitle}>Aktive Wettkämpfe</Text>

      <FlatList
        data={wettkaempfe}
        renderItem={renderItem}
        keyExtractor={(item) => item.id.toString()}
        contentContainerStyle={styles.list}
        refreshing={loading}
        onRefresh={loadWettkaempfe}
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Text style={styles.empty}>Keine Wettkämpfe verfügbar.</Text>
            <Button title="Aktualisieren" onPress={loadWettkaempfe} variant="secondary" />
          </View>
        }
      />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  header: {
    padding: spacing.lg,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: colors.surface,
    borderBottomWidth: 1,
    borderBottomColor: colors.primaryLight,
  },
  welcome: {
    fontSize: 14,
    color: colors.textLight,
  },
  userName: {
    fontSize: 20,
    fontWeight: 'bold',
    color: colors.text,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: colors.text,
    marginLeft: spacing.lg,
    marginTop: spacing.lg,
    marginBottom: spacing.sm,
  },
  list: {
    padding: spacing.lg,
  },
  card: {
    backgroundColor: colors.surface,
    padding: spacing.md,
    borderRadius: layout.borderRadius,
    marginBottom: spacing.md,
    flexDirection: 'row',
    alignItems: 'center',
    shadowColor: colors.primary,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 8,
    elevation: 2,
  },
  cardIcon: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: colors.primaryLight,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: spacing.md,
  },
  iconText: {
    fontSize: 24,
  },
  cardContent: {
    flex: 1,
  },
  cardTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: colors.text,
    marginBottom: 4,
  },
  cardDate: {
    fontSize: 14,
    color: colors.textLight,
  },
  chevron: {
    fontSize: 24,
    color: colors.primary,
    fontWeight: '300',
  },
  emptyContainer: {
    alignItems: 'center',
    marginTop: spacing.xl,
  },
  empty: {
    textAlign: 'center',
    color: colors.textLight,
    marginBottom: spacing.md,
  },
});
