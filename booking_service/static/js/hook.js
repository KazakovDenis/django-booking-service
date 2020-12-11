"use strict";

window.addEventListener('DOMContentLoaded', () => {

    let appointments;
    const hideClass = 'd-none';
    const doctorSelect = document.querySelector('select[name="doctor"]');
    const dateInput = document.querySelector('input[name="date"]');
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

    function setAvailableHours(event) {
        // Установить доступные для выбора часы приёма
        let date = dateInput.value;
        let pattern = /[0-9]{2}\.[0-9]{2}\.[0-9]{4}/;

        if (!date && !date.match(pattern)) {
            alert('Дата должна быть указана в формате: 12.04.1961');
        } else {
            setTimeOptions(date);
        };
    };
    dateInput.addEventListener('change', setAvailableHours);
});
