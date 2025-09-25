// Современный JavaScript для Кулинарной книги

document.addEventListener("DOMContentLoaded", function () {
    // Инициализация всех компонентов
    initRecipeForms();
    initIngredientRemoval();
    initImageForms();
    initSearch();
    initAnimations();
    initTooltips();
    initSmoothScrolling();
});

// Современная инициализация форм рецептов
function initRecipeForms() {
    const addBtn = document.getElementById("add-form");
    const container = document.getElementById("ingredient-list");
    const totalForms = document.getElementById("id_ingredients-TOTAL_FORMS");

    if (addBtn && container && totalForms) {
        // Удаляем существующие обработчики, если они есть
        addBtn.removeEventListener("click", addIngredientHandler);
        
        // Добавляем новый обработчик
        addBtn.addEventListener("click", addIngredientHandler);
    }
}

// Обработчик добавления ингредиента
function addIngredientHandler(e) {
    e.preventDefault();
    
    const addBtn = document.getElementById("add-form");
    const container = document.getElementById("ingredient-list");
    const totalForms = document.getElementById("id_ingredients-TOTAL_FORMS");
    const template = document.getElementById("empty-form-template");
    
    if (!addBtn || !container || !totalForms || !template) return;
    
    const formNum = parseInt(totalForms.value, 10);
    
    // Используем шаблон из HTML
    let newFormHtml = template.content.firstElementChild.outerHTML.replace(/__prefix__/g, formNum);
    container.insertAdjacentHTML('beforeend', newFormHtml);
    
    // Анимация появления для последнего добавленного элемента
    const newForm = container.lastElementChild;
    if (newForm) {
        newForm.style.opacity = '0';
        newForm.style.transform = 'translateY(-20px)';
        
        setTimeout(() => {
            newForm.style.transition = 'all 0.3s ease';
            newForm.style.opacity = '1';
            newForm.style.transform = 'translateY(0)';
        }, 10);
    }
    
    totalForms.value = formNum + 1;
    
    // Добавляем эффект пульсации к кнопке
    addBtn.style.animation = 'pulse 0.6s ease';
    setTimeout(() => {
        addBtn.style.animation = '';
    }, 600);
}

// Инициализация удаления ингредиентов
function initIngredientRemoval() {
    const container = document.getElementById("ingredient-list");
    
    if (container) {
        // Удаление ингредиентов с анимацией
        container.addEventListener("click", function(e) {
            if (e.target.classList.contains("remove-ingredient")) {
                e.preventDefault();
                const formRow = e.target.closest(".form-row");
                
                if (formRow) {
                    // Анимация удаления
                    formRow.style.transition = 'all 0.3s ease';
                    formRow.style.opacity = '0';
                    formRow.style.transform = 'translateX(-100%)';
                    
                    setTimeout(() => {
                        formRow.remove();
                    }, 300);
                }
            }
        });
    }
}

// Инициализация форм изображений
function initImageForms() {
    const addImgBtn = document.getElementById("add-image-form");
    const imgContainer = document.getElementById("image-list");
    const totalImgForms = document.getElementById("id_images-TOTAL_FORMS");

    if (addImgBtn && imgContainer && totalImgForms) {
        // Удаляем существующие обработчики, если они есть
        addImgBtn.removeEventListener("click", addImageHandler);
        
        // Добавляем новый обработчик
        addImgBtn.addEventListener("click", addImageHandler);
        
        // Удаление изображений с анимацией
        imgContainer.addEventListener("click", function(e) {
            if (e.target.classList.contains("remove-image")) {
                e.preventDefault();
                const formRow = e.target.closest(".form-row");
                
                if (formRow) {
                    // Анимация удаления
                    formRow.style.transition = 'all 0.3s ease';
                    formRow.style.opacity = '0';
                    formRow.style.transform = 'scale(0.8)';
                    
                    setTimeout(() => {
                        formRow.remove();
                    }, 300);
                }
            }
        });
    }
}

