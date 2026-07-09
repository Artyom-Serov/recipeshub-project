import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { BrowserRouter } from 'react-router-dom'

ReactDOM.render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>,
  document.getElementById('root')
);

// Если хотите начать измерять производительность в приложении, передайте функцию
// для логирования результатов (например: reportWebVitals(console.log))
// или отправьте на analytics-эндпоинт. Подробнее: https://bit.ly/CRA-vitals
reportWebVitals();
