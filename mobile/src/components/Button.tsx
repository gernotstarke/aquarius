import React from 'react';
import { TouchableOpacity, Text, StyleSheet, ActivityIndicator } from 'react-native';

interface ButtonProps {
  title: string;
  onPress: () => void;
  variant?: 'primary' | 'secondary' | 'outline';
  loading?: boolean;
  disabled?: boolean;
}

export const Button: React.FC<ButtonProps> = ({ 
  title, 
  onPress, 
  variant = 'primary', 
  loading = false,
  disabled = false 
}) => {
  return (
    <TouchableOpacity 
      style={[
        styles.container, 
        styles[variant], 
        disabled && styles.disabled
      ]} 
      onPress={onPress}
      disabled={disabled || loading}
    >
      {loading ? (
        <ActivityIndicator color={variant === 'outline' ? '#0ea5e9' : 'white'} />
      ) : (
        <Text style={[styles.text, variant === 'outline' && styles.textOutline]}>
          {title}
        </Text>
      )}
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    paddingVertical: 12,
    paddingHorizontal: 16,
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: 48,
  },
  primary: {
    backgroundColor: '#0ea5e9', // primary-500
  },
  secondary: {
    backgroundColor: '#64748b', // neutral-500
  },
  outline: {
    backgroundColor: 'transparent',
    borderWidth: 1,
    borderColor: '#0ea5e9',
  },
  disabled: {
    opacity: 0.6,
  },
  text: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
  },
  textOutline: {
    color: '#0ea5e9',
  },
});
