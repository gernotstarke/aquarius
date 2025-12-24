import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, FlatList, TouchableOpacity, Alert } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useAppStore } from '../store/useAppStore';
import apiClient from '../api/client';
import { Figur, Wettkampf } from '../types';
import { Button } from '../components/Button';
import { colors, layout, spacing } from '../theme';

interface WettkampfDetail extends Wettkampf {
  figuren: Figur[];
}

export const FigureSelectionScreen = () => {
  const navigation = useNavigation();
  const [loading, setLoading] = useState(false);
  const [availableFiguren, setAvailableFiguren] = useState<Figur[]>([]);
  const { selectedWettkampf, selectFigur } = useAppStore();

  const loadFigures = async () => {
    if (!selectedWettkampf) return;
    
    setLoading(true);
    try {
      const response = await apiClient.get(`/wettkampf/${selectedWettkampf.id}`);
      const detail: WettkampfDetail = response.data;
      
      if (detail.figuren) {
        setAvailableFiguren(detail.figuren);
      } else {
        setAvailableFiguren([]);
      }
    } catch (error) {
      Alert.alert('Fehler', 'Figuren konnten nicht geladen werden.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadFigures();
  }, [selectedWettkampf]);

  const handleSelect = (figur: Figur) => {
    selectFigur(figur);
    Alert.alert('Info', `Figur "${figur.name}" gewählt. Bewertungs-Screen folgt.`);
  };

  const renderItem = ({ item }: { item: Figur }) => (
    <TouchableOpacity 
      style={styles.card} 
      onPress={() => handleSelect(item)}
    >
      <View style={styles.cardHeader}>
        <Text style={styles.cardTitle}>{item.name}</Text>
        <Text style={styles.difficulty}>{item.schwierigkeitsgrad ? (item.schwierigkeitsgrad / 10).toFixed(1) : '-'}</Text>
      </View>
      <Text style={styles.cardDesc} numberOfLines={2}>{item.beschreibung}</Text>
    </TouchableOpacity>
  );

  if (!selectedWettkampf) {
    return <View style={styles.container}><Text>Kein Wettkampf gewählt</Text></View>;
  }

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Button 
          title="Zurück" 
          variant="outline" 
          onPress={() => navigation.goBack()} 
        />
        <View style={styles.headerInfo}>
          <Text style={styles.subTitle}>{selectedWettkampf.name}</Text>
          <Text style={styles.title}>Figur wählen</Text>
        </View>
        <View style={{ width: 80 }} />
      </View>

      <FlatList
        data={availableFiguren}
        renderItem={renderItem}
        keyExtractor={(item) => item.id.toString()}
        contentContainerStyle={styles.list}
        refreshing={loading}
        onRefresh={loadFigures}
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Text style={styles.empty}>Keine Figuren definiert.</Text>
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
    padding: spacing.md,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: colors.surface,
    borderBottomWidth: 1,
    borderBottomColor: colors.primaryLight,
  },
  headerInfo: {
    alignItems: 'center',
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    color: colors.text,
  },
  subTitle: {
    fontSize: 12,
    color: colors.textLight,
    marginBottom: 2,
  },
  list: {
    padding: spacing.lg,
  },
  card: {
    backgroundColor: colors.surface,
    padding: spacing.lg,
    borderRadius: layout.borderRadius,
    marginBottom: spacing.md,
    shadowColor: colors.primary,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 8,
    elevation: 2,
    borderLeftWidth: 4,
    borderLeftColor: colors.primary,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: spacing.sm,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: colors.text,
    flex: 1,
    marginRight: spacing.sm,
  },
  difficulty: {
    fontSize: 16,
    fontWeight: 'bold',
    color: colors.primary,
    backgroundColor: colors.primaryLight,
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
    overflow: 'hidden',
  },
  cardDesc: {
    fontSize: 14,
    color: colors.textLight,
    lineHeight: 20,
  },
  emptyContainer: {
    marginTop: spacing.xl,
    alignItems: 'center',
  },
  empty: {
    textAlign: 'center',
    color: colors.textLight,
  },
});
