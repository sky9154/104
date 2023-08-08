SELECT
    [CardNo] AS '員工編號',
    [DateTime] AS '打卡時間'
FROM (
    SELECT 
        [Person].[CardNo],
        [DoorLog].[DateTime],
        ROW_NUMBER() OVER (PARTITION BY [Person].[CardNo] ORDER BY [Person].[CardNo] ASC) AS row_num
    FROM [Person], [DoorLog]
    WHERE
        [DoorLog].[EmployeeID] = [Person].[EmployeeID] and
        [DoorLog].[EventAlarmCode] = '正常' and
        [DoorLog].[DateTime] >= '_BEGINDATE_' and
        [DoorLog].[DateTime] <= '_ENDDATE_'
) AS subquery
WHERE row_num = 1
ORDER BY [CardNo]