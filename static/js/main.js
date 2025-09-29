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
    
    // Инициализация для PythonAnywhere
    initPythonAnywhereFallbacks();
}

// Инициализация fallback решений для PythonAnywhere
function initPythonAnywhereFallbacks() {
    console.log('🔧 Инициализация fallback решений для PythonAnywhere');
    
    // Проверяем доступность API endpoints
    testAPIEndpoints();
    
    // Инициализируем простой выбор ингредиентов
    initSimpleIngredientSelection();
    
    // Применяем стили для чекбоксов
    applyCheckboxStyles();
}

// Тестирование API endpoints
function testAPIEndpoints() {
    const endpoints = [
        '/recipes/api/search-ingredients/',
        '/recipes/api/create-ingredient/',
        '/collections/api/user-collections/',
        '/collections/api/add-recipe/'
    ];
    
    endpoints.forEach(endpoint => {
        fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({})
        })
        .then(response => {
            if (response.ok) {
                console.log(`✅ API endpoint ${endpoint} доступен`);
            } else {
                console.warn(`⚠️ API endpoint ${endpoint} недоступен: ${response.status}`);
            }
        })
        .catch(error => {
            console.warn(`❌ API endpoint ${endpoint} ошибка:`, error);
        });
    });
}

// Простой выбор ингредиентов без AJAX
function initSimpleIngredientSelection() {
    const ingredientRows = document.querySelectorAll('.form-row');
    
    ingredientRows.forEach(row => {
        const selectBtn = row.querySelector('.btn-primary');
        if (selectBtn) {
            selectBtn.addEventListener('click', function(e) {
                e.preventDefault();
                openSimpleIngredientModal(this);
            });
        }
    });
}

// Открытие простой модалки выбора ингредиентов
function openSimpleIngredientModal(button) {
    console.log('🚀 Открываем простую модалку выбора ингредиентов');
    
    // Создаем модалку если её нет
    let modal = document.getElementById('simpleIngredientModal');
    if (!modal) {
        modal = createSimpleIngredientModal();
        document.body.appendChild(modal);
    }
    
    currentIngredientRow = button.closest('.form-row');
    modal.style.display = 'block';
}

