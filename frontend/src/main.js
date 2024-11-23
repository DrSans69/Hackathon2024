import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './main.css'; // Ваш CSS

function Main() {
  const [field1, setField1] = useState('');
  const [field2, setField2] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log('Поле 1:', field1);
    console.log('Поле 2:', field2);
    setField1('');
    setField2('');
  };

  // Функція для автоматичного розширення textarea
  const adjustTextareaHeight = (e) => {
    e.target.style.height = 'auto'; // Скидання висоти, щоб отримати актуальну висоту
    e.target.style.height = `${e.target.scrollHeight}px`; // Встановлення висоти від значення scrollHeight
  };

  return (
    <div className="container mt-5">
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="field1">File:</label>
          <textarea 
            id="field1"
            value={field1}
            onChange={(e) => {
              setField1(e.target.value);
              adjustTextareaHeight(e); // Виклик функції для автоматичного розширення
            }} 
            className="form-control input-field-1"
            rows="1" // Мінімальна кількість рядків
          />
        </div>
        <div className="form-group">
          <label htmlFor="field2">Instruction:</label>
          <textarea 
            id="field2"
            value={field2}
            onChange={(e) => {
              setField2(e.target.value);
              adjustTextareaHeight(e); // Виклик функції для автоматичного розширення
            }} 
            className="form-control input-field-2"
            rows="1" // Мінімальна кількість рядків
          />
        </div>
        <button type="submit" className="btn btn-primary btn-block">Submit</button>
      </form>
    </div>
  );
}

export default Main;