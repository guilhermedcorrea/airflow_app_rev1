CREATE TABLE comercial.ranking_atendimento_tim(
	cod_ranking INT IDENTITY(1,1) PRIMARY KEY,
	id_agente INT,
	horas_logado INT,
	horas_falando FLOAT,
	tempo_falando FLOAT,
	qtde_venda INT,
	qtde_linha INT,
	qtde_ligacoes INT,
	conversao_venda FLOAT,
	fim_ultimo_alo DATETIME,
	ultima_atualizacao DATETIME DEFAULT GETDATE(),
	ranking INT,
	grupo INT)