// Создание простой модалки
function createSimpleIngredientModal() {
    const modal = document.createElement('div');
    modal.id = 'simpleIngredientModal';
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.5);
        display: none;
        z-index: 9999;
    `;
    
    modal.innerHTML = `
        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); 
                    background: white; padding: 20px; border-radius: 8px; max-width: 500px; width: 90%;">
            <h3 style="margin: 0 0 20px 0; color: #007bff; text-align: center;">🔍 Выбрать ингредиент</h3>
            
            <div style="margin-bottom: 20px;">
                <label>Поиск ингредиента:</label>
                <input type="text" id="simpleIngredientSearch" placeholder="Введите название ингредиента..." 
                       style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
            </div>
            
            <div id="simpleIngredientResults" style="max-height: 300px; overflow-y: auto; margin-bottom: 20px;">
                <!-- Результаты будут здесь -->
            </div>
            
            <div style="text-align: center;">
                <button type="button" onclick="closeSimpleIngredientModal()" 
                        style="background: #6c757d; color: white; border: none; padding: 10px 20px; border-radius: 4px; margin-right: 10px;">
                    Отмена
                </button>
            </div>
        </div>
    `;
    
    // Обработчик поиска
    const searchInput = modal.querySelector('#simpleIngredientSearch');
    searchInput.addEventListener('input', function() {
        searchSimpleIngredients(this.value);
    });
    
    // Закрытие при клике вне модалки
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeSimpleIngredientModal();
        }
    });
    
    return modal;
}

// Поиск ингредиентов в простом режиме
function searchSimpleIngredients(query) {
    const resultsDiv = document.getElementById('simpleIngredientResults');
    
    if (query.length < 2) {
        resultsDiv.innerHTML = '';
        return;
    }
    
    // Сначала пробуем AJAX
    fetch('/recipes/api/search-ingredients/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ query: query })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displaySimpleIngredientResults(data.ingredients);
        } else {
            // Fallback: показываем сообщение об ошибке
            resultsDiv.innerHTML = `
                <div style="color: red; padding: 10px; text-align: center;">
                    Ошибка поиска. Попробуйте обновить страницу.
                </div>
            `;
        }
    })
    .catch(error => {
        console.error('Ошибка поиска ингредиентов:', error);
        resultsDiv.innerHTML = `
            <div style="color: red; padding: 10px; text-align: center;">
                Ошибка сети. Проверьте подключение к интернету.
            </div>
        `;
    });
}

// Отображение результатов простого поиска
function displaySimpleIngredientResults(ingredients) {
    const resultsDiv = document.getElementById('simpleIngredientResults');
    
    if (ingredients.length === 0) {
        resultsDiv.innerHTML = `
            <div style="color: #6c757d; padding: 10px; text-align: center;">
                Ингредиенты не найдены
            </div>
        `;
        return;
    }
    
    let html = '';
    ingredients.forEach(ingredient => {
        html += `
            <div class="ingredient-item" onclick="selectSimpleIngredient(${ingredient.id}, '${ingredient.name}')" 
                 style="padding: 10px; border: 1px solid #ddd; margin: 5px 0; border-radius: 4px; cursor: pointer; background: #f8f9fa;">
                <strong>${ingredient.name}</strong>
            </div>
        `;
    });
    
    resultsDiv.innerHTML = html;
}

// Выбор ингредиента в простом режиме
function selectSimpleIngredient(ingredientId, ingredientName) {
    if (currentIngredientRow) {
        const idInput = currentIngredientRow.querySelector('.ingredient-id-input');
        const nameDisplay = currentIngredientRow.querySelector('.ingredient-name-display');
        
        if (idInput) idInput.value = ingredientId;
        if (nameDisplay) {
            nameDisplay.value = ingredientName;
            // Убираем readonly для корректного отображения
            nameDisplay.removeAttribute('readonly');
            nameDisplay.style.background = '#fff';
        }
        
        closeSimpleIngredientModal();
        console.log(`✅ Выбран ингредиент: ${ingredientName}`);
    }
}

// Закрытие простой модалки
function closeSimpleIngredientModal() {
    const modal = document.getElementById('simpleIngredientModal');
    if (modal) {
        modal.style.display = 'none';
    }
    currentIngredientRow = null;
}

// Применение стилей для чекбоксов
function applyCheckboxStyles() {
    const checkboxes = document.querySelectorAll('.form-check-input');
    
    checkboxes.forEach(checkbox => {
        // Применяем стили для увеличенных чекбоксов
        if (checkbox.closest('.collection-form')) {
            checkbox.style.width = '24px';
            checkbox.style.height = '24px';
            checkbox.style.transform = 'scale(1.5)';
            checkbox.style.marginRight = '15px';
        }
        
        // Стилизация чекбоксов удаления изображений
        if (checkbox.name && checkbox.name.includes('DELETE')) {
            checkbox.style.transform = 'scale(1.5)';
            checkbox.style.marginRight = '10px';
        }
    });
}

// Функция для очистки пустых форм ингредиентов
function cleanEmptyIngredientForms() {
    const ingredientInputs = document.querySelectorAll('.ingredient-id-input');
    const amountInputs = document.querySelectorAll('input[name*="amount"]');
    const totalFormsInput = document.getElementById('id_ingredients-TOTAL_FORMS');
    
    let validFormsCount = 0;
    
    ingredientInputs.forEach((input, index) => {
        const formRow = input.closest('.form-row');
        const amountInput = amountInputs[index];
        
        // Если нет ингредиента или количества, помечаем форму для удаления
        if ((!input.value || input.value.trim() === '') || 
            (!amountInput.value || amountInput.value.trim() === '')) {
            
            // Находим чекбокс DELETE
            const deleteCheckbox = formRow.querySelector('input[name*="DELETE"]');
            if (deleteCheckbox) {
                deleteCheckbox.checked = true;
            }
            
            // Очищаем поля
            input.value = '';
            if (amountInput) amountInput.value = '';
            
            const nameDisplay = formRow.querySelector('.ingredient-name-display');
            if (nameDisplay) nameDisplay.value = '';
            
            // Также очищаем поле unit
            const unitInput = formRow.querySelector('input[name*="unit"]');
            if (unitInput) unitInput.value = '';
        } else {
            validFormsCount++;
        }
    });
    
    // Обновляем TOTAL_FORMS на количество валидных форм
    if (totalFormsInput) {
        totalFormsInput.value = validFormsCount;
    }
}

// Функция для проверки дубликатов ингредиентов
function checkDuplicateIngredients() {
    const ingredientInputs = document.querySelectorAll('.ingredient-id-input');
    const ingredients = [];
    const duplicates = [];
    
    ingredientInputs.forEach(input => {
        if (input.value && input.value.trim() !== '') {
            const ingredientId = input.value;
            if (ingredients.includes(ingredientId)) {
                // Найден дубликат
                const formRow = input.closest('.form-row');
                const nameDisplay = formRow.querySelector('.ingredient-name-display');
                const ingredientName = nameDisplay ? nameDisplay.value : 'неизвестный ингредиент';
                duplicates.push(ingredientName);
            } else {
                ingredients.push(ingredientId);
            }
        }
    });
    
    if (duplicates.length > 0) {
        const duplicateNames = duplicates.join(', ');
        showInfoModal(
            'Дубликат ингредиента',
            `⚠️ Внимание: Ингредиенты "${duplicateNames}" добавлены несколько раз. Удалите дубликаты или выберите другие ингредиенты.`
        );
        return false;
    }
    return true;
}

// Функция для показа информационного окна
function showInfoModal(title, message) {
    // Создаем модальное окно
    const modal = document.createElement('div');
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        z-index: 2000;
        display: flex;
        align-items: center;
        justify-content: center;
    `;
    
    modal.innerHTML = `
        <div style="
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            max-width: 500px;
            width: 90%;
            text-align: center;
            position: relative;
        ">
            <div style="
                position: absolute;
                top: 15px;
                right: 20px;
                font-size: 24px;
                cursor: pointer;
                color: #999;
                font-weight: bold;
            " onclick="this.closest('.info-modal').remove()">&times;</div>
            
            <div style="
                font-size: 48px;
                margin-bottom: 20px;
                color: #ffc107;
            ">⚠️</div>
            
            <h3 style="
                margin: 0 0 15px 0;
                color: #333;
                font-size: 24px;
            ">${title}</h3>
            
            <p style="
                margin: 0 0 25px 0;
                color: #666;
                line-height: 1.5;
                font-size: 16px;
            ">${message}</p>
            
            <button onclick="this.closest('.info-modal').remove()" style="
                background: linear-gradient(135deg, #007bff, #0056b3);
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 25px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(0, 123, 255, 0.3);
            " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 20px rgba(0, 123, 255, 0.4)'" 
               onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 15px rgba(0, 123, 255, 0.3)'">
                Понятно
            </button>
        </div>
    `;
    
    modal.className = 'info-modal';
    document.body.appendChild(modal);
    
    // Закрытие по клику на фон
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.remove();
        }
    });
    
    // Закрытие по Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            modal.remove();
        }
    });
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
                    const idInput = formRow.querySelector('input[name*="-id"]');
                    
                    if (idInput && idInput.value) {
                        // Если это существующий ингредиент, создаем скрытый чекбокс DELETE
                        const deleteCheckbox = document.createElement('input');
                        deleteCheckbox.type = 'hidden';
                        deleteCheckbox.name = idInput.name.replace('-id', '-DELETE');
                        deleteCheckbox.value = 'on';
                        formRow.appendChild(deleteCheckbox);
                        
                        // Скрываем форму, но не удаляем из DOM
                        formRow.style.transition = 'all 0.3s ease';
                        formRow.style.opacity = '0';
                        formRow.style.transform = 'translateX(-100%)';
                        
                        setTimeout(() => {
                            formRow.style.display = 'none';
                        }, 300);
                    } else {
                        // Если это новая форма, просто удаляем из DOM
                        formRow.style.transition = 'all 0.3s ease';
                        formRow.style.opacity = '0';
                        formRow.style.transform = 'translateX(-100%)';
                        
                        setTimeout(() => {
                            formRow.remove();
                        }, 300);
                    }
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
                const formRow = e.target.closest(".image-form-row");
                
                if (formRow) {
                    const idInput = formRow.querySelector('input[name*="-id"]');
                    
                    if (idInput && idInput.value) {
                        // Если это существующее изображение, создаем скрытый чекбокс DELETE
                        const deleteCheckbox = document.createElement('input');
                        deleteCheckbox.type = 'hidden';
                        deleteCheckbox.name = idInput.name.replace('-id', '-DELETE');
                        deleteCheckbox.value = 'on';
                        formRow.appendChild(deleteCheckbox);
                        
                        // Скрываем форму, но не удаляем из DOM
                        formRow.style.transition = 'all 0.3s ease';
                        formRow.style.opacity = '0';
                        formRow.style.transform = 'scale(0.8)';
                        
                        setTimeout(() => {
                            formRow.style.display = 'none';
                        }, 300);
                    } else {
                        // Если это новая форма, просто удаляем из DOM
                        formRow.style.transition = 'all 0.3s ease';
                        formRow.style.opacity = '0';
                        formRow.style.transform = 'scale(0.8)';
                        
                        setTimeout(() => {
                            formRow.remove();
                        }, 300);
                    }
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
        // Поиск по Enter - НЕ перехватываем для веб-формы
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const form = this.closest('form');
                if (form && form.classList.contains('search-form')) {
                    // Для веб-формы поиска - не перехватываем
                    return;
                }
                e.preventDefault();
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
    console.log('showCollectionModal called with recipeId:', recipeId);
    const modal = document.getElementById('collectionModal');
    if (modal) {
        console.log('Modal found, showing...');
        modal.style.display = 'flex';
        loadCollectionsForRecipe(recipeId);
    } else {
        console.error('Modal not found!');
    }
}

