import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, FlatList, TouchableOpacity, Alert } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useAppStore } from '../store/useAppStore';
import apiClient from '../api/client';
import { Figur, Wettkampf } from '../types';
import { Button } from '../components/Button';

// Extended type for this screen logic
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
      // Need to fetch details of the competition to get associated figures
      // Endpoint: /wettkampf/{id} which should return WettkampfWithDetails
      const response = await apiClient.get(`/wettkampf/${selectedWettkampf.id}`);
      const detail: WettkampfDetail = response.data;
      
      if (detail.figuren) {
        setAvailableFiguren(detail.figuren);
      } else {
        // Fallback or error handling if no figures attached
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
    // navigation.navigate('RatingScreen'); // Next step
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
        <View style={{ width: 60 }} />{/* Spacer for alignment */}
      </View>

      <FlatList
        data={availableFiguren}
        renderItem={renderItem}
        keyExtractor={(item) => item.id.toString()}
        contentContainerStyle={styles.list}
        refreshing={loading}
        onRefresh={loadFigures}
        ListEmptyComponent={
          <Text style={styles.empty}>Keine Figuren für diesen Wettkampf definiert.</Text>
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
    padding: 16,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: 'white',
    borderBottomWidth: 1,
    borderBottomColor: '#e2e8f0',
  },
  headerInfo: {
    alignItems: 'center',
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#0f172a',
  },
  subTitle: {
    fontSize: 12,
    color: '#64748b',
    marginBottom: 2,
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
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  cardTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#0f172a',
    flex: 1,
    marginRight: 8,
  },
  difficulty: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#0ea5e9',
    backgroundColor: '#e0f2fe',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 6,
  },
  cardDesc: {
    fontSize: 14,
    color: '#64748b',
  },
  empty: {
    textAlign: 'center',
    marginTop: 40,
    color: '#94a3b8',
  },
});
