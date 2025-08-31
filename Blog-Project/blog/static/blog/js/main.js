// Global small utilities
document.addEventListener('DOMContentLoaded', ()=> {
  // tiny fade in for cards
  document.querySelectorAll('.card').forEach((el,i)=> {
    el.style.opacity = 0;
    setTimeout(()=> { el.style.transition='opacity 300ms ease, transform 300ms ease'; el.style.opacity=1; }, 60*i);
  });

  // attach sharePost global used by template
  window.sharePost = async function(url){
    if(navigator.share){
      try{ await navigator.share({ title: document.title, url }); }catch(e){}
    } else {
      navigator.clipboard.writeText(url);
      alert('Link copied to clipboard!');
    }
  };
});