function hideCollectionModal() {
    const modal = document.getElementById('collectionModal');
    if (modal) {
        modal.style.display = 'none';
    }
}

function loadCollectionsForRecipe(recipeId) {
    console.log('Loading collections for recipe:', recipeId);
    const recipeInfo = document.getElementById('modalRecipeInfo');
    const collectionsDiv = document.getElementById('modalCollections');
    
    if (recipeInfo) {
        recipeInfo.innerHTML = ``;
    }
    
    // Загружаем коллекции пользователя через AJAX
    console.log('Fetching collections from API...');
    fetch('/collections/api/user-collections/')
        .then(response => response.json())
        .then(data => {
            console.log('API response:', data);
            if (data.success && data.collections) {
                displayCollections(data.collections, recipeId);
            } else {
                showNoCollectionsMessage(recipeId);
            }
        })
        .catch(error => {
            console.error('Ошибка загрузки коллекций:', error);
            showNoCollectionsMessage(recipeId);
        });
}

function displayCollections(collections, recipeId) {
    console.log('displayCollections called with:', collections, recipeId);
    const collectionsDiv = document.getElementById('modalCollections');
    
    if (collections.length === 0) {
        console.log('No collections found, showing message');
        showNoCollectionsMessage(recipeId);
        return;
    }
    
    console.log('Displaying', collections.length, 'collections');
    let html = '<div class="collections-list">';
    collections.forEach(collection => {
        html += `
            <div class="collection-item">
                <div class="collection-info" style="display: flex; align-items: flex-start;">
                    <h5 style="margin: 0; padding-top: 8px;">${collection.title}</h5>
                </div>
                <button class="btn btn-primary" onclick="addToCollection(${collection.id}, ${recipeId})" style="min-width: 100px;">
                    <i class="fas fa-plus"></i> Добавить
                </button>
            </div>
        `;
    });
    html += '</div>';
    
    // Добавляем кнопку "Отмена"
    html += `
        <div class="text-center mt-3">
            <button class="btn btn-light px-3 py-2" onclick="hideCollectionModal()" style="border-radius: 12px; font-weight: 500; border: 1px solid #dee2e6; color: #6c757d; background: #f8f9fa; transition: all 0.3s ease;">
                <i class="fas fa-times me-1"></i>Отмена
            </button>
        </div>
    `;
    
    collectionsDiv.innerHTML = html;
    console.log('Collections HTML set');
}

