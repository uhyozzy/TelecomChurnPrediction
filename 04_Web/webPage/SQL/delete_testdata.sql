SELECT * FROM tb_user;

set sql_safe_updates=0;
DELETE FROM tb_user WHERE Customer_ID = '1' and Membership = '1';