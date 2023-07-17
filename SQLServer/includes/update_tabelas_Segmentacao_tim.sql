
-- UPDATE TEMPO
IF NOT EXISTS (SELECT * FROM tempo_operacional_agente_tim
	WHERE ID_AGENTE IN (SELECT idagente FROM BANCO_TESTE.comercial.tempo_trabalhado))

		BEGIN
			INSERT INTO BANCO_TESTE.comercial.tempo_trabalhado(idagente ,tempo_logado ,tempo_disponivel ,tempo_medio_disponivel ,tempo_falado,horas_logado
								  ,horas_falando,porcentagem_tempo_falado,data_cadastro ,id_campanha, cod_derivado)

			SELECT ID_AGENTE,TEMPO_LOGADO,TEMPO_DISPONIVEL,TEMPO_MEDIO_DISPONIVEL,TEMPO_FALADO,HORAS_LOGADO
				,HORAS_FALANDO,PORCENTAGEM_TEMPO_FALADO,DATACADASTRO,ID_CAMPANHA,cod_derivado
				FROM  tempo_operacional_agente_tim
		END
	ELSE
		BEGIN
		UPDATE temp
		SET temp.idagente = seg.ID_AGENTE
		,temp.tempo_logado = seg.TEMPO_LOGADO
		,temp.tempo_disponivel = seg.TEMPO_DISPONIVEL
		,temp.tempo_medio_disponivel = seg.TEMPO_MEDIO_DISPONIVEL
		,temp.tempo_falado = seg.TEMPO_FALADO
		,temp.horas_logado = seg.HORAS_LOGADO
		,temp.horas_falando = seg.HORAS_FALANDO
		,temp.porcentagem_tempo_falado = seg.PORCENTAGEM_TEMPO_FALADO
		,temp.data_cadastro = seg.DATACADASTRO
		,temp.cod_derivado = tabseg.cod_derivado
		,temp.id_campanha = seg.ID_CAMPANHA
     
		FROM tempo_operacional_agente_tim AS seg
		LEFT JOIN [BANCO_TESTE].[comercial].[tempo_trabalhado] AS temp ON temp.idagente = seg.ID_AGENTE
		LEFT JOIN [BANCO_TESTE].[comercial].[segmentacao_tim] AS tabseg ON tabseg.idagente = seg.ID_AGENTE

	END



-- UPDATE SEGMENTACAO

IF NOT EXISTS (SELECT * FROM BANCO_TESTE.dbo.SEGMENTACAO_atendimento_tim
	WHERE IDAGENTE IN (SELECT idagente FROM comercial.segmentacao_tim))
	BEGIN

		INSERT INTO comercial.segmentacao_tim (idagente,tipo_campanha,qtd_deriv,qtd_venda,qtd_manual,conversao_derivada,linhas,data_cadastro)
		SELECT IDAGENTE,TIPO_CAMPANHA,QTD_DERIV,QTD_VENDA,QTDE_MANUAL,CONV_DERIVADA,linhas,DATACADASTRO
		FROM BANCO_TESTE.dbo.SEGMENTACAO_atendimento_tim
	END

ELSE
	BEGIN
		UPDATE seg
			SET 
			seg.idagente = satendimento.IDAGENTE
			,seg.tipo_campanha =satendimento.TIPO_CAMPANHA
			,seg.qtd_deriv =satendimento.QTD_DERIV
			,seg.qtd_venda =satendimento.QTD_VENDA
			,seg.qtd_manual =satendimento.QTDE_MANUAL
			,seg.conversao_derivada =satendimento.CONV_DERIVADA
			,seg.linhas =satendimento.linhas
			,seg.data_cadastro = satendimento.DATACADASTRO

		FROM comercial.segmentacao_tim as seg
		LEFT JOIN BANCO_TESTE.dbo.SEGMENTACAO_atendimento_tim as satendimento ON seg.idagente = satendimento.IDAGENTE

	END