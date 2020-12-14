"use strict";

let appointments;
const hideClass = 'd-none';
const doctorSelect = document.querySelector('select[name="doctor"]');
const dateInput = document.querySelector('input[name="date"]');
const dateDiv = document.querySelectorAll('.form-group')[2];
const timeSelect = document.querySelector('select[name="time"]');


function hideElement(elem) {
    // Скрыть элемент
    elem.classList.add(hideClass);
}

function showElement(elem) {
    // Отобразить элемент
    elem.classList.remove(hideClass);
}

function showMessage(elem, msg) {
    // Показать сообщение об ошибке в валидации элемента
    let msgDiv = elem.parentElement.parentElement.querySelector('.message');
    showElement(msgDiv);
    msgDiv.innerHTML = msg;
}

function hideMessage(elem) {
    // Скрыть сообщение об ошибке в валидации элемента
    let msgDiv = elem.parentElement.parentElement.querySelector('.message');
    hideElement(msgDiv);
    msgDiv.innerHTML = '';
}

async function send_request(method, url, data=null, headers={}) {
    const resp = await fetch(url, {
        method: method,
        headers: headers,
        body: data,
    });

    if (!resp.ok){
        throw new Error(`Could not fetch ${url}, status: ${resp.status}`);
    };
    return await resp.json();
};

function getDoctorSchedule(event) {
    // Подгрузить расписание выбранного врача
    event.preventDefault()
    let doctorId = doctorSelect.value;
    if (doctorId) {
        let schedule = send_request('GET', `/schedule/${doctorId}`)
            .then(response => {
                appointments = response['result'];
            })
            .catch(err => console.error(err));
    } else {
        appointments = [];
    };
}
doctorSelect.addEventListener('change', getDoctorSchedule);

function hideTimeOption(time) {
    // Скрыть опцию у выпадающего списка выбора времени
    let option = timeSelect.querySelector(`[value="${time}"]`);
    option.disabled = true;
}

function hideAllTimeOptions() {
    // Скрыть все опции выбора времени
    let options = timeSelect.querySelectorAll('option');
    options.forEach(opt => {
        opt.disabled = true;
    });
}

function setTimeOptions(date) {
    // Установить опции выбора времени в соответствии с датой

    let options = timeSelect.querySelectorAll(`option`);
    options.forEach(opt => {
        opt.disabled = false;
    });

    // получаем все приёмы за указанную дату
    let reservedHours;

    if (appointments) {
        reservedHours = appointments.filter(item => {
            return item.date == date
        }).map(item => {
            return item.time
        });

        // скрываем часы, на которые уже есть запись
        reservedHours.forEach(hour => {
            hideTimeOption(hour)
        });
    };
}

function getDate(rawDate) {
    // Получить объект даты из формы
    let reversed = rawDate.split('.').reverse();
    let formatted = reversed.join('-');
    let date = new Date(formatted);
    return date;
}

function validateDate(formDate) {
    // Проверить соответствие даты требованиям
    if (!formDate) { return false; }

    // Проверяем, что дата введена в правильном формате
    let pattern = /[0-9]{2}\.[0-9]{2}\.[0-9]{4}/;
    if (!formDate.match(pattern)) {
        showMessage(dateInput, 'Дата должна быть указана в формате: 12.04.1961');
        return false;
    }

    let date = getDate(formDate);

    // Проверяем, что дата не ранее сегодня
    let today = new Date();
    today.setHours(0, 0, 0 ,0);
    let lastAvailable = new Date(today.getFullYear() + 1, 11, 31);

    if (date < today) {
        showMessage(dateInput, 'Дата записи не может быть ранее сегодня');
        return false;
    } else if (date > lastAvailable) {
        showMessage(dateInput, 'Дата записи не может быть позднее 31 декабря следующего года');
        return false;
    }

    // Проверяем, что дата - не выходной день
    let weekday = date.getDay();
    if (weekday == 0 || weekday == 6) {
        showMessage(dateInput, 'К сожалению, приём не ведётся по выходным дням');
        return false;
    };

    return formDate;
}

function setAvailableHours(event) {
    // Установить доступные для выбора часы приёма
    let validDate = validateDate(dateInput.value);

    if (!validDate) {
        dateInput.style.background = 'pink';
        hideAllTimeOptions();
    } else {
        setTimeOptions(validDate);
    };
};
doctorSelect.addEventListener('focusin', (event) => {
    event.target.style.background = '';
    hideMessage(doctorSelect);
});
dateInput.addEventListener('focusin', (event) => {
    event.target.style.background = '';
    hideMessage(dateInput);
});
dateInput.addEventListener('focusout', setAvailableHours);

function validateDoctor() {
    // Проверить, что врач выбран
    if (!doctorSelect.value) {
        doctorSelect.style.background = 'pink';
        hideAllTimeOptions();
        showMessage(doctorSelect, 'Укажите врача');
    };
}
timeSelect.addEventListener('focusin', validateDoctor);
timeSelect.addEventListener('focusin', setAvailableHours);


// Работа с календарём
let calendar, calendarBox, calendarBack, calendarNext;

function lockCalendar() {
// Блокирует переключение календаря на доступные для записи месяцы
    if (!calendar) {
        calendar = window.DateTimeShortcuts.calendars[0];
        calendarBox = document.querySelector('#calendarbox0');
        calendarBack = document.querySelector('a.calendarnav-previous');
        calendarNext = document.querySelector('a.calendarnav-next');

        function hideCalendarArrow(event) {
            // Скрыть стрелки календаря, для указанных временных рамок
            let today = new Date();
            let currentMonth = new Date(today.getFullYear(), today.getMonth());
            let availableYear = currentMonth.getFullYear() + 1;
            let displayedMonth = new Date(calendar.currentYear, calendar.currentMonth - 1);
            let displayedYear = displayedMonth.getFullYear();

            if (currentMonth >= displayedMonth) {
            // Скрываем кнопку "назад" в календаре, если месяц ранее текущего
                hideElement(calendarBack);
                showElement(calendarNext);
            } else if (displayedYear >= availableYear && calendar.currentMonth == 12) {
            // Скрываем кнопку "вперёд", если год больше текущего + 1
                hideElement(calendarNext);
                showElement(calendarBack);
            } else {
                showElement(calendarBack);
                showElement(calendarNext);
            }
        }
        calendarBox.addEventListener('click', hideCalendarArrow);
    }
}
dateDiv.addEventListener('mouseenter', lockCalendar);
