SELECT
	  [Person].[CardNo] AS '員工編號',
	  [DoorLog].[LogArrivalDateTime] AS '打卡時間'
FROM [DoorLog], [Person]
WHERE
    [DoorLog].[EmployeeID] = [Person].[EmployeeID] and
    [DoorLog].[EventAlarmCode] = '正常' and
    [DoorLog].[LogArrivalDateTime] >= '_BEGINDATE_' and
    [DoorLog].[LogArrivalDateTime] <= '_ENDDATE_'