// Обработчик добавления изображения
function addImageHandler(e) {
    e.preventDefault();
    
    const addImgBtn = document.getElementById("add-image-form");
    const imgContainer = document.getElementById("image-list");
    const totalImgForms = document.getElementById("id_images-TOTAL_FORMS");
    const imgTemplate = document.getElementById("empty-image-template");
    
    if (!addImgBtn || !imgContainer || !totalImgForms || !imgTemplate) return;
    
    const formNum = parseInt(totalImgForms.value, 10);
    
    // Используем шаблон из HTML
    let newFormHtml = imgTemplate.content.firstElementChild.outerHTML.replace(/__prefix__/g, formNum);
    imgContainer.insertAdjacentHTML('beforeend', newFormHtml);
    
    // Анимация появления для последнего добавленного элемента
    const newForm = imgContainer.lastElementChild;
    if (newForm) {
        newForm.style.opacity = '0';
        newForm.style.transform = 'scale(0.8)';
        
        setTimeout(() => {
            newForm.style.transition = 'all 0.3s ease';
            newForm.style.opacity = '1';
            newForm.style.transform = 'scale(1)';
        }, 10);
    }
    
    totalImgForms.value = formNum + 1;
}

// Современная инициализация поиска
function initSearch() {
    const searchInputs = document.querySelectorAll('input[name="q"]');
    const searchForms = document.querySelectorAll('.search-form');
    
    searchInputs.forEach(input => {
        // Поиск по Enter
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                const form = this.closest('form');
                if (form) {
                    // Добавляем эффект загрузки
                    const submitBtn = form.querySelector('button[type="submit"]');
                    if (submitBtn) {
                        submitBtn.style.background = 'linear-gradient(45deg, #56ab2f, #a8e6cf)';
                        submitBtn.textContent = 'Поиск...';
                    }
                    form.submit();
                }
            }
        });
        
        // Анимация фокуса
        input.addEventListener('focus', function() {
            this.parentElement.style.transform = 'scale(1.02)';
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.style.transform = 'scale(1)';
        });
    });
    
    // Анимация форм поиска
    searchForms.forEach(form => {
        form.style.opacity = '0';
        form.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            form.style.transition = 'all 0.6s ease';
            form.style.opacity = '1';
            form.style.transform = 'translateY(0)';
        }, 200);
    });
}

// Инициализация анимаций
function initAnimations() {
    // Анимация появления карточек рецептов
    const recipeCards = document.querySelectorAll('.recipe-card');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, index * 100);
            }
        });
    }, {
        threshold: 0.1
    });
    
    recipeCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'all 0.6s ease';
        observer.observe(card);
    });
    
    // Анимация кнопок
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px) scale(1.05)';
        });
        
        btn.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
}

// Инициализация подсказок
function initTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = this.getAttribute('data-tooltip');
            tooltip.style.cssText = `
                position: absolute;
                background: rgba(0, 0, 0, 0.8);
                color: white;
                padding: 8px 12px;
                border-radius: 6px;
                font-size: 0.8rem;
                z-index: 1000;
                pointer-events: none;
                opacity: 0;
                transition: opacity 0.3s ease;
            `;
            
            document.body.appendChild(tooltip);
            
            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
            tooltip.style.top = rect.top - tooltip.offsetHeight - 8 + 'px';
            
            setTimeout(() => {
                tooltip.style.opacity = '1';
            }, 10);
            
            this._tooltip = tooltip;
        });
        
        element.addEventListener('mouseleave', function() {
            if (this._tooltip) {
                this._tooltip.remove();
                this._tooltip = null;
            }
        });
    });
}

