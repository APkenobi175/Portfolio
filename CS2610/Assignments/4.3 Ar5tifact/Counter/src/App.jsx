import { useState } from 'react';
import './App.css';

export default function App(){
  const [count, setCount] = useState(0);

  function increment(){
    setCount((oldState) => oldState + 1);
  }

  function decrement(){
    setCount((oldState) => oldState - 1);
  }
  function incrementByFive(){
    setCount((oldState) => oldState + 5);
  }
  function decrementByFive(){
    setCount((oldState) => oldState - 5);
  }
  function multiplyByTwo(){
    setCount((oldState) => oldState * 2);
  }
  function divideByTwo(){
    setCount((oldState) => oldState / 2);
  }
  function reset(){
    setCount(() => 0);
  }

  return(


    <main className = "counter">
      <h1>Counter Application</h1>
      <h2 className="count">Current Count: {count}</h2>
      <div className = "buttons">
        <button onClick={increment}>Increment +1</button>
        <button onClick={decrement}>Decrement -1</button>
        <button onClick={incrementByFive}>Increment +5</button>
        <button onClick={decrementByFive}>Decrement -5</button>
        <button onClick={multiplyByTwo}>Multiply by 2</button>
        <button onClick={divideByTwo}>Divide by 2</button>
        <button className="reset" onClick={reset}>Reset</button>
      </div>
    </main>

  )

}