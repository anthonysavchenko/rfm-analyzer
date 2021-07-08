SELECT
	--t1.WeeksSinceFirstMonday,
    --t1.CustomerId,
	t1.Phone,
	t1.CustomerName,
	t1.WeeksSinceLastPay,
	t1.PayedWeeks,
	t1.PayedTotal,
	ROUND((t1.WeeksSinceFirstMonday - t1.WeeksSinceLastPay) / PayedWeeks, 2) AS Ntc,
	CASE
		WHEN
			t1.WeeksSinceLastPay >= ROUND((t1.WeeksSinceFirstMonday - t1.WeeksSinceLastPay) / PayedWeeks, 2) * 3
		THEN
			'4 - Black'
		WHEN
			t1.WeeksSinceLastPay >= ROUND((t1.WeeksSinceFirstMonday - t1.WeeksSinceLastPay) / PayedWeeks, 2) * 2
		THEN
			'1 - Red'
		WHEN
			t1.WeeksSinceLastPay >= ROUND((t1.WeeksSinceFirstMonday - t1.WeeksSinceLastPay) / PayedWeeks, 2)
		THEN
			'2 - Yellow'
		ELSE
			'3 - Green'
	END AS Sector
FROM
    (SELECT
	    c.Id AS CustomerId,
        '+' || SUBSTR(c.Phone, 1, 1) || ' (' || SUBSTR(c.Phone, 2, 3) || ') ' || SUBSTR(c.Phone, 5, 3)
			|| '-' || SUBSTR(c.Phone, 8, 2) || '-' || SUBSTR(c.Phone, 10, 2) AS Phone,
		c.CustomerName,
		(JULIANDAY('2021-07-05') - JULIANDAY('2021-01-04')) / 7 AS WeeksSinceFirstMonday, --Current week monday param AND First monday param
		CAST((JULIANDAY('2021-07-05') - JULIANDAY(MAX(w.Since))) / 7 AS INTEGER) AS WeeksSinceLastPay, --Current week monday param
        COUNT(w.ID) AS PayedWeeks,
        SUM(w.Payed) AS PayedTotal
    FROM
        Customers AS c
    JOIN
        Weeks AS w
    ON
        c.ID = w.CustomerId
    GROUP BY
        c.ID,
        c.CustomerName,
        c.Phone) AS t1
ORDER BY
	Sector,
	PayedTotal DESC;
