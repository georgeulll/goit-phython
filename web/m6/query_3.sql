--3. Найти средний балл в группах по определенному предмету.
SELECT d.name as discipline_name, sg.name as Groups_Name, ROUND(AVG(g.grade),2) as Average_grade
FROM grades g
LEFT JOIN students s ON g.student_id = s.id
LEFT JOIN disciplines d ON g.discipline_id =d.id
LEFT JOIN st_groups sg ON s.group_id =sg.id
WHERE d.id = 6
GROUP BY sg.name
ORDER BY sg.id