// Плавная прокрутка
function initSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Современное подтверждение удаления
function confirmDelete(message) {
    return new Promise((resolve) => {
        // Создаем модальное окно
        const modal = document.createElement('div');
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 10000;
            opacity: 0;
            transition: opacity 0.3s ease;
        `;
        
        const dialog = document.createElement('div');
        dialog.style.cssText = `
            background: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            text-align: center;
            max-width: 400px;
            transform: scale(0.8);
            transition: transform 0.3s ease;
        `;
        
        dialog.innerHTML = `
            <h3 style="margin-bottom: 20px; color: #333;">Подтверждение</h3>
            <p style="margin-bottom: 25px; color: #666;">${message || 'Вы уверены, что хотите удалить этот элемент?'}</p>
            <div style="display: flex; gap: 15px; justify-content: center;">
                <button class="btn-confirm" style="background: linear-gradient(45deg, #ff416c, #ff4b2b); color: white; border: none; padding: 10px 20px; border-radius: 25px; cursor: pointer;">Да, удалить</button>
                <button class="btn-cancel" style="background: linear-gradient(45deg, #667eea, #764ba2); color: white; border: none; padding: 10px 20px; border-radius: 25px; cursor: pointer;">Отмена</button>
            </div>
        `;
        
        modal.appendChild(dialog);
        document.body.appendChild(modal);
        
        // Анимация появления
        setTimeout(() => {
            modal.style.opacity = '1';
            dialog.style.transform = 'scale(1)';
        }, 10);
        
        // Обработчики событий
        dialog.querySelector('.btn-confirm').addEventListener('click', () => {
            modal.remove();
            resolve(true);
        });
        
        dialog.querySelector('.btn-cancel').addEventListener('click', () => {
            modal.remove();
            resolve(false);
        });
        
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
                resolve(false);
            }
        });
    });
}

// Добавляем CSS анимации
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .btn {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .recipe-card {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .form-input, .form-textarea {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
`;
document.head.appendChild(style);

// Функции для работы с коллекциями
function showCollectionModal(recipeId) {
    const modal = document.getElementById('collectionModal');
    if (modal) {
        modal.style.display = 'flex';
        loadCollectionsForRecipe(recipeId);
    }
}

function hideCollectionModal() {
    const modal = document.getElementById('collectionModal');
    if (modal) {
        modal.style.display = 'none';
    }
}

function loadCollectionsForRecipe(recipeId) {
    // Здесь можно добавить AJAX запрос для загрузки коллекций пользователя
    // Пока что просто показываем базовую информацию
    const recipeInfo = document.getElementById('modalRecipeInfo');
    const collectionsDiv = document.getElementById('modalCollections');
    
    if (recipeInfo) {
        recipeInfo.innerHTML = `<p><strong>Рецепт ID:</strong> ${recipeId}</p>`;
    }
    
    if (collectionsDiv) {
        collectionsDiv.innerHTML = `
            <p>Для добавления в коллекцию перейдите на страницу рецепта.</p>
            <a href="/recipes/${recipeId}/" class="btn btn-primary">Перейти к рецепту</a>
        `;
    }
}

// Закрытие модального окна
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('collectionModal');
    const closeBtn = document.querySelector('.close');
    
    if (closeBtn) {
        closeBtn.onclick = hideCollectionModal;
    }
    
    if (modal) {
        modal.onclick = function(event) {
            if (event.target === modal) {
                hideCollectionModal();
            }
        };
    }
});

// Автоматический выбор единиц измерения на основе ингредиента
function initIngredientUnitSelection() {
    // Добавляем обработчики для существующих форм
    document.querySelectorAll('select[name*="ingredient"]').forEach(function(select) {
        select.addEventListener('change', function() {
            updateUnitForIngredient(this);
        });
    });
    
    // Добавляем обработчики для новых форм при их добавлении
    document.addEventListener('click', function(e) {
        if (e.target && e.target.id === 'add-form') {
            setTimeout(function() {
                document.querySelectorAll('select[name*="ingredient"]').forEach(function(select) {
                    if (!select.hasAttribute('data-unit-listener')) {
                        select.addEventListener('change', function() {
                            updateUnitForIngredient(this);
                        });
                        select.setAttribute('data-unit-listener', 'true');
                    }
                });
            }, 100);
        }
    });
}

function updateUnitForIngredient(ingredientSelect) {
    const formRow = ingredientSelect.closest('.form-row');
    const unitSelect = formRow.querySelector('select[name*="unit"]');
    
    if (!unitSelect) return;
    
    // Получаем выбранный ингредиент
    const selectedIngredientId = ingredientSelect.value;
    
    if (selectedIngredientId) {
        // AJAX запрос для получения default_unit из базы данных
        fetch('/recipes/api/ingredient-unit/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                ingredient_id: selectedIngredientId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success && data.default_unit) {
                unitSelect.value = data.default_unit;
            }
        })
        .catch(error => {
            console.error('Ошибка при получении единиц измерения:', error);
        });
    }
}

// Функция для получения CSRF токена
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Инициализируем при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    initIngredientUnitSelection();
});