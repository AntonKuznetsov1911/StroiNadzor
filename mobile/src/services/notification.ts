/**
 * Сервис уведомлений
 */
import { Platform, Alert } from 'react-native';

export interface LocalNotification {
  id: string;
  title: string;
  message: string;
  data?: any;
  scheduledTime?: Date;
}

class NotificationService {
  /**
   * Запрос разрешения на уведомления
   */
  async requestPermission(): Promise<boolean> {
    // В реальном приложении используйте @react-native-community/push-notification-ios
    // или react-native-push-notification

    // if (Platform.OS === 'ios') {
    //   const authStatus = await messaging().requestPermission();
    //   const enabled =
    //     authStatus === messaging.AuthorizationStatus.AUTHORIZED ||
    //     authStatus === messaging.AuthorizationStatus.PROVISIONAL;
    //   return enabled;
    // }

    return true; // Заглушка
  }

  /**
   * Отправка локального уведомления
   */
  async sendLocalNotification(notification: LocalNotification): Promise<void> {
    // В реальном приложении используйте react-native-push-notification

    // PushNotification.localNotification({
    //   id: notification.id,
    //   title: notification.title,
    //   message: notification.message,
    //   userInfo: notification.data,
    //   date: notification.scheduledTime,
    // });

    console.log('Local notification sent:', notification);
  }

  /**
   * Планирование уведомления
   */
  async scheduleNotification(
    notification: LocalNotification,
    scheduledTime: Date
  ): Promise<void> {
    // PushNotification.localNotificationSchedule({
    //   id: notification.id,
    //   title: notification.title,
    //   message: notification.message,
    //   date: scheduledTime,
    //   userInfo: notification.data,
    // });

    console.log('Notification scheduled:', notification, scheduledTime);
  }

  /**
   * Отмена уведомления
   */
  async cancelNotification(notificationId: string): Promise<void> {
    // PushNotification.cancelLocalNotifications({ id: notificationId });

    console.log('Notification cancelled:', notificationId);
  }

  /**
   * Отмена всех уведомлений
   */
  async cancelAllNotifications(): Promise<void> {
    // PushNotification.cancelAllLocalNotifications();

    console.log('All notifications cancelled');
  }

  /**
   * Получение FCM токена для push-уведомлений
   */
  async getFCMToken(): Promise<string | null> {
    // В реальном приложении используйте @react-native-firebase/messaging

    // const token = await messaging().getToken();
    // return token;

    return null; // Заглушка
  }

  /**
   * Подписка на получение уведомлений
   */
  onNotificationReceived(callback: (notification: any) => void): () => void {
    // В реальном приложении используйте @react-native-firebase/messaging

    // const unsubscribe = messaging().onMessage(async (remoteMessage) => {
    //   callback(remoteMessage);
    // });

    // return unsubscribe;

    return () => {}; // Заглушка
  }

  /**
   * Обработка нажатия на уведомление
   */
  onNotificationOpened(callback: (notification: any) => void): () => void {
    // messaging().onNotificationOpenedApp((remoteMessage) => {
    //   callback(remoteMessage);
    // });

    // messaging()
    //   .getInitialNotification()
    //   .then((remoteMessage) => {
    //     if (remoteMessage) {
    //       callback(remoteMessage);
    //     }
    //   });

    return () => {}; // Заглушка
  }

  /**
   * Уведомление о новой проверке
   */
  async notifyNewInspection(
    projectName: string,
    inspectionDate: Date
  ): Promise<void> {
    await this.sendLocalNotification({
      id: `inspection_${Date.now()}`,
      title: 'Новая проверка назначена',
      message: `Проверка на объекте "${projectName}" назначена на ${inspectionDate.toLocaleDateString()}`,
    });
  }

  /**
   * Уведомление о критическом дефекте
   */
  async notifyCriticalDefect(defectType: string): Promise<void> {
    await this.sendLocalNotification({
      id: `defect_${Date.now()}`,
      title: 'Обнаружен критический дефект!',
      message: `ML-модель обнаружила критический дефект: ${defectType}`,
    });
  }

  /**
   * Уведомление о скрытых работах
   */
  async notifyHiddenWork(workType: string, location: string): Promise<void> {
    await this.sendLocalNotification({
      id: `hidden_work_${Date.now()}`,
      title: 'Скрытые работы требуют проверки',
      message: `${workType} в ${location} готовы к освидетельствованию`,
    });
  }

  /**
   * Напоминание о проверке
   */
  async scheduleInspectionReminder(
    projectName: string,
    inspectionDate: Date
  ): Promise<void> {
    // Напоминание за день до проверки
    const reminderTime = new Date(inspectionDate);
    reminderTime.setDate(reminderTime.getDate() - 1);
    reminderTime.setHours(9, 0, 0, 0);

    await this.scheduleNotification(
      {
        id: `reminder_${Date.now()}`,
        title: 'Напоминание о проверке',
        message: `Завтра проверка на объекте "${projectName}"`,
      },
      reminderTime
    );
  }
}

// Singleton экземпляр
export const notificationService = new NotificationService();
