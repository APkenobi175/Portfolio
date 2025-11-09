import "./App.css";
import { useEffect, useMemo, useRef, useState } from "react";
import { ROWS, SHIFTED, PHRASES } from "./keyboardandphrases";

export default function App() {
  // set up state variables
  const [phraseIndex, setPhraseIndex] = useState(0);
  const [index, setIndex] = useState(0); // current char position
  const [pressedKeys, setPressedKeys] = useState(new Set());
  //useRef from react to track currently pressed keys
  const pressedRef = useRef(new Set());
  const phrase = PHRASES[phraseIndex];
  const nextChar = phrase[index] ?? null;
  // current phrase, and next character to type

  // Ensure we start at phrase 0, because star wars quotes in order
  useEffect(() => {
    setPhraseIndex(0);
    setIndex(0);
  }, []);

  // Debug: log phrase index changes so we can trace order (i want them to appear in order but for some reason its skipping by 2)
  // useEffect(() => {
  //   // phrase changed
  //   console.log('phraseIndex changed ->', phraseIndex);
  // }, [phraseIndex]);

  // Compute required keyboard key + whether Shift is needed


  //useMemo from react memorizes the key calculation unless nextChar changes
  const required = useMemo(() => {
    if (!nextChar) return null;
    if (nextChar === " ") return { key: "Space", needsShift: false };
    if (/[A-Z]/.test(nextChar)) return { key: nextChar.toLowerCase(), needsShift: true };
    for (const [base, shifted] of Object.entries(SHIFTED)) {
      if (shifted === nextChar) return { key: base, needsShift: true };
    }
    return { key: nextChar, needsShift: false };
  }, [nextChar]);

  const shiftActive = pressedKeys.has("Shift"); // determine if Shift is currently pressed

    useEffect(() => { // keydown/keyup handlers






    function onDown(e) { 
      if (e.repeat) return; // don’t advance on held key
      const k = normalizeKey(e.key);
      // ignore duplicate keydown events for the same physical key
      if (pressedRef.current.has(k)) return;
      pressedRef.current.add(k);
      setPressedKeys(prev => { // add to pressed keys
        const n = new Set(prev);
        n.add(k);
        return n;
      });

      if (!nextChar) return; 

      // Actual character produced by this keydown
      const produced = charFromEvent(e);
      if (!produced) return; // ignore control keys

      if (produced === nextChar) {
        // check if this is the last character in the phrase
        const isLastChar = index === phrase.length - 1;

        if (isLastChar) {
          // phrase complete: advance to the next phrase in order and reset char index. 
          // I want it to go in order and not be random becauyse star wars
          setPhraseIndex(p => (p + 1) % PHRASES.length);
          setIndex(0);
        } else {
          // just move to the next character
          setIndex(i => i + 1);
        }
      }
    }




    function onUp(e) { // on key release remove from pressed keys
      const k = normalizeKey(e.key);
      // update ref first so duplicate handling is prevented
      pressedRef.current.delete(k);
      setPressedKeys(prev => {
        const n = new Set(prev);
        n.delete(k); // remopve key from set
        return n; // return set minus released key
      });
    }

    // event listeners for keydown and keyup
    window.addEventListener("keydown", onDown);
    window.addEventListener("keyup", onUp);
    return () => {
      window.removeEventListener("keydown", onDown);
      window.removeEventListener("keyup", onUp);
    };
  }, [nextChar, phrase, index]);







  /// BUILD THE KEYBOARD AND PHRASE DISPLAY

  // split phrase into typed / current / remaining
  const typed = phrase.slice(0, index);
  const current = phrase[index] ?? "";
  const remaining = phrase.slice(index + 1);

  // build the keyboard display
  const requiredKey = required?.key ?? null;
  const needsShift = required?.needsShift ?? false;

  const showLetterHighlight =
    requiredKey && (!needsShift || (needsShift && shiftActive));
  const showShiftHighlight = needsShift && !shiftActive;
  // for loop to build the keyboard rows
  const rows = [];
  for (let i = 0; i < ROWS.length; i++) {
    const rowKeys = []; // keys in the current row
    // iterate over each key in the row, building its display
    for (let j = 0; j < ROWS[i].length; j++) {
      const raw = ROWS[i][j];
      const label = displayLabel(raw, shiftActive);
      const isPressed = pressedKeys.has(raw);
      const isRequiredLetter = showLetterHighlight && raw === requiredKey;
      const isRequiredShift = showShiftHighlight && raw === "Shift";
      // build class names based on the key's state
      let classes = "key";
      if (raw === "Space") classes += " space";
      if (raw === "Shift") classes += " shift";
      if (isPressed) classes += " pressed";
      if (isRequiredLetter || isRequiredShift) classes += " needs";
      // add the key to the current row
      rowKeys.push(
        <div key={raw + i + j} className={classes}>
          {raw === "Space" ? "Space" : label}
        </div>
      );
    } // end of keys in row
    // add the completed row to the keyboard
    rows.push(
      <div className="kb-row" key={i}>
        {rowKeys}
      </div>
    );
  }

  return (
    <div className="app">
      <div className="phrase">
        <span className="typed">{typed}</span>
        {current && <span className="underline">{current}</span>}
        <span className="remaining">{remaining}</span>
      </div>
      <div className="kb">{rows}</div>
    </div>
  );
}

// normalize the key to our keyboard keys (if he key is not recognized then just ignore it
function normalizeKey(k) {
  if (k === " ") return "Space";
  if (k === "ShiftLeft" || k === "ShiftRight") return "Shift";

  if (k.length === 1) {
    // if this is a shifted symbol, find its base key so we can animate it
    for (const [base, shifted] of Object.entries(SHIFTED)) {
      if (shifted === k) {
        return base;
      }
    }
    // letters and unshifted symbols
    return k.toLowerCase();
  }

  return k; 
}

// Character actually produced (used to compare against phrase char)
function charFromEvent(e) {
  if (e.key === " ") return " ";
  if (e.key.length === 1) return e.key; // includes shifted symbols and uppercase
  return ""; // keys that don't matter we will ignore
}

// helper function for building the keyboard that gets the label for the keys based on if shift is pressed or not
function displayLabel(k, shift) {
  if (k === "Space") return " ";
  if (k === "Shift") return "Shift";
  if (/[a-z]/.test(k)) return shift ? k.toUpperCase() : k;
  return shift && SHIFTED[k] ? SHIFTED[k] : k;
}
