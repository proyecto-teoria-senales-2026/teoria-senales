(() => {
  "use strict";

  const PASSING_SCORE = 60;
  const OBJECTIVE_PASSING_SCORE = 60;
  const content = document.querySelector("#application-content");
  const nameNode = document.querySelector("#student-name");
  const runtime = window.TeoriaSenalesScorm12;
  const guidedSteps = [
    {
      title: "Verifica el desplazamiento temporal",
      prompt: "Para x(t−t₀), identifica qué aspecto del espectro se conserva y cuál cambia.",
      formula: "x(t−t₀) ↔ X(f)e^(−j2πft₀)",
      expected: { magnitude: "conserva", phase: "cambia" },
      options: [["magnitude", "Magnitud de X(f):", [["conserva", "Se conserva"], ["anula", "Se anula"], ["duplica", "Se duplica"]]], ["phase", "Fase del espectro:", [["cambia", "Cambia por el factor exponencial"], ["igual", "Permanece igual"], ["cero", "Siempre es cero"]]]],
      hint: "El desplazamiento temporal se representa mediante un factor de fase; la magnitud de X(f) se conserva.",
    },
    {
      title: "Aplica el escalado temporal",
      prompt: "Relaciona x(at) con su transformada y el efecto de comprimir la señal en el tiempo.",
      formula: "x(at) ↔ (1/|a|)X(f/a)",
      expected: { factor: "inverse", frequency: "expande" },
      options: [["factor", "Factor de amplitud:", [["direct", "|a|"], ["inverse", "1/|a|"], ["none", "No hay factor"]]], ["frequency", "Al comprimir en tiempo, la representación en frecuencia:", [["expande", "Se expande"], ["comprime", "Se comprime"], ["igual", "No cambia"]]]],
      hint: "El escalado incorpora 1/|a|. Una compresión temporal produce una expansión en frecuencia.",
    },
    {
      title: "Usa la linealidad",
      prompt: "Completa la relación para y(t)=a·x₁(t)+b·x₂(t).",
      formula: "Y(f) = aX₁(f) + bX₂(f)",
      expected: { spectrum: "linear" },
      options: [["spectrum", "Transformada de la combinación:", [["linear", "aX₁(f)+bX₂(f)"], ["product", "X₁(f)X₂(f)"], ["sum", "X₁(f)+X₂(f) sin coeficientes"]]]],
      hint: "La transformada es lineal: los mismos coeficientes de la combinación temporal multiplican cada espectro.",
    },
    {
      title: "Interpreta la dualidad",
      prompt: "Si x(t) ↔ X(f), selecciona el par que expresa la propiedad de dualidad.",
      formula: "X(t) ↔ x(−f)",
      expected: { duality: "correct" },
      options: [["duality", "Propiedad de dualidad:", [["correct", "X(t) ↔ x(−f)"], ["same", "X(t) ↔ x(f)"], ["zero", "X(t) ↔ 0"]]]],
      hint: "La dualidad intercambia señal y espectro, e introduce inversión en la variable de frecuencia.",
    },
  ];
  const questionBank = [
    ["C2-3-P01", "mc", "En x(t−t₀), la magnitud de X(f):", "b", [["a", "Cambia"], ["b", "Se conserva"], ["c", "Se anula"], ["d", "Se duplica"]]],
    ["C2-3-P02", "mc", "El desplazamiento temporal introduce principalmente:", "a", [["a", "Un cambio de fase"], ["b", "Energía"], ["c", "Ruido"], ["d", "Muestreo"]]],
    ["C2-3-P03", "mc", "x(at) se transforma con el factor:", "b", [["a", "|a|"], ["b", "1/|a|"], ["c", "a²"], ["d", "0"]]],
    ["C2-3-P04", "mc", "Comprimir en tiempo produce:", "b", [["a", "Compresión en frecuencia"], ["b", "Expansión en frecuencia"], ["c", "Fase nula"], ["d", "Dualidad"]]],
    ["C2-3-P05", "mc", "La transformada de a·x₁(t)+b·x₂(t) es:", "a", [["a", "aX₁(f)+bX₂(f)"], ["b", "X₁(f)X₂(f)"], ["c", "X₁(f)/X₂(f)"], ["d", "0"]]],
    ["C2-3-P06", "mc", "La linealidad permite:", "a", [["a", "Combinar espectros"], ["b", "Eliminar la fase"], ["c", "Cambiar Fs"], ["d", "Centrar datos"]]],
    ["C2-3-P07", "mc", "La dualidad relaciona:", "a", [["a", "x(t) y X(f)"], ["b", "Dos ventanas"], ["c", "Fs y N"], ["d", "Dos fases"]]],
    ["C2-3-P08", "mc", "Si x(t) ↔ X(f), entonces X(t) ↔:", "b", [["a", "x(f)"], ["b", "x(−f)"], ["c", "−x(f)"], ["d", "0"]]],
    ["C2-3-P09", "mc", "Usar una propiedad evita principalmente:", "a", [["a", "Recalcular la integral"], ["b", "Usar señales"], ["c", "Medir fase"], ["d", "Usar frecuencia"]]],
    ["C2-3-P10", "tf", "Un desplazamiento temporal cambia la fase del espectro.", true],
    ["C2-3-P11", "tf", "El escalado temporal no modifica la variable de frecuencia.", false],
    ["C2-3-P12", "tf", "La linealidad conserva los coeficientes de una combinación.", true],
    ["C2-3-P13", "tf", "La dualidad requiere inversión en la variable de frecuencia.", true],
    ["C2-3-P14", "tf", "La magnitud siempre cambia por un desplazamiento temporal.", false],
    ["C2-3-P15", "tf", "Las propiedades permiten contrastar una predicción con un resultado gráfico.", true],
  ];

  function seededRandom(seed) { let value = 2166136261; for (let i = 0; i < seed.length; i += 1) value = Math.imul(value ^ seed.charCodeAt(i), 16777619); return () => { value += 0x6D2B79F5; let out = value; out = Math.imul(out ^ out >>> 15, out | 1); out ^= out + Math.imul(out ^ out >>> 7, out | 61); return ((out ^ out >>> 14) >>> 0) / 4294967296; }; }
  function sample(items, count, random) { const pool = [...items]; for (let i = pool.length - 1; i > 0; i -= 1) { const j = Math.floor(random() * (i + 1)); [pool[i], pool[j]] = [pool[j], pool[i]]; } return pool.slice(0, count); }
  function selectQuestions(seed) { const random = seededRandom(seed); const selected = [...sample(questionBank.filter((q) => q[1] === "mc"), 3, random), ...sample(questionBank.filter((q) => q[1] === "tf"), 2, random)]; return sample(selected, selected.length, random); }
  function criterionForQuestion(id) { const n = Number(id.slice(-2)); if ([1, 2, 10].includes(n)) return "C2_3_CR1"; if ([3, 4, 11].includes(n)) return "C2_3_CR2"; if ([5, 6, 12, 14].includes(n)) return "C2_3_CR3"; return "C2_3_CR4"; }
  function createState() { const identity = runtime.studentId() || runtime.studentName() || "sesion-local"; return { version: 2, seed: `${identity}-c-2-3`, startedAt: new Date().toISOString(), completedAt: null, stage: 0, answers: {}, attempts: [0, 0, 0, 0], guidedPoints: [0, 0, 0, 0], helpUsed: [false, false, false, false], evaluated: false, points: 0, score: null, feedback: null, feedbackKind: "info" }; }
  let state;
  const save = () => runtime.saveState(state);
  const progress = () => state.evaluated ? 100 : Math.round((state.stage / 5) * 100);
  const heading = (current) => `<div class="progress"><span>Paso ${current} de 5</span><a class="guide-link" href="guia_estudiante_C-2-3.pdf" target="_blank" rel="noopener">Ver guía del estudiante</a><span>${progress()} % completado</span></div><div class="progress-bar"><span style="width:${progress()}%"></span></div>`;
  const feedback = (message, kind) => message ? `<p class="feedback ${kind}">${message}</p>` : "";
  const numericEqual = (actual, expected) => Number.isFinite(actual) && Math.abs(actual - expected) <= 0.001;
  const formatDateTime = (value) => { try { return new Intl.DateTimeFormat("es-CO", { dateStyle: "medium", timeStyle: "medium" }).format(new Date(value)); } catch (_) { return value; } };

  function renderIntro() {
    content.innerHTML = `<section class="card stack"><h2>Actividad guiada</h2><p>Aplica desplazamiento, escalado temporal, linealidad y dualidad para obtener e interpretar transformadas sin recalcular la integral.</p><div class="notice"><strong>Tu avance se guarda en Moodle.</strong> Puedes salir y continuar el mismo intento más tarde.</div><div class="guide-access"><h3>Guía del estudiante C-2-3</h3><p>Consulta la guía antes de comenzar. Permanecerá disponible durante todo el recorrido.</p><a class="button-link secondary" href="guia_estudiante_C-2-3.pdf" target="_blank" rel="noopener">Ver guía del estudiante</a></div><p><strong>Puntaje de los pasos guiados:</strong> cada paso vale 3 puntos si se responde correctamente en el primer intento y 2 puntos si se corrige después.</p><p class="small">La evaluación final selecciona cinco preguntas del banco: tres de selección múltiple y dos de verdadero/falso.</p><div class="actions"><button id="start">Iniciar ejercicio C-2-3</button></div></section>`;
    document.querySelector("#start").addEventListener("click", () => { state.stage = 1; state.feedback = null; save(); render(); });
  }

  function renderGuidedStep(index) {
    const step = guidedSteps[index]; const saved = state.answers[index] || {};
    const fields = (step.fields || []).map(([key, label]) => `<label>${label}<input data-field="${key}" value="${saved[key] ?? ""}" placeholder="Escribe un valor" inputmode="decimal" autocomplete="off"></label>`).join("");
    const options = (step.options || []).map(([key, label, choices]) => `<fieldset><legend>${label}</legend><div class="options">${choices.map(([value, text]) => `<label class="option"><input type="radio" name="${key}" value="${value}" ${saved[key] === value ? "checked" : ""}>${text}</label>`).join("")}</div></fieldset>`).join("");
    const decimalNotice = (step.fields || []).length ? '<p class="notice"><strong>Importante:</strong> utiliza punto (.) como separador decimal. Ejemplo: 1.5</p>' : "";
    content.innerHTML = `<section class="card stack">${heading(index + 1)}<h2>${step.title}</h2><p>${step.prompt}</p><p class="small">Puntaje: 3 puntos al acertar en el primer intento; 2 puntos al corregir después.</p>${decimalNotice}<p class="formula">${step.formula}</p><form id="guided-form"><div class="input-grid">${fields}</div>${options}<div class="actions"><button type="submit">Verificar respuesta</button><button class="secondary" type="button" id="help" ${state.helpUsed[index] ? "disabled" : ""}>Ver orientación</button></div></form>${feedback(state.feedback, state.feedbackKind || "info")}</section>`;
    document.querySelector("#guided-form").addEventListener("submit", (event) => { event.preventDefault(); validateGuidedStep(index); });
    document.querySelector("#help").addEventListener("click", () => { state.helpUsed[index] = true; state.feedback = step.hint; state.feedbackKind = "info"; save(); render(); });
  }

  function validateGuidedStep(index) {
    const step = guidedSteps[index]; const answer = {};
    (step.fields || []).forEach(([key]) => { answer[key] = document.querySelector(`[data-field="${key}"]`).value; });
    (step.options || []).forEach(([key]) => { answer[key] = document.querySelector(`input[name="${key}"]:checked`)?.value || ""; });
    state.answers[index] = answer; state.attempts[index] += 1;
    const correct = Object.entries(step.expected).every(([key, expected]) => typeof expected === "number" ? numericEqual(Number(answer[key]), expected) : answer[key] === expected);
    runtime.recordInteraction({ id: `C2_3_PASO_${index + 1}_${state.attempts[index]}`, type: "fill-in", response: JSON.stringify(answer), correct, weighting: 1 });
    if (correct) { state.guidedPoints[index] = state.attempts[index] === 1 ? 3 : 2; runtime.recordObjective({ id: `C2_3_CR${Math.min(index + 1, 3)}`, score: (state.guidedPoints[index] / 3) * 100, passingScore: OBJECTIVE_PASSING_SCORE }); state.stage += 1; state.feedback = null; state.feedbackKind = null; }
    else { state.feedback = `El resultado todavía no coincide. Intento ${state.attempts[index]} registrado. Revisa el procedimiento y vuelve a intentarlo.`; state.feedbackKind = "error"; }
    save(); runtime.setProgress(progress()); render();
  }

  function renderEvaluation() {
    const questions = selectQuestions(state.seed);
    content.innerHTML = `<section class="card stack">${heading(5)}<h2>Evaluación final</h2><p>Responde las cinco preguntas asignadas. La calificación final se registra en Moodle en la escala de 0 a 100.</p><p class="small"><strong>Distribución:</strong> pasos guiados: hasta 12 puntos; selección múltiple: 6 puntos; verdadero/falso: 2 puntos.</p><form id="evaluation-form" class="stack">${questions.map(([id, type, prompt, expected, options]) => `<fieldset><legend>${id} · ${prompt}</legend><div class="options">${type === "mc" ? options.map(([key, label]) => `<label class="option"><input type="radio" name="${id}" value="${key}">${key.toUpperCase()}. ${label}</label>`).join("") : `<label class="option"><input type="radio" name="${id}" value="true">Verdadero</label><label class="option"><input type="radio" name="${id}" value="false">Falso</label>`}</div></fieldset>`).join("")}<div class="actions"><button type="submit">Calificar y finalizar</button></div></form>${feedback(state.feedback, state.feedbackKind || "info")}</section>`;
    document.querySelector("#evaluation-form").addEventListener("submit", (event) => { event.preventDefault(); gradeEvaluation(questions); });
  }

  function gradeEvaluation(questions) {
    let conceptualPoints = 0; const unanswered = []; const criterionResults = {};
    questions.forEach(([id, type, prompt, expected]) => { const response = document.querySelector(`input[name="${id}"]:checked`)?.value; if (response === undefined) { unanswered.push(id); return; } const normalized = type === "tf" ? response === "true" : response; const correct = normalized === expected; const weighting = type === "mc" ? 2 : 1; runtime.recordInteraction({ id, type: type === "tf" ? "true-false" : "choice", response: normalized, correct, weighting }); const criterion = criterionForQuestion(id); criterionResults[criterion] ||= { correct: 0, total: 0 }; criterionResults[criterion].total += 1; if (correct) { criterionResults[criterion].correct += 1; conceptualPoints += weighting; } });
    if (unanswered.length) { state.feedback = `Responde todas las preguntas antes de calificar: ${unanswered.join(", ")}.`; state.feedbackKind = "error"; render(); return; }
    state.evaluated = true; state.points = state.guidedPoints.reduce((total, value) => total + value, 0) + conceptualPoints; state.score = Math.round((state.points / 20) * 100); state.completedAt = new Date().toISOString(); state.feedback = null; runtime.setProgress(100); Object.entries(criterionResults).forEach(([id, result]) => runtime.recordObjective({ id, score: (result.correct / result.total) * 100, passingScore: OBJECTIVE_PASSING_SCORE })); runtime.reportScore({ score: state.score, passingScore: PASSING_SCORE, completed: true }); save(); render();
  }

  function renderResult() {
    const status = state.score >= PASSING_SCORE ? "Actividad aprobada" : "Actividad finalizada";
    content.innerHTML = `<section class="card stack"><p class="eyebrow">Resultado registrado</p><h2>${status}</h2><p class="score">${state.score.toFixed(2).replace(".", ",")} / 100</p><p>${state.points} / 20 puntos</p><p>Finalización registrada: <strong>${formatDateTime(state.completedAt || new Date().toISOString())}</strong>.</p><p>La actividad envió a Moodle la nota, el estado de finalización, el avance, las interacciones y los resultados por criterio.</p><div class="notice">El docente consulta el resultado y la fecha/hora oficial del intento directamente desde Moodle. No necesitas descargar ni entregar un archivo adicional.</div><div class="actions"><button id="finish">Finalizar y salir</button></div><p id="finish-status" class="small" aria-live="polite"></p></section>`;
    document.querySelector("#finish").addEventListener("click", () => { const button = document.querySelector("#finish"); const finishStatus = document.querySelector("#finish-status"); button.disabled = true; button.textContent = "Guardando y saliendo…"; save(); runtime.commit(); const finished = runtime.finish(); finishStatus.textContent = finished ? "Sesión finalizada. Regresando a Moodle…" : "Moodle no confirmó el cierre, pero el estado ya fue guardado. Regresando…"; setTimeout(() => { if (!leaveScormPlayer()) { button.textContent = "Sesión finalizada"; finishStatus.textContent = "La sesión quedó guardada. Usa el control de salida del reproductor de Moodle para volver al curso."; } }, 150); });
  }

  function moodleReturnUrl() { const candidates = []; let frame = window; for (let depth = 0; depth < 10; depth += 1) { try { candidates.push(frame.document.referrer, frame.location.href); if (frame === frame.parent) break; frame = frame.parent; } catch (_) { break; } } for (const value of candidates) { if (!value) continue; try { const url = new URL(value, window.location.href); if (url.origin !== window.location.origin) continue; if (url.pathname.includes("/mod/scorm/view.php") || url.pathname.includes("/course/view.php")) return url.href; if (url.pathname.includes("/mod/scorm/player.php")) { const courseModule = url.searchParams.get("cm") || url.searchParams.get("cmid"); if (courseModule) return new URL(`/mod/scorm/view.php?id=${encodeURIComponent(courseModule)}`, url.origin).href; } } catch (_) { continue; } } return ""; }
  function leaveScormPlayer() { const target = moodleReturnUrl(); try { if (target) { window.top.location.assign(target); return true; } if (window.top.history.length > 1) { window.top.history.back(); return true; } } catch (_) { if (window.history.length > 1) { window.history.back(); return true; } } return false; }
  function render() { nameNode.textContent = runtime.studentName() ? `Estudiante: ${runtime.studentName()}` : "Modo de prueba local"; if (state.evaluated) renderResult(); else if (state.stage === 0) renderIntro(); else if (state.stage <= 4) renderGuidedStep(state.stage - 1); else renderEvaluation(); }

  runtime.initialize(); state = runtime.restoreState() || createState();
  if (!Array.isArray(state.guidedPoints)) { state.guidedPoints = [0, 0, 0, 0]; for (let index = 0; index < 4; index += 1) if (state.stage > index + 1 && state.attempts?.[index] > 0) state.guidedPoints[index] = state.attempts[index] === 1 ? 3 : 2; }
  if (!Number.isFinite(state.points)) state.points = 0;
  if (!Array.isArray(state.helpUsed)) state.helpUsed = state.help || [false, false, false, false];
  render();
})();
