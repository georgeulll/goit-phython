SELECT ROUND(AVG(g.grade), 2) as Average_Grade, s.name 
FROM grades g 
LEFT JOIN students s ON g.student_id =s.id 
GROUP BY s.name 
ORDER BY Average_Grade DESC
LIMIT 5