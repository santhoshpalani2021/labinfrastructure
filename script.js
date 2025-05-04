const button1 = document.getElementById('button1');
const popup1 = document.getElementById('popup1');
const button2 = document.getElementById('button2');

const popup2 = document.getElementById('popup2');
const button3 = document.getElementById('button3');
const popup3 = document.getElementById('popup3');
const button4 = document.getElementById('button4');
const popup4 = document.getElementById('popup4');
const button5 = document.getElementById('button5');
const popup5 = document.getElementById('popup5');
const button6 = document.getElementById('button6');
const popup6 = document.getElementById('popup6');
const button7 = document.getElementById('button7');
const popup7 = document.getElementById('popup7');
const button8 = document.getElementById('button8');
const popup8 = document.getElementById('popup8');
const button9 = document.getElementById('button9');
const popup9 = document.getElementById('popup9');
const button10 = document.getElementById('button10');
const popup10 = document.getElementById('popup10');
const button11 = document.getElementById('button11');
const popup11 = document.getElementById('popup11');
const button12 = document.getElementById('button12');
const popup12 = document.getElementById('popup12');
const button13 = document.getElementById('button13');
const popup13 = document.getElementById('popup13');
const button14 = document.getElementById('button14');
const popup14 = document.getElementById('popup14');
const button15 = document.getElementById('button15');
const popup15 = document.getElementById('popup15');
const button16 = document.getElementById('button16');
const popup16 = document.getElementById('popup16');
const button17 = document.getElementById('button17');
const popup17 = document.getElementById('popup17');
const button18 = document.getElementById('button18');
const popup18 = document.getElementById('popup18');
const button19 = document.getElementById('button19');
const popup19 = document.getElementById('popup19');
const button20 = document.getElementById('button20');
const popup20 = document.getElementById('popup20');
const button21 = document.getElementById('button21');
const popup21 = document.getElementById('popup21');
const button22 = document.getElementById('button22');
const popup22 = document.getElementById('popup22');
const button23 = document.getElementById('button23');
const popup23 = document.getElementById('popup23');
const button24 = document.getElementById('button24');
const popup24 = document.getElementById('popup24');
const button25 = document.getElementById('button25');
const popup25 = document.getElementById('popup25');









// Open Lab Popup
button1.onclick = () => {
  popup1.style.display = 'flex';
};

// Open Hello World Popup
button2.onclick = () => {
  popup2.style.display = 'flex';
};
button3.onclick = () => {
  popup3.style.display = 'flex';
};
button4.onclick = () => {
  popup4.style.display = 'flex';
};
button5.onclick = () => {
  popup5.style.display = 'flex';
};
button6.onclick = () => {
  popup6.style.display = 'flex';
};
button7.onclick = () => {
  popup7.style.display = 'flex';
};
button8.onclick = () => {
  popup8.style.display = 'flex';
};
button9.onclick = () => {
  popup9.style.display = 'flex';
};
button10.onclick = () => {
  popup10.style.display = 'flex';
};
button11.onclick = () => {
  popup11.style.display = 'flex';
};
button12.onclick = () => {
  popup12.style.display = 'flex';
};
button13.onclick = () => {
  popup13.style.display = 'flex';
};
button14.onclick = () => {
  popup14.style.display = 'flex';
};
button15.onclick = () => {
  popup15.style.display = 'flex';
};
button16.onclick = () => {
  popup16.style.display = 'flex';
};
button17.onclick = () => {
  popup17.style.display = 'flex';
};
button18.onclick = () => {
  popup18.style.display = 'flex';
};
button19.onclick = () => {
  popup19.style.display = 'flex';
};
button20.onclick = () => {
  popup20.style.display = 'flex';
};
button21.onclick = () => {
  popup21.style.display = 'flex';
};
button22.onclick = () => {
  popup22.style.display = 'flex';
};
button23.onclick = () => {
  popup23.style.display = 'flex';
};
button24.onclick = () => {
  popup24.style.display = 'flex';
};
button25.onclick = () => {
  popup25.style.display = 'flex';
};

// Close popup on '×' click (dynamic for both popups)
document.querySelectorAll('.close-btn').forEach(btn => {
  btn.onclick = () => {
    const targetPopup = document.getElementById(btn.getAttribute('data-popup'));
    targetPopup.style.display = 'none';
  };
});

// Close popup when clicking outside content
window.onclick = event => {
  if (event.target.classList.contains('popup')) {
    event.target.style.display = 'none';
  }
};

// Toggle dropdowns
document.querySelectorAll('.dropdown-btn').forEach(button => {
  button.addEventListener('click', () => {
    const content = button.nextElementSibling;
    const isOpen = content.style.display === 'block';

    // Close all dropdowns
    document.querySelectorAll('.dropdown-content').forEach(c => c.style.display = 'none');

    // Toggle current
    if (!isOpen) content.style.display = 'block';
  });
});


