import AgroEstoqueApp from './App.js';

const root = document.getElementById('root');

if (!root) {
  throw new Error('Root element not found.');
}

root.innerHTML = AgroEstoqueApp();
