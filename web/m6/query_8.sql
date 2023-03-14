--8.Найти средний балл, который ставит определенный преподаватель по своим предметам.
SELECT t.fullname , d.name , ROUND(AVG(g.grade),2) as Average_Grade
FROM grades g
LEFT JOIN disciplines d ON g.discipline_id =d.id
LEFT JOIN teachers t ON d.teacher_id =t.id
WHERE t.id = 3
GROUP BY d.id
ORDER BY Average_Grade DESC