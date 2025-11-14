/**
 * Hook для работы с формами
 */
import { useState, useCallback } from 'react';

export interface FormErrors {
  [key: string]: string;
}

export interface UseFormOptions<T> {
  initialValues: T;
  validate?: (values: T) => FormErrors;
  onSubmit: (values: T) => void | Promise<void>;
}

export function useForm<T extends Record<string, any>>({
  initialValues,
  validate,
  onSubmit,
}: UseFormOptions<T>) {
  const [values, setValues] = useState<T>(initialValues);
  const [errors, setErrors] = useState<FormErrors>({});
  const [touched, setTouched] = useState<Record<string, boolean>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  /**
   * Изменение значения поля
   */
  const handleChange = useCallback(
    (name: keyof T, value: any) => {
      setValues((prev) => ({
        ...prev,
        [name]: value,
      }));

      // Очищаем ошибку при изменении
      if (errors[name as string]) {
        setErrors((prev) => {
          const newErrors = { ...prev };
          delete newErrors[name as string];
          return newErrors;
        });
      }
    },
    [errors]
  );

  /**
   * Установка значения поля как "тронутое"
   */
  const handleBlur = useCallback((name: keyof T) => {
    setTouched((prev) => ({
      ...prev,
      [name]: true,
    }));
  }, []);

  /**
   * Валидация формы
   */
  const validateForm = useCallback((): boolean => {
    if (!validate) return true;

    const validationErrors = validate(values);
    setErrors(validationErrors);

    return Object.keys(validationErrors).length === 0;
  }, [validate, values]);

  /**
   * Отправка формы
   */
  const handleSubmit = useCallback(async () => {
    // Помечаем все поля как тронутые
    const allTouched = Object.keys(values).reduce(
      (acc, key) => ({ ...acc, [key]: true }),
      {}
    );
    setTouched(allTouched);

    // Валидация
    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);

    try {
      await onSubmit(values);
    } catch (error) {
      console.error('Form submission error:', error);
    } finally {
      setIsSubmitting(false);
    }
  }, [values, validateForm, onSubmit]);

  /**
   * Сброс формы
   */
  const reset = useCallback(() => {
    setValues(initialValues);
    setErrors({});
    setTouched({});
    setIsSubmitting(false);
  }, [initialValues]);

  /**
   * Установка значений формы
   */
  const setFormValues = useCallback((newValues: Partial<T>) => {
    setValues((prev) => ({
      ...prev,
      ...newValues,
    }));
  }, []);

  /**
   * Установка ошибок формы
   */
  const setFormErrors = useCallback((newErrors: FormErrors) => {
    setErrors(newErrors);
  }, []);

  /**
   * Получение ошибки для поля
   */
  const getFieldError = useCallback(
    (name: keyof T): string | undefined => {
      return touched[name as string] ? errors[name as string] : undefined;
    },
    [errors, touched]
  );

  /**
   * Проверка, есть ли ошибка у поля
   */
  const hasFieldError = useCallback(
    (name: keyof T): boolean => {
      return Boolean(getFieldError(name));
    },
    [getFieldError]
  );

  /**
   * Проверка, изменилась ли форма
   */
  const isDirty = useCallback((): boolean => {
    return JSON.stringify(values) !== JSON.stringify(initialValues);
  }, [values, initialValues]);

  /**
   * Проверка, валидна ли форма
   */
  const isValid = useCallback((): boolean => {
    if (!validate) return true;
    const validationErrors = validate(values);
    return Object.keys(validationErrors).length === 0;
  }, [validate, values]);

  return {
    values,
    errors,
    touched,
    isSubmitting,
    handleChange,
    handleBlur,
    handleSubmit,
    reset,
    setFormValues,
    setFormErrors,
    getFieldError,
    hasFieldError,
    isDirty: isDirty(),
    isValid: isValid(),
  };
}
