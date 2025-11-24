# Деплой ТехНадзор на Render.com

## Автоматический деплой (1 клик!)

1. **Перейдите по ссылке:**

   [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/AntonKuznetsov1911/StroiNadzor)

2. **Или вручную:**

   - Откройте https://dashboard.render.com/
   - Нажмите "New +" → "Web Service"
   - Подключите GitHub аккаунт (если еще не подключен)
   - Выберите репозиторий **StroiNadzor**
   - Render автоматически обнаружит `render.yaml`
   - Нажмите "Create Web Service"

3. **Настройки (уже в render.yaml):**
   - **Name:** tehnadzor-backend
   - **Region:** Frankfurt (ближайший к России)
   - **Branch:** main
   - **Build Command:** `cd backend && pip install -r requirements-railway.txt`
   - **Start Command:** `cd backend && uvicorn demo_server:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free

4. **После деплоя:**
   - Скопируйте URL (например: `https://tehnadzor-backend.onrender.com`)
   - Проверьте `/docs` - должен открыться Swagger UI
   - Проверьте `/webapp` - должно открыться веб-приложение

## Преимущества Render перед Railway:

✅ Бесплатный план навсегда (Railway - только 5$ кредитов)
✅ Автоматический деплой из GitHub
✅ SSL сертификаты автоматически
✅ Нет необходимости в CLI
✅ Европейский регион (Frankfurt)

## Обновление Telegram бота

После получения URL от Render, выполните:

```bash
cd C:\Users\PC\StroiNadzorAI
python update_webapp_url.py "https://ваш-url.onrender.com/webapp"
```

## Проверка статуса

- Dashboard: https://dashboard.render.com/
- Логи доступны в реальном времени
- Автоматические перезапуски при сбоях

## Важно!

⚠️ **Бесплатный план Render засыпает после 15 минут неактивности**
- Первый запрос может занять 30-60 секунд (cold start)
- Для постоянной работы нужен платный план ($7/месяц)
- Или используйте UptimeRobot для пинга каждые 5 минут
