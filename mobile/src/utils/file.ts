/**
 * Утилиты для работы с файлами
 */
import { Platform } from 'react-native';

export interface FileInfo {
  name: string;
  path: string;
  size: number;
  extension: string;
  mimeType: string;
  createdAt?: Date;
  modifiedAt?: Date;
}

/**
 * Получение информации о файле
 */
export async function getFileInfo(filePath: string): Promise<FileInfo | null> {
  try {
    // В реальном приложении используйте react-native-fs
    // import RNFS from 'react-native-fs';
    // const stat = await RNFS.stat(filePath);

    // return {
    //   name: stat.name,
    //   path: stat.path,
    //   size: stat.size,
    //   extension: getFileExtension(stat.name),
    //   mimeType: getMimeType(stat.name),
    //   createdAt: new Date(stat.ctime),
    //   modifiedAt: new Date(stat.mtime),
    // };

    // Заглушка
    return null;
  } catch (error) {
    console.error('Error getting file info:', error);
    return null;
  }
}

/**
 * Проверка существования файла
 */
export async function fileExists(filePath: string): Promise<boolean> {
  try {
    // В реальном приложении используйте react-native-fs
    // import RNFS from 'react-native-fs';
    // return await RNFS.exists(filePath);

    // Заглушка
    return false;
  } catch (error) {
    console.error('Error checking file existence:', error);
    return false;
  }
}

/**
 * Удаление файла
 */
export async function deleteFile(filePath: string): Promise<boolean> {
  try {
    // В реальном приложении используйте react-native-fs
    // import RNFS from 'react-native-fs';
    // await RNFS.unlink(filePath);
    // return true;

    // Заглушка
    return false;
  } catch (error) {
    console.error('Error deleting file:', error);
    return false;
  }
}

/**
 * Копирование файла
 */
export async function copyFile(
  sourcePath: string,
  destinationPath: string
): Promise<boolean> {
  try {
    // В реальном приложении используйте react-native-fs
    // import RNFS from 'react-native-fs';
    // await RNFS.copyFile(sourcePath, destinationPath);
    // return true;

    // Заглушка
    return false;
  } catch (error) {
    console.error('Error copying file:', error);
    return false;
  }
}

/**
 * Перемещение файла
 */
export async function moveFile(
  sourcePath: string,
  destinationPath: string
): Promise<boolean> {
  try {
    // В реальном приложении используйте react-native-fs
    // import RNFS from 'react-native-fs';
    // await RNFS.moveFile(sourcePath, destinationPath);
    // return true;

    // Заглушка
    return false;
  } catch (error) {
    console.error('Error moving file:', error);
    return false;
  }
}

/**
 * Чтение файла как текста
 */
export async function readFileAsText(filePath: string): Promise<string | null> {
  try {
    // В реальном приложении используйте react-native-fs
    // import RNFS from 'react-native-fs';
    // const content = await RNFS.readFile(filePath, 'utf8');
    // return content;

    // Заглушка
    return null;
  } catch (error) {
    console.error('Error reading file:', error);
    return null;
  }
}

/**
 * Запись текста в файл
 */
export async function writeTextToFile(
  filePath: string,
  content: string
): Promise<boolean> {
  try {
    // В реальном приложении используйте react-native-fs
    // import RNFS from 'react-native-fs';
    // await RNFS.writeFile(filePath, content, 'utf8');
    // return true;

    // Заглушка
    return false;
  } catch (error) {
    console.error('Error writing file:', error);
    return false;
  }
}

/**
 * Получение расширения файла
 */
export function getFileExtension(fileName: string): string {
  const parts = fileName.split('.');
  return parts.length > 1 ? parts[parts.length - 1].toLowerCase() : '';
}

/**
 * Получение MIME типа по расширению
 */
export function getMimeType(fileName: string): string {
  const extension = getFileExtension(fileName);

  const mimeTypes: Record<string, string> = {
    // Изображения
    jpg: 'image/jpeg',
    jpeg: 'image/jpeg',
    png: 'image/png',
    gif: 'image/gif',
    webp: 'image/webp',
    svg: 'image/svg+xml',
    // Документы
    pdf: 'application/pdf',
    doc: 'application/msword',
    docx: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    xls: 'application/vnd.ms-excel',
    xlsx: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    ppt: 'application/vnd.ms-powerpoint',
    pptx: 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    // Текстовые файлы
    txt: 'text/plain',
    json: 'application/json',
    xml: 'application/xml',
    csv: 'text/csv',
    // Видео
    mp4: 'video/mp4',
    avi: 'video/x-msvideo',
    mov: 'video/quicktime',
    // Аудио
    mp3: 'audio/mpeg',
    wav: 'audio/wav',
    // Архивы
    zip: 'application/zip',
    rar: 'application/x-rar-compressed',
    '7z': 'application/x-7z-compressed',
  };

  return mimeTypes[extension] || 'application/octet-stream';
}

/**
 * Получение директории для временных файлов
 */
export function getTemporaryDirectory(): string {
  // В реальном приложении используйте react-native-fs
  // import RNFS from 'react-native-fs';
  // return RNFS.TemporaryDirectoryPath;

  // Заглушка
  return Platform.OS === 'ios' ? '/tmp' : '/data/tmp';
}

/**
 * Получение директории для документов
 */
export function getDocumentsDirectory(): string {
  // В реальном приложении используйте react-native-fs
  // import RNFS from 'react-native-fs';
  // return RNFS.DocumentDirectoryPath;

  // Заглушка
  return Platform.OS === 'ios' ? '/Documents' : '/data/Documents';
}

/**
 * Получение директории для кэша
 */
export function getCacheDirectory(): string {
  // В реальном приложении используйте react-native-fs
  // import RNFS from 'react-native-fs';
  // return RNFS.CachesDirectoryPath;

  // Заглушка
  return Platform.OS === 'ios' ? '/Library/Caches' : '/data/cache';
}

/**
 * Форматирование размера файла
 */
export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Б';

  const k = 1024;
  const sizes = ['Б', 'КБ', 'МБ', 'ГБ', 'ТБ'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`;
}

/**
 * Создание директории
 */
export async function createDirectory(directoryPath: string): Promise<boolean> {
  try {
    // В реальном приложении используйте react-native-fs
    // import RNFS from 'react-native-fs';
    // await RNFS.mkdir(directoryPath);
    // return true;

    // Заглушка
    return false;
  } catch (error) {
    console.error('Error creating directory:', error);
    return false;
  }
}

/**
 * Получение списка файлов в директории
 */
export async function readDirectory(directoryPath: string): Promise<string[]> {
  try {
    // В реальном приложении используйте react-native-fs
    // import RNFS from 'react-native-fs';
    // const files = await RNFS.readDir(directoryPath);
    // return files.map((file) => file.name);

    // Заглушка
    return [];
  } catch (error) {
    console.error('Error reading directory:', error);
    return [];
  }
}

/**
 * Очистка временных файлов
 */
export async function clearTemporaryFiles(): Promise<number> {
  try {
    const tempDir = getTemporaryDirectory();
    const files = await readDirectory(tempDir);
    let deletedCount = 0;

    for (const file of files) {
      const filePath = `${tempDir}/${file}`;
      const deleted = await deleteFile(filePath);
      if (deleted) deletedCount++;
    }

    return deletedCount;
  } catch (error) {
    console.error('Error clearing temporary files:', error);
    return 0;
  }
}
