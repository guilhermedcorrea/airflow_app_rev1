CREATE OR ALTER TRIGGER update_table_ranking_tim_d0
ON [BIGDATA].[dbo].[teste_001]
AFTER INSERT, UPDATE, DELETE 
AS
	BEGIN
DECLARE @ranking INT, @grupo INT,@idagente INT

SELECT @idagente = ID_AGENTE ,@grupo = Quartile , @ranking = [RANKING] FROM INSERTED

IF NOT EXISTS(SELECT [ID_AGENTE] FROM [BIGDATA].[comercial].[ranking_atendimento_tim] WHERE id_agente = @idagente )

	INSERT INTO comercial.ranking_atendimento_tim(id_agente,ranking,grupo)
	VALUES(@idagente,@ranking,@grupo)
	
ELSE
	UPDATE [BIGDATA].[comercial].[ranking_atendimento_tim]
	SET ranking = @ranking,grupo =@grupo

	WHERE  [id_agente] = @idagente
	
END
