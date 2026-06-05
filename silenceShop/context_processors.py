def clearance_processor(request):
    """
    Глобально передает уровень допуска (clearance_level) во все HTML-шаблоны.
    """
    user = request.user
    if not user.is_authenticated:
        return {'clearance_level': 0}
    
    if user.is_superuser:
        return {'clearance_level': 10} # У суперпользователя максимальный допуск
        
    try:
        # Пытаемся получить уровень допуска из профиля и роли фиксера
        profile = user.fixerprofile
        if profile.role:
            return {'clearance_level': profile.role.clearance_level}
    except Exception:
        pass
        
    return {'clearance_level': 1} # Уровень по умолчанию для зарегистрированных фиксеров