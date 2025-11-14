/**
 * Экран регистрации
 */
import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  ScrollView,
} from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { register } from '../store/slices/authSlice';
import { AppDispatch, RootState } from '../store/store';

const RegisterScreen = ({ navigation }: any) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [phone, setPhone] = useState('');
  const [position, setPosition] = useState('');
  const [company, setCompany] = useState('');

  const dispatch = useDispatch<AppDispatch>();
  const { loading, error } = useSelector((state: RootState) => state.auth);

  const [validationError, setValidationError] = useState('');

  const handleRegister = async () => {
    // Валидация
    if (!email || !password || !fullName) {
      setValidationError('Заполните обязательные поля');
      return;
    }

    if (password !== confirmPassword) {
      setValidationError('Пароли не совпадают');
      return;
    }

    if (password.length < 8) {
      setValidationError('Пароль должен содержать минимум 8 символов');
      return;
    }

    setValidationError('');

    try {
      await dispatch(
        register({
          email,
          password,
          full_name: fullName,
          phone,
          position,
          company,
          role: 'engineer',
        })
      ).unwrap();

      // После успешной регистрации переходим на экран входа
      navigation.navigate('Login');
    } catch (err) {
      console.error('Registration failed:', err);
    }
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <Text style={styles.title}>Регистрация</Text>
        <Text style={styles.subtitle}>Создайте аккаунт в ТехНадзор</Text>
      </View>

      <View style={styles.form}>
        <Text style={styles.label}>
          Email <Text style={styles.required}>*</Text>
        </Text>
        <TextInput
          style={styles.input}
          placeholder="email@example.com"
          value={email}
          onChangeText={setEmail}
          keyboardType="email-address"
          autoCapitalize="none"
        />

        <Text style={styles.label}>
          ФИО <Text style={styles.required}>*</Text>
        </Text>
        <TextInput
          style={styles.input}
          placeholder="Иван Иванов"
          value={fullName}
          onChangeText={setFullName}
        />

        <Text style={styles.label}>Телефон</Text>
        <TextInput
          style={styles.input}
          placeholder="+7 (999) 123-45-67"
          value={phone}
          onChangeText={setPhone}
          keyboardType="phone-pad"
        />

        <Text style={styles.label}>Должность</Text>
        <TextInput
          style={styles.input}
          placeholder="Старший инженер"
          value={position}
          onChangeText={setPosition}
        />

        <Text style={styles.label}>Компания</Text>
        <TextInput
          style={styles.input}
          placeholder="ООО 'Стройка'"
          value={company}
          onChangeText={setCompany}
        />

        <Text style={styles.label}>
          Пароль <Text style={styles.required}>*</Text>
        </Text>
        <TextInput
          style={styles.input}
          placeholder="Минимум 8 символов"
          value={password}
          onChangeText={setPassword}
          secureTextEntry
        />

        <Text style={styles.label}>
          Подтвердите пароль <Text style={styles.required}>*</Text>
        </Text>
        <TextInput
          style={styles.input}
          placeholder="Повторите пароль"
          value={confirmPassword}
          onChangeText={setConfirmPassword}
          secureTextEntry
        />

        {(validationError || error) && (
          <Text style={styles.error}>{validationError || error}</Text>
        )}

        <TouchableOpacity
          style={styles.button}
          onPress={handleRegister}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.buttonText}>Зарегистрироваться</Text>
          )}
        </TouchableOpacity>

        <TouchableOpacity
          onPress={() => navigation.navigate('Login')}
          style={styles.linkButton}
        >
          <Text style={styles.linkText}>Уже есть аккаунт? Войти</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F9FAFB',
  },
  content: {
    padding: 20,
    paddingTop: 40,
  },
  header: {
    marginBottom: 30,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#1E3A8A',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#6B7280',
  },
  form: {
    backgroundColor: '#fff',
    padding: 24,
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  label: {
    fontSize: 14,
    fontWeight: '600',
    color: '#374151',
    marginBottom: 8,
  },
  required: {
    color: '#EF4444',
  },
  input: {
    borderWidth: 1,
    borderColor: '#D1D5DB',
    borderRadius: 8,
    padding: 12,
    marginBottom: 16,
    fontSize: 16,
  },
  button: {
    backgroundColor: '#1E3A8A',
    padding: 16,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 8,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  linkButton: {
    marginTop: 16,
    alignItems: 'center',
  },
  linkText: {
    color: '#1E3A8A',
    fontSize: 14,
  },
  error: {
    color: '#EF4444',
    fontSize: 14,
    marginBottom: 12,
  },
});

export default RegisterScreen;
