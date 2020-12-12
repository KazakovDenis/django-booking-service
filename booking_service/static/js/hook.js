"use strict";

window.addEventListener('DOMContentLoaded', () => {

    let appointments;
    const hideClass = 'd-none';
    const doctorSelect = document.querySelector('select[name="doctor"]');
    const dateInput = document.querySelector('input[name="date"]');
    const dateLinks = document.querySelectorAll('#calendarbox0 a:not([class])');
    const todayLink = document.querySelector('.datetimeshortcuts a');
    const timeSelect = document.querySelector('select[name="time"]');

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
        option.classList.add(hideClass);
    }

    function hideAllTimeOptions() {
        // Скрыть опцию у выпадающего списка выбора времени
        let options = timeSelect.querySelectorAll('option');
        options.forEach(opt => {
            opt.classList.add(hideClass);
        });
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
    dateInput.addEventListener('focusin', (event) => {
        event.target.style.background = '';
    });
    dateInput.addEventListener('focusout', setAvailableHours);
});
