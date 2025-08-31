document.addEventListener('DOMContentLoaded', ()=>{
  const form = document.getElementById('contactForm');
  if(!form) return;
  form.addEventListener('submit', (e)=>{
    e.preventDefault();
    alert('Thanks! (demo) — no mail server configured.');
    form.reset();
  });
});
