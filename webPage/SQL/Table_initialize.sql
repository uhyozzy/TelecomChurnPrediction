-- Main Table create
DROP TABLE IF EXISTS `tb_user`;
CREATE TABLE `tb_user` ( -- User information
	`Customer_ID`	CHAR(10)	NOT NULL,
	`Age`	INT	NOT NULL,
	`Satisfaction_Score`	INT	NOT NULL,
    `Membership`	CHAR(10)	NULL,
	`Churn_Value`	Boolean	NULL	DEFAULT 0,
    `Changed` Boolean NULL DEFAULT 0, -- Changed
    `Churn_proba` INT Null DEFAULT 0, -- Probability
    `Churn_proba_group` CHAR(10) Null DEFAULT 0 -- Probability Group
); 

DROP TABLE IF EXISTS `tb_contract`;
CREATE TABLE `tb_contract` ( -- Contract information
	`Customer_ID`	CHAR(10)	NOT NULL,
	`Contract`	VARCHAR(20)	NULL,
	`Tenure_in_months`	BIGINT	NULL,
	`Monthly_Charge`	FLOAT	NULL,
	`Total_Revenue`	FLOAT	NULL
);

DROP TABLE IF EXISTS `tb_service`;
CREATE TABLE `tb_service` ( -- Service information
	`Customer_ID`	CHAR(10)	NOT NULL,
	`Tech_services`	INT	NULL,
	`Streaming_services`	INT	NULL,
	`Combined_Product`	INT	NULL,
	`Number_of_Dependents`	INT	NULL
);

DROP TABLE IF EXISTS `tb_user_log`;
CREATE TABLE `tb_user_log` ( -- Change log information
	`Customer_ID`	CHAR(10)	NOT NULL,
    `Change_time` DATETIME NOT NULL,
	`Age`	INT	NOT NULL,
	`Satisfaction_Score`	INT	NOT NULL,
	`Churn_Value`	Boolean	NULL	DEFAULT 0
);

DROP TABLE IF EXISTS `tb_contract_log`;
CREATE TABLE `tb_contract_log` ( -- Change log information
	`Customer_ID`	CHAR(10)	NOT NULL,
    `Change_time` DATETIME NOT NULL,
	`Contract`	VARCHAR(20)	NULL,
	`Tenure_in_months`	BIGINT	NULL,
	`Monthly_Charge`	FLOAT	NULL,
	`Total_Revenue`	FLOAT	NULL
);

DROP TABLE IF EXISTS `tb_service_log`;
CREATE TABLE `tb_service_log` ( -- Change log information
	`Customer_ID`	CHAR(10)	NOT NULL,
    `Change_time` DATETIME NOT NULL,
    `Tech_services`	INT	NULL,
	`Streaming_services`	INT	NULL,
	`Combined_Product`	INT	NULL,
	`Number_of_Dependents`	INT	NULL
);

-- Statistics table create, user
DROP TABLE IF EXISTS `tb_user_SS`;
CREATE TABLE `tb_user_SS` (  -- User satisfaction score
	`SS_0`	BIGINT	NULL, -- Score 0
	`SS_1`	BIGINT	NULL,
	`SS_2`	BIGINT	NULL,
	`SS_3`	BIGINT	NULL,
	`SS_4`	BIGINT	NULL,
	`SS_5`	BIGINT	NULL -- Score 5
);

DROP TABLE IF EXISTS `tb_user_CV`;
CREATE TABLE `tb_user_CV` ( -- User churn status value
	`Churned`	BIGINT	NULL,
	`Stayed`	BIGINT	NULL
);

DROP TABLE IF EXISTS `tb_user_age_range`;
CREATE TABLE `tb_user_age_range` ( -- User age range
	`Under_10`	BIGINT	NULL, -- 0~9
	`Age_10`	BIGINT	NULL, -- 10~19
	`Age_20`	BIGINT	NULL,
	`Age_30`	BIGINT	NULL,
	`Age_40`	BIGINT	NULL,
	`Age_50`	BIGINT	NULL,
	`Age_60`	BIGINT	NULL,
	`Age_70`	BIGINT	NULL,
	`Age_80`	BIGINT	NULL, -- 80~89
	`Age_90`	BIGINT	NULL -- Over 90
);


