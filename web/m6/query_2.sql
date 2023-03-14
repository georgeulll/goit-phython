--2. Знайти студента із найвищим середнім балом з певного предмета.
SELECT g.discipline_id, d.name as discipline_name, AVG(g.grade) as Average_grade, s.name
FROM grades g
LEFT JOIN students s ON g.student_id = s.id
LEFT JOIN disciplines d ON g.discipline_id =d.id
WHERE g.discipline_id = 6
GROUP BY s.name
ORDER BY Average_grade DESC
LIMIT 5