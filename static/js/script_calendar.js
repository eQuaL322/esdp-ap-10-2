
let nav = 0;
let clicked = null;
let events = document.getElementById('data').innerHTML;
events = JSON.parse(events)

// let response = fetch('/all_lessons')
//   .then(response => { return response.json()})
//   .then(data => console.log(data));



const calendar = document.getElementById('calendar');
const newEventModal = document.getElementById('newEventModal');
const hourEventModal = document.getElementById('hourEventModal');
const backDrop = document.getElementById('modalBackDrop');
const eventTitleInput = document.getElementById('eventTitleInput');
const weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
const startHour = 8;
const endHour = 22;
const currentHour = new Date().getHours();
const currentMinute = new Date().getMinutes();
const hour_events_table = document
  .querySelector('.hour_events_table');
hour_events_table.style.setProperty(
  '--start-hour', startHour);
hour_events_table.style.setProperty(
  '--end-hour', endHour);
const hourTemplate = document.querySelector(
  '#template-hour');
const hourGrid = document.querySelector(
  '.calendar__hour-grid');
const eventTemplate = document
  .querySelector('#template-event');
const calendarEvents = document
  .querySelector('.calendar__events');
const resolution = 2;
hour_events_table.style.setProperty(
  '--resolution', resolution);

function sameDay(d1, d2) {
    return d1.getFullYear() === d2.getFullYear() &&
      d1.getMonth() === d2.getMonth() &&
      d1.getDate() === d2.getDate();
  }

function openModal(date) {
  clicked = new Date(date);
  const eventForDay = events.filter(e => sameDay(new Date(e.start), clicked));

  if (eventForDay) {
    hourEventModal.style.display = 'block';
  } else {
    newEventModal.style.display = 'block';
  }

  backDrop.style.display = 'block';


for (let i = startHour; i < endHour; i++) {
  const hourNode = hourTemplate.content
    .firstElementChild.cloneNode(true);
  hourGrid.appendChild(hourNode);
  hourNode.querySelector('.label')
    .innerText = `${i}`.padStart(2, '0').padEnd(5, ":00");
  if (currentHour === i) {
    hourNode.classList.add('active');
    hourNode.style.setProperty(
      '--current-minute', currentMinute
    );
  }
}

eventForDay.forEach((event) => {
  const eventNode = eventTemplate.content
    .firstElementChild.cloneNode(true);
  calendarEvents.appendChild(eventNode);

  eventNode.querySelector('.label')
    .innerText = event.title;
  eventNode.querySelector('.label').href = `lesson/${event.id}`
  eventNode.style.setProperty(
    '--start', new Date(event.start).getHours());
  eventNode.style.setProperty(
    '--end', new Date(event.end).getHours());
});
}

function load() {
  const dt = new Date();

  if (nav !== 0) {
    dt.setMonth(new Date().getMonth() + nav);
  }

  const day = dt.getDate();
  const month = dt.getMonth();
  const year = dt.getFullYear();

  const firstDayOfMonth = new Date(year, month, 1);
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  
  const dateString = firstDayOfMonth.toLocaleDateString('en-GB', {
      weekday: 'long',
      year: 'numeric',
      month: 'numeric',
      day: 'numeric',
    });

  const paddingDays = weekdays.indexOf(dateString.split(', ')[0]);

  
  if (document.getElementById('language').value === 'en') {
    document.getElementById('monthDisplay').innerText =`${dt.toLocaleDateString('en-GB', { month: 'long' })} ${year}`;
  } else {
     let string = `${dt.toLocaleDateString('ru-RU', { month: 'long' })} ${year}`
    document.getElementById('monthDisplay').innerText = string.charAt(0).toUpperCase()+ string.slice(1);
  }


  calendar.innerHTML = '';


  for(let i = 1; i <= paddingDays + daysInMonth; i++) {
    const daySquare = document.createElement('div');
    daySquare.classList.add('day');

    const dayString = `${year}-${month + 1}-${i - paddingDays}`;
    
    

    if (i > paddingDays) {
      daySquare.innerText = i - paddingDays;
      
      checkDate = new Date(`${year}-${month + 1}-${i - paddingDays}`);

      const eventForDay = events.filter(e => sameDay(new Date(e.start), checkDate));
      

      if (i - paddingDays === day && nav === 0) {
        daySquare.id = 'currentDay';
      }

      if (eventForDay.length !== 0) {
        const eventDiv = document.createElement('div');
        eventDiv.classList.add('event');
        eventForDay.forEach(e => {
          eventDiv.innerHTML += `<a id="${e.title}" class="lesson_event" href="lesson/${e.id}"><div class="lesson_content">
            <span class="fc-time"></span> <span class="fc-title">${e.title}</span></div></a>`
        });
        let date =  checkDate;
        daySquare.addEventListener('click', () => openModal(date));
        daySquare.appendChild(eventDiv);

      }
      else {
        daySquare.addEventListener('click', () => openModal(checkDate));
      }

      
    } else {
      daySquare.classList.add('padding');
    }

    calendar.appendChild(daySquare);    
  }
  const lessonLinks = document.querySelectorAll(".lesson_event")
  lessonLinks.forEach((link)=>{
    link.addEventListener('click',(e)=>e.stopPropagation())
  })
}


function closeModal() {
  hourGrid.innerHTML = ''
  calendarEvents.innerHTML = ''
  eventTitleInput.classList.remove('error');
  newEventModal.style.display = 'none';
  hourEventModal.style.display = 'none';
  backDrop.style.display = 'none';
  eventTitleInput.value = '';
  clicked = null;
  load();
}

function saveEvent() {
  if (eventTitleInput.value) {
    eventTitleInput.classList.remove('error');

    events.push({
      date: clicked,
      title: eventTitleInput.value,
    });

    localStorage.setItem('events', JSON.stringify(events));
    closeModal();
  } else {
    eventTitleInput.classList.add('error');
  }
}

function deleteEvent() {
  events = events.filter(e => e.date !== clicked);
  localStorage.setItem('events', JSON.stringify(events));
  closeModal();
}

function initButtons() {
  document.getElementById('nextButton').addEventListener('click', () => {
    nav++;
    load();
  });

  document.getElementById('backButton').addEventListener('click', () => {
    nav--;
    load();
  });

  document.getElementById('saveButton').addEventListener('click', saveEvent);
  document.getElementById('cancelButton').addEventListener('click', closeModal);
  document.getElementById('closeButton').addEventListener('click', closeModal);
}

initButtons();
load();
