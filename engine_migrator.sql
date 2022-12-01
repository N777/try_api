SET TERM ^ ;

execute block

as
begin
UPDATE CONFIG SET LB3_BILLING_URL = 'http://127.0.0.1:8001' WHERE LB3_BILLING_URL = 'https://billing.litebox.ru';
UPDATE CONFIG SET LB3_BILLING_CLIENT_URL = 'http://127.0.0.1:8001' WHERE LB3_BILLING_CLIENT_URL = 'https://billing.litebox.ru';
UPDATE CONFIG SET LB_SERVICE_URL = 'http://127.0.0.1:8000/' WHERE LB_SERVICE_URL = 'https://lbs.litebox.ru/';
update engine_bases b set b.db_path = 'MYSHOP.FDB', b.db_ip = '127.0.0.1/3050', b.db_pass = 'masterkey' where b.id_base=2;
end^

commit^
SET TERM ; ^
