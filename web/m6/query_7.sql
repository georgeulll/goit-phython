--7.Найти оценки студентов в отдельной группе по определенному предмету.
SELECT s.name, g.grade, sg.name , d.name
FROM grades g
LEFT JOIN students s ON g.student_id =s.id
LEFT JOIN st_groups sg ON s.group_id =sg.id
LEFT JOIN disciplines d ON g.discipline_id =d.id
WHERE sg.id = 2 AND d.id = 2
GROUP BY s.id
ORDER BY g.grade DESC