function showNoCollectionsMessage(recipeId) {
    const collectionsDiv = document.getElementById('modalCollections');
    collectionsDiv.innerHTML = `
        <div class="text-center py-3">
            <i class="fas fa-folder-open fa-2x text-muted mb-2"></i>
            <p class="text-muted mb-3">У вас пока нет коллекций.</p>
            <div class="d-flex gap-2 justify-content-center">
                <a href="/collections/add/" class="btn btn-primary px-3 py-2" style="background: linear-gradient(135deg, #28a745, #20c997); border: none; border-radius: 12px; font-weight: 500; box-shadow: 0 2px 8px rgba(40, 167, 69, 0.3); transition: all 0.3s ease;">
                    <i class="fas fa-plus me-1"></i>Создать коллекцию
                </a>
                <button class="btn btn-light px-3 py-2" onclick="hideCollectionModal()" style="border-radius: 12px; font-weight: 500; border: 1px solid #dee2e6; color: #6c757d; background: #f8f9fa; transition: all 0.3s ease;">
                    <i class="fas fa-times me-1"></i>Отмена
                </button>
            </div>
        </div>
    `;
}

function addToCollection(collectionId, recipeId) {
    // Отправляем запрос на добавление рецепта в коллекцию
    fetch('/collections/api/add-recipe/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            collection_id: collectionId,
            recipe_id: recipeId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Рецепт успешно добавлен в коллекцию!');
            hideCollectionModal();
        } else {
            alert('Ошибка: ' + (data.error || 'Не удалось добавить рецепт'));
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при добавлении рецепта');
    });
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
    
    // Закрытие по клавише Escape
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && modal && modal.style.display !== 'none') {
            hideCollectionModal();
        }
    });
    
    // Инициализация фильтрации на главной странице
    initHomePageFilter();
});

