const date = new Date();
var current_month;
var c_m_str;
var zero = '0';
const renderCalendar = () => {
  date.setDate(1);

  const monthDays = document.querySelector(".days");

  const lastDay = new Date(
    date.getFullYear(),
    date.getMonth() + 1,
    0
  ).getDate();
  const prevLastDay = new Date(
    date.getFullYear(),
    date.getMonth(),
    0
  ).getDate();

  const firstDayIndex = date.getDay();

  const lastDayIndex = new Date(
    date.getFullYear(),
    date.getMonth() + 1,
    0
  ).getDay();

  const nextDays = 7 - lastDayIndex - 1;

  const months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];

  
  // console.log("current month : ", current_month)1;
  var current_year = date.getFullYear();
  current_month = date.getMonth()+1;

  if(current_month < 10){
    c_m_str = current_month.toString();
    c_m_str = zero.concat(c_m_str)
    console.log("int c_m_str : ", c_m_str);
  }
  else{
    c_m_str = current_month.toString();
  }

  document.querySelector(".date h1").innerHTML = months[date.getMonth()];

  document.querySelector(".date p").innerHTML = new Date().toDateString();

  let days = "";

  for (let x = firstDayIndex; x > 0; x--) {
    days += `<div class="prev-date">${prevLastDay - x + 1}</div>`;
  }

// console.log(obj1);

  for (let i = 1; i <= lastDay; i++) {
    if (obj1 && obj1.hasOwnProperty('2022') && obj1['2022'].hasOwnProperty(c_m_str) && obj1['2022'][c_m_str].includes(i)) {
      console.log("current day")
      console.log("condition : ", obj1['2022'][c_m_str]);
      days += `<div class="today">${i}</div>`;
    } 
    // if(i === obj1['2022'][c_m_str] && date.getMonth() === new Date().getMonth()){
    //   console.log("holiday")
    //   days += `<div class="today">${i}</div>`;
    // }
    else {
      days += `<div>${i}</div>`;
    }
  }

  // for (let i = 1; i <= lastDay; i++) {
  //   if (
  //     i === obj1['2022'][c_m_str] &&
  //     date.getMonth() === new Date().getMonth()
  //   ) {
  //     days += `<div class="today">${i}</div>`;
  //   } else {
  //     days += `<div>${i}</div>`;
  //   }
  // }

  for (let j = 1; j <= nextDays; j++) {
    days += `<div class="next-date">${j}</div>`;
    monthDays.innerHTML = days;
  }
};

// console.log("c m o : ",current_month);



document.querySelector(".prev").addEventListener("click", () => {
  date.setMonth(date.getMonth() - 1);
  
  // current_month-=1;
  // if(current_month < 10){
  //   c_m_str = current_month.toString();
  //   c_m_str = zero.concat(c_m_str)
  //   console.log("int c_m_str : ", c_m_str);
  // }
  // else{
  //   c_m_str = current_month.toString();
  // }
  console.log("prev month")
  renderCalendar();
});

document.querySelector(".next").addEventListener("click", () => {
  console.log("hello")
  // console.log("current mont doc : ",current_month);
  date.setMonth(date.getMonth() + 1);
  
  // current_month+=1;
  // if(current_month < 10){
  //   c_m_str = current_month.toString();
  //   c_m_str = zero.concat(c_m_str)
  //   console.log("int c_m_str : ", c_m_str);
  // }
  // else{
  //   c_m_str = current_month.toString();
  // }
  renderCalendar();
});

// console.log("month holiday : ",c_m_str)

renderCalendar();
