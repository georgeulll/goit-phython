--10.Список курсов, которые определенному студенту читает определенный преподаватель.
SELECT d.name as Discipline_name , s.name as Student_Name , t.fullname as Teacher_name
FROM grades g
LEFT JOIN students s ON g.student_id = s.id
LEFT JOIN disciplines d ON g.discipline_id = d.id
LEFT JOIN teachers t ON d.teacher_id = t.id
WHERE s.id = 4 AND t.id = 2
GROUP BY d.name