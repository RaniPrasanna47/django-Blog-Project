// debounce helper
function debounce(fn, delay=3000){
  let t;
  return function(...args){
    clearTimeout(t);
    t = setTimeout(()=>fn.apply(this,args), delay);
  };
}

document.addEventListener('DOMContentLoaded', ()=> {
  const input = document.getElementById('searchInput');
  if(!input) return;
  const handler = debounce(()=> {
    const q = input.value.trim();
    const params = new URLSearchParams(window.location.search);
    if(q) params.set('q', q); else params.delete('q');
    params.delete('page'); // reset pagination when searching
    window.location.search = params.toString();
  }, 450);
  input.addEventListener('input', handler);
});
