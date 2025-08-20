import { useEffect, useState } from 'react';
import { View, Text, StyleSheet, Pressable, FlatList } from 'react-native';
import { colors, spacing, radius, text } from '../theme';
import API from './api';
import ServiceCard from '../components/ServiceCard';

type Tab = 'vaccines' | 'medicines';

interface Vaccine { id: number; name: string; type?: string | null; age_group?: string | null; timing?: string | null; }
interface Medicine { id: number; name: string; description?: string | null; availability?: string | null; }

export default function Services() {
  const [tab, setTab] = useState<Tab>('vaccines');
  const [vaccines, setVaccines] = useState<Vaccine[]>([]);
  const [medicines, setMedicines] = useState<Medicine[]>([]);

  useEffect(() => {
    (async () => {
      try {
        const [vaxRes, medRes] = await Promise.all([
          API.get('/api/services/vaccines/'),
          API.get('/api/services/medicines/'),
        ]);
        setVaccines(vaxRes.data ?? []);
        setMedicines(medRes.data ?? []);
      } catch (e) {
        console.warn('Failed to load services', e);
      }
    })();
  }, []);

  const data = tab === 'vaccines' ? vaccines : medicines;

  return (
    <View style={styles.container}>
      <View style={styles.tabs}>
        <Pressable style={[styles.tab, tab === 'vaccines' && styles.tabActive]} onPress={() => setTab('vaccines')}>
          <Text style={[styles.tabText, tab === 'vaccines' && styles.tabTextActive]}>Vaccines</Text>
        </Pressable>
        <Pressable style={[styles.tab, tab === 'medicines' && styles.tabActive]} onPress={() => setTab('medicines')}>
          <Text style={[styles.tabText, tab === 'medicines' && styles.tabTextActive]}>Medicines</Text>
        </Pressable>
      </View>

      <FlatList
        contentContainerStyle={styles.listContent}
        style={{ flex: 1 }}
        data={data}
        keyExtractor={(item) => String(item.id)}
        renderItem={({ item }) => <ServiceCard item={item} type={tab} />}
        ListEmptyComponent={<Text style={styles.empty}>No data available.</Text>}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: 'transparent', padding: spacing.lg },
  tabs: { flexDirection: 'row', marginBottom: spacing.md, gap: spacing.sm },
  tab: { flex: 1, paddingVertical: spacing.sm, paddingHorizontal: spacing.md, borderRadius: radius.md, backgroundColor: colors.subtle, alignItems: 'center', borderWidth: 1, borderColor: colors.border },
  tabActive: { backgroundColor: colors.primary },
  tabText: { color: colors.text, fontWeight: '700' },
  tabTextActive: { color: colors.buttonTextOnPrimary },
  listContent: { paddingBottom: spacing.xl },
  empty: { textAlign: 'center', color: colors.textSubtle, marginTop: spacing.xl },
});
