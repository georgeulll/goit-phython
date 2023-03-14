--5.Найти какие курсы читает определенный преподаватель.
SELECT t.id as Teacher_id , t.fullname , d.name as disciplines_name
FROM disciplines d
LEFT JOIN teachers t ON d.teacher_id =t.id
WHERE t.id = 1
GROUP BY d.id
ORDER BY t.id