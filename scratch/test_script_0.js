
    // Independent inline failsafe: guarantees splash screen dismisses automatically
    function dismissSplashScreen() {
      var s = document.getElementById('app-splash-screen');
      if (s) {
        s.classList.add('opacity-0', 'pointer-events-none');
        setTimeout(function() { s.style.display = 'none'; }, 600);
      }
    }
    setTimeout(dismissSplashScreen, 2200);
  