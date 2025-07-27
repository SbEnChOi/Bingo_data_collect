(() => {
  const modal          = document.getElementById('modal');
  const main           = document.getElementById('main');
  const startBtn       = document.getElementById('start-btn');
  const nickInput      = document.getElementById('nickname-input');
  const titleEl        = document.getElementById('title');
  const boardEl        = document.getElementById('board');
  const overlay        = document.getElementById('completion-overlay');
  const completeScreen = document.getElementById('complete-screen');
  const retryBtn       = document.getElementById('retry-btn');
  const clickSound      = document.getElementById('click-sound');
  //const transitionSound = document.getElementById('transition-sound');

  let nickname = '';
  let sessionId = '';
  let boardSize = 3;
  let seq = 0;
  const clicked = new Set();

  // UUID 생성
  function genUUID() {
    return crypto.randomUUID();
  }

  // 완료 애니메이션
  const showOverlay = callback => {
    overlay.style.display = 'flex';
    setTimeout(() => {
      overlay.style.display = 'none';
      callback();
    }, 1000);
  };

  // 빙고판 렌더링
  function renderBoard() {
    titleEl.textContent = `${boardSize}×${boardSize} 빙고`;
    boardEl.innerHTML = '';
    clicked.clear();
    seq = 0;

    for (let i = 0; i < boardSize; i++) {
      const row = document.createElement('div'); row.className = 'row';
      for (let j = 0; j < boardSize; j++) {
        const btn = document.createElement('button');
        btn.className = 'cell';
        btn.dataset.key = `${i},${j}`;
        btn.addEventListener('click', () => onCellClick(i, j, btn));
        row.append(btn);
      }
      boardEl.append(row);
    }
  }

  // 셀 클릭 핸들러
  function onCellClick(row, col, btn) {
    const key = `${row},${col}`;
    if (clicked.has(key)) return;
    if (clickSound) {
    clickSound.currentTime = 0;
    clickSound.play();
    }

    seq++;
    clicked.add(key);
    btn.textContent = seq;
    btn.classList.add('clicked');

    const payload = {
      session_id: sessionId,
      nickname,
      board_size: boardSize,
      seq,
      row,
      col,
      timestamp: new Date().toISOString()
    };
    fetch('/api/fill', {
      method: 'POST',
      headers: { 'Content-Type':'application/json' },
      body: JSON.stringify(payload)
    });

    // 보드 완료 시 처리
    if (seq === boardSize * boardSize) {
      showOverlay(() => {
        if (boardSize < 5) {
          boardSize++;
          renderBoard();
        } else {
          // 5×5 완료: 메인 숨기고 완료 화면 표시
          main.style.display = 'none';
          completeScreen.style.display = 'flex';
        }
      });
    }
  }

    // 다시 하기 → 3×3 빙고로 바로 돌아감
  retryBtn.addEventListener('click', () => {
    completeScreen.style.display = 'none';
    boardSize = 3; seq = 0; clicked.clear();
    renderBoard();
    main.style.display = 'flex';
  });

    // 시작 버튼 → 바로 3×3 렌더, 애니메이션 생략
  startBtn.addEventListener('click', () => {
    const val = nickInput.value.trim(); if (!val) return;
    nickname = val; sessionId = genUUID();
    modal.style.display = 'none'; main.style.display = 'flex';
    renderBoard();
  });
})();