// Функции для фильтрации на главной странице
function initHomePageFilter() {
    const applyButton = document.getElementById('apply-filter');
    const clearButton = document.getElementById('clear-filter');
    
    if (applyButton) {
        applyButton.addEventListener('click', applyFilter);
    }
    
    if (clearButton) {
        clearButton.addEventListener('click', clearFilter);
    }
    
    // Автоматическая фильтрация при изменении значений
    const filterSelects = document.querySelectorAll('#filter-form select');
    filterSelects.forEach(select => {
        select.addEventListener('change', applyFilter);
    });
}

function applyFilter() {
    const ingredientFilter = document.getElementById('ingredient-filter');
    const difficultyFilter = document.getElementById('difficulty-filter');
    const categoryFilter = document.getElementById('category-filter');
    const applyButton = document.getElementById('apply-filter');
    
    const filters = {
        ingredient_name: ingredientFilter ? ingredientFilter.value.trim() : '',
        difficulty: difficultyFilter ? difficultyFilter.value : '',
        category: categoryFilter ? categoryFilter.value : ''
    };
    
    console.log('Applying filters:', filters);
    
    // Показываем индикатор загрузки
    if (applyButton) {
        const originalText = applyButton.innerHTML;
        applyButton.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Фильтрация...';
        applyButton.disabled = true;
    }
    
    // Отправляем AJAX запрос
    fetch('/recipes/api/search/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(filters)
    })
    .then(response => {
        console.log('Filter response status:', response.status);
        return response.json();
    })
    .then(data => {
        console.log('Filter response:', data);
        if (data.success) {
            displayFilterResults(data.recipes);
        } else {
            console.error('Ошибка фильтрации:', data.error);
            showFilterError();
        }
    })
    .catch(error => {
        console.error('Ошибка AJAX фильтрации:', error);
        showFilterError();
    })
    .finally(() => {
        // Восстанавливаем кнопку
        if (applyButton) {
            applyButton.innerHTML = '<i class="fas fa-filter me-1"></i>Применить фильтр';
            applyButton.disabled = false;
        }
    });
}

function clearFilter() {
    const ingredientFilter = document.getElementById('ingredient-filter');
    const difficultyFilter = document.getElementById('difficulty-filter');
    const categoryFilter = document.getElementById('category-filter');
    
    if (ingredientFilter) ingredientFilter.value = '';
    if (difficultyFilter) difficultyFilter.value = '';
    if (categoryFilter) categoryFilter.value = '';
    
    // Применяем пустой фильтр (показываем все рецепты)
    applyFilter();
}

