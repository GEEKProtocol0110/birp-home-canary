const states = {
 calm: {color:'#7cac9b',orbit:'0deg',title:'At the top.',detail:'CO₂ & particles · steady',description:'Bird at the top. Teal halo. Better conditions in this simulated example.'},
 attention: {color:'#d8b353',orbit:'90deg',title:'Partway down.',detail:'CO₂ · attention tier',description:'Bird at the side. Amber halo. A simulated intermediate position; the display names the cause.'},
 high: {color:'#ce7d68',orbit:'180deg',title:'At the bottom.',detail:'Particles · high tier',description:'Bird at the bottom. Red halo. A simulated high-tier position, not an emergency alarm.'},
 unavailable: {color:'#aa93ba',orbit:null,title:'Reading unavailable.',detail:'Bird holds its last position',description:'Violet halo. The bird stays at its last position, which does not represent a current reading.'}
};
const device=document.querySelector('.device');
for (const button of document.querySelectorAll('[data-mode]')) {
 button.addEventListener('click',()=>{
  const mode=button.dataset.mode, state=states[mode];
  device.dataset.state=mode;
  device.style.setProperty('--halo',state.color);
  if(state.orbit!==null) device.style.setProperty('--orbit',state.orbit);
  document.getElementById('device-status').textContent=state.title;
  document.getElementById('device-detail').textContent=state.detail;
  document.getElementById('demo-description').textContent=state.description;
  for(const option of document.querySelectorAll('[data-mode]')) option.setAttribute('aria-pressed',String(option===button));
 });
}