-- Statistics table create, service
DROP TABLE IF EXISTS `tb_service_TS`;
CREATE TABLE `tb_service_TS` (
	`TS_0`	BIGINT	NULL,
	`TS_1`	BIGINT	NULL,
	`TS_2`	BIGINT	NULL,
	`TS_3`	BIGINT	NULL,
	`TS_4`	BIGINT	NULL
);

DROP TABLE IF EXISTS `tb_service_StS`;
CREATE TABLE `tb_service_StS` (
	`StS_0`	BIGINT	NULL,
	`StS_1`	BIGINT	NULL,
	`StS_2`	BIGINT	NULL
);

DROP TABLE IF EXISTS `tb_service_CP`;
CREATE TABLE `tb_service_CP` (
	`CP_0`	BIGINT	NULL,
	`CP_1`	BIGINT	NULL,
	`CP_2`	BIGINT	NULL,
	`CP_3`	BIGINT	NULL,
	`CP_4`	BIGINT	NULL
);

DROP TABLE IF EXISTS `tb_service_NoD`;
CREATE TABLE `tb_service_NoD` (
	`NoD_0`	BIGINT	NULL,
	`NoD_1`	BIGINT	NULL,
	`NoD_2`	BIGINT	NULL,
	`NoD_3`	BIGINT	NULL,
	`NoD_4`	BIGINT	NULL,
	`NoD_5`	BIGINT	NULL
);


-- Statistics table create, contract
DROP TABLE IF EXISTS `tb_contract_contract`;
CREATE TABLE `tb_contract_contract` (
	`M2M`	BIGINT	NULL,
	`OY`	BIGINT	NULL,
	`TY`	BIGINT	NULL
);

DROP TABLE IF EXISTS `tb_contract_TiM`;
CREATE TABLE `tb_contract_TiM` (
	`TiM_3`	BIGINT	NULL,
	`TiM_6`	BIGINT	NULL,
	`TiM_12`	BIGINT	NULL,
	`TiM_24`	BIGINT	NULL,
	`TiM_36`	BIGINT	NULL,
	`TiM_37`	BIGINT	NULL
);

DROP TABLE IF EXISTS `tb_contract_MonthC`;
CREATE TABLE `tb_contract_MonthC` (
	`MC_20`	BIGINT	NULL,
	`MC_30`	BIGINT	NULL,
	`MC_40`	BIGINT	NULL,
	`MC_50`	BIGINT	NULL,
	`MC_60`	BIGINT	NULL,
	`MC_70`	BIGINT	NULL,
	`MC_80`	BIGINT	NULL,
	`MC_90`	BIGINT	NULL,
	`MC_100`	BIGINT	NULL,
	`Over_100`	BIGINT	NULL
);


-- CONSTRAINTs
ALTER TABLE `tb_service` ADD CONSTRAINT `PK_TB_SERVICE` PRIMARY KEY (
	`Customer_ID`
);

ALTER TABLE `tb_user` ADD CONSTRAINT `PK_TB_USER` PRIMARY KEY (
	`Customer_ID`
);

ALTER TABLE `tb_contract` ADD CONSTRAINT `PK_TB_CONTRACT` PRIMARY KEY (
	`Customer_ID`
);

ALTER TABLE `tb_service` ADD CONSTRAINT `FK_tb_user_TO_tb_service_1` FOREIGN KEY (
	`Customer_ID`
)
REFERENCES `tb_user` (
	`Customer_ID`
) ON DELETE CASCADE;

ALTER TABLE `tb_contract` ADD CONSTRAINT `FK_tb_user_TO_tb_contract_1` FOREIGN KEY (
	`Customer_ID`
)
REFERENCES `tb_user` (
	`Customer_ID`
) ON DELETE CASCADE;

ALTER TABLE `tb_user_log` ADD CONSTRAINT `FK_tb_user_TO_tb_user_log_1` FOREIGN KEY (
	`Customer_ID`
)
REFERENCES `tb_user` (
	`Customer_ID`
) ON DELETE CASCADE;

ALTER TABLE `tb_service_log` ADD CONSTRAINT `FK_tb_service_TO_tb_service_log_1` FOREIGN KEY (
	`Customer_ID`
)
REFERENCES `tb_service` (
	`Customer_ID`
) ON DELETE CASCADE;

ALTER TABLE `tb_contract_log` ADD CONSTRAINT `FK_tb_contract_TO_tb_contract_log_1` FOREIGN KEY (
	`Customer_ID`
)
REFERENCES `tb_contract` (
	`Customer_ID`
) ON DELETE CASCADE;