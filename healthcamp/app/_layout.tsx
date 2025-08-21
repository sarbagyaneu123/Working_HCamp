import 'react-native-gesture-handler';
import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaView } from 'react-native-safe-area-context';
import { View, StyleSheet } from 'react-native';
import { colors, gradients } from '../theme';

export default function Layout() {
  // Use expo-linear-gradient if available; fallback to a normal View to avoid crashes
  // eslint-disable-next-line @typescript-eslint/no-var-requires
  let LinearGradientComp: any = View;
  try {
    const pkg = 'expo-linear-gradient';
    // eslint-disable-next-line @typescript-eslint/no-var-requires
    const { LinearGradient } = require(pkg);
    LinearGradientComp = LinearGradient;
  } catch (e) {
    // gradient package not installed; fallback gracefully
  }
  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: 'transparent' }}>
      <StatusBar style="dark" />
      <View style={{ flex: 1 }}>
        <LinearGradientComp
          colors={gradients.appBg as any}
          start={{ x: 0, y: 0 }}
          end={{ x: 0, y: 1 }}
          style={StyleSheet.absoluteFill}
        />
        <Stack
          screenOptions={{
            headerShown: true,
            headerShadowVisible: false,
            headerStyle: { backgroundColor: colors.background },
            contentStyle: { backgroundColor: 'transparent' },
          }}
        >
          <Stack.Screen
            name="index"
            options={{
              title: 'eArogya HealthCamp',
              headerTitleAlign: 'center',
              headerTitleStyle: { fontWeight: '800' },
            }}
          />
          <Stack.Screen
            name="health-campaigns"
            options={{
              title: 'HEALTH CAMPAIGNS',
              headerTitleAlign: 'center',
              headerTitleStyle: { fontWeight: '800' },
            }}
          />
          <Stack.Screen
            name="my-registrations"
            options={{
              title: 'MY REGISTRATIONS',
              headerTitleAlign: 'center',
              headerTitleStyle: { fontWeight: '800' },
            }}
          />
        </Stack>
      </View>
    </SafeAreaView>
  );
}
