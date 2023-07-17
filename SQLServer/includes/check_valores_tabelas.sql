IF NOT EXISTS(SELECT [ID_AGENTE] FROM [BIGDATA].[dbo].[teste_001] WHERE [ID_AGENTE] IN (SELECT id_agente FROM  comercial.ranking_atendimento_tim))

	INSERT INTO comercial.ranking_atendimento_tim(id_agente,ranking,grupo)

	SELECT x.[ID_AGENTE],x.[RANKING],x.[Quartile]

	FROM [BIGDATA].[dbo].[teste_001] as x
	left join  comercial.ranking_atendimento_tim AS Y
	ON Y.id_agente = X.ID_AGENTE 
	WHERE NOT EXISTS(SELECT * FROM comercial.ranking_atendimento_tim as t WHERE t.id_agente = x.ID_AGENTE)
ELSE
	UPDATE tranking
	SET ranking = base.[RANKING]
	,grupo =base.[Quartile]
	,id_agente = base.[ID_AGENTE]
	FROM comercial.ranking_atendimento_tim AS tranking
	LEFT JOIN [BIGDATA].[dbo].[teste_001] AS base ON base.ID_AGENTE = tranking.id_agente
	WHERE tranking.id_agente = base.ID_AGENTE