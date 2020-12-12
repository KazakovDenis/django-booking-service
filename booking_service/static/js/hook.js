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
    hideElement(option);
}

function hideAllTimeOptions() {
    // Скрыть опцию у выпадающего списка выбора времени
    let options = timeSelect.querySelectorAll('option');
    options.forEach(opt => hideElement(opt));
}

function setTimeOptions(date) {
    // Установить опции выбора времени в соответствии с датой

    let options = timeSelect.querySelectorAll(`option`);
    options.forEach(opt => {
        opt.classList.remove(hideClass);
    });

    // получаем все приёмы за указанную дату
    let reservedHours;

    if (!appointments) {
        console.error('Не смогли получить информацию о приёмах у данного врача');
    } else {
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

function getDate(raw_date) {
    // Получить объект даты из формы
    let reversed = raw_date.split('.').reverse();
    let formatted = reversed.join('-');
    let date = new Date(formatted);
    return date;
}

function validateDate(form_date) {
    // Проверить соответствие даты требованиям
    if (!form_date) { return false; }
    let date = getDate(form_date);

    // Проверяем, что дата введена в правильном формате
    let pattern = /[0-9]{2}\.[0-9]{2}\.[0-9]{4}/;
    if (!form_date.match(pattern)) {
        alert('Дата должна быть указана в формате: 12.04.1961');
        return false;
    }

    // Проверяем, что дата не ранее сегодня
    let today = new Date();
    today.setHours(0, 0, 0 ,0);
    let last_available = new Date(today.getFullYear() + 1, 11, 31);

    if (date < today) {
        alert('Дата записи не может быть ранее сегодня');
        return false;
    } else if (date > last_available) {
        alert('Дата записи не может быть позднее 31 декабря следующего года');
        return false;
    }

    // Проверяем, что дата - не выходной день
    let weekday = date.getDay();
    if (weekday > 5) {
        alert('К сожалению, приём не ведётся по выходным дням');
        return false;
    };

    return form_date;
}

function setAvailableHours(event) {
    // Установить доступные для выбора часы приёма
    let valid_date = validateDate(dateInput.value);

    if (!valid_date) {
        dateInput.style.background = 'pink';
        hideAllTimeOptions();
    } else {
        setTimeOptions(valid_date);
    };
};
doctorSelect.addEventListener('focusin', (event) => {
    event.target.style.background = '';
});
dateInput.addEventListener('focusin', (event) => {
    event.target.style.background = '';
});
dateInput.addEventListener('focusout', setAvailableHours);

function validateDoctor() {
    // Проверить, что врач выбран
    if (!doctorSelect.value) {
        doctorSelect.style.background = 'pink';
        hideAllTimeOptions();
        alert('Укажите врача');
    };
}
timeSelect.addEventListener('focusin', validateDoctor, setAvailableHours);


// Работа с календарём
let calendar, calendarBox, calendarBack, calendarNext;

function lockCalendar() {
// Блокирует переключение календаря на доступные для записи месяцы
    if (!calendar) {
        calendar = window.DateTimeShortcuts.calendars[0];
        calendarBox = document.querySelector('#calendarbox0');
        calendarBack = document.querySelector('a.calendarnav-previous');
        calendarNext = document.querySelector('a.calendarnav-next');

        // TODO: показывает на 1 месяц больше до и после
        function hideCalendarArrow(event) {
            // Скрыть стрелки календаря, для указанных временных рамок
            let today = new Date();
            let currentMonth = new Date(today.getFullYear(), today.getMonth());
            let availableYear = currentMonth.getFullYear() + 1;
            let displayedMonth = new Date(calendar.currentYear, calendar.currentMonth - 1);
            let displayedYear = displayedMonth.getFullYear();

            if (currentMonth > displayedMonth) {
            // Скрываем кнопку "назад" в календаре, если месяц ранее текущего
                hideElement(calendarBack);
                showElement(calendarNext);
            } else if (displayedYear > availableYear) {
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
dateDiv.addEventListener('mouseover', lockCalendar);
