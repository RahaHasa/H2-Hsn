const express = require('express');
const router = express.Router();
const db = require('../database');

// Получить всех пользователей
router.get('/', (req, res) => {
  db.all('SELECT * FROM users', [], (err, rows) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    res.json({ users: rows });
  });
});

// Добавить нового пользователя
router.post('/', (req, res) => {
  const { name, phone, type, car_number, discount, bonuses, registration_date } = req.body;
  db.run(`INSERT INTO users (name, phone, type, car_number, discount, bonuses, registration_date) VALUES (?, ?, ?, ?, ?, ?, ?)`,
    [name, phone, type, car_number, discount, bonuses, registration_date],
    function(err) {
      if (err) {
        return res.status(500).json({ error: err.message });
      }
      res.json({ id: this.lastID });
    });
});

module.exports = router; 