SELECT
	--t1.WeeksSinceFirstMonday,
    --t1.CustomerId,
	t1.Phone,
	t1.CustomerName,
	t1.WeeksSinceFirstPay,
	t1.WeeksSinceLastPay,
	t1.PayedWeeks,
	t1.PayedTotal,
	ROUND(CAST((t1.WeeksSinceFirstPay - t1.WeeksSinceLastPay) AS REAL) / (PayedWeeks - 1), 2) AS Ntc,
	CASE
		WHEN
			PayedWeeks <= 1
		THEN
			'5 - Unknown'
		WHEN
			t1.WeeksSinceLastPay > ROUND(CAST((t1.WeeksSinceFirstPay - t1.WeeksSinceLastPay) AS REAL) / (PayedWeeks - 1), 2) * 3
		THEN
			'4 - Black'
		WHEN
			t1.WeeksSinceLastPay > ROUND(CAST((t1.WeeksSinceFirstPay - t1.WeeksSinceLastPay) AS REAL) / (PayedWeeks - 1), 2) * 2
		THEN
			'1 - Red'
		WHEN
			t1.WeeksSinceLastPay > ROUND(CAST((t1.WeeksSinceFirstPay - t1.WeeksSinceLastPay) AS REAL) / (PayedWeeks - 1), 2)
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
		CAST((JULIANDAY('2021-10-11') - JULIANDAY('2021-01-04')) / 7 AS INTEGER) AS WeeksSinceFirstMonday, --Current week monday param AND First monday param
		CAST((JULIANDAY('2021-10-11') - JULIANDAY(MAX(w.Since))) / 7 AS INTEGER) AS WeeksSinceLastPay, --Current week monday param
		CAST((JULIANDAY('2021-10-11') - JULIANDAY(MIN(w.Since))) / 7 AS INTEGER) AS WeeksSinceFirstPay, --Current week monday param
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