function displayFilterResults(recipes) {
    const recipesContainer = document.getElementById('recipes-container');
    if (!recipesContainer) return;
    
    // Проверяем, авторизован ли пользователь
    const isUserAuthenticated = document.body.classList.contains('user-authenticated') || 
                               document.querySelector('a[href*="logout"]') !== null;
    
    if (recipes.length === 0) {
        recipesContainer.innerHTML = `
            <div class="text-center py-5">
                <i class="fas fa-search fa-4x text-muted mb-3"></i>
                <h4 class="text-muted">Рецепты не найдены</h4>
                <p class="text-muted">Попробуйте изменить параметры фильтрации</p>
            </div>
        `;
        return;
    }
    
    let html = '<div class="row">';
    recipes.forEach(recipe => {
        html += `
            <div class="col-lg-6 col-md-6 mb-4">
                <div class="card h-100" style="border-radius: 20px; border: none; box-shadow: 0 2px 10px rgba(0,0,0,0.08); background: white; height: 350px;">
                    <div class="card-header" style="background: linear-gradient(135deg, #6f42c1, #007bff); height: 6px; border-radius: 20px 20px 0 0; padding: 0;"></div>
                    
                    <div class="card-body d-flex flex-column" style="padding: 25px; height: 100%;">
                        <h5 class="card-title mb-3" style="font-size: 1.3rem; font-weight: 700; color: #2c3e50; line-height: 1.3;">
                            <a href="${recipe.url}" class="text-decoration-none text-dark">
                                ${recipe.title}
                            </a>
                        </h5>
                        
                        <!-- Детали рецепта -->
                        <div class="mb-3">
                            <div class="row g-2 mb-2">
                                <div class="col-4">
                                    <span class="badge" style="background: #f8f9fa; color: #495057; border-radius: 25px; padding: 6px 10px; font-size: 0.75rem; font-weight: 500;">
                                        <i class="fas fa-user me-1" style="color: #6c757d;"></i>Автор: ${recipe.author}
                                    </span>
                                </div>
                                ${recipe.category ? `
                                <div class="col-4">
                                    <span class="badge" style="background: #f8f9fa; color: #495057; border-radius: 25px; padding: 6px 10px; font-size: 0.75rem; font-weight: 500;">
                                        <i class="fas fa-folder me-1" style="color: #6c757d;"></i>Категория: ${recipe.category}
                                    </span>
                                </div>
                                ` : ''}
                                <div class="col-4">
                                    <span class="badge" style="background: #f8f9fa; color: #495057; border-radius: 25px; padding: 6px 10px; font-size: 0.75rem; font-weight: 500;">
                                        <i class="fas fa-bolt me-1" style="color: #6c757d;"></i>Сложность: ${recipe.difficulty_display}
                                    </span>
                                </div>
                            </div>
                            <div class="row g-2">
                                <div class="col-6">
                                    <span class="badge" style="background: #f8f9fa; color: #495057; border-radius: 25px; padding: 6px 10px; font-size: 0.75rem; font-weight: 500;">
                                        <i class="fas fa-star me-1" style="color: #ffc107;"></i>Рейтинг: ${formatRating(recipe.rating)}
                                    </span>
                                </div>
                                <div class="col-6">
                                    <span class="badge" style="background: #f8f9fa; color: #495057; border-radius: 25px; padding: 6px 10px; font-size: 0.75rem; font-weight: 500;">
                                        <i class="fas fa-clock me-1" style="color: #6c757d;"></i>Время: ${recipe.cook_time} мин
                                    </span>
                                </div>
                            </div>
                        </div>
                        
                        ${recipe.description ? `
                            <p class="card-text text-muted flex-grow-1 mb-3" style="font-size: 0.9rem; line-height: 1.5; color: #6c757d;">
                                ${recipe.description}
                            </p>
                        ` : ''}
                        
                        <div class="mt-auto">
                            <div class="d-flex gap-2">
                                <a href="${recipe.url}" class="btn flex-fill" style="background: linear-gradient(135deg, #6f42c1, #5a32a3); border: none; border-radius: 25px; padding: 12px 20px; color: white; font-weight: 600; text-decoration: none; transition: all 0.3s ease;">
                                    <i class="fas fa-eye me-1"></i>Просмотр
                                </a>
                                ${isUserAuthenticated ? `
                                <button class="btn flex-fill" onclick="showCollectionModal(${recipe.id})" style="background: linear-gradient(135deg, #28a745, #20c997); border: none; border-radius: 25px; padding: 12px 20px; color: white; font-weight: 600; transition: all 0.3s ease;">
                                    <i class="fas fa-plus me-1"></i>В коллекцию
                                </button>
                                ` : ''}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });
    html += '</div>';
    
    recipesContainer.innerHTML = html;
}

function formatRating(rating) {
    // Форматируем рейтинг с одним знаком после запятой
    return parseFloat(rating).toFixed(1);
}

function showFilterError() {
    const recipesContainer = document.getElementById('recipes-container');
    if (!recipesContainer) return;
    
    recipesContainer.innerHTML = `
        <div class="text-center py-5">
            <i class="fas fa-exclamation-triangle fa-4x text-warning mb-3"></i>
            <h4 class="text-muted">Ошибка фильтрации</h4>
            <p class="text-muted">Попробуйте повторить запрос позже</p>
        </div>
    `;
}

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

// Функции для работы с модалкой выбора ингредиентов
let currentIngredientRow = null;

function openIngredientModal(button) {
    console.log('🚀 Открываем модалку выбора ингредиентов');
    currentIngredientRow = button.closest('.form-row');
    console.log('📍 Текущая строка:', currentIngredientRow);
    
    const modal = document.getElementById('ingredientModal');
    console.log('🪟 Модалка найдена:', modal ? 'ДА' : 'НЕТ');
    
    if (modal) {
        modal.style.display = 'block';
        document.getElementById('ingredientSearch').value = '';
        document.getElementById('ingredientResults').innerHTML = '';
        document.getElementById('ingredientSearch').focus();
        console.log('✅ Модалка открыта успешно');
    } else {
        console.error('❌ Модалка не найдена!');
    }
}

function closeIngredientModal() {
    document.getElementById('ingredientModal').style.display = 'none';
    currentIngredientRow = null;
}

function switchToFallback() {
    console.log('🔄 Переключаемся на fallback режим');
    closeIngredientModal();
    document.getElementById('ingredientFallback').style.display = 'block';
}

// Добавляем функцию в глобальную область видимости
window.switchToFallback = switchToFallback;

function searchIngredients(query) {
    console.log('🔍 Поиск ингредиентов:', query);
    
    if (query.length < 2) {
        document.getElementById('ingredientResults').innerHTML = '';
        return;
    }
    
    const csrfToken = getCookie('csrftoken');
    console.log('🔑 CSRF токен:', csrfToken ? 'найден' : 'НЕ НАЙДЕН');
    
    fetch('/recipes/api/search-ingredients/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ query: query })
    })
    .then(response => {
        console.log('📡 Ответ сервера:', response.status, response.statusText);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('📊 Данные от сервера:', data);
        if (data.success) {
            displayIngredientResults(data.ingredients);
        } else {
            console.error('❌ Ошибка поиска ингредиентов:', data.error);
            document.getElementById('ingredientResults').innerHTML = 
                `<div style="color: red; padding: 10px;">Ошибка: ${data.error}</div>`;
        }
    })
    .catch(error => {
        console.error('💥 Ошибка при поиске ингредиентов:', error);
        document.getElementById('ingredientResults').innerHTML = 
            `<div style="color: red; padding: 10px;">Ошибка сети: ${error.message}</div>`;
    });
}

function displayIngredientResults(ingredients) {
    const resultsDiv = document.getElementById('ingredientResults');
    
    if (ingredients.length === 0) {
        resultsDiv.innerHTML = '<p style="text-align: center; color: #666; padding: 20px;">Ингредиенты не найдены</p>';
        return;
    }
    
    let html = '';
    ingredients.forEach(ingredient => {
        html += `
            <div class="ingredient-item" onclick="selectIngredient(${ingredient.id}, '${ingredient.name}')" 
                 style="padding: 10px; border: 1px solid #ddd; margin: 5px 0; border-radius: 4px; cursor: pointer; background: #f8f9fa;">
                <strong>${ingredient.name}</strong>
            </div>
        `;
    });
    
    resultsDiv.innerHTML = html;
}

function selectIngredient(ingredientId, ingredientName) {
    if (currentIngredientRow) {
        // Проверяем дубликаты перед добавлением
        const allIngredientInputs = document.querySelectorAll('.ingredient-id-input');
        for (let input of allIngredientInputs) {
            if (input.value === ingredientId && input !== currentIngredientRow.querySelector('.ingredient-id-input')) {
                showInfoModal(
                    'Дубликат ингредиента',
                    `⚠️ Внимание: Ингредиент "${ingredientName}" уже добавлен в рецепт. Выберите другой ингредиент или удалите существующий.`
                );
                return;
            }
        }
        
        // Находим элементы в текущей строке
        const idInput = currentIngredientRow.querySelector('.ingredient-id-input');
        const nameDisplay = currentIngredientRow.querySelector('.ingredient-name-display');
        
        if (idInput && nameDisplay) {
            idInput.value = ingredientId;
            nameDisplay.value = ingredientName;
            // Убираем readonly для корректного отображения
            nameDisplay.removeAttribute('readonly');
            nameDisplay.style.background = '#fff';
        }
    }
    
    closeIngredientModal();
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Обработчики для кнопок выбора ингредиентов
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('select-ingredient')) {
            openIngredientModal(e.target);
        }
    });
    
    // Обработчик для поиска ингредиентов
    const searchInput = document.getElementById('ingredientSearch');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                searchIngredients(this.value);
            }, 300); // Задержка 300мс для оптимизации
        });
    }
    
    // Закрытие модалки при клике вне её
    document.getElementById('ingredientModal').addEventListener('click', function(e) {
        if (e.target === this) {
            closeIngredientModal();
        }
    });
    
    // Загружаем названия ингредиентов для существующих полей
    loadExistingIngredientNames();
});

function loadExistingIngredientNames() {
    // Находим все скрытые поля с ID ингредиентов
    const ingredientIdInputs = document.querySelectorAll('.ingredient-id-input');
    
    ingredientIdInputs.forEach(input => {
        if (input.value) {
            // Получаем название ингредиента по ID
            fetch('/recipes/api/search-ingredients/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ query: '' })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Находим ингредиент по ID
                    const ingredient = data.ingredients.find(ing => ing.id == input.value);
                    if (ingredient) {
                        const nameDisplay = input.closest('.form-row').querySelector('.ingredient-name-display');
                        if (nameDisplay) {
                            nameDisplay.value = ingredient.name;
                        }
                    }
                }
            })
            .catch(error => {
                console.error('Ошибка при загрузке названия ингредиента:', error);
            });
        }
    });
}

// Функции для создания нового ингредиента
function showCreateNew() {
    document.getElementById('createNewIngredient').style.display = 'block';
    document.getElementById('newIngredientName').focus();
}

function hideCreateNew() {
    document.getElementById('createNewIngredient').style.display = 'none';
    document.getElementById('newIngredientName').value = '';
}

function createNewIngredient() {
    const name = document.getElementById('newIngredientName').value.trim();
    
    if (!name) {
        alert('Введите название ингредиента');
        return;
    }
    
    fetch('/recipes/api/create-ingredient/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ name: name })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Выбираем созданный ингредиент
            selectIngredient(data.ingredient.id, data.ingredient.name);
            hideCreateNew();
        } else {
            // Показываем ошибку с возможностью исправить
            let errorMessage = data.error;
            
            // Если есть похожие ингредиенты, предлагаем их выбрать
            if (data.similar && data.similar.length > 0) {
                const similarList = data.similar.map(ing => `"${ing}"`).join(', ');
                errorMessage += `\n\nВозможно, вы имели в виду: ${similarList}?`;
                
                // Предлагаем выбрать из похожих
                const choice = confirm(errorMessage + '\n\nНажмите OK, чтобы выбрать из похожих ингредиентов, или Отмена, чтобы исправить название.');
                
                if (choice) {
                    // Показываем похожие ингредиенты в результатах поиска
                    displayIngredientResults(data.similar.map(name => ({ id: 0, name: name })));
                    hideCreateNew();
                }
            } else {
                alert('Ошибка: ' + errorMessage);
            }
        }
    })
    .catch(error => {
        console.error('Ошибка при создании ингредиента:', error);
        alert('Произошла ошибка при создании ингредиента');
    });
}

// Инициализируем при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    initIngredientUnitSelection();
});