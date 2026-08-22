(function attachRuntime(global) {
  "use strict";
  let api = null, initialized = false, startedAt = null;
  const find = (target) => { let current = target; for (let i = 0; current && i < 10; i += 1) { try { if (current.API) return current.API; if (!current.parent || current.parent === current) break; current = current.parent; } catch (_) { break; } } return null; };
  const call = (method, ...args) => api && typeof api[method] === "function" ? api[method](...args) : "false";
  const set = (key, value) => initialized && call("LMSSetValue", key, String(value)) === "true";
  const get = (key) => initialized ? call("LMSGetValue", key) : "";
  const commit = () => initialized && call("LMSCommit", "") === "true";
  function initialize() { if (initialized) return true; api = find(global) || find(global.opener); if (!api) return false; initialized = call("LMSInitialize", "") === "true"; if (initialized) { startedAt = Date.now(); const status = get("cmi.core.lesson_status"); if (!status || status === "not attempted") { set("cmi.core.lesson_status", "incomplete"); commit(); } } return initialized; }
  function restoreState() { try { return JSON.parse(get("cmi.suspend_data") || "null"); } catch (_) { return null; } }
  function saveState(state) { const raw = JSON.stringify(state); return raw.length <= 3800 && set("cmi.suspend_data", raw) && commit(); }
  function setProgress(value) { return set("cmi.core.lesson_location", Math.max(0, Math.min(100, Math.round(value)))); }
  function recordInteraction({id,type,response,correct,weighting=1}) { if (!initialized) return false; const n = get("cmi.interactions._count") || "0", p = `cmi.interactions.${n}`, scormType = type === "true-false" ? "true-false" : type === "numeric" ? "fill-in" : "choice", answer = type === "true-false" ? (response ? "true" : "false") : String(response); return [set(`${p}.id`,id),set(`${p}.type`,scormType),set(`${p}.student_response`,answer),set(`${p}.result`,correct ? "correct" : "wrong"),set(`${p}.weighting`,weighting)].every(Boolean); }
  function recordObjective({id,score,passingScore=60}) { if (!initialized) return false; const n = get("cmi.objectives._count") || "0", p = `cmi.objectives.${n}`, raw = Math.max(0,Math.min(100,Math.round(score*100)/100)); return [set(`${p}.id`,id),set(`${p}.score.min`,0),set(`${p}.score.max`,100),set(`${p}.score.raw`,raw),set(`${p}.status`,raw >= passingScore ? "passed" : "failed")].every(Boolean); }
  function reportScore({score,passingScore=60,completed=true}) { const raw = Math.max(0,Math.min(100,Math.round(score*100)/100)), status = completed ? (raw >= passingScore ? "passed" : "failed") : "incomplete"; return [set("cmi.core.score.min",0),set("cmi.core.score.max",100),set("cmi.core.score.raw",raw),set("cmi.core.lesson_status",status)].every(Boolean) && commit(); }
  function finish() { if (!initialized) return true; const seconds = Math.floor((Date.now() - startedAt) / 1000), pad = n => String(n).padStart(2,"0"); set("cmi.core.session_time", `${pad(Math.floor(seconds/3600))}:${pad(Math.floor(seconds%3600/60))}:${pad(seconds%60)}`); commit(); const done = call("LMSFinish", "") === "true"; initialized = false; api = null; return done; }
  global.TeoriaSenalesScorm12 = Object.freeze({initialize,isConnected:()=>initialized,studentName:()=>get("cmi.core.student_name"),studentId:()=>get("cmi.core.student_id"),restoreState,saveState,setProgress,recordInteraction,recordObjective,reportScore,commit,finish});
  global.addEventListener("pagehide", finish, {once:true});
})(window);
