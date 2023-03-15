--6. Найти список студентов в определенной группе.
SELECT s.id, s.name, sg.name
FROM students s
LEFT JOIN st_groups sg ON s.group_id =sg.id
WHERE sg.id = 1
GROUP BY s.name
ORDER BY s.id