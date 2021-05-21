Перед деплоем дать права на исполнение entrypoint.sh (chmod +x entrypoint.sh)
Проверить наличие каталога в проекте "docker/databases", если его нет, создать(mkdir docker/databases).
Если каталог databases уже пристуствовал, проверить является ли текущий пользователь его владельцом, если нет поменять(sudo chown -R user:user docker/databases)
После деплоя, автоматически создается учетка login: admin, password: admin, рекомендуется сменить пароль через интерфейс http://127.0.0.1/django-admin/
