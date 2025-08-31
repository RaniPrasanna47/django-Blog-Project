// graceful entrance for comments
document.addEventListener('DOMContentLoaded', ()=>{
  document.querySelectorAll('.comments .comment').forEach((c,i)=>{
    c.style.opacity=0;
    setTimeout(()=>{ c.style.transition='opacity 300ms ease'; c.style.opacity=1 }, 80*i);
  });
});
