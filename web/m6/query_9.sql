--9.Найти список курсов, которые посещает определенный студент.
SELECT s.name, d.name
FROM grades g
LEFT JOIN disciplines d ON g.discipline_id =d.id
LEFT JOIN students s ON g.student_id = s.id
WHERE s.id = 10
GROUP BY d.name
ORDER BY d.name