def NoutCO2Query(**kwargs):

    return f'''
    WITH CTE AS
    (
      SELECT  
        clientid,
        max(hp1_thermalEnergyCounter) - min(hp1_thermalEnergyCounter) AS Q_hp1,
        max(hp1_electricalEnergyCounter) - min(hp1_electricalEnergyCounter) AS E_hp1,
        ifNull(max(hp2_thermalEnergyCounter) - min(hp2_thermalEnergyCounter), 0) AS Q_hp2,
        ifNull(max(hp2_electricalEnergyCounter) - min(hp2_electricalEnergyCounter), 0) AS E_hp2,
        max(qc_cvEnergyCounter) - min(qc_cvEnergyCounter) AS Q_cv
      FROM 
        "cic_stats"
      WHERE
        time_ts BETWEEN '{kwargs.get('StartTime')}' AND '{kwargs.get('EndTime')}' 
        AND qc_supervisoryControlMode in (2,3,4)
      GROUP BY
        clientid
      HAVING
        (Q_hp1 + Q_hp2 + Q_cv) >  {kwargs.get('Q_min')}*1000
    )
    SELECT
      COUNT(clientid) AS ActiveClientID,
      SUM(Q_hp1 + Q_hp2) AS Total_hpHeat_diff,
      SUM(E_hp1 + E_hp2) AS Total_hpElectric_diff,
      SUM(Q_cv) AS Total_boilerHeat_diff,
      SUM(Q_hp1 + Q_hp2)/SUM(E_hp1 + E_hp2) AS Total_COP,
      SUM(Q_hp1 + Q_hp2) / 1000 / 8.8 AS Savings_Gas, 
      SUM(Q_hp1 + Q_hp2) / 1000 / 8.8 * 1.788 AS CO2_Gas_Saved, 
      SUM(E_hp1 + E_hp2) * 0.272 / 1000 AS CO2_Electricity,
      ((SUM(Q_hp1 + Q_hp2) / 8.8 * 1.788) - (SUM(E_hp1 + E_hp2) * 0.272)) / 1000 AS Savings_CO2
    FROM
      CTE
    '''




