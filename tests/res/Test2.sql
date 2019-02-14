create procedure [dbo].[Test2]
    @ScenarioID int
        -- The scenario to terminate
    ,@Variable2 int
        -- The user who requested termination
    
    ,@PollUntilTerminated bit
        -- When TRUE(1) then the routine will ONLY return when
        -- the scenario has been terminated, and will poll until
        -- this happens
    ,@TestParam    INT = 1
    ,@TestParam2        varchar(100) = 'hello world'
    ,  @TestSpaces varchar(50)
as/*
=============================================================================================
[dbo].[Test2]
    Terminates the EOS Solve Job for the specified ScenarioID

Returns
    * 0: when solve-job was succesful and is not currently running
    * 1: when solve-job is currently running
    * -1: solve-job is aborted

HISTORY
    
    |Release/date       |Editor     |Change
    |-------------------|-----------|--------------------------------------------------------
    |2018-12 (Dec) r3   |J. Phan    |Initial version
=============================================================================================
*/begin

    ;set nocount on

    ;return

end
go