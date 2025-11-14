# Инструкция по установке - ТехНадзор Mobile

## 📋 Требования

### Системные требования
- **Node.js:** >= 18.0.0
- **npm:** >= 9.0.0
- **React Native CLI:** Установлен глобально
- **Xcode:** >= 14.0 (для iOS)
- **Android Studio:** >= 2022.1.1 (для Android)
- **JDK:** >= 11

### Проверка версий
```bash
node --version  # должно быть >= 18.0.0
npm --version   # должно быть >= 9.0.0
```

---

## 🚀 Установка

### 1. Клонирование репозитория
```bash
git clone https://github.com/your-repo/StroiNadzor.git
cd StroiNadzor/mobile
```

### 2. Установка зависимостей
```bash
npm install
```

### 3. Установка дополнительных пакетов

Некоторые нативные библиотеки требуют дополнительной настройки:

#### iOS (только для Mac)
```bash
cd ios
pod install
cd ..
```

#### Android
Убедитесь, что у вас установлен Android SDK через Android Studio.

---

## 📦 Конфигурация

### 1. Конфигурация API
Создайте файл `.env` в корне mobile директории:

```env
API_BASE_URL=http://localhost:8000
API_TIMEOUT=30000
ENABLE_OFFLINE_MODE=true
```

### 2. Настройка Google Maps (для компонентов карт)

#### Android
Добавьте API ключ в `android/app/src/main/AndroidManifest.xml`:
```xml
<application>
  <meta-data
    android:name="com.google.android.geo.API_KEY"
    android:value="YOUR_GOOGLE_MAPS_API_KEY"/>
</application>
```

#### iOS
Добавьте API ключ в `ios/TehNadzorMobile/AppDelegate.mm`:
```objc
#import <GoogleMaps/GoogleMaps.h>

- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions
{
  [GMSServices provideAPIKey:@"YOUR_GOOGLE_MAPS_API_KEY"];
  // ...
}
```

### 3. Настройка разрешений

#### Android (`android/app/src/main/AndroidManifest.xml`)
```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
```

#### iOS (`ios/TehNadzorMobile/Info.plist`)
```xml
<key>NSLocationWhenInUseUsageDescription</key>
<string>Приложению нужен доступ к геолокации для фотофиксации объектов</string>
<key>NSCameraUsageDescription</key>
<string>Приложению нужен доступ к камере для съемки объектов</string>
<key>NSPhotoLibraryUsageDescription</key>
<string>Приложению нужен доступ к галерее для сохранения фотографий</string>
```

---

## 🏃 Запуск

### Запуск Metro Bundler
```bash
npm start
```

### Запуск на Android
```bash
npm run android
```

### Запуск на iOS (только Mac)
```bash
npm run ios
```

---

## 🗄️ WatermelonDB

### Инициализация базы данных
При первом запуске приложения база данных WatermelonDB будет автоматически создана.

### Сброс базы данных (для разработки)
```javascript
import { resetDatabase } from './src/database';

// В режиме разработки
if (__DEV__) {
  await resetDatabase();
}
```

---

## 📊 Компоненты требующие дополнительной настройки

### 1. Charts (react-native-chart-kit)
Уже установлен и настроен. Требует `react-native-svg`.

```bash
# Если возникают проблемы
npm install react-native-svg
cd ios && pod install
```

### 2. Maps (react-native-maps)
Требует API ключ Google Maps (см. выше).

```bash
# Android: автоматически устанавливается
# iOS: требует pod install
cd ios && pod install
```

### 3. PDF Viewer (react-native-pdf)
```bash
# iOS: требует pod install
cd ios && pod install
```

### 4. File System (react-native-fs)
```bash
# iOS: требует pod install
cd ios && pod install
```

---

## 🔧 Troubleshooting

### Проблема: "Unable to resolve module"
```bash
# Очистите кэш Metro
npm start -- --reset-cache

# Или переустановите зависимости
npm run clean
```

### Проблема: iOS build fails
```bash
cd ios
rm -rf Pods Podfile.lock
pod install
cd ..
```

### Проблема: Android build fails
```bash
cd android
./gradlew clean
cd ..
```

### Проблема: WatermelonDB JSI error
Убедитесь, что используете последнюю версию React Native (>= 0.72):
```bash
# Проверьте версию в package.json
```

### Проблема: Google Maps не отображается
1. Проверьте API ключ
2. Убедитесь, что включены Google Maps SDK для Android/iOS
3. Проверьте разрешения в манифесте

---

## 📱 Тестирование

### Запуск тестов
```bash
npm test
```

### Запуск с coverage
```bash
npm test -- --coverage
```

---

## 🏗️ Build для Production

### Android APK
```bash
cd android
./gradlew assembleRelease
# APK: android/app/build/outputs/apk/release/app-release.apk
```

### Android Bundle (для Google Play)
```bash
cd android
./gradlew bundleRelease
# Bundle: android/app/build/outputs/bundle/release/app-release.aab
```

### iOS (требует Mac + Xcode)
```bash
# Открыть в Xcode
open ios/TehNadzorMobile.xcworkspace

# Выбрать схему "Release" и собрать
```

---

## 📚 Дополнительные ресурсы

- [React Native Documentation](https://reactnative.dev/)
- [WatermelonDB Documentation](https://nozbe.github.io/WatermelonDB/)
- [React Navigation](https://reactnavigation.org/)
- [Redux Toolkit](https://redux-toolkit.js.org/)

---

## ⚠️ Важные замечания

1. **WatermelonDB JSI** - Требует React Native >= 0.72 и включенного New Architecture
2. **Google Maps** - Бесплатный tier имеет лимиты, используйте billing account для production
3. **Permissions** - Всегда запрашивайте разрешения перед использованием (см. `src/utils/permissions.ts`)
4. **Offline Mode** - Автоматическая синхронизация каждые 15 минут (настраивается в `src/services/sync.ts`)

---

**Последнее обновление:** 08.11.2025
**Версия:** 1.2.0
