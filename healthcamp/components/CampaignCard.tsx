import { useState } from 'react';
import { View, Text, StyleSheet, Pressable } from 'react-native';
import { colors, spacing, radius, shadow, text } from '../theme';
import FrostedCard from './FrostedCard';
import { useRouter, Link } from 'expo-router';

type Props = {
  campaign: {
    id: number;
    title: string;
    timing?: string | null;
    location?: string | null;
    helpline?: string | null;
    vaccines?: { id: number; name: string; type?: string | null; age_group?: string | null; timing?: string | null }[];
    medicines?: { id: number; name: string; type?: string | null; age_group?: string | null; description?: string | null; availability?: string | null }[];
  };
  onRegister?: (campaignId: number) => void;
};

export default function CampaignCard({ campaign, onRegister }: Props) {
  const [showServices, setShowServices] = useState(false);
  const router = useRouter();
  return (
    <FrostedCard style={styles.cardOuter}>
      <Text style={styles.title}>{campaign.title}</Text>
      {campaign.timing ? <Text style={styles.meta}>⏰ {campaign.timing}</Text> : null}
      {campaign.location ? <Text style={styles.meta}>📍 {campaign.location}</Text> : null}
      {campaign.helpline ? <Text style={styles.meta}>☎️ {campaign.helpline}</Text> : null}

      {(campaign.vaccines?.length || campaign.medicines?.length) ? (
        <View style={{ marginTop: spacing.sm }}>
          <Pressable onPress={() => setShowServices((v) => !v)} style={({ pressed }) => [styles.toggle, { opacity: pressed ? 0.95 : 1 }] }>
            <Text style={styles.toggleText}>{showServices ? 'Hide' : 'Show'} Services</Text>
          </Pressable>
          {showServices ? (
            <View style={styles.servicesBox}>
              {campaign.vaccines && campaign.vaccines.length > 0 ? (
                <View style={styles.serviceGroup}>
                  <Text style={styles.groupTitle}>Vaccines</Text>
                  {campaign.vaccines.map((v) => (
                    <Text key={`v-${v.id}`} style={styles.serviceItem}>• {v.name}{v.type ? ` (${v.type})` : ''}{v.age_group ? ` • ${v.age_group}` : ''}{v.timing ? ` • ${v.timing}` : ''}</Text>
                  ))}
                </View>
              ) : null}
              {campaign.medicines && campaign.medicines.length > 0 ? (
                <View style={styles.serviceGroup}>
                  <Text style={styles.groupTitle}>Medicines</Text>
                  {campaign.medicines.map((m) => (
                    <Text key={`m-${m.id}`} style={styles.serviceItem}>• {m.name}{m.type ? ` (${m.type})` : ''}{m.age_group ? ` • ${m.age_group}` : ''}{m.availability ? ` • ${m.availability}` : ''}{m.description ? ` — ${m.description}` : ''}</Text>
                  ))}
                </View>
              ) : null}
            </View>
          ) : null}
        </View>
      ) : null}

      <View style={styles.row}>
        <Link href={{ pathname: '/campaign/[id]', params: { id: String(campaign.id) } } as any} asChild>
          <Pressable style={({ pressed }) => [
            styles.btn,
            styles.btnGhost,
            { opacity: pressed ? 0.96 : 1, transform: [{ scale: pressed ? 0.98 : 1 }] },
          ] }>
            <Text style={styles.btnGhostText}>View Details</Text>
          </Pressable>
        </Link>
        <Pressable
          onPress={() => onRegister?.(campaign.id)}
          style={({ pressed }) => [
            styles.btn,
            styles.btnPrimary,
            { opacity: pressed ? 0.96 : 1, transform: [{ scale: pressed ? 0.98 : 1 }] },
          ]}
        >
          <Text style={styles.btnPrimaryText}>Register</Text>
        </Pressable>
      </View>
    </FrostedCard>
  );
}

const styles = StyleSheet.create({
  cardOuter: { padding: 0 },
  title: { ...text.title, marginBottom: spacing.xs },
  meta: { ...text.muted, marginTop: spacing.xs },
  toggle: { alignSelf: 'flex-start', marginTop: spacing.xs, backgroundColor: colors.subtle, paddingHorizontal: spacing.md, paddingVertical: spacing.xs, borderRadius: radius.sm, borderWidth: 1, borderColor: colors.border },
  toggleText: { ...text.button },
  servicesBox: { marginTop: spacing.sm, backgroundColor: colors.subtle, borderWidth: 1, borderColor: colors.border, borderRadius: radius.md, padding: spacing.md },
  serviceGroup: { marginTop: spacing.xs },
  groupTitle: { fontWeight: '800', color: colors.text, marginBottom: spacing.xs },
  serviceItem: { color: colors.textMuted, marginTop: 2 },
  row: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', gap: spacing.sm, marginTop: spacing.md },
  btn: { paddingVertical: spacing.sm, paddingHorizontal: spacing.md, borderRadius: radius.md },
  btnPrimary: { backgroundColor: colors.primary },
  btnPrimaryText: { ...text.buttonPrimary },
  btnGhost: { backgroundColor: colors.primarySoft },
  btnGhostText: { ...text.button },
});

