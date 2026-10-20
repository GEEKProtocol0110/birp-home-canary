const states = {
 calm: {color:'#7cac9b',lean:'0deg',title:'A little calm.',detail:'CO₂ & particles · steady',description:'Upright bird. Teal halo. The calm concept pose.'},
 attention: {color:'#d8b353',lean:'12deg',title:'A little attention.',detail:'CO₂ · attention tier',description:'A gentle lean and amber halo. The display names the measurement behind the change.'},
 high: {color:'#ce7d68',lean:'35deg',title:'A stronger signal.',detail:'Particles · high tier',description:'A deeper lean and red halo. This is a simulated high-tier pose, not an emergency alarm.'},
 unavailable: {color:'#aa93ba',lean:'0deg',title:'Waiting for a reading.',detail:'Sensor unavailable',description:'A neutral pose and violet halo. A missing reading is shown as unknown.'}
};
const device=document.querySelector('.device');
for (const button of document.querySelectorAll('[data-mode]')) {
 button.addEventListener('click',()=>{
  const mode=button.dataset.mode, state=states[mode];
  device.dataset.state=mode;
  device.style.setProperty('--halo',state.color);
  device.style.setProperty('--lean',state.lean);
  document.getElementById('device-status').textContent=state.title;
  document.getElementById('device-detail').textContent=state.detail;
  document.getElementById('demo-description').textContent=state.description;
  for(const option of document.querySelectorAll('[data-mode]')) option.setAttribute('aria-pressed',String(option===button));
 });
}
