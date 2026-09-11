(() => {
  "use strict";

  const PASSING_SCORE = 60;
  const OBJECTIVE_PASSING_SCORE = 60;
  const content = document.querySelector("#application-content");
  const nameNode = document.querySelector("#student-name");
  const runtime = window.TeoriaSenalesScorm12;

  const guidedSteps = [
    {
      title: "Reconoce el pulso rectangular",
      prompt: "Para x(t) = 1 en el intervalo −1 ≤ t ≤ 1 y cero fuera de él, identifica los límites y la duración total.",
      formula: "x(t) = 1, si −1 ≤ t ≤ 1; &nbsp; x(t) = 0, en otro caso",
      fields: [["start", "Límite inicial (s)"], ["end", "Límite final (s)"], ["duration", "Duración T (s)"]],
      expected: { start: -1, end: 1, duration: 2 },
      hint: "Identifica los extremos del soporte y calcula la duración como límite final menos límite inicial.",
      criterion: "C2_1_CR1",
    },
    {
      title: "Obtén la transformada rectangular sinc",
      prompt: "Con la convención X(f) = ∫x(t)e^(−j2πft)dt, selecciona la transformada del pulso de amplitud 1 y duración T = 2 s.",
      formula: "X(f) = T sinc(fT), donde sinc(u) = sin(πu)/(πu)",
      fields: [],
      optionSets: [["transform", "Expresión de X(f)", [["incorrect1", "sinc(2f)"], ["correct", "2 sinc(2f)"], ["incorrect2", "2 cos(2f)"], ["incorrect3", "sinc(f/2)"]]]],
      expected: { transform: "correct" },
      hint: "Sustituye T = 2 en la expresión general y conserva tanto el factor exterior como el argumento de sinc.",
      criterion: "C2_1_CR2",
    },
    {
      title: "Identifica valores y ceros del espectro",
      prompt: "Usa X(f) = 2 sinc(2f). Determina el valor en frecuencia cero y el primer cero positivo.",
      formula: "X(0) = área del pulso; &nbsp; ceros: f = k/T, k ≠ 0",
      fields: [["central", "X(0)"], ["zero", "Primer cero positivo (Hz)"]],
      expected: { central: 2, zero: 0.5 },
      hint: "Relaciona X(0) con el área del pulso y usa la duración T para ubicar el primer cero positivo.",
      criterion: "C2_1_CR3",
    },
    {
      title: "Interpreta magnitud y fase",
      prompt: "Relaciona la duración temporal con el espectro y reconoce qué ocurre con la fase cuando la magnitud es cero.",
      formula: "Mayor T → ceros más cercanos; &nbsp; fase no definida cuando |X(f)| = 0",
      fields: [],
      optionSets: [
        ["width", "Si aumenta T, el espectro:", [["wider", "Tiene ceros más separados"], ["narrower", "Tiene ceros más cercanos"], ["same", "No cambia"]]],
        ["phase", "En un cero exacto del espectro, la fase:", [["zero", "Siempre es cero"], ["undefined", "No está definida"], ["pi", "Siempre es π"]]],
      ],
      expected: { width: "narrower", phase: "undefined" },
      hint: "Revisa la relación inversa entre duración y separación de ceros. Cuando la magnitud es nula, no existe un ángulo de fase definido.",
      criterion: "C2_1_CR4",
    },
  ];

  const questionBank = [
    ["C2-1-P01", "mc", "Para un pulso rectangular de amplitud A y duración T, ¿cuál expresión corresponde a su transformada?", "a", [["a", "AT sinc(fT)"], ["b", "A sinc(f)/T"], ["c", "AT cos(fT)"], ["d", "A/T"]]],
    ["C2-1-P02", "mc", "Para T = 2 s y A = 1, ¿cuál es X(f)?", "b", [["a", "sinc(2f)"], ["b", "2 sinc(2f)"], ["c", "2 sinc(f)"], ["d", "sinc(f/2)"]]],
    ["C2-1-P03", "mc", "¿Cuál es el primer cero positivo de 2 sinc(2f)?", "b", [["a", "0.25 Hz"], ["b", "0.5 Hz"], ["c", "1 Hz"], ["d", "2 Hz"]]],
    ["C2-1-P04", "mc", "¿Cuál es el valor X(0) del pulso de amplitud 1 y duración 2 s?", "c", [["a", "0"], ["b", "1"], ["c", "2"], ["d", "π"]]],
    ["C2-1-P05", "mc", "Al aumentar la duración T de un pulso, la separación entre ceros del espectro:", "b", [["a", "Aumenta"], ["b", "Disminuye"], ["c", "No cambia"], ["d", "Es infinita"]]],
    ["C2-1-P06", "mc", "Para el pulso propuesto, el soporte temporal es:", "a", [["a", "[−1, 1] s"], ["b", "[0, 2] s"], ["c", "[−2, 2] s"], ["d", "[−0.5, 0.5] s"]]],
    ["C2-1-P07", "mc", "¿Cuál relación describe la fase de un espectro real que cambia de signo?", "d", [["a", "Siempre vale π/2"], ["b", "No depende del signo"], ["c", "Siempre vale cero"], ["d", "Puede ser 0 o π, según el signo"]]],
    ["C2-1-P08", "mc", "Los ceros de T sinc(fT), excepto f = 0, se ubican en:", "c", [["a", "f = kT"], ["b", "f = T/k"], ["c", "f = k/T"], ["d", "f = k + T"]]],
    ["C2-1-P09", "mc", "El valor X(0) de una señal corresponde a:", "a", [["a", "El área de la señal en el tiempo"], ["b", "El primer cero"], ["c", "La fase máxima"], ["d", "La duración dividida entre dos"]]],
    ["C2-1-P10", "tf", "La magnitud del espectro de un pulso rectangular tiene forma sinc.", true],
    ["C2-1-P11", "tf", "La fase está definida en un cero exacto de la magnitud.", false],
    ["C2-1-P12", "tf", "Para el pulso propuesto, la duración total es 2 s.", true],
    ["C2-1-P13", "tf", "Un pulso de mayor duración tiene ceros más separados en frecuencia.", false],
    ["C2-1-P14", "tf", "Con A = 1 y T = 2, el valor X(0) es 2.", true],
    ["C2-1-P15", "tf", "La relación rectangular sinc conecta una señal temporal con su espectro en frecuencia.", true],
  ];

  function seededRandom(seed) {
    let value = 2166136261;
    for (let index = 0; index < seed.length; index += 1) value = Math.imul(value ^ seed.charCodeAt(index), 16777619);
    return () => {
      value += 0x6D2B79F5;
      let output = value;
      output = Math.imul(output ^ output >>> 15, output | 1);
      output ^= output + Math.imul(output ^ output >>> 7, output | 61);
      return ((output ^ output >>> 14) >>> 0) / 4294967296;
    };
  }

  function sample(items, count, random) {
    const pool = [...items];
    for (let index = pool.length - 1; index > 0; index -= 1) {
      const replacement = Math.floor(random() * (index + 1));
      [pool[index], pool[replacement]] = [pool[replacement], pool[index]];
    }
    return pool.slice(0, count);
  }

  function selectQuestions(seed) {
    const random = seededRandom(seed);
    const selected = [...sample(questionBank.filter((question) => question[1] === "mc"), 3, random), ...sample(questionBank.filter((question) => question[1] === "tf"), 2, random)];
    return sample(selected, selected.length, random);
  }

  function createState() {
    const identity = runtime.studentId() || runtime.studentName() || "sesion-local";
    return { version: 2, seed: `${identity}-c2-1`, startedAt: new Date().toISOString(), completedAt: null, stage: 0, answers: {}, attempts: [0, 0, 0, 0], guidedPoints: [0, 0, 0, 0], helpUsed: [false, false, false, false], evaluated: false, points: 0, score: null, feedback: null };
  }

  let state;
  function save() { runtime.saveState(state); }
  function progress() { return state.evaluated ? 100 : Math.round((state.stage / 5) * 100); }
  function heading(current) { return `<div class="progress"><span>Paso ${current} de 5</span><a class="guide-link" href="guia_estudiante_C-2-1.pdf" target="_blank" rel="noopener">Ver guía del estudiante</a><span>${progress()} % completado</span></div><div class="progress-bar"><span style="width:${progress()}%"></span></div>`; }
  function feedback(message, kind) { return message ? `<p class="feedback ${kind}">${message}</p>` : ""; }
  function numericEqual(actual, expected) { return Number.isFinite(actual) && Math.abs(actual - expected) <= 0.000001; }
  function formatDateTime(value) { return new Intl.DateTimeFormat("es-CO", { dateStyle: "medium", timeStyle: "short" }).format(new Date(value)); }
  function criterionForQuestion(questionId) {
    const number = Number(questionId.slice(-2));
    if ([6, 12].includes(number)) return "C2_1_CR1";
    if ([1, 2, 10, 15].includes(number)) return "C2_1_CR2";
    if ([3, 4, 8, 9, 14].includes(number)) return "C2_1_CR3";
    if ([7, 11].includes(number)) return "C2_1_CR4";
    return "C2_1_CR5";
  }

  function renderIntro() {
    content.innerHTML = `<section class="card stack"><h2>Actividad guiada</h2><p>Relaciona un pulso rectangular de tiempo continuo con su transformada de Fourier, la función sinc, los ceros del espectro, la magnitud y la fase mediante cuatro pasos guiados y una evaluación final.</p><div class="notice"><strong>Tu avance se guarda en Moodle.</strong> Puedes salir y continuar el mismo intento más tarde.</div><div class="guide-access"><h3>Guía del estudiante C‑2‑1</h3><p>Consulta la guía antes de comenzar. Permanecerá disponible durante todo el recorrido.</p><a class="button-link secondary" href="guia_estudiante_C-2-1.pdf" target="_blank" rel="noopener">Ver guía del estudiante</a></div><p><strong>Puntaje de los pasos guiados:</strong> cada paso vale 3 puntos si se responde correctamente en el primer intento y 2 puntos si se corrige después.</p><p class="small">La evaluación final selecciona cinco preguntas del banco: tres de selección múltiple y dos de verdadero/falso.</p><div class="actions"><button id="start">Iniciar ejercicio C-2-1</button></div></section>`;
    document.querySelector("#start").addEventListener("click", () => { state.stage = 1; state.feedback = null; save(); render(); });
  }

  function renderGuidedStep(index) {
    const step = guidedSteps[index];
    const saved = state.answers[index] || {};
    const fields = step.fields.map(([key, label]) => `<label>${label}<input data-field="${key}" value="${saved[key] ?? ""}" placeholder="Escribe un valor" inputmode="decimal" autocomplete="off"></label>`).join("");
    const options = (step.optionSets || []).map(([key, label, choices]) => `<fieldset><legend>${label}</legend><div class="options">${choices.map(([value, text]) => `<label class="option"><input type="radio" name="${key}" value="${value}" ${saved[key] === value ? "checked" : ""}>${text}</label>`).join("")}</div></fieldset>`).join("");
    const decimalNotice = index === 2 ? `<p class="notice"><strong>Importante:</strong> utiliza punto (.) como separador decimal. Ejemplo: 1.5</p>` : "";
    content.innerHTML = `<section class="card stack">${heading(index + 1)}<h2>${step.title}</h2><p>${step.prompt}</p><p class="small">Puntaje: 3 puntos al acertar en el primer intento; 2 puntos al corregir después.</p>${decimalNotice}<p class="formula">${step.formula}</p><form id="guided-form"><div class="input-grid">${fields}</div>${options}<div class="actions"><button type="submit">Verificar respuesta</button><button class="secondary" type="button" id="help" ${state.helpUsed[index] ? "disabled" : ""}>Ver orientación</button></div></form>${feedback(state.feedback, state.feedbackKind || "info")}</section>`;
    document.querySelector("#guided-form").addEventListener("submit", (event) => { event.preventDefault(); validateGuidedStep(index); });
    document.querySelector("#help").addEventListener("click", () => { state.helpUsed[index] = true; state.feedback = step.hint; state.feedbackKind = "info"; save(); render(); });
  }

  function validateGuidedStep(index) {
    const step = guidedSteps[index];
    const answer = {};
    step.fields.forEach(([key]) => { answer[key] = document.querySelector(`[data-field="${key}"]`).value; });
    (step.optionSets || []).forEach(([key]) => { answer[key] = document.querySelector(`input[name="${key}"]:checked`)?.value || ""; });
    state.answers[index] = answer;
    const optionKeys = new Set((step.optionSets || []).map(([key]) => key));
    const correct = Object.entries(step.expected).every(([key, expected]) => optionKeys.has(key) ? answer[key] === expected : numericEqual(Number(answer[key]), expected));
    state.attempts[index] += 1;
    const interactionResponse = [...step.fields.map(([key]) => answer[key]), ...(step.optionSets || []).map(([key]) => answer[key])].join(" | ");
    runtime.recordInteraction({ id: `C2-1-G0${index + 1}-${state.attempts[index]}`, type: step.fields.length ? "fill-in" : "choice", response: interactionResponse, correct, weighting: 3 });
    if (correct) {
      state.guidedPoints[index] = state.attempts[index] === 1 ? 3 : 2;
      runtime.recordObjective({ id: step.criterion, score: (state.guidedPoints[index] / 3) * 100, passingScore: OBJECTIVE_PASSING_SCORE });
      state.stage += 1;
      state.feedback = null;
      state.feedbackKind = null;
    } else {
      runtime.recordObjective({ id: step.criterion, score: 0, passingScore: OBJECTIVE_PASSING_SCORE });
      state.feedback = `El resultado todavía no coincide. Intento ${state.attempts[index]} registrado. Revisa el procedimiento y vuelve a intentarlo.`;
      state.feedbackKind = "error";
    }
    save(); runtime.setProgress(progress()); render();
  }

  function renderEvaluation() {
    const questions = selectQuestions(state.seed);
    content.innerHTML = `<section class="card stack">${heading(5)}<h2>Evaluación final</h2><p>Responde las cinco preguntas asignadas. La calificación final se registra en Moodle en la escala de 0 a 100.</p><p class="small"><strong>Distribución:</strong> pasos guiados: hasta 12 puntos; selección múltiple: 6 puntos; verdadero/falso: 2 puntos.</p><form id="evaluation-form" class="stack">${questions.map(([id, type, prompt, expected, options]) => `<fieldset><legend>${id} · ${prompt}</legend><div class="options">${type === "mc" ? options.map(([key, label]) => `<label class="option"><input type="radio" name="${id}" value="${key}">${key.toUpperCase()}. ${label}</label>`).join("") : `<label class="option"><input type="radio" name="${id}" value="true">Verdadero</label><label class="option"><input type="radio" name="${id}" value="false">Falso</label>`}</div></fieldset>`).join("")}<div class="actions"><button type="submit">Calificar y finalizar</button></div></form>${feedback(state.feedback, state.feedbackKind || "info")}</section>`;
    document.querySelector("#evaluation-form").addEventListener("submit", (event) => { event.preventDefault(); gradeEvaluation(questions); });
  }

  function gradeEvaluation(questions) {
    let conceptualPoints = 0;
    const unanswered = [];
    const submitted = questions.map(([id, type, prompt, expected]) => {
      const response = document.querySelector(`input[name="${id}"]:checked`)?.value;
      if (response === undefined) unanswered.push(id);
      return { id, type, expected, response };
    });
    if (unanswered.length) {
      state.feedback = `Responde todas las preguntas antes de calificar: ${unanswered.join(", ")}.`;
      state.feedbackKind = "error";
      render();
      return;
    }
    const criterionResults = {};
    submitted.forEach(({ id, type, expected, response }) => {
      const normalized = type === "tf" ? response === "true" : response;
      const correct = normalized === expected;
      const weighting = type === "tf" ? 1 : 2;
      runtime.recordInteraction({ id, type: type === "tf" ? "true-false" : "choice", response: normalized, correct, weighting });
      const criterion = criterionForQuestion(id);
      criterionResults[criterion] ||= { correct: 0, total: 0 };
      criterionResults[criterion].total += 1;
      if (correct) criterionResults[criterion].correct += 1;
      if (correct) conceptualPoints += weighting;
    });
    state.evaluated = true;
    state.points = state.guidedPoints.reduce((total, value) => total + value, 0) + conceptualPoints;
    state.score = Math.round((state.points / 20) * 100);
    state.completedAt = new Date().toISOString();
    state.feedback = null;
    runtime.setProgress(100);
    Object.entries(criterionResults).forEach(([id, result]) => {
      runtime.recordObjective({ id, score: (result.correct / result.total) * 100, passingScore: OBJECTIVE_PASSING_SCORE });
    });
    runtime.reportScore({ score: state.score, passingScore: PASSING_SCORE, completed: true });
    save();
    render();
  }

  function renderResult() {
    const status = state.score >= PASSING_SCORE ? "Actividad aprobada" : "Actividad finalizada";
    content.innerHTML = `<section class="card stack"><p class="eyebrow">Resultado registrado</p><h2>${status}</h2><p class="score">${state.score.toFixed(2).replace(".", ",")} / 100</p><p>${state.points} / 20 puntos</p><p>Finalización registrada: <strong>${formatDateTime(state.completedAt || new Date().toISOString())}</strong>.</p><p>La actividad envió a Moodle la nota, el estado de finalización, el avance, las interacciones y los resultados por criterio.</p><div class="notice">El docente consulta el resultado y la fecha/hora oficial del intento directamente desde Moodle. No necesitas descargar ni entregar un archivo adicional.</div><div class="actions"><button id="finish">Finalizar y salir</button></div><p id="finish-status" class="small" aria-live="polite"></p></section>`;
    document.querySelector("#finish").addEventListener("click", () => {
      const button = document.querySelector("#finish");
      const finishStatus = document.querySelector("#finish-status");
      button.disabled = true;
      button.textContent = "Guardando y saliendo…";
      save();
      runtime.commit();
      const finished = runtime.finish();
      finishStatus.textContent = finished ? "Sesión finalizada. Regresando a Moodle…" : "Moodle no confirmó el cierre, pero el estado ya fue guardado. Regresando…";
      setTimeout(() => {
        if (!leaveScormPlayer()) {
          button.textContent = "Sesión finalizada";
          finishStatus.textContent = "La sesión quedó guardada. Usa el control de salida del reproductor de Moodle para volver al curso.";
        }
      }, 150);
    });
  }

  function moodleReturnUrl() {
    const candidates = [];
    let frame = window;
    for (let depth = 0; depth < 10; depth += 1) {
      try {
        candidates.push(frame.document.referrer, frame.location.href);
        if (frame === frame.parent) break;
        frame = frame.parent;
      } catch (_) {
        break;
      }
    }
    for (const value of candidates) {
      if (!value) continue;
      try {
        const url = new URL(value, window.location.href);
        if (url.origin !== window.location.origin) continue;
        if (url.pathname.includes("/mod/scorm/view.php") || url.pathname.includes("/course/view.php")) return url.href;
        if (url.pathname.includes("/mod/scorm/player.php")) {
          const courseModule = url.searchParams.get("cm") || url.searchParams.get("cmid");
          if (courseModule) return new URL(`/mod/scorm/view.php?id=${encodeURIComponent(courseModule)}`, url.origin).href;
        }
      } catch (_) {
        continue;
      }
    }
    return "";
  }

  function leaveScormPlayer() {
    const target = moodleReturnUrl();
    try {
      if (target) { window.top.location.assign(target); return true; }
      if (window.top.history.length > 1) { window.top.history.back(); return true; }
    } catch (_) {
      if (window.history.length > 1) { window.history.back(); return true; }
    }
    return false;
  }

  function render() {
    nameNode.textContent = runtime.studentName() ? `Estudiante: ${runtime.studentName()}` : "Modo de prueba local";
    if (state.evaluated) renderResult();
    else if (state.stage === 0) renderIntro();
    else if (state.stage <= 4) renderGuidedStep(state.stage - 1);
    else renderEvaluation();
  }

  runtime.initialize();
  state = runtime.restoreState() || createState();
  if (!Array.isArray(state.guidedPoints)) {
    state.guidedPoints = [0, 0, 0, 0];
    for (let index = 0; index < 4; index += 1) {
      if (state.stage > index + 1 && state.attempts?.[index] > 0) state.guidedPoints[index] = state.attempts[index] === 1 ? 3 : 2;
    }
  }
  if (!Number.isFinite(state.points)) state.points = 0;
  render();
